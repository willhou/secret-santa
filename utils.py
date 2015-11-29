import string
import os
import logging
from google.appengine.ext.webapp import template

def fillTemplate(response, filename, values):
  path = os.path.join(os.path.dirname(__file__), filename)
  response.out.write(template.render(path, values))