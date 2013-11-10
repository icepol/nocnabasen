from django.views.generic import TemplateView
from django.shortcuts import redirect

from .models import Basen

# logger
import logging
l = logging.getLogger('debug')


class NocnaBasenView(TemplateView):
    template_name = 'nocna_basen/basen.html'

    def get(self, request, *args, **kwargs):
        basen = list(Basen.objects.filter(enabled=1).order_by('-id')[:20])
        basen.reverse()

        return self.render_to_response({
            'basen': basen,
            'user': request.user,
        })


class AddTextView(TemplateView):
    template_name = 'nocna_basen/basen.html'

    def post(self, request, *args, **kwargs):
        vers = self.request.POST.get('vers')
        if vers:
            Basen.objects.create(
                vers=vers,
                user=request.user,
                ip=request.META['REMOTE_ADDR'],
                user_agent=request.META['HTTP_USER_AGENT']
            )

        return redirect('/')
