#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import xbmc
from pathlib import Path
import glob
import os
import xbmcaddon
import xbmcvfs



def GetAddonsWithSettings():
	'''Returns a list of dicts of addons inc path,addon id and name that have a settings.xml'''
	addon_with = list()
	addon_data = os.path.join(xbmcvfs.translatePath('special://userdata'),'addon_data')
	query = os.path.join(addon_data,'**','settings.xml')
	matches = glob.glob(query,recursive=True)
	for match in matches:
		sp = Path(match).parts
		addon_id   = sp[-2]
		addon_info = xbmc.executeJSONRPC(json.dumps({ "jsonrpc": "2.0", "method": "Addons.GetAddonDetails","params":{"addonid":f"{addon_id}","properties":["name","thumbnail","enabled"]}, "id": "1"}))
		addon_info = json.loads(addon_info)
		try:
			addon_enabled = addon_info['result']['addon']['enabled']
			addon_name    = addon_info['result']['addon']['name']
			addon_type    = addon_info['result']['addon']['type']
			addon_thumb   = addon_info['result']['addon']['thumbnail']
			addon_with.append({'addon_id':addon_id,'addon_info':addon_info,'path':match,'addon_enabled':addon_enabled,'addon_name':addon_name,'addon_type':addon_type,'addon_thumb':addon_thumb})
		except KeyError:
			pass
		
	return addon_with


def GetSysAddons():
	addons = xbmc.executeJSONRPC(json.dumps({"jsonrpc":"2.0","method":"Addons.GetAddons","params":{"enabled":True},"id":"1"}))
	addons = json.loads(addons)['result']['addons']
	return addons

	