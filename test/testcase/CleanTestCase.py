#!/usr/bin/python

import os, sys, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if os.environ.get('TRAVIS'):
  from test.testcase.AptTestCase import AptTestCase as CleanTestCase
else:
  from test.testcase.DockerTestCase import DockerTestCase as CleanTestCase
