from djangoutils.templatetags.context_tag import context_tag
from django import template
from django.conf import settings
from djangoutils import paths

register = template.Library()

@context_tag(register)
def media_url(context, path = None): 
  return paths.media_url(path)

@context_tag(register)
def static_url(context, path = None): 
  return paths.static_url(path)

@context_tag(register)
def site_url_absolute(context, *args):
  return paths.site_url_absolute("".join(map(unicode, args)))

@context_tag(register)
def path_absolute(context, *args):
  return paths.path_absolute("".join(map(unicode, args)))

@register.simple_tag
def url_prefix():
  return settings.URL_PREFIX

