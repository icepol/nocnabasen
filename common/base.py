"""
TODO: what is this?
"""
import Image

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def save_image(path, foto):
    with open(path, 'wb+') as dst:
        for chunk in foto.chunks():
            dst.write(chunk)

    return Image.open(path)


def save_thumbnail(img, path, size):
    thumbnail = create_thumbnail(img, size)
    thumbnail.save(path, format='JPEG')


def create_thumbnail(img, size):
    if img.mode not in ('L', 'RGB'):
        img = img.convert('RGB')

    width, height = img.size

    if width < size and height < size:
        # image is small
        return img

    const = float(width) / float(size)
    if const > 1:
        img.thumbnail((size, height * const), Image.ANTIALIAS)

    return img


def send_invitation_mail(email, user, code):
    message = render_to_string('profile/send_invitation_email.html', {
        'user': user,
        'code': code,
        'SITE_HOME': settings.SITE_HOME
    })

    send_mail('Pozvanka na Nocnu Basen', message, 'noreply@nocnabasen.sk', [email], fail_silently=True)