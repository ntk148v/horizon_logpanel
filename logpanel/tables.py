from django import template
from django.template import defaultfilters as filters
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon.utils import filters as utils_filters

SERVICE_ENABLED = "enabled"
SERVICE_DISABLED = "disabled"

SERVICE_STATUS_DISPLAY_CHOICES = (
    (SERVICE_ENABLED, _("Enabled")),
    (SERVICE_DISABLED, _("Disabled")),
)

SERVICE_STATE_DISPLAY_CHOICES = (
    ('up', _("Up")),
    ('down', _("Down")),
)


class ServiceFilterAction(tables.FilterAction):
    filter_field = 'type'

    def filter(self, table, services, filter_string):
        q = filter_string.lower()

        def comp(service):
            attr = getattr(service, self.filter_field, '')
            if attr is not None and q in attr.lower():
                return True
            return False

        return filter(comp, services)


class SubServiceFilterAction(ServiceFilterAction):
    filter_field = 'binary'


def get_agent_status(agent):
    template_name = 'admin/info/_cell_status.html'
    context = {
        'status': agent.status,
        'disabled_reason': agent.disabled_reason
    }
    return template.loader.render_to_string(template_name, context)


class UpdateRow(tables.Row):
    ajax = True

    def get_data(self, request):
        pass


class ShowLog(tables.LinkAction):
    name = "show"
    verbose_name = _("Show Log")
    url = "horizon:mydashboard:logpanel:show_log"
    classes = ("ajax-modal",)

    # def allowed(self, request, instance=None):
    #     return instance.status in ("ACTIVE") and not is_deleting(instance)


class NovaServiceLogsTable(tables.DataTable):
    binary = tables.Column("binary", verbose_name=_('Name'))
    host = tables.Column("host", verbose_name=_('Host'))
    zone = tables.Column("zone", verbose_name=_('Zone'))
    status = tables.Column(get_agent_status, verbose_name=_('Status'))
    state = tables.Column("state", verbose_name=_('State'),
                          display_choices=SERVICE_STATE_DISPLAY_CHOICES)
    updated_at = tables.Column('updated_at',
                               verbose_name=pgettext_lazy(
                                   'Time since the last update',
                                   u'Last Updated'),
                               filters=(utils_filters.parse_isotime,
                                        filters.timesince))

    def get_object_id(self, obj):
        # return "%s-%s-%s" % (obj.binary, obj.host, obj.zone)
        return obj.binary

    class Meta(object):
        name = "nova_service_logs"
        verbose_name = _("Compute Service Logs")
        table_actions = (SubServiceFilterAction, )
        row_actions = (ShowLog, )
        multi_select = False
        row_class = UpdateRow
