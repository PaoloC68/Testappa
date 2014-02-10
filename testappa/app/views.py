# Create your views here.
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.views.generic import TemplateView
import requests


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
grade_naming_inv = {v: k for k, v in grade_naming.items()}

class IndexView(TemplateView):
    template_name = 'index.html'

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'protected.html'

    def get_context_data(self, **kwargs):
        ctx = super(ProtectedView, self).get_context_data(**kwargs)
        headers = {'content-type': 'application/json'}
        user = self.request.user
        organization = user.organization
        api_res = requests.get('http://idp.logintex.me:8088/api/districts/{0}/'.format(organization),
                               headers=headers).json()
        auth = False
        for r in api_res['resources']:
            if r['url'].lower() == settings.RESOURCE_URL.lower() and organization in r['district']:
                if r[grade_naming_inv[user.grade]]:
                    auth = True

        ctx['app_auth'] = auth
        ctx['api'] = api_res
        ctx['distict_name'] = api_res['district_name']
        ctx['resources'] = api_res['resources']
        ctx['user'] = user
        return ctx