"""
TODO: what is this?
"""
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from .views import DennychDvestoView, AddTextView, AddImageView, ShowTopic

urlpatterns = patterns('',
    url(r'^add/text/$', login_required(AddTextView.as_view()), name='add_text'),
    url(r'^add/image/$', login_required(AddImageView.as_view()), name='add_image'),
    url(r'^topic/(?P<topic_id>\d+)/(.*?)/$', ShowTopic.as_view(), name='show_topic'),
    url(r'^$', DennychDvestoView.as_view(), name='home'),
)