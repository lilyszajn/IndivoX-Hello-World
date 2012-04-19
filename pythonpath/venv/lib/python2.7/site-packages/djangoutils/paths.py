from datetime import datetime
from django.conf import settings
import re
import os


def join_urls(front, back = None):
  """
  Join two sections of a url, being sensible with slashes.  eg:

    >>> join_urls("http://playfi.com", "explore")
    'http://playfi.com/explore'

    >>> join_urls("http://playfi.com", "/explore")
    'http://playfi.com/explore'

    >>> join_urls("http://playfi.com/", "/explore")
    'http://playfi.com/explore'

    >>> join_urls("http://localhost/playfi/", "/playfi/explore")
    'http://localhost/playfi/explore'

  Also, if back is unspecified, just returns front:
    >>> join_urls("http://playfi.com/")
    'http://playfi.com/'
  """

  if back:
    if back.startswith('/'):
      n = 0
      m = re.search('[^/]/[^/]', front)
      if m:
        n = m.start() + 1
      else:
        m = re.search('[^/]/$', front)
        if m:
          n = m.start() + 1
        else:
          m = re.search('//', front)
          if m:
            n = len(front)
      return "%s/%s" % (front[0:n], back[1:])

    return "%s/%s" % (front[0:-1] if front.endswith("/") else front, back)

  else:
    return front


def site_url_absolute(url = None):
  """
  Returns a full URL, eg: "http://playfi.com/explore".
  """
  return join_urls(settings.SITE_URL, url)


def path_absolute(url = None):
  """
  ...
  """
  return join_urls(settings.URL_PREFIX, url)


def static_url(url = None, is_secure = False):
  return join_urls(settings.STATIC_URL, url)

def media_url(url = None):
  return join_urls(settings.MEDIA_URL, url)


def media_path(path = None):
  if path == None:
    return settings.MEDIA_ROOT
  else:
    return os.path.join(settings.MEDIA_ROOT, path)


