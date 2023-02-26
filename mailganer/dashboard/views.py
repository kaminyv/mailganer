# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Views for dashboard application.
"""

import os

from typing import Any

from mailganer import celery_app
from .tasks import send_email, count_views

from celery.result import AsyncResult

from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import reverse, render
from django.utils import timezone
from django.views import generic

from .models import Contact, ContactList, Template, Mailing
from .forms import ContactForm, ContactListForm, TemplateForm, MailingForm


class IndexView(generic.RedirectView):
    """Presents a index page."""
    url = reverse_lazy('contact-list')


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
    """Represents the creation of a new contact list for the mailing list."""
    model = ContactList
    form_class = ContactListForm
    success_url = reverse_lazy('contactlist-list')


class ContactListUpdateView(generic.UpdateView):
    """Represents an update of the contact list for the mailing list."""
    model = ContactList
    form_class = ContactListForm
    success_url = reverse_lazy('contactlist-list')


class ContactListDeleteView(generic.DeleteView):
    """Represents the deletion of a contact list for a mailing list."""
    model = ContactList
    success_url = reverse_lazy('contactlist-list')
    template_name_suffix = '_delete'


class TemplateView(generic.ListView):
    """Presents a list of templates for the mailing list."""
    model = Template


class TemplateCreateView(generic.CreateView):
    """Represents the creation of a new template for the mailing list."""
    model = Template
    form_class = TemplateForm
    success_url = reverse_lazy('template-list')


class TemplateUpdateView(generic.UpdateView):
    """Represents a template update for the mailing list."""
    model = Template
    form_class = TemplateForm
    success_url = reverse_lazy('template-list')


class TemplateDeleteView(generic.DeleteView):
    """Represents the removal of a template for a mailing list."""
    model = Template
    success_url = reverse_lazy('template-list')
    template_name_suffix = '_delete'


class MailingView(generic.ListView):
    """Presents a list of mailings."""
    model = Mailing


class MailingModifiedView(generic.ListView):
    """Presents a list of mailing lists for ajax."""
    model = Mailing
    template_name_suffix = '_list_modified'


class MailingCreateView(generic.CreateView):
    """Represents the creation of a new mailing."""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing-list')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True})


class MailingUpdateView(generic.UpdateView):
    """Represents a mailing update"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing-list')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True})


class MailingDeleteView(generic.DeleteView):
    """Represents a mailing update"""
    model = Mailing
    success_url = reverse_lazy('mailing-list')
    template_name_suffix = '_delete'

    def delete(self, request, *args, **kwargs):
        # type: (MailingDeleteView, Any, object, object) -> JsonResponse
        """Custom mailing removal method for ajax."""
        mailing_id = self.kwargs.get('pk')
        mailing = Mailing.objects.get(pk=mailing_id)
        mailing.delete()

        return JsonResponse({'success': True})


class SendEmailsView(generic.View):
    """View for sent mailing"""
    def get(self, *args, **kwargs):
        # type: (SendEmailsView, object, object) -> JsonResponse
        """Send a mailing list to the queue."""
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
            mailing.status = AsyncResult(task.id).state
            mailing.start = timezone.now()
            mailing.task = task.id
            mailing.save()
            return JsonResponse({'task_id': task.id})

        if mailing.start < timezone.now():
            return JsonResponse(
                {'message': 'The time of the task is set in the past.'})

        task = send_email.apply_async((contacts, template, setting),
                                      eta=mailing.start)
        mailing.status = AsyncResult(task.id).state
        mailing.task = task.id
        mailing.save()

        return JsonResponse({'task_id': task.id})


class StopSendEmailView(generic.View):
    """View for stop sent mailing"""
    def get(self, *args, **kwargs):
        # type: (StopSendEmailView, object, object) -> JsonResponse
        """Cancels a running task."""
        mailing = Mailing.objects.get(pk=self.kwargs.get('pk'))

        if not mailing.task:
            return JsonResponse({'Message': 'Mailing not task'})

        celery_app.control.revoke(task_id=mailing.task, terminate=True)
        mailing.status = None
        mailing.task = None
        mailing.save()
        return JsonResponse({'Message': 'Abort task'})


class ImageResponseView(generic.View):
    """View for response pixel for email"""
    def get(self, *args, **kwargs):
        # type: (ImageResponseView, object, object) -> HttpResponse
        """
        Returns the pixel for the email and the created item for the count.
        """
        mailing_id = self.request.GET.get('mid')
        contact_id = self.request.GET.get('cid')
        if mailing_id and contact_id:
            count_views.delay(mailing_id, contact_id)

        with default_storage.open(os.path.join(
                'dashboard', 'static', 'dashboard', 'images/pixel.png'), 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")


