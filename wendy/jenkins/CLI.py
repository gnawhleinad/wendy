#!/usr/bin/python

import subprocess

from .Parameters import Parameters

class CLI:
  def __init__(self, parameters):
    self._parameters = parameters

  def run(self, command):
    return subprocess.check_output(['java', '-jar', self._parameters.cli,
                                            '-s', self._parameters.url,
                                            command],
                                   universal_newlines=True)
