from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.db.models import Count
from django import forms
from models import Category, Topic, Comment

import logging
l = logging.getLogger('debug')

class LoginForm(forms.Form):
    login = forms.CharField(max_length = 64)
    password = forms.CharField(max_length = 64)

def home(request):
    categories = Category.objects.all()
    topics = Topic.objects.filter(enabled = 1).annotate(comment_count = Count('comment')).order_by('-id')[:50]
    if request.user.is_authenticated():
        # user is logged in
        pass
    else:
        # user is not logged in
        pass

    if request.method == 'POST':
        topic_type = request.POST.get('topic_type', '')
        category = request.POST.get('category', '')
        
        if topic_type:
            if topic_type == '1':
                # textovy prispevok
                topic = request.POST.get('topic', '')
                if topic and category:
                    Topic(topic_type = 1, topic = topic, category_id = category, user_id = 0,
                        ip = request.META['REMOTE_ADDR'], user_agent = request.META['HTTP_USER_AGENT'] ).save()
            elif topic_type == '2':
                # foto prispevok 
                foto = request.FILES.get('foto', '')
                if foto and category:
                    if foto.content_type == 'image/jpeg' and foto.size < 5242880:
                        # vytvorime topic
                        t = Topic(topic_type = 2, topic = '', category_id = category, user_id = 0,
                            ip = request.META['REMOTE_ADDR'], user_agent = request.META['HTTP_USER_AGENT'] )
                        t.save()
                        # ulozime obrazok
                        dst = open("%s/photo/%d.jpg" % (settings.MEDIA_ROOT, t.id), 'wb+')
                        for chunk in foto.chunks():
                            dst.write(chunk)
                        dst.close()

    t = loader.get_template('dennych_dvesto/home.html')
    c = RequestContext(request, {
        'categories': categories,
        'topics': topics,
        'active_category': request.COOKIES.get('category_id', None),
        'active_author': request.COOKIES.get('author_id', None),
        #'user': request.user,
        'form': LoginForm()
    })

    return HttpResponse(t.render(c))
    
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            pass
            # login usera

    return HttpResponseRedirect('/home/')
    
