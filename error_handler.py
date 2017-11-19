import falcon

__author__ = 'Maged'


class ErrorHandler(Exception):
    @staticmethod
    def handle(ex, req, resp, params):
        raise falcon.HTTPPreconditionFailed("X and Y are not fitting with the first image.")
