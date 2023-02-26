# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Urls for dashboard application.
"""


from django.conf.urls import url
import views

urlpatterns = [
    # The url to track the opening of the mailing list.
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
    url(r'^contactlist/update/(?P<pk>\d+)$',
        views.ContactListUpdateView.as_view(),
        name='contactlist-update'),
    url(r'^contactlist/delete/(?P<pk>\d+)$',
        views.ContactListDeleteView.as_view(),
        name='contactlist-delete'),
    # Template urls
    url(r'^templates/$', views.TemplateView.as_view(), name='template-list'),
    url(r'^template/create$', views.TemplateCreateView.as_view(),
        name='template-create'),
    url(r'^template/update/(?P<pk>\d+)$', views.TemplateUpdateView.as_view(),
        name='template-update'),
    url(r'^template/delete/(?P<pk>\d+)$', views.TemplateDeleteView.as_view(),
        name='template-delete'),
    # Mailing urls
    url(r'^mailings/$', views.MailingView.as_view(), name='mailing-list'),
    url(r'^mailings/main/$', views.MailingMainView.as_view(),
        name='mailing-main'),
    url(r'^mailing/create$', views.MailingCreateView.as_view(),
        name='mailing-create'),
    url(r'^mailing/update/(?P<pk>\d+)$', views.MailingUpdateView.as_view(),
        name='mailing-update'),
    url(r'^mailing/delete/(?P<pk>\d+)$', views.MailingDeleteView.as_view(),
        name='mailing-delete'),
    url(r'^mailing/start/(?P<pk>\d+)$', views.SendEmailsView.as_view(),
        name='mailing-start'),
    url(r'^mailing/stop/(?P<pk>\d+)$', views.StopSendEmailView.as_view(),
        name='mailing-stop'),
    # Index urls
    url(r'^', views.IndexView.as_view(), name='index')
]
