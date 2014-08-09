#!/usr/bin/python

import os
import urllib
import getpass

class InvalidHome(Exception):
  def __init__(self, home):
    self.home = home
  def __str__(self):
    return 'Invalid jenkins home "{0}"'.format(self.home)

class InvalidHomeAccess(Exception):
  def __init__(self, home):
    self.home = home
  def __str__(self):
    return 'Invalid access for user "{0}" at jenkins home "{1}"'.format(
      getpass.getuser(),
      self.home)

class Parameters:
  def __init__(self, port=None, home=None):
    if port is None:
      port = 8080

    if home is None:
      home = '/var/lib/jenkins'

    self.home = home
    if os.path.isdir(self.home):
      if not os.access(self.home, os.W_OK):
        raise InvalidHomeAccess(self.home)
    else:
      raise InvalidHome(self.home)

    cli_location = '/usr/local/jenkins-cli'
    if not os.path.isdir(cli_location) or not os.access(cli_location, os.W_OK):
      cli_location = os.path.join(os.path.expanduser('~'), 
                                  '.wendy/jenkins-cli')
      if not os.path.isdir(cli_location):
        # http://bugs.python.org/issue21082
        os.makedirs(cli_location, exist_ok=True)

    self.cli = os.path.join(cli_location, 'jenkins-cli.jar')
    self.url = 'http://localhost:{0}'.format(port)
    if not os.path.isfile(self.cli):
      urllib.request.urlretrieve(
        '{0}/jnlpJars/jenkins-cli.jar'.format(self.url), self.cli)
