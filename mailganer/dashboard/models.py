# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class ContactList(BaseModel):
    name = models.CharField(verbose_name='name', max_length=50, unique=True)
    contact = models.ManyToManyField('Contact', related_name='lists')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'contact list'
        verbose_name_plural = 'contacts lists'
        ordering = ('-created_at', 'name',)


class Contact(BaseModel):
    email = models.EmailField(verbose_name='email', unique=True)
    last_name = models.CharField(verbose_name='last name', max_length=50,
                                 blank=True)
    first_name = models.CharField(verbose_name='first name', max_length=50)
    middle_name = models.CharField(verbose_name='middle name', max_length=50,
                                   blank=True)
    date_of_birth = models.DateField(verbose_name='birth day', blank=True,
                                     null=True)

    def __unicode__(self):
        return ' '.join((self.last_name, self.first_name, self.middle_name))

    class Meta:
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'
        ordering = ('email',)


class Template(BaseModel):
    name = models.CharField(verbose_name='name', max_length=100, unique=True)
    subject = models.CharField(verbose_name='subject', max_length=250)
    body = models.TextField(verbose_name='body')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'template'
        verbose_name_plural = 'templates'
        ordering = ('-created_at',)


class Mailing(BaseModel):
    contact_list = models.ForeignKey(ContactList, on_delete=models.SET_NULL,
                                     blank=False, null=True)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL,
                                 blank=False, null=True)
    start = models.DateTimeField(blank=True, null=True)
    sent = models.IntegerField(blank=True, default=0, editable=False)
    task = models.UUIDField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'mailing'
        verbose_name_plural = 'mailings'
        ordering = ('-created_at',)


class Viewed(BaseModel):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', on_delete=models.SET_NULL,
                                null=True)

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'viewed'
        verbose_name_plural = 'viewed'
