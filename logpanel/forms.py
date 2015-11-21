from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api


class ShowLog(forms.SelfHandlingForm):
    def handle(self, request, data):
        try:
            return None
        except Exception, e:
            exceptions.handle(request, _('Unable to show log.'))
