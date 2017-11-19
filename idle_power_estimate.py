import falcon

__author__ = 'Maged'


class IdlePowerEstimate(object):
    def on_get(self, req, resp):
        counter = 0
        while counter < 1000000000:
            counter += 1
        resp.body = str(counter)
        resp.status = falcon.HTTP_200  # OK
