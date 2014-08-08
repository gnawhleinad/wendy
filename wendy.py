#!/usr/bin/python

import os
import urllib

class Jenkins:
  def __init__(self, port):
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
