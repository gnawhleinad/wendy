#!/usr/bin/python

import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wendy.jenkins.Jenkins import Jenkins
from test.testcase.DockerTestCase import DockerTestCase

class TestPlugin(DockerTestCase):
  def test_version(self):
    jenkins = Jenkins(self.port)
    self.assertIsNotNone(jenkins.get_plugin_version('ssh-credentials'))
