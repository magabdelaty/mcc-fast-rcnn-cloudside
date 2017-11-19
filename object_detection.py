import mimetypes
import uuid
import _init_paths
import sys
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from utils.cython_nms import nms
from utils.timer import Timer
import numpy as np
import caffe, os, cv2
import argparse
import dlib
import falcon
from time import time
import estimate_cost

CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')


def _generate_id():
    return str(uuid.uuid4())


def read_synset(storage_path):
    synset = ()
    synset_path = os.path.join(storage_path, 'fastrcnn_synset')
    with open(synset_path, "r") as f:
        for line in f.readlines():
            synset = synset + (line.rstrip(),)
    return synset


def vis_detections(im, class_name, dets, thresh=0.8):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]

    if len(inds) == 0 or str(class_name).startswith('__background__'):
        return

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        cv2.rectangle(im, (bbox[0], bbox[1]), (bbox[2], bbox[3]),
                      (255, 0, 0), 2)
        cv2.putText(im, '{:s} {:.3f}'.format(class_name, score),
                    (bbox[0], int(bbox[1] - 5)), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 0, 0), 2, cv2.LINE_AA)
    return im


class Detect(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_get(self, req, resp, name):
        t1 = time()
        names = name.split("&")

        prototxt = os.path.join(cfg.ROOT_DIR, 'models/CaffeNet/test.prototxt')
        caffemodel = os.path.join(cfg.ROOT_DIR,
                                  'data/fast_rcnn_models/'
                                  'caffenet_fast_rcnn_iter_40000.caffemodel')
        if not os.path.isfile(caffemodel):
            raise falcon.HTTPPreconditionFailed("Error", "Caffe model not found")
        caffe.set_mode_cpu()
        net = caffe.Net(prototxt, caffemodel, caffe.TEST)
        classes = read_synset(self.storage_path)
        ext = os.path.splitext(names[0])[1][1:]
        image_path = os.path.join(self.storage_path, names[0])
        im = cv2.imread(image_path)
        rects = []
        dlib.find_candidate_object_locations(im, rects, min_size=np.size(im, 1))
        obj_proposals = np.empty((len(rects), 4), dtype=int)
        for k, d in enumerate(rects):
            obj_proposals[k] = [d.left(), d.top(), d.right(), d.bottom()]
        scores, boxes = im_detect(net, im, obj_proposals)
        CONF_THRESH = 0.9
        NMS_THRESH = 0.3
        for cls in classes:
            if str(cls).startswith('__background__'):
                continue
            cls_ind = CLASSES.index(cls)
            cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
            cls_scores = scores[:, cls_ind]
            keep = np.where(cls_scores >= CONF_THRESH)[0]
            cls_boxes = cls_boxes[keep, :]
            cls_scores = cls_scores[keep]
            dets = np.hstack((cls_boxes,
                              cls_scores[:, np.newaxis])).astype(np.float32)
            keep = nms(dets, NMS_THRESH)
            dets = dets[keep, :]
            vis_detections(im, cls, dets, thresh=CONF_THRESH)

        result_image_path = os.path.join(self.storage_path, "{0}.{1}".format(_generate_id(), ext))
        if 'image/jpeg' == mimetypes.guess_type(image_path, strict=False):
            cv2.imwrite(result_image_path, im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        else:
            cv2.imwrite(result_image_path, im)
        t2 = time() - t1
        data_size = os.path.getsize(image_path)
        data_size += os.path.getsize(result_image_path)
        data_size /= 1024.0 * 1024.0
        cost = estimate_cost.estimateCost(data_size, t2, data_size)
        resp.status = falcon.HTTP_200  # OK
        resp.body = os.path.split(result_image_path)[1] + '&' + str(
            os.path.getsize(result_image_path) / 1024) + '&' + str(t2 * 1000.0) + '&' + "{:2.5f}".format(cost)
