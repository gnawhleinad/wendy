#!/usr/bin/python

import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from wendy.jenkins.Parameters import Parameters

PORT = 8080

class TestInitialize(unittest.TestCase):
  def test_init(self):
    parameters = Parameters(PORT)
    self.assertTrue(os.path.isdir(parameters.home))
    self.assertTrue(os.access(parameters.home, os.W_OK))
    self.assertTrue(os.path.isfile(parameters.cli))
