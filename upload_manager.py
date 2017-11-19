import os
import uuid
import falcon
import mimetypes

__author__ = 'Maged'

ALLOWED_TYPES = (
    'text/plain',
    'image/gif',
    'image/jpeg',
    'image/png'
)


def _generate_id():
    return str(uuid.uuid4())


def validate_file_type(req, resp, resource, params):
    # debug: params: empty list
    # debug: resource: .storage_path = /home/maged/share/Python/look_collection_json/matrices
    # if req.content_type not in ALLOWED_IMAGE_TYPES:
    if req.content_type not in ALLOWED_TYPES:
        # from pudb import set_trace; set_trace()
        msg = 'File type not allowed. Must be plain text, jpeg, png or gif'
        raise falcon.HTTPBadRequest('Bad request', msg)


class Collection(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    @falcon.before(validate_file_type)
    def on_post(self, req, resp):

        file_id = _generate_id()
        ext = mimetypes.guess_extension(req.content_type, strict=False)

        file_name = file_id + ext

        file_path = os.path.join(self.storage_path, file_name)
        with open(file_path, 'wb') as file_file:
            while True:
                chunk = req.stream.read(4096)
                if not chunk:
                    break
                file_file.write(chunk)
        resp.status = falcon.HTTP_201  # CREATED
        resp.body = file_name