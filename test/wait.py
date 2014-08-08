#!/usr/bin/python

import urllib
import time

PORT = 8080

def check():
  return urllib.request.urlopen('http://localhost:{0}'.format(PORT)).getcode()

def main():
  code = 0
  retry = 0
  while code != 200 and retry < 10:
    retry += 1
    try:
      code = check()
    except:
      time.sleep(4.2)
      pass

if __name__ == '__main__':
  main()
