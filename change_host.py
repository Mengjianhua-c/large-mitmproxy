"""
Author: Meng
Date: 2019/8/10
"""
from settings import HOST_FILE_PATH
import os
import pickle


def host_manage(url, port):
    path = os.path.join(HOST_FILE_PATH, f'{port}_host.txt')
    result = read_file(path)
    hosts = result['hosts']
    ip = None
    print('*' * 100)
    print(url)
    if url in hosts:
        ips = result['ips']
        ip = ips[url]
    return ip


def read_file(path):
    with open(path, 'rb') as f:
        value = pickle.loads(f.read())
    return value


def to_dict(value):
    result = {}
    for item in value.keys():
        result[item] = value[item]
    return result