from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.mydashboard.logpanel import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<binary>[^/]+)/show_log/$',
        views.ShowLogView.as_view(),
        name='show_log'),
)
