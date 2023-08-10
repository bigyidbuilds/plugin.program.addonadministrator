#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import xbmcvfs
from .utils import Log

def _GetData(path):
	if path.startswith('special://'):
		path = xbmcvfs.translatePath(path)
	if xbmcvfs.exists(path):
		f = open(path)
		data = json.load(f)
		f.close()
		return data
	else:
		Log('No data to return')
		return None

def ReadAddonInfo(path,addonid,backup_dt):
	#returns addon info for a specified backup from datetime key
	data = _GetData(path)
	if data:
		a = data.get(addonid)
		if a:
			backup_data = a.get(backup_dt)
			if backup_data:
				return backup_data.get('addon')
			else:
				return None
		else:
			return None
	else:
		return None	

def ReadAddons(path):
	#Reads back up file and returns a list of addon id's that have a back up
	data = _GetData(path)
	if data:
		keys = data.keys()
		Log(keys)
		return list(keys)
	else:
		Log('No addon data to return')
		return None

def ReadChoices(path,addonid):
	#Reads back up file and returns a list of backup choices for a addon id passed through
	data = _GetData(path)
	if data:
		addondata = data.get(addonid)
		if addondata:
			keys = addondata.keys()
			Log(keys)
			return list(keys)
		else:
			Log('No Choices data to return')
			return None


def ReadSavedSettings(path,addonid,backup_dt):
	#returns addon settings for a specified backup from datetime key
	data = _GetData(path)
	if data:
		a = data.get(addonid)
		if a:
			backup_data = a.get(backup_dt)
			if backup_data:
				return backup_data.get('settings')
			else:
				return None
		else:
			return None
	else:
		return None	


def ReadSavedSetting(path,addonid,backup_dt,settingId):
	#returns addon settings for a specified backup from datetime key
	Log(settingId)
	data = _GetData(path)
	if data:
		a = data.get(addonid)
		if a:
			backup_data = a.get(backup_dt)
			if backup_data:
				settings = backup_data.get('settings')
				if settings:
					return settings.get(settingId)
				else:
					return None
			else:
				return None
		else:
			return None
	else:
		return None		


