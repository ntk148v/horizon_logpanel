from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.mydashboard import dashboard


class Logpanel(horizon.Panel):
    name = _("Log Panel")
    slug = "logpanel"
    permissions = ('openstack.services.compute',)


dashboard.Mydashboard.register(Logpanel)
