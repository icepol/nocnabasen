from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import redirect, Http404
from django.db.models import Count

from common.views import AjaxView
from common.base import save_image, save_thumbnail
from models import Category, Topic
from forms import CommentForm

# logger
import logging
l = logging.getLogger('debug')


class DennychDvestoView(TemplateView):
    template_name = 'dennych_dvesto/dvesto.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        topics = Topic.objects.filter(enabled=1).annotate(comment_count=Count('comment')).order_by('-id')[:50]

        return self.render_to_response({
            'categories': categories,
            'topics': topics,
            'active_category': request.COOKIES.get('category_id', None),
            'active_author': request.COOKIES.get('author_id', None),
            'user': request.user,
        })


class AddTextView(TemplateView, AjaxView):
    template_name = 'dennych_dvesto/dvesto.html'

    def post(self, request, *args, **kwargs):
        category = request.POST.get('category')
        topic = request.POST.get('topic')

        if topic and category:
            Topic.objects.create(
                topic_type=1,
                topic=topic,
                category_id=category,
                user=request.user,
                ip=request.META['REMOTE_ADDR'],
                user_agent=request.META['HTTP_USER_AGENT']
            )

        if request.is_ajax():
            return self.render_to_response_json({'status': 'ok'})

        return redirect('/')


class AddImageView(TemplateView, AjaxView):
    template_name = 'dennych_dvesto/dvesto.html'

    def post(self, request, *args, **kwargs):
        category = request.POST.get('category')
        foto = request.FILES.get('foto', '')

        if foto and category:
            if foto.content_type == 'image/jpeg' and foto.size < 5242880:
                # vytvorime topic
                t = Topic.objects.create(
                    topic_type=2,
                    topic='',
                    category_id=category,
                    user=request.user,
                    ip=request.META['REMOTE_ADDR'],
                    user_agent=request.META['HTTP_USER_AGENT']
                )

                # ulozime obrazok
                original_path = "%s/photo/%d_o.jpg" % (settings.MEDIA_ROOT, t.id)
                img = save_image(original_path, foto)

                # velka kopia
                path = "%s/photo/%d_b.jpg" % (settings.MEDIA_ROOT, t.id)
                save_thumbnail(img, path, 800)

                # nahlad
                path = "%s/photo/%d.jpg" % (settings.MEDIA_ROOT, t.id)
                save_thumbnail(img, path, 260)

        if request.is_ajax():
            return self.render_to_response_json({'status': 'ok'})

        return redirect('/')


class ShowTopic(TemplateView):
    """
    Get topic with comments.
    """
    template_name = 'dennych_dvesto/topic.html'

    def get_context_data(self, **kwargs):
        topic = kwargs.get('topic')
        if topic is None:
            try:
                topic = Topic.objects.get(id=kwargs.get('topic_id'))
            except Topic.DoesNotExist:
                return Http404

        context = {
            'user': self.request.user,
            'topic': topic,
            'comments': topic.comment_set.all().order_by('id')
        }

        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(context=self.get_context_data(topic_id=kwargs['topic_id']))

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            raise Http404

        try:
            topic = Topic.objects.get(id=kwargs['topic_id'])
        except Topic.DoesNotExist:
            return Http404

        form = CommentForm(request.POST)
        if form.is_valid():
            topic.comment_set.create(
                user=request.user,
                comment=form.cleaned_data['comment'],
                ip=request.META['REMOTE_ADDR'],
                user_agent=request.META['HTTP_USER_AGENT']
            )

        return self.render_to_response(context=self.get_context_data(topic=topic))
