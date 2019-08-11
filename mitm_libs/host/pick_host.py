"""
Author: Meng
Date: 2019/8/10
"""
from settings import HOST_FILE_PATH
import os
import pickle


class HostFile:
    def __init__(self, port):
        self.path = self._join_path(port)

    @staticmethod
    def _join_path(port):
        return os.path.join(HOST_FILE_PATH, f'{port}_host.txt')

    def read_file(self):
        with open(self.path, 'rb') as f:
            value = pickle.loads(f.read())
        return value

    def _write_file(self, value):
        with open(self.path, 'wb') as f:
            f.write(pickle.dumps(value))

    def update_host(self, value:str):
        value = value.split(';')
        result = {'hosts': [], 'ips':{}}
        for item in value:
            ip, host = item.split('_')
            if host not in result['hosts']:
                result['hosts'].append(host)
                result['ips'][host] = ip

        self._write_file(result)

    def remove_host(self):
        os.remove(self.path)


if __name__ == '__main__':
    h = HostFile(8080)
    h.update_host('172.22.33.245_app.bilibili.com;172.22.33.245_app.biliapi.net')
    print(h.read_file())