import os
import falcon
import json
import cpuinfo
from psutil import virtual_memory

__author__ = 'Maged'


class Discover(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_get(self, req, resp):
        discovery_file = os.path.join(self.storage_path, 'service_discovery.json')

        with open(discovery_file, 'r+') as data_file:
            data = json.load(data_file)
            info = cpuinfo.get_cpu_info()
            data["cpu_speed"] = str(info['hz_actual_raw'][0]) # hz
            data["cpu_core"] = str(info['count'])
            mem = virtual_memory()
            data["ram_avail"] = str(mem.available)
            data_file.seek(0, 0)
            jsonString = json.dumps(data)
            data_file.write(jsonString)
            data_file.truncate()
        with open(discovery_file) as data_file:
            data = json.load(data_file)
            resp.body = json.dumps(data)
            resp.status = falcon.HTTP_200  # OK