#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

from resources.lib.modules.utils import Log

__addon__ = xbmcaddon.Addon('plugin.program.addonadministrator')

def HiddenFiles():
	check_status = CheckStatus()
	check_status = json.loads(check_status)['result']['value']
	Log(check_status)
	if check_status:
		__addon__.setSetting('general.hidden.files', __addon__.getLocalizedString(30022))
		w = __addon__.getLocalizedString(30023)
		s = False
	else:
		__addon__.setSetting('general.hidden.files', __addon__.getLocalizedString(30023))
		w = __addon__.getLocalizedString(30022)
		s = True
	msg = f"{__addon__.getLocalizedString(30021)} {__addon__.getSettingString('general.hidden.files')}\n{__addon__.getLocalizedString(30025)} {w}"
	ret = xbmcgui.Dialog().yesno(__addon__.getAddonInfo('name'), msg)
	if ret:
		xbmc.executeJSONRPC(json.dumps({ "jsonrpc": "2.0", "method": "Settings.SetSettingValue","params":{"setting":"filelists.showhidden", "value":s}, "id": "1"}))
		if json.loads(CheckStatus())['result']['value']:
			__addon__.setSetting('general.hidden.files', __addon__.getLocalizedString(30022))
		else:
			__addon__.setSetting('general.hidden.files', __addon__.getLocalizedString(30023))

def ImportPath():
	items = [{'name':__addon__.getLocalizedString(30026),'method':'select_path','path':__addon__.getSettingString('import.path')},{'name':'special://home','method':'fixed_path','path':xbmcvfs.translatePath('special://home')},{'name':'special://userdata','method':'fixed_path','path':xbmcvfs.translatePath('special://userdata')}]
	itemlist = []
	for i in items:
		li = xbmcgui.ListItem(i.get('name'))
		li.setProperties(i)
		itemlist.append(li)
	ret = xbmcgui.Dialog().select(__addon__.getLocalizedString(30027), itemlist)
	selected = items[ret]
	method = selected.get('method')
	path = selected.get('path')
	if method == 'select_path':
		__addon__.setSetting('import.path',xbmcgui.Dialog().browseSingle(0,__addon__.getLocalizedString(30015),'',defaultt=path))
	elif method == 'fixed_path':
		__addon__.setSetting('import.path',path)
	else:
		return


def CheckStatus():
	return xbmc.executeJSONRPC(json.dumps({ "jsonrpc": "2.0", "method": "Settings.GetSettingValue","params":{"setting":"filelists.showhidden"}, "id": "1"}))