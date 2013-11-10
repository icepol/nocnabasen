"""
TODO: what is this?
"""
from datetime import datetime

from django.http import HttpResponseRedirect


class TimeSwitchMiddleware(object):
    """
    Rozhodne, ci bude bezat nocna basen alebo dennych 200
    """
    def process_request(self, request):
        path = request.path
        now = datetime.now()
        if 6 > now.hour > 21:
            if not path.startswith('/basen'):
                return HttpResponseRedirect('/basen/')
        else:
            if not path.startswith('/dvesto'):
                return HttpResponseRedirect('/dvesto/')

        return None