# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Models for dashboard application.
"""

from django.db import models


class BaseModel(models.Model):
    """The base model is an abstract model."""
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class ContactList(BaseModel):
    """The model represents a mailing list of contacts."""
    name = models.CharField(max_length=50, unique=True, verbose_name='name',
                            help_text='Enter a name for the list.')
    contact = models.ManyToManyField('Contact', related_name='lists')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'contact list'
        verbose_name_plural = 'contacts lists'
        ordering = ('-created_at', 'name',)


class Contact(BaseModel):
    """The model represents the contacts for the mailing list."""
    email = models.EmailField(unique=True, verbose_name='email',
                              help_text='Enter e-mail address.')
    last_name = models.CharField(max_length=50, blank=True, default='',
                                 verbose_name='last name',
                                 help_text='Enter a last name.')
    first_name = models.CharField(max_length=50, verbose_name='first name',
                                  help_text='Enter a first name.')
    middle_name = models.CharField(max_length=50, blank=True, default='',
                                   verbose_name='middle name',
                                   help_text='Enter a middle name.')
    date_of_birth = models.DateField(blank=True, null=True,
                                     verbose_name='birthday',
                                     help_text='Enter date of birth.')

    def __unicode__(self):
        return ' '.join((self.last_name, self.first_name, self.middle_name))

    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'
        ordering = ('-created_at',)


class Template(BaseModel):
    """The model presents templates for mailings."""
    name = models.CharField(max_length=100, unique=True, verbose_name='name',
                            help_text='Enter the template name')
    subject = models.CharField(max_length=250, verbose_name='subject',
                               help_text='Enter the subject line.')
    body = models.TextField(verbose_name='body',
                            help_text='Enter the letter body template.')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'template'
        verbose_name_plural = 'templates'
        ordering = ('-created_at',)


class Mailing(BaseModel):
    """The model represents a mailing list."""
    contact_list = models.ForeignKey(ContactList, on_delete=models.SET_NULL,
                                     blank=False, null=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL,
                                 blank=False, null=True)
    start = models.DateTimeField(blank=True, null=True,
                                 verbose_name='Start mailing',
                                 help_text=
                                 'Select the UTC time to start the mailing.')
    sent = models.IntegerField(blank=True, default=0, editable=False,
                               verbose_name='number of shipments')
    task = models.UUIDField(blank=True, null=True, editable=False,
                            verbose_name='task number')
    status = models.CharField(max_length=10, blank=True, null=True,
                              editable=False, verbose_name='mailing status')

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'mailing'
        verbose_name_plural = 'mailings'
        ordering = ('-created_at',)

    def get_count_views(self):
        # type: (Mailing) -> str
        """Returns the number of views for the mailing."""
        count_views = Viewed.objects.filter(mailing=self.id).count()
        return '' if count_views == 0 else str(count_views)


class Viewed(BaseModel):
    """The model represents email reading labels."""
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', on_delete=models.SET_NULL,
                                null=True)

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'viewed'
        verbose_name_plural = 'viewed'
