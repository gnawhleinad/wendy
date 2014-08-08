#!/usr/bin/python

import os, subprocess
import urllib
import re

class Jenkins:
  def __init__(self, port):
    cli_location = '/usr/local/jenkins-cli'
    if not os.path.isdir(cli_location) or not os.access(cli_location, os.W_OK):
      cli_location = os.path.join(os.path.expanduser('~'), 
                                  '.wendy/jenkins-cli')
      if not os.path.isdir(cli_location):
        # http://bugs.python.org/issue21082
        os.makedirs(cli_location, exist_ok=True)

    self._cli = os.path.join(cli_location, 'jenkins-cli.jar')
    self._url = 'http://localhost:{0}'.format(port)
    if not os.path.isfile(self._cli):
      urllib.request.urlretrieve(
        '{0}/jnlpJars/jenkins-cli.jar'.format(self._url), self._cli)

  def _run_cli(self, command):
    return subprocess.check_output(['java', '-jar', self._cli, 
                                            '-s', self._url,
                                            command],
                                   universal_newlines=True)

  def get_plugin_version(self, plugin):
    return re.match('.*\n{0}\s+[^\n]*?([\d\.]+)\n'.format(plugin), 
                    self._run_cli('list-plugins'), 
                    re.MULTILINE|re.DOTALL)
