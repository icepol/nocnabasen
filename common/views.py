"""
TODO: what is this?
"""
import ujson

from django.http import HttpResponse


class AjaxView(object):
    def render_to_response_json(self, context, **response_kwargs):
        """
        Return json representation of context.
        """
        return HttpResponse(ujson.dumps(context), mimetype="application/json", **response_kwargs)