from celery.task import task
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template import loader, Template, Context
from .models import Mailing, Viewed
from typing import Dict, List, AnyStr


@task()
def send_email(contacts, template, setting):
    # type: (List, Dict, Dict) -> int
    """

    :param contacts:
    :param template:
    :param setting:
    :return:
    """
    setting_context = dict(setting=setting, template=template)

    messages = []

    for contact in contacts:
        setting_context['setting']['contact_id'] = contact.get('id')
        plaintext = Template(template.get('body'))
        html = Template(
            loader.render_to_string(template_name='mail_template.html',
                                    context=setting_context))

        contact_context = Context(contact)

        message = EmailMultiAlternatives(
            subject=template.get('subject'),
            body=plaintext.render(contact_context),
            from_email='mail@mailganer.ru',
            to=[contact.get('email')]
        )
        message.attach_alternative(html.render(contact_context), 'text/html')
        messages.append(message)

    connection = get_connection()
    count_sends = connection.send_messages(messages)
    mailing = Mailing.objects.get(pk=setting.get('mailing_id'))
    mailing.sent = count_sends
    mailing.status = 'READY'
    mailing.task = None
    mailing.save()

    return count_sends


@task()
def count_views(mailing_id, contact_id):
    # type: (AnyStr, AnyStr) -> str
    """

    :param mailing_id:
    :param contact_id:
    :return:
    """
    if not mailing_id.isdigit() or not contact_id.isdigit():
        raise Exception('Parameters are not a number.')

    if not Mailing.objects.filter(pk=mailing_id).filter(
            contact_list__contact=contact_id).exists():
        raise Exception('Not object.')

    viewed, result = Viewed.objects.get_or_create(
        mailing_id=mailing_id,
        contact_id=contact_id
    )

    return '{} {}'.format(viewed, result)
