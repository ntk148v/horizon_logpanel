from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.mydashboard.logpanel import tables
from openstack_dashboard.api import nova

class NovaServiceLogsTab(tabs.TableTab):
    table_classes = (tables.NovaServiceLogsTable,)
    name = _("Compute Service Logs")
    slug = "nova_service_logs"
    template_name = 'horizon/common/_detail_table.html'
    permissions = ('openstack.services.compute',)

    def get_nova_service_logs_data(self):
        try:
            services = nova.service_list(self.tab_group.request)
        except Exception:
            msg = _('Unable to get nova services list.')
            exceptions.check_message(["Connection", "refused"], msg)
            exceptions.handle(self.request, msg)
            services = []
        return services

class LogPanelTabs(tabs.TabGroup):
    slug = "logpanel_tabs"
    tabs = (NovaServiceLogsTab,)
    sticky = True