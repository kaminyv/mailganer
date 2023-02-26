# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Forms for the dashboard application.
"""

from django.forms import DateInput, DateTimeInput, ModelForm, DateTimeField
from .models import Contact, ContactList, Template, Mailing


class CustomDateInput(DateInput):
    """A custom class for a field of type date."""
    input_type = 'date'


class CustomDateTimeInput(DateTimeInput):
    """A custom class for a field of type datetime."""
    input_type = 'datetime-local'


class ContactForm(ModelForm):
    """A form to display the fields for a Contact."""

    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'date_of_birth': CustomDateInput()
        }


class ContactListForm(ModelForm):
    """A form to display the fields for a Contact list."""

    class Meta:
        model = ContactList
        fields = '__all__'


class TemplateForm(ModelForm):
    """A form to display the fields for a Template."""

    class Meta:
        model = Template
        fields = '__all__'


class MailingForm(ModelForm):
    """A form to display the fields for a Template."""
    start = DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'),
        required=False
    )

    class Meta:
        model = Mailing
        fields = '__all__'
