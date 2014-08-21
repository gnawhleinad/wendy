#!/usr/bin/python

import urllib
import time
import math

def check(port):
  return urllib.request.urlopen('http://localhost:{0}'.format(port)).getcode()

def main(port):
  time.sleep(314/60)

  code = 0
  retry = 0
  while code != 200 and retry < 5:
    retry += 1
    try:
      code = check(port)
    except:
      time.sleep(math.pow(4.2, retry))
      pass

if __name__ == '__main__':
  main()
