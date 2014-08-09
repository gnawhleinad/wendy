#!/usr/bin/python

import re
import uuid

from lxml import etree

from .Parameters import Parameters
from .CLI import CLI

class Jenkins:
  def __init__(self, port=None, home=None):
    self._parameters = Parameter(port, home)
    self.cli = CLI(self._paramters)

  def get_plugin_version(self, plugin):
    return re.match('.*\n{0}\s+[^\n]*?([\d\.]+)'.format(plugin),
                    self.cli.run('list-plugins'), 
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
