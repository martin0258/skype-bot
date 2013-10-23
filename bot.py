#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2013 martinku <martinku@ss-martin-ku>
#
# Distributed under terms of the MIT license.

"""
Send a message to someone (or a group).
"""

import Skype4Py
import platform
import ConfigParser
import argparse
import sys
import datetime
import os

# main program
if __name__ == "__main__":
  folder = os.path.dirname(os.path.abspath(__file__))

  description = "========== Use Skype Bot to send messages automatically =========="
  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-c', '--config', default='example.cfg', help='config file. Use [example.cfg] by default')
  parser.add_argument('-l', '--logfile', default='running.log', help='log file. Use [running.log] by default')
  parser.add_argument('-v', '--version', action='version', version='Skype Bot 0.1')
  args = parser.parse_args()

  # Read configurations from config file
  configFullPath     = "%s/%s" % (folder, args.config)
  config             = ConfigParser.ConfigParser()
  config.optionxform = str
  config.read(configFullPath)
  Skype4PyInterface = config.get('Skype4Py','interface')
  blob              = config.get('Skype','blob')
  message           = config.get('Skype','message')
  triggerDay        = config.get('Automation', 'weekday')

  # Set up log file
  executionTime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
  logFileFullPath = "%s/%s" % (folder, args.logfile)
  logFile = open(logFileFullPath, 'a+')
  logFile.write('[%s] ' % executionTime)
  logMessage = 'Message not sent. (for some reasons)'

  if str(datetime.date.today().weekday()) == triggerDay:
    osPlatform = platform.system()
    skype = Skype4Py.Skype(Transport=Skype4PyInterface) if osPlatform=="Linux" else Skype4Py.Skype()
    skype.Attach()
    chat = skype.CreateChatUsingBlob(blob)
    chat.SendMessage(message)
    logMessage = 'Message sent.'

  logFile.write('%s\n' % logMessage)
  logFile.flush()
  os.fsync(logFile.fileno())
  logFile.close()
  sys.exit(0)
