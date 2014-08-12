#!/usr/bin/python

import os
import re
import uuid

from lxml import etree

from .Parameters import Parameters
from .CLI import CLI

class Jenkins:
  def __init__(self, port=None, home=None):
    self._parameters = Parameters(port, home)
    self.cli = CLI(self._parameters)

  def get_plugin_version(self, plugin):
    return re.match('.*\n{0}\s+[^\n]*?([\d\.]+)'.format(plugin),
                    self.cli.run('list-plugins'), 
                    re.MULTILINE|re.DOTALL).group(1)

  def add_credential(self, username, description, private_key_location):
    credentials_file = os.path.join(self._parameters.home, 'credentials.xml')

    credentials = None
    if os.path.isfile(credentials_file):
      parser = etree.XMLParser(remove_blank_text=True)
      credentials = etree.parse(credentials_file, parser)
    else:
      credentials = self._create_credentials()

    credential_list = credentials.xpath(
      '/{0}/{1}/{2}/{3}'.format(
        'com.cloudbees.plugins.credentials.SystemCredentialsProvider',
        'domainCredentialsMap',
        'entry',
        'java.util.concurrent.CopyOnWriteArrayList'))[0]

    credential_list.append(self._add_credential(username, 
                                                description, 
                                                private_key_location))

    with open(credentials_file, 'w') as f:
      f.write(etree.tostring(credentials,
                             xml_declaration=True,
                             encoding='UTF-8',
                             pretty_print=True).decode('utf-8'))

  def _add_credential(self, 
                      username, 
                      description, 
                      private_key_location):
    name = \
      'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey'
    credential = etree.Element(name,
      plugin='ssh-credentials@{0}'.format(self.get_plugin_version(
        'ssh-credentials')))

    etree.SubElement(credential, 'scope').text = 'SYSTEM'
    etree.SubElement(credential, 'id').text = str(uuid.uuid4())
    etree.SubElement(credential, 'description').text = description
    etree.SubElement(credential, 'username').text = username
    etree.SubElement(credential, 'passphrase')
    private_key = etree.SubElement(credential, 'privateKeySource',
      attrib={'class':
        '{0}$FileOnMasterPrivateKeySource'.format(name)})
    etree.SubElement(private_key, 'privateKeyFile').text = private_key_location

    return credential

  def _create_credentials(self):
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

    etree.SubElement(entry, 'java.util.concurrent.CopyOnWriteArrayList')

    return credentials.getroottree()
