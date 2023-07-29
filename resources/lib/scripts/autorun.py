#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json

from xbmc      import executeJSONRPC,log,Monitor
from xbmcaddon import Addon

__addon__ = Addon('plugin.program.addonadministrator')

def checkfilesetting():
	check_status = executeJSONRPC(json.dumps({ "jsonrpc": "2.0", "method": "Settings.GetSettingValue","params":{"setting":"filelists.showhidden"}, "id": "1"}))
	check_status = json.loads(check_status)['result']['value']
	if check_status:
		__addon__.setSetting('general.hidden.files', __addon__.getLocalizedString(30022))
	else:
		__addon__.setSetting('general.hidden.files', __addon__.getLocalizedString(30023))
	Log(f'filelists.showhidden = {check_status} addon setting = {__addon__.getSetting("general.hidden.files")}')

def Log(msg):
	if __addon__.getSettingBool('general.debug'):
		from inspect import getframeinfo, stack
		fileinfo = getframeinfo(stack()[1][0])
		log('*__{}__{}*{} Python file name = {} Line Number = {}'.format(__addon__.getAddonInfo('name'),__addon__.getAddonInfo('version'),msg,fileinfo.filename,fileinfo.lineno), level=xbmc.LOGINFO)

if __name__ == '__main__':
	monitor = Monitor()
	while not monitor.abortRequested():
		if monitor.waitForAbort(600):
			break
		checkfilesetting()