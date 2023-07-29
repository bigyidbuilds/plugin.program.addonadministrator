#!/usr/bin/python3
# -*- coding: utf-8 -*-

def DateTimeNow(fmt='%Y.%m.%d-%H:%M'):
	from datetime import datetime
	return datetime.now().strftime(fmt)


def Log(msg):
	import xbmc
	import xbmcaddon
	__addon__ = xbmcaddon.Addon('plugin.program.addonadministrator')
	if __addon__.getSettingBool('general.debug'):
		from inspect import getframeinfo, stack
		fileinfo = getframeinfo(stack()[1][0])
		xbmc.log('*__{}__{}*{} Python file name = {} Line Number = {}'.format(__addon__.getAddonInfo('name'),__addon__.getAddonInfo('version'),msg,fileinfo.filename,fileinfo.lineno), level=xbmc.LOGINFO)

def PathTranslate(path):
	from xbmcvfs import translatePath
	if path.startswith('special'):
		path = translatePath(path)
	return path