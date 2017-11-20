# sample.py

import falcon


from psutil import virtual_memory

mem = virtual_memory()
total = mem.total  # total physical memory available


class MemResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        response = {
            'total': total
        }

        resp.media = response


class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote

api = falcon.API()
api.add_route('/quote', QuoteResource())
api.add_route('/mem', MemResource())


