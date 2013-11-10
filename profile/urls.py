"""
TODO: what is this?
"""
from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required

from .views import ProfileView, SendInvitationView, SendInvitationDoneView, RegistrationView, \
    RegistrationWrongCodeView, RegistrationDoneView, RegistrationNotNeeded

profile_patterns = patterns('',
    url(r'profile/', login_required(ProfileView.as_view()), name='profile'),
    url(r'send-invitation/', login_required(SendInvitationView.as_view()), name='send_invitation'),
    url(r'send-invitation-done/', login_required(SendInvitationDoneView.as_view()),
        name='send_invitation_done'),
    url(r'invitation/(?P<code>.+?)/', RegistrationView.as_view(), name='invitation'),
    url(r'registration-done/', login_required(RegistrationDoneView.as_view()), name='registration_done'),
    url(r'registration-wrong-code/', RegistrationWrongCodeView.as_view(), name='registration_wrong_code'),
    url(r'registration-not-needed/', RegistrationNotNeeded.as_view(), name='registration_not_needed'),
)

login_patterns = patterns('',
    url(r'login/', 'django.contrib.auth.views.login', {'template_name': 'profile/login.html'}, name='login'),
    url(r'logout/', 'django.contrib.auth.views.logout', {'template_name': 'profile/logut.html'}, name='logout'),
)

urlpatterns = patterns('',
   (r'', include(profile_patterns)),
   (r'', include(login_patterns)),
)