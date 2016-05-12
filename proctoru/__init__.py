# do not include any code here, since this module is loaded by the LMS/CMS
# settings.

from .proctoru import ProctorUXBlock
from django.template.loader import add_to_builtins

add_to_builtins('proctoru.templatetags.proctoru_validator')