# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from mailganer import celery_app

from django.core.files.storage import default_storage
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import reverse
from django.utils import timezone
from django.views.generic import View
from .models import Mailing
from .tasks import send_email, count_views


class SendEmailsView(View):
    """

    """
    def get(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        mailing = Mailing.objects.get(pk=self.kwargs.get('pk'))

        contacts = [model_to_dict(contact)
                    for contact in mailing.contact_list.contact.all()]

        template = model_to_dict(mailing.template)

        setting = dict(
            mailing_id=mailing.pk,
            pixel_url=self.request.build_absolute_uri(
                reverse(viewname='image-response')
            )
        )

        if mailing.task:
            return JsonResponse({'message': 'The task is started.'})

        if not mailing.start:
            task = send_email.delay(contacts, template, setting)
            mailing.start = timezone.now()
            mailing.task = task.id
            mailing.save()
            return JsonResponse({'task_id': task.id})

        if mailing.start < timezone.now():
            return JsonResponse(
                {'message': 'The time of the task is set in the past.'})

        task = send_email.apply_async((contacts, template, setting),
                                      eta=mailing.start)
        mailing.task = task.id
        mailing.save()

        return JsonResponse({'task_id': task.id})


class StopSendEmailView(View):
    def get(self, *args, **kwargs):
        mailing = Mailing.objects.get(pk=self.kwargs.get('pk'))

        if not mailing.task:
            return JsonResponse({'Message': 'Mailing not task'})

        celery_app.control.revoke(task_id=mailing.task, terminate=True)
        mailing.task = None
        mailing.save()
        return JsonResponse({'Message': 'Abort task'})


class ImageResponseView(View):
    def get(self, *args, **kwargs):
        mailing_id = self.request.GET.get('mid')
        contact_id = self.request.GET.get('cid')
        if mailing_id and contact_id:
            count_views.delay(mailing_id, contact_id)

        with default_storage.open(os.path.join(
                'dashboard', 'static', 'dashboard', 'images/pixel.png'), 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")


