#!/usr/bin/python

import unittest
import urllib
import os, sys, subprocess
import docker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wendy.jenkins.Jenkins import Jenkins
from test import wait

PORT = 8080

class DockerTestCase(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    self._client = docker.Client(base_url='unix://var/run/docker.sock')
    if self._client.containers(all=True, quiet=True):
      self._container = self._client.containers(all=True, quiet=True)[0]
    else:
      self._container = self._client.create_container('wendy/dev', ports=[8080])
    super(DockerTestCase, self).__init__(*args, **kwargs)

  def setUp(self):
    self._client.start(self._container, 
                       binds={'/var/lib/jenkins': {
                                'bind': '/var/lib/jenkins', 
                                'ro': False}}, 
                       port_bindings={8080:8080})
    wait.main()
    subprocess.check_call(['/bin/bash', '-c', 
      os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                   'permission.sh')])
    super(DockerTestCase, self).setUp()

  def tearDown(self):
    self._client.kill(self._container)
    super(DockerTestCase, self).tearDown()

class TestPlugin(DockerTestCase):
  def test_version(self):
    jenkins = Jenkins(PORT)
    self.assertIsNotNone(jenkins.get_plugin_version('ssh-credentials'))
