# Create your views here.
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib.sites.models import Site
from django.views.generic import TemplateView
import requests
import re


grade_naming = {
    'k': 'K',
    'first': '1',
    'second': '2',
    'third': '3',
    'forth': '4',
    'fifth': '5',
    'sixth': '6',
    'seventh': '7',
    'eighth': '8',
    'ninth': '9',
    'tenth': '10',
    'eleventh': '11',
    'twelfth': '12'
}
grade_naming_inv = dict(zip(grade_naming.values(), grade_naming.keys()))

def current_site(context):
        current_site = Site.objects.get_current()
        for s in Site.objects.all():
            if self.request.META['HTTP_HOST'] in s.domain:
                current_site = s


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        current_site = Site.objects.get_current()
        for s in Site.objects.all():
            if self.request.META['HTTP_HOST'] in s.domain:
                current_site = s

        ctx['sitename'] = current_site.name.lower()
        return ctx

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'protected.html'

    def get_context_data(self, **kwargs):
        ctx = super(ProtectedView, self).get_context_data(**kwargs)
        headers = {'content-type': 'application/json'}
        user = self.request.user
        organization = user.organization
        api_res = None

        try:
            api_urls = requests.get(settings.BASE_API_URL, headers=headers).json()
            res = requests.get('{0}{1}/'.format(api_urls['districts'], organization), headers=headers)
        except Exception:
            res = None

        auth = False
        other_res = []
        current_site = Site.objects.get_current()
        p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
        for s in Site.objects.all():
            if re.search(p, self.request.META['HTTP_HOST']).group('host') in s.domain:
                current_site = s

        ctx['sitename'] = current_site.name.lower()
        sites = map(lambda x: x['domain'], Site.objects.values('domain'))
        if res and res.status_code == 200:
            api_res = res.json()
            for r in api_res['resources']:
                if r[grade_naming_inv[user.grade]]:
                    if (r['teacher'] and user.role.lower() == 'teacher') or (r['student'] and user.role.lower() == 'student'):
                        other_res.append(dict(name=r['name'], url=r['url']))
                        if current_site.name.lower() in r['name'].lower():
                            auth = True


            ctx['app_auth'] = auth
            ctx['api'] = api_res
            ctx['district_name'] = api_res['district_name']
            ctx['resources'] = api_res['resources']
            ctx['other_resources'] = other_res
            ctx['user'] = user
        return ctx