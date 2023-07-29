#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import xml.etree.ElementTree as ET

from .utils import DateTimeNow,Log


def BackUp(addon_id,path):
	__addon__ = xbmcaddon.Addon('plugin.program.addonadministrator')
	__retaddon__ = xbmcaddon.Addon(addon_id)
	data  = {}
	data2 = {}
	dtnow = DateTimeNow()
	settings_path = os.path.join(xbmcvfs.translatePath('special://userdata'),'addon_data',f'{addon_id}','settings.xml')
	if path.startswith('special'):
		path = xbmcvfs.translatePath(path)
	if not xbmcvfs.exists(path):
		xbmcvfs.mkdirs(path)
	save_file_path = os.path.join(path,'addonsettings.buk')
	if xbmcvfs.exists(save_file_path):
		f = open(save_file_path)
		data = json.load(f)
		f.close()
	if xbmcvfs.exists(settings_path):
		if data.get(addon_id) is None:
			data.update({addon_id:{}})
		addondata = data.get(addon_id)
		try:
			addoninfo = xbmcaddon.Addon(addon_id)
			name = addoninfo.getAddonInfo('name')
			version = addoninfo.getAddonInfo('version')
		except:
			name = addon_id
			version = None
		addondata[dtnow] = {'addon':{'id':addon_id,'name':name,'version':version},'settings':{}}
		tree = ET.parse(settings_path)
		root = tree.getroot()
		settings = addondata.get(dtnow).get('settings')
		for s in root.findall('setting'):
			setting_id = s.get('id')
			setting_value = s.text
			settings[setting_id]=setting_value
	with open(save_file_path,'w') as fp:
		fp.seek(0, 0)
		json.dump(data,fp,indent=4)
	xbmcgui.Dialog().notification(__addon__.getAddonInfo('name'),f"{__retaddon__.getAddonInfo('name')} {__addon__.getLocalizedString(30042)}",__retaddon__.getAddonInfo('icon'))
