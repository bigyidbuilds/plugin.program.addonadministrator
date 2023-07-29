#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

from .import backupfile
from .utils import Log,PathTranslate


def Restore(addonid,backup_path):
	__addon__ = xbmcaddon.Addon('plugin.program.addonadministrator')
	__retaddon__ = xbmcaddon.Addon(addonid)
	choice = []
	backup_path = PathTranslate(backup_path)
	if xbmcvfs.exists(backup_path):
		choices = backupfile.ReadChoices(backup_path,addonid)
		for date in choices:
			choice.append(xbmcgui.ListItem(date))
		ret = xbmcgui.Dialog().select(f"{__addon__.getLocalizedString(30014)} {__retaddon__.getAddonInfo('name')}",choice)
		if ret >= 0:
			from .guicontrol import SettingsCheck
			d=SettingsCheck(addonid,backup_path,choice[ret].getLabel())
			d.doModal()
			check_cont = d.buttonPressed
			settings   = d.settingsRet
			del d
			if check_cont:
				# settings = data.get(list(data.keys())[ret])
				for k,v in settings.items():
					if type(v) == str and not v in ['true','false']:
						xbmcaddon.Addon(addonid).setSettingString(k,v)
					elif v in ['true','false'] :
						v = json.loads(v)
						xbmcaddon.Addon(addonid).setSettingBool(k,v)
					elif type(v) == int:
						xbmcaddon.Addon(addonid).setSettingInt(k,v)
					elif type(v) == float:
						xbmcaddon.Addon(addonid).setSettingNumber(k,v)
					else:
						continue
				xbmcgui.Dialog().notification(__addon__.getAddonInfo('name'),f"{__retaddon__.getAddonInfo('name')} {__addon__.getLocalizedString(30041)}",__retaddon__.getAddonInfo('icon'))
			else:
				return
		else:
			return
	else:
		return




