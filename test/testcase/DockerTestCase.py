#!/usr/bin/python

import unittest
import os, sys, subprocess, shutil
import docker

from test.util import wait

PORT = 4242
HOME = '/var/lib/jenkins/test'

class DockerTestCase(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    self._client = docker.Client(base_url='unix://var/run/docker.sock')
    if self._client.containers(all=True, quiet=True):
      self._container = self._client.containers(all=True, quiet=True)[0]
    else:
      self._container = self._client.create_container('wendy/dev', ports=[8080])
    self.port = PORT
    super(DockerTestCase, self).__init__(*args, **kwargs)

  def setUp(self):
    permission = os.path.join(
      os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
      'util',
      'permission.sh')
    subprocess.check_call(['/bin/bash', '-c', permission])
    os.mkdir(HOME)
    self._client.start(self._container, 
                       binds={'/var/lib/jenkins': {
                                'bind': HOME,
                                'ro': False}}, 
                       port_bindings={8080:PORT})
    wait.main(PORT)
    subprocess.check_call(['/bin/bash', '-c', permission])
    super(DockerTestCase, self).setUp()

  def tearDown(self):
    self._client.kill(self._container)
    shutil.rmtree(HOME)
    super(DockerTestCase, self).tearDown()
