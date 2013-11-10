"""
TODO: what is this?
"""
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import AddTextView, NocnaBasenView

urlpatterns = patterns('',
    url(r'add/', login_required(AddTextView.as_view()), name='add_vers'),
    url(r'', NocnaBasenView.as_view(), name='nocna_basen'),
)