# -*- coding: utf-8 -*-
"""
Views for dashboard app.
"""
from __future__ import unicode_literals

import os

from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import reverse, render
from django.utils import timezone
from django.views import generic
from .models import Contact, ContactList, Template, Mailing
from mailganer import celery_app
from .tasks import send_email, count_views
from .forms import ContactForm, ContactListForm, TemplateForm


class IndexView(generic.RedirectView):
    """Presents a index page."""
    url = reverse_lazy('contactlist-list')


class ContactView(generic.ListView):
    """Presents a list of contacts."""
    model = Contact


class ContactCreateView(generic.CreateView):
    """Presents the creation of a new contact."""
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact-list')


class ContactUpdateView(generic.UpdateView):
    """Represents editing the selected contact."""
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contact-list')


class ContactDeleteView(generic.DeleteView):
    """Represents the deletion of the selected contact."""
    model = Contact
    success_url = reverse_lazy('contact-list')
    template_name_suffix = '_delete'


class ContactListView(generic.ListView):
    """Presents a list of contacts list."""
    model = ContactList


class ContactListCreateView(generic.CreateView):
    model = ContactList
    form_class = ContactListForm
    success_url = reverse_lazy('contactlist-list')


class ContactListUpdateView(generic.UpdateView):
    model = ContactList
    form_class = ContactListForm
    success_url = reverse_lazy('contactlist-list')


class ContactListDeleteView(generic.DeleteView):
    model = ContactList
    success_url = reverse_lazy('contactlist-list')
    template_name_suffix = '_delete'


class TemplateView(generic.ListView):
    model = Template


class TemplateCreateView(generic.CreateView):
    model = Template
    form_class = TemplateForm
    success_url = reverse_lazy('template-list')


class TemplateUpdateView(generic.UpdateView):
    model = Template
    form_class = TemplateForm
    success_url = reverse_lazy('template-list')


class TemplateDeleteView(generic.DeleteView):
    model = Template
    success_url = reverse_lazy('template-list')
    template_name_suffix = '_delete'


class MailingView(generic.ListView):
    model = Mailing


class SendEmailsView(generic.View):
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


class StopSendEmailView(generic.View):
    def get(self, *args, **kwargs):
        mailing = Mailing.objects.get(pk=self.kwargs.get('pk'))

        if not mailing.task:
            return JsonResponse({'Message': 'Mailing not task'})

        celery_app.control.revoke(task_id=mailing.task, terminate=True)
        mailing.task = None
        mailing.save()
        return JsonResponse({'Message': 'Abort task'})


class ImageResponseView(generic.View):
    def get(self, *args, **kwargs):
        mailing_id = self.request.GET.get('mid')
        contact_id = self.request.GET.get('cid')
        if mailing_id and contact_id:
            count_views.delay(mailing_id, contact_id)

        with default_storage.open(os.path.join(
                'dashboard', 'static', 'dashboard', 'images/pixel.png'), 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")


