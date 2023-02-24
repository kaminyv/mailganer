from django.conf.urls import url
from .views import SendEmailsView, StopSendEmailView, ImageResponseView

urlpatterns = [
    url(r'^sendemail/start/(?P<pk>\d)', SendEmailsView.as_view(), name='sendemail-start'),
    url(r'^sendemail/stop/(?P<pk>\d)', StopSendEmailView.as_view(), name='sendemail-stop'),
    url(r'^mailing/images/pixel.png', ImageResponseView.as_view(), name='image-response')
]
