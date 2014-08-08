#!/usr/bin/python

import os, subprocess
import urllib
import re
import getpass
import uuid

from lxml import etree

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

class Jenkins:
  def __init__(self, port=None, home=None):
    if port is None:
      port = 8080

    if home is None:
      home = '/var/lib/jenkins'

    self._home = home
    if os.path.isdir(self._home):
      if not os.access(self._home, os.W_OK):
        raise InvalidHomeAccess(self._home)
    else:
      raise InvalidHome(self._home)

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
    return re.match('.*\n{0}\s+[^\n]*?([\d\.]+)'.format(plugin),
                    self._run_cli('list-plugins'), 
                    re.MULTILINE|re.DOTALL)

  def add_credential(self, username, description, private_key_location):
    return self._create_credentials(username, description, private_key_location)

  def _create_credentials(self, username, description, private_key_location):
    credentials = etree.Element(
      'com.cloudbees.plugins.credentials.SystemCredentialsProvider',
      plugin='credentials@{0}'.format(self.get_plugin_version('credentials')))
    dcm = etree.SubElement(credentials,
                           'domainCredentialsMap',
                           attrib={'class': 'hudson.util.CopyOnWriteMap$Hash'})
    entry = etree.SubElement(dcm, 'entry')

    domain_credentials = etree.SubElement(entry,
      'com.cloudbees.plugins.credentials.domains.Domain')
    domain_credentials.append(etree.Element('specifications'))

    ssh_credentials_element = \
      'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey'
    cowal = etree.SubElement(entry, 'java.util.concurrent.CopyOnWriteArrayList')
    ssh_credentials = etree.SubElement(cowal, ssh_credentials_element,
      plugin='ssh-credentials@{0}'.format(self.get_plugin_version(
        'ssh-credentials')))
    etree.SubElement(ssh_credentials, 'scope').text = 'SYSTEM'
    etree.SubElement(ssh_credentials, 'id').text = str(uuid.uuid4())
    etree.SubElement(ssh_credentials, 'description').text = description
    etree.SubElement(ssh_credentials, 'username').text = username
    etree.SubElement(ssh_credentials, 'passphrase')
    private_key = etree.SubElement(ssh_credentials, 'privateKeySource',
      attrib={'class':
        '{0}$FileOnMasterPrivateKeySource'.format(ssh_credentials_element)})
    etree.SubElement(private_key, 'privateKeyFile').text = private_key_location

    return etree.tostring(credentials,
             xml_declaration=True, encoding='UTF-8', pretty_print=True)
