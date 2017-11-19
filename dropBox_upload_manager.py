import os
import urllib2
import uuid
import falcon
import mimetypes
import requests
import logging
from datetime import datetime

__author__ = 'Maged'

logging.basicConfig(filename='dropbox_upload_manager.log', level=logging.DEBUG)

WGET_CMD = '/usr/bin/wget'

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

    def on_post(self, req, resp):
        url = urllib2.unquote(req.get_header("DBX-Uri")).decode('utf8')
        ext = os.path.splitext(url)[1][1:]
        file_name = os.path.basename(url)
        file_path = os.path.join(self.storage_path, file_name)
        logging.debug("before_write")
        logging.debug(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'))
        with os.popen(WGET_CMD + ' -nc --no-dns-cache -4 ' + url + ' -O ' + file_path) as wget_output:
            resp.status = falcon.HTTP_201  # CREATED
            resp.body = file_name
        logging.debug("after_write")
        logging.debug(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f'))
