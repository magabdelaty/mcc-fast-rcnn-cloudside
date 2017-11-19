import mimetypes
import os
import uuid
import falcon

__author__ = 'Maged'


def _ext_to_media_type(ext):
    return "image/" + ext


class Item(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_get(self, req, resp, name):
        file_path = os.path.join(self.storage_path, name)
        if not os.path.exists(file_path):
            msg = 'Resource doesn\'t Exist'
            raise falcon.HTTPNotFound('Not Found', msg)
        resp.content_type = mimetypes.guess_type(file_path, strict=False)

        image_path = os.path.join(self.storage_path, name)
        resp.stream = open(image_path, 'rb')
        resp.stream_len = os.path.getsize(image_path)


def _generate_id():
    return str(uuid.uuid4())


class Collection(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_post(self, req, resp):
        # just read the stream without writing it to a file
        while True:
            chunk = req.stream.read(4096)
            if not chunk:
                break
        resp.status = falcon.HTTP_201  # CREATED