#!/usr/bin/python

import unittest
import urllib
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
from wendy.jenkins import Jenkins

PORT = 8080

class TestInstall(unittest.TestCase):
  def test_exists(self):
    self.assertEqual(
      urllib.request.urlopen('http://localhost:{0}'.format(PORT)).getcode(),
      200)

class TestInitialize(unittest.TestCase):
  def test_init(self):
    jenkins = Jenkins(PORT)
    self.assertTrue(os.path.isfile(jenkins._cli))

class TestPlugin(unittest.TestCase):
  def test_version(self):
    jenkins = Jenkins(PORT)
    self.assertIsNotNone(jenkins.get_plugin_version('ssh-credentials'))
