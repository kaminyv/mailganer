# -*- coding: utf-8 -*-
"""
Urls for dashboard app.
"""
from __future__ import unicode_literals

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^sendemail/start/(?P<pk>\d+)$', views.SendEmailsView.as_view(),
        name='sendemail-start'),
    url(r'^sendemail/stop/(?P<pk>\d+)$', views.StopSendEmailView.as_view(),
        name='sendemail-stop'),
    url(r'^mailing/images/pixel.png', views.ImageResponseView.as_view(),
        name='image-response'),
    # Contact urls
    url(r'^contacts/$', views.ContactView.as_view(), name='contact-list'),
    url(r'^contact/create$', views.ContactCreateView.as_view(),
        name='contact-create'),
    url(r'^contact/update/(?P<pk>\d+)$', views.ContactUpdateView.as_view(),
        name='contact-update'),
    url(r'^contact/delete/(?P<pk>\d+)$', views.ContactDeleteView.as_view(),
        name='contact-delete'),
    # ContactList urls
    url(r'^contactlists/$', views.ContactListView.as_view(),
        name='contactlist-list'),
    url(r'^contactlist/create$', views.ContactListCreateView.as_view(),
        name='contactlist-create'),
    url(r'^contactlist/update/(?P<pk>\d+)$', views.ContactListUpdateView.as_view(),
        name='contactlist-update'),
    url(r'^contactlist/delete/(?P<pk>\d+)$', views.ContactListDeleteView.as_view(),
        name='contactlist-delete'),
    # Template urls
    url(r'^templates/$', views.TemplateView.as_view(), name='template-list'),
    url(r'^template/create$', views.TemplateCreateView.as_view(),
        name='template-create'),
    url(r'^template/update/(?P<pk>\d+)$', views.TemplateUpdateView.as_view(),
        name='template-update'),
    url(r'^template/delete/(?P<pk>\d+)$', views.TemplateDeleteView.as_view(),
        name='template-delete'),
    url(r'^mailing/$', views.MailingView.as_view(), name='mailing-list'),

    url(r'^', views.IndexView.as_view(), name='index')
]
