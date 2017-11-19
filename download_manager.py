import mimetypes
import os
import falcon

__author__ = 'Maged'


class Item(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_get(self, req, resp, name):
        file_path = os.path.join(self.storage_path, name)
        if not os.path.exists(file_path):
            # from pudb import set_trace; set_trace()
            msg = 'Resource doesn\'t Exist'
            raise falcon.HTTPNotFound('Not Found', msg)
        resp.content_type = mimetypes.guess_type(file_path, strict=False)
        resp.stream = open(file_path, 'rb')
        resp.stream_len = os.path.getsize(file_path)
