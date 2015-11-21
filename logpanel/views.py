# from horizon import views
# from subprocess import Popen, PIPE
# import shlex

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from horizon import exceptions
from horizon import tabs
from horizon import version
from horizon import forms
from horizon.utils import memoized

from openstack_dashboard import api
from openstack_dashboard.dashboards.mydashboard.logpanel import tabs as project_tabs
from openstack_dashboard.dashboards.mydashboard.logpanel import forms as project_forms

from subprocess import Popen, PIPE
import shlex


class IndexView(tabs.TabbedTableView):
    tab_group_class = project_tabs.LogPanelTabs
    template_name = "mydashboard/logpanel/logs.html"
    page_title = _("Logging Information")

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class ShowLogView(forms.ModalFormView):
    form_class = project_forms.ShowLog
    template_name = 'mydashboard/logpanel/show_log.html'
    modal_id = "show_log_id"
    modal_header = _("Show Log")

    def get_initial(self):
        return {"binary": self.kwargs["binary"]}

    def get_context_data(self, **kwargs):
        context = super(ShowLogView, self).get_context_data(**kwargs)
        binary = self.kwargs['binary']
        log_file_name =  binary + ".log"
        log_file_path = "/var/log/nova/" + log_file_name
        log_file_content = process = Popen(
            shlex.split("cat " + log_file_path), stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        log_file_content = stdout.splitlines()
        context['log_file_name'] = log_file_name
        context['log_file_path'] = log_file_path
        context['log_file_content'] = log_file_content
        log_file_content_html = ""
        for log_line in log_file_content
            log_file_content_html = log_file_content_html + "<p>" + log_line + "</p>"
        context['log_file_content_html'] = log_file_content_html
        return context
