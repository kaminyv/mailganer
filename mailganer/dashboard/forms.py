# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Forms for the dashboard application.
"""


from django.forms import DateInput, DateTimeInput, ModelForm
from .models import Contact, ContactList, Template, Mailing


class CustomDateInput(DateInput):
    """A custom class for a field of type date."""
    input_type = 'date'


class CustomDateTimeInput(DateTimeInput):
    """A custom class for a field of type datetime."""
    input_type = 'datetime-local'


class ContactForm(ModelForm):
    """A form to display the fields for a Contact."""
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        # Adding a class for all form fields.
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-4'

    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'date_of_birth': CustomDateInput()
        }


class ContactListForm(ModelForm):
    """A form to display the fields for a Contact list."""
    def __init__(self, *args, **kwargs):
        super(ContactListForm, self).__init__(*args, **kwargs)
        # Adding a class for all form fields.
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-4'

    class Meta:
        model = ContactList
        fields = '__all__'


class TemplateForm(ModelForm):
    """A form to display the fields for a Template."""
    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        # Adding a class for all form fields.
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-4'

    class Meta:
        model = Template
        fields = '__all__'
