import os
import math
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch

depth_ = 5


def create_index(index, es):
    if not es.indices.exists(index_name):
        es.indices.create(index, ignore=400)
    return es


def insert_to_index(es, index, data):
    print(data)
    es.index(index=index, doc_type='_doc', body=data)


def get_directory_size(dir):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        # print("[+] Getting the size of", dir)
        for entry in os.scandir(dir):
            if entry.is_file(follow_symlinks=False):
                # if it's a file, use stat() function
                total += entry.stat(follow_symlinks=False).st_size
            elif entry.is_dir(follow_symlinks=False):
                # if it's a directory, recursively call this function
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        # if `directory` isn't a directory, get the file size then
        return os.path.getsize(dir) if not os.path.islink(dir) else 0
    except PermissionError:
        # if for whatever reason we can't open the folder, return 0
        return 0
    except FileNotFoundError:
        return 0
    return total


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def scan_dir(folder_path, depth, es):
    start_time = time.time()
    subfolders = {}
    data = {}
    # iterate over all the directories inside this path
    if depth > 0 and os.path.isdir(folder_path):
        try:
            for directory in os.scandir(folder_path):
                if directory.is_dir(follow_symlinks=False):
                    directory_ = os.path.join(folder_path, directory)
                    if not os.path.islink(directory_):
                        subfolders[os.path.basename(directory_)] = scan_dir(directory_, depth - 1, es)
        except NotADirectoryError:
            # TODO
            None
        except PermissionError:
            # TODO
            None
        data['total_size_bit'] = sum([subfolders[s]['total_size_bit'] for s in subfolders])
        for directory in os.scandir(folder_path):
            subdirectory = os.path.join(folder_path, directory)
            data['total_size_bit'] += get_directory_size(subdirectory) if directory.is_file(
                follow_symlinks=False) else 0
        data['total_size'] = convert_size(data['total_size_bit'])
    else:
        directory_size = get_directory_size(folder_path)
        data['total_size_bit'] = directory_size
        data['total_size'] = convert_size(directory_size)
    data['time'] = round(time.time() - start_time, 2)
    data['path'] = folder_path
    data['depth'] = depth_ - depth
    #print(json.dumps(data))
    data_for_elastic = {
        'folder_name': folder_path,
        'size': data['total_size_bit'],
        'duration': data['time'],
        'depth': data['depth'],
        'date': datetime.now().timestamp() * 1000
    }
    print(data_for_elastic)
    #print(es.indices)
    insert_to_index(es, index_name, data_for_elastic)
    return data


if __name__ == "__main__":
    today = datetime.today().strftime('%Y-%m-%d')
    folder_path = '/your/path'
    index_name = f'my-index-{today}'
    es_obj = Elasticsearch()
    es_idx = create_index(index_name, es_obj)
    d = scan_dir(folder_path, depth_, es_idx)
    print(json.dumps(d))