from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def send_email_custom(rec,subject,context):

    html_content = render_to_string("email/activating_email.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [rec],
    )
    email.attach_alternative(html_content, "text/html")
    return email.send()