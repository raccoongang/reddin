"""Xblock which render remote content by url in iframe and send crypted student data in GET param."""

import json
import logging
import urllib
from importlib.resources import files

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean, Dict, Scope, String
from xblock.utils.studio_editable import StudioEditableXBlockMixin

from django.contrib.auth import get_user_model
from django.template import Template, Context
from django.conf import settings
from openedx.core.djangoapps.theming.helpers import get_current_request

from .utils import AESCipher

log = logging.getLogger(__name__)

# Make '_' a no-op so we can scrape strings
_ = lambda text: text


@XBlock.needs('user')
class ReddinXBlock(StudioEditableXBlockMixin, XBlock):
    """
    Xblock which render remote content by url in iframe and send crypted student data in GET param.
    """

    display_name = String(
        display_name=_("Display Name"),
        help=_("This name appears in the horizontal navigation at the top of the page."),
        default="Reddin XBlock",
        scope=Scope.settings
    )

    url = String(
        display_name=_("Reddin URL"),
        default="",
        scope=Scope.content
    )

    data_params = Dict(
        display_name=_("URL Parameters"),
        help=_('Example: {"name1": "value1", "name2": "value2"}'),
        default={},
        scope=Scope.content
    )

    session_variable = Boolean(
        display_name=_("Session Variable"),
        help=_('Add the session variable to the URL.'),
        default=False,
        scope=Scope.content
    )

    editable_fields = ('display_name', 'url', 'data_params', 'session_variable')

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        return files(__package__).joinpath(path).read_text(encoding="utf8")

    def student_view(self, context=None):
        """
        The primary view of the ReddinXBlock, shown to students
        when viewing courses.
        """
        if context is None:
            context = {}

        encoded = self.get_encoded_data()
        parameters = ''
        if self.data_params:
            for key, value in self.data_params.items():
                parameter = f'&{key}={value}'
                parameters += parameter

        if self.url:
            context['url_string'] = self.url + encoded + parameters
            if self.session_variable:
                session_id = self.get_session_id()
                if session_id:
                    context['url_string'] += '&SessionID=' + urllib.parse.quote(session_id)
                else:
                    log.warning("Reddin block %s: no session cookie, SessionID omitted", self.scope_ids.usage_id)
        else:
            context['url_string'] = ''

        html = self.render_template("static/html/reddin.html", context)
        frag = Fragment(html.format(self=self))
        return frag

    def render_template(self, template_path, context):
        """
        Allow django template processing

        :param template_path: path to template
        :param context: context dictionary
        :return: rendered content
        """
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        return template.render(Context(context))

    def get_session_id(self):
        """
        Get the LMS/Studio session id of the current request, or None outside a request
        """
        request = get_current_request()
        if request is None:
            return None
        return request.COOKIES.get(settings.SESSION_COOKIE_NAME)

    @property
    def reddin_secret_key(self):
        """
        Get Reddin secret key from settings
        """
        return getattr(settings, 'REDDIN_SECRET_KEY', '')

    def get_encoded_data(self):
        """
        Collect all data needed and encode it
        Returns: string

        """
        xblock_user = self.runtime.service(self, "user").get_current_user()
        # First/last name aren't exposed by the user service; load them by id so
        # masquerading staff still get the masqueraded learner's name.
        user = get_user_model().objects.get(id=xblock_user.opt_attrs['edx-platform.user_id'])
        data = {
            'course_id': str(self.course_id),
            'username': xblock_user.opt_attrs['edx-platform.username'],
            'email': xblock_user.emails[0],
            'fullname': f'{user.first_name} {user.last_name}'
        }
        row = json.dumps(data)
        encoded = AESCipher(self.reddin_secret_key).encrypt(row)

        return f'?data={urllib.parse.quote(encoded)}'
