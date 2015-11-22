# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import settings
from django.template.defaultfilters import floatformat  # noqa
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon.utils import csvbase

from openstack_dashboard import api
from openstack_dashboard import usage

from subprocess import Popen, PIPE
import shlex

class GlobalUsageCsvRenderer(csvbase.BaseCsvResponse):

    columns = [_("Project Name"), _("VCPUs"), _("RAM (MB)"),
               _("Disk (GB)"), _("Usage (Hours)")]

    def get_row_data(self):

        for u in self.context['usage'].usage_list:
            yield (u.project_name or u.tenant_id,
                   u.vcpus,
                   u.memory_mb,
                   u.local_gb,
                   floatformat(u.vcpu_hours, 2))


class GlobalOverview(usage.UsageView):
    table_class = usage.GlobalUsageTable
    usage_class = usage.GlobalUsage
    template_name = 'mydashboard/overview/usage.html'
    csv_response_class = GlobalUsageCsvRenderer

    def get_context_data(self, **kwargs):
        context = super(GlobalOverview, self).get_context_data(**kwargs)
        context['monitoring'] = getattr(settings, 'EXTERNAL_MONITORING', [])
        return context

    def get_data(self):
        data = super(GlobalOverview, self).get_data()
        # Pre-fill project names
        try:
            projects, has_more = api.keystone.tenant_list(self.request)
        except Exception:
            projects = []
            exceptions.handle(self.request,
                              _('Unable to retrieve project list.'))
        for instance in data:
            project = filter(lambda t: t.id == instance.tenant_id, projects)
            # If we could not get the project name, show the tenant_id with
            # a 'Deleted' identifier instead.
            if project:
                instance.project_name = getattr(project[0], "name", None)
            else:
                deleted = _("Deleted")
                instance.project_name = translation.string_concat(
                    instance.tenant_id, " (", deleted, ")")
        return data

# some_app/views.py
from django.views.generic import View
from django.shortcuts import render
import os

class AboutView(View):
    template_name = "mydashboard/overview/logs.html"
    
    def get(self, request, **kwargs):
        log_file_path = "/var/log/nova/nova-compute.log"
        #log_file_content = process = Popen(
        #   shlex.split("cat " + log_file_path), stdout=PIPE, stderr=PIPE)
        #stdout, stderr = process.communicate()
        #log_file_content = stdout.splitlines()
    log_file_content = ['Dang', 'Van', 'Dai']
        return render(request, self.template_name, {'log_file_content': log_file_content})

