# get-nfs-metrics
Python script to compute the size of each subfolder from a root directory and send these custom metrics to ELK.

The goal of this project is to compute the size of subfolder on a NFS and send them to the ELK stack to visualize the data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You must have python3 installed

* [Python](https://realpython.com/installing-python/)

Install the ``elasticsearch`` package with `pip
<https://pypi.python.org/pypi/elasticsearch>`_::

    pip install elasticsearch

#### Clone this project to your local machine:

```bash
$ git clone https://github.com/ayoubbts/get-nfs-metrics.git
```

#### Go into the cloned dir:

```bash
$ cd get-nfs-metrics
```
 Check out [Usage](#usage).

## Usage

Example 1:
```
$ python3  get_nfs_metrics.py
```

## Authors

See also the list of [contributors](https://github.com/ayoubbts/serverless-image-resizing/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Python
* Elastic