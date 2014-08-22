#!/usr/bin/python

import unittest
import os, sys, subprocess

from test.util import wait

PORT = 8080
DATA = '/var/lib/jenkins/'

class AptTestCase(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    self.port = PORT
    super(AptTestCase, self).__init__(*args, **kwargs)

  def setUp(self):
    subprocess.check_call(['/bin/bash', '-c', 
                           'sudo apt-get purge --yes jenkins'])
    subprocess.check_call(['/bin/bash', '-c', 
                           'sudo apt-get update -qq'])
    subprocess.check_call(['/bin/bash', '-c', 
                           'sudo apt-get install --yes jenkins'])
    subprocess.check_call(['/bin/bash', '-c', 
      '{0} {1}'.format(
        os.path.join(
          os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
          'util',
          'permission.sh'),
        '$(id -gn)')])
    subprocess.check_call(
      ['/bin/bash',
       os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    'util', 
                    'run.sh'),
       'false',
       'true'])
    wait.main(PORT)
    super(AptTestCase, self).setUp()
