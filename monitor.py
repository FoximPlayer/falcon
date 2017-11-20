import falcon
from psutil import virtual_memory


class MemResource:
    def on_get(self, req, resp):
        mem = virtual_memory()
        response = {
            'free': mem.free,
            'total': mem.total
        }
        resp.media = response

api = falcon.API()
api.add_route('/mem', MemResource())


