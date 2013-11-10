"""
TODO: what is this?
"""
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from common.base import send_invitation_mail

from .forms import InvitationForm, RegistrationForm, ProfileUpdateForm, PasswordChangeForm
from .models import Invitation


class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        return {
            'profile_form': ProfileUpdateForm(initial={
                'name': self.request.user.first_name,
            }),
            'password_form': PasswordChangeForm(),
        }

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        action = request.POST.get('action')
        if action == 'profile':
            form = ProfileUpdateForm(request.POST)
            if form.is_valid():
                self.request.user.first_name = form.cleaned_data['name']
                self.request.user.save()

                return HttpResponseRedirect(reverse('profile'))

            context['profile_form'] = form
        elif action == 'password':
            form = PasswordChangeForm(request.POST, user=self.request.user)
            if form.is_valid():
                self.request.user.set_password(form.cleaned_data['password1'])
                self.request.user.save()

                return HttpResponseRedirect(reverse('profile'))

            context['password_form'] = form
        else:
            raise Http404

        return self.render_to_response(context=context)


class SendInvitationView(TemplateView):
    template_name = 'profile/send_invitation.html'

    def get_context_data(self, **kwargs):
        return {
            'form': InvitationForm()
        }

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = InvitationForm(self.request.POST)
        if form.is_valid():
            try:
                # check if this user is registered already
                User.objects.get(email=form.cleaned_data['email'])

                context['form'] = form
                context['registered_user'] = True

                return self.render_to_response(context=context)
            except User.DoesNotExist:
                pass

            try:
                # check if invitation exists
                invitation = Invitation.objects.get(email=form.cleaned_data['email'])

                forced_email = self.request.POST.get('forced_email')
                if forced_email == form.cleaned_data['email']:
                    send_invitation_mail(form.cleaned_data['email'], request.user, invitation.code)
                    return HttpResponseRedirect(reverse('send_invitation_done'))

                context['show_force_send'] = True
                context['forced_email'] = form.cleaned_data['email']
            except Invitation.DoesNotExist:
                invitation = Invitation.objects.create(
                    sender=request.user,
                    email=form.cleaned_data['email']
                )

                send_invitation_mail(form.cleaned_data['email'], request.user, invitation.code)
                return HttpResponseRedirect(reverse('send_invitation_done'))

        context['form'] = form

        return self.render_to_response(context=context)


class SendInvitationDoneView(TemplateView):
    template_name = 'profile/send_invitation_done.html'


class RegistrationView(TemplateView):
    template_name = 'profile/registration.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous():
            return HttpResponseRedirect(reverse('registration_not_needed'))

        invitation = self.get_invitation(kwargs['code'])
        if not invitation:
            return HttpResponseRedirect(reverse('registration_wrong_code'))

        form = RegistrationForm(initial={'email': invitation.email})

        return self.render_to_response(context={'form': form})

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous():
            return HttpResponseRedirect(reverse('registration_not_needed'))

        invitation = self.get_invitation(kwargs['code'])
        if not invitation:
            return HttpResponseRedirect(reverse('registration_wrong_code'))

        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=invitation.email,
                email=invitation.email,
                password=form.cleaned_data['password1']
            )

            user.first_name = form.cleaned_data['name']
            user.save()

            invitation.valid = False
            invitation.save()

            authentcated_user = authenticate(username=invitation.email, password=form.cleaned_data['password1'])
            if authentcated_user is not None:
                login(request, authentcated_user)

            return HttpResponseRedirect(reverse('registration_done'))

        return self.render_to_response(context={'form': form})

    def get_invitation(self, code):
        try:
            return Invitation.objects.get(code=code, valid=True)
        except Invitation.DoesNotExist:
            return False


class RegistrationWrongCodeView(TemplateView):
    template_name = 'profile/registration_wrong_code.html'


class RegistrationDoneView(TemplateView):
    template_name = 'profile/registration_done.html'


class RegistrationNotNeeded(TemplateView):
    template_name = 'profile/registration_not_needed.html'


class LoginView(TemplateView):
    template_name = 'profile/login.html'


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None or user.is_active():
        login(request, user)
        return HttpResponseRedirect('/')

    return HttpResponseRedirect(reverse('wrong_login'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')