from .proctoru import ProctorUXBlock
from django.template.loader import add_to_builtins

add_to_builtins('proctoru.templatetags.validator')
