#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import json


from.utils import Log

from .backupfile import ReadSavedSetting,ReadAddonInfo,ReadSavedSettings
from .getsettings import GetSettingsCats,GetSettingLabel,GetSettingsInfo,GetSettingsGrp,GetSettings,GetSettingOptions

__addon__     = xbmcaddon.Addon('plugin.program.addonadministrator')
__addonpath__ = xbmcvfs.translatePath(__addon__.getAddonInfo('path'))

#ACTIONS
ACTION_LEFT          = 1
ACTION_RIGHT         = 2
ACTION_UP            = 3
ACTION_DOWN          = 4
ACTION_SELECT_ITEM   = 7
ACTION_PREVIOUS_MENU = 10
ACTION_NAV_BACK      = 92
KEY_ESC              = 61467

class SettingsCheck(xbmcgui.WindowXMLDialog):

	CLOSE                      = 1000
	HEADER                     = 1001
	CONTINUE                   = 2001
	CANCEL                     = 2002
	# MOREINFO                   = 2003
	ADDONCHECK_LABEL           = 3001
	ADDONCHECK_TICK            = 3002
	ADDONCHECK_X               = 3003
	SETTINGCHECK_LABEL         = 3004
	SETTINGCHECK_TICK          = 3005
	SETTINGCHECK_X             = 3006
	ADDONCHECK_VER_INFO        = 3007
	SETTINGCHECK_OUTCOME_LABEL = 3008
	SETTINGCHECK_NAMES         = 3009

	buttonPressed = False
	settingsRet      = {}
	
	def __new__(cls,addonid,backup_path,backup_dt):
		return super(SettingsCheck, cls).__new__(cls,'Settings_Check.xml', __addonpath__,'Default', '720p')

	def __init__(self,addonid,backup_path,backup_dt):
		super(SettingsCheck,self).__init__()
		self.settinginfo  = GetSettingsInfo(addonid)

		self.addoninfo_bk = ReadAddonInfo(backup_path,addonid,backup_dt)
		self.settings_bk  = ReadSavedSettings(backup_path,addonid,backup_dt)
		self.settings_bk_id = list(self.settings_bk.keys())
		Log(self.settings_bk)
		self.addon = xbmcaddon.Addon(addonid)
		self.addonname = self.addon.getAddonInfo('name')
		self.addoninfo_bk_ver = self.addoninfo_bk.get('version')
		self.checkaddon = True if self.addoninfo_bk_ver == self.addon.getAddonInfo('version') else False
		self.settingcheck = []
		for i in self.settinginfo:
			if not i.get('id') in self.settings_bk_id:
				self.settingcheck.append(i)
		self.settingcheck_name_str = ""
		if len(self.settingcheck) >= 1:
			for i in self.settingcheck:
				self.settingcheck_name_str += f"{GetSettingLabel(addonid,i.get('label'))}\n"



	def onInit(self):
		self.getControl(self.HEADER).setLabel(self.addonname)
		self.getControl(self.ADDONCHECK_LABEL).setLabel(f'{self.addonname} {__addon__.getLocalizedString(30038)}')
		if self.checkaddon:
			self.getControl(self.ADDONCHECK_X).setVisible(False)
		else:
			self.getControl(self.ADDONCHECK_TICK).setVisible(False)
		self.getControl(self.ADDONCHECK_VER_INFO).setLabel(__addon__.getLocalizedString(30039).format(self.addon.getAddonInfo('version'),self.addoninfo_bk_ver))
		if len(self.settingcheck) == 0:
			self.getControl(self.SETTINGCHECK_X).setVisible(False)
			self.getControl(self.SETTINGCHECK_OUTCOME_LABEL).setVisible(False)
		else:
			self.getControl(self.SETTINGCHECK_TICK).setVisible(False)
			self.getControl(self.SETTINGCHECK_NAMES).setText(self.settingcheck_name_str)

	def onClick(self,controlId):
		if controlId == self.CLOSE:
			self.Close()
		elif controlId == self.CONTINUE:
			self.buttonPressed = True
			self.settingsRet = self.settings_bk
			self.Close()
		elif controlId == self.CANCEL:
			self.buttonPressed = False
			self.Close()



	def Close(self):
		super(SettingsCheck,self).close()


class SettingCompare(xbmcgui.WindowXMLDialog):

	CATLIST     = 1000
	GROUPLIST   = 2000
	SETTINGLIST = 3000
	RESETBUTTON = 4001
	APPLYBUTTON = 4002
	CLOSEBUTTON = 4003

	def __new__(cls,backup_file,addonid,bckupdt):
		return super(SettingCompare,cls).__new__(cls,'Setting_Compare.xml', __addonpath__,'Default', '720p')

	def __init__(self,backup_file,addonid,bckupdt):
		super(SettingCompare,self).__init__()
		self.backup_file = backup_file
		self.addonid = addonid
		self.bckupdt = bckupdt
		self.cat = GetSettingsCats(self.addonid)
		self.selectedforchange = {}
		self.setlist = []
		self.__addon__ = xbmcaddon.Addon('plugin.program.addonadministrator')
		self.__ADDON__ = xbmcaddon.Addon(self.addonid)

	def onInit(self):
		self.catlistcontr = self.getControl(self.CATLIST)
		self.grplistctr = self.getControl(self.GROUPLIST)
		self.setlistctr = self.getControl(self.SETTINGLIST)
		for i in self.cat:
			li = xbmcgui.ListItem(GetSettingLabel(self.addonid,i.get('label')))
			for k,v in i.items():
				li.setProperty(k,str(v))
			self.catlistcontr.addItem(li)
		self.setFocusId(self.CATLIST)

	def onAction(self,action):
		focusid = self.getFocusId()
		if action.getId() in [ACTION_NAV_BACK,ACTION_PREVIOUS_MENU,KEY_ESC]:
			self.Close()
		elif action.getId() in [ACTION_UP]:
			if focusid == self.CATLIST:
				self.setlistctr.reset()
				pos = self.ContainerPostion(self.CATLIST)
				self.LoadGroupCtrl(self.catlistcontr.getListItem(pos))
			elif focusid == self.GROUPLIST:
				pos = self.ContainerPostion(self.GROUPLIST)
				self.LoadSetCtrl(self.grplistctr.getListItem(pos))
		elif action.getId() in [ACTION_DOWN]:
			if focusid == self.CATLIST:
				self.setlistctr.reset()
				pos = self.ContainerPostion(self.CATLIST)
				self.LoadGroupCtrl(self.catlistcontr.getListItem(pos))
			elif focusid == self.GROUPLIST:
				pos = self.ContainerPostion(self.GROUPLIST)
				self.LoadSetCtrl(self.grplistctr.getListItem(pos))
		elif action.getId() in [ACTION_SELECT_ITEM]:
			if focusid == self.SETTINGLIST:
				item = self.setlistctr.getSelectedItem()
				pos = self.setlistctr.getSelectedPosition()
				self.UpdateSelected(item)
				self.ReLoadSetCtrl(item,pos)

	def onClick(self,controlId):
		if controlId == self.CLOSEBUTTON:
			self.Close()
		elif controlId == self.APPLYBUTTON:
			self.ApplySettings()
		elif controlId == self.RESETBUTTON:
			self.ResetList()

	def onFocus(self,controlId):
		if controlId in [self.CATLIST,self.GROUPLIST,self.SETTINGLIST]:
			self.setProperty('lastfocus',str(controlId))
		if controlId == self.CATLIST:
			self.setlistctr.reset()
			pos = self.ContainerPostion(self.CATLIST)
			self.LoadGroupCtrl(self.catlistcontr.getListItem(pos))
		elif controlId == self.GROUPLIST:
			pos = self.ContainerPostion(self.GROUPLIST)
			self.LoadSetCtrl(self.grplistctr.getListItem(pos))


	def Close(self):
		super(SettingCompare,self).close()

	def LoadGroupCtrl(self,item):
		catId = item.getProperty('id')
		Log(catId)
		items = GetSettingsGrp(self.addonid,catId)
		self.grplistctr.reset()
		for i in items:
			li = xbmcgui.ListItem(GetSettingLabel(self.addonid,i.get('label')))
			li.setProperty('catid',catId)
			for k,v in i.items():
				li.setProperty(k,str(v))
			self.grplistctr.addItem(li)

	def LoadSetCtrl(self,item):
		catId = item.getProperty('catid')
		groupId = item.getProperty('id')
		self.setlistctr = self.getControl(self.SETTINGLIST)
		self.setlistctr.reset()
		items = GetSettings(self.addonid,catId,groupId)
		Log(items)
		for i in items:
			addoninfo = '[I][COLOR orange]Addon:[/I][/COLOR] '
			backupinfo = f'[I][COLOR orange]{self.__addon__.getLocalizedString(30002)}:[/I][/COLOR] '
			settinginfo = f'[I][COLOR orange]{self.__addon__.getLocalizedString(30063)}:[/I][/COLOR] '
			backupvalue = ReadSavedSetting(self.backup_file,self.addonid,self.bckupdt,i.get('id'))
			options = GetSettingOptions(self.addonid,catId,groupId,i.get('id'))
			settingvalue = self.__ADDON__.getSetting(i.get('id'))
			lilabel = GetSettingLabel(self.addonid,i.get('label'))
			settinginfo += f'{lilabel} '
			settinginfo += f'[I][COLOR grey]type:[/I][/COLOR] {i.get("type")}'
			moreinfo = False
			if options:
				moreinfo = True
				settinglabel = GetSettingLabel(self.addonid,options.get(settingvalue))
				backuplabel = GetSettingLabel(self.addonid,options.get(backupvalue))
				addoninfo += f'[I][COLOR grey]{self.__addon__.getLocalizedString(30064)}:[/I][/COLOR] {settinglabel}'
				backupinfo += f'[I][COLOR grey]{self.__addon__.getLocalizedString(30064)}:[/I][/COLOR] {backuplabel}'
			if settingvalue:
				if not options:
					settinglabel = settingvalue
					backuplabel = backupvalue
				moreinfo =True
				addoninfo += f'[I][COLOR grey]{self.__addon__.getLocalizedString(30065)}:[/I][/COLOR] {settingvalue}'
				backupinfo += f'[I][COLOR grey]{self.__addon__.getLocalizedString(30065)}:[/I][/COLOR] {backupvalue}'
			li = xbmcgui.ListItem(lilabel)
			li.setProperties({'backuplabel':backuplabel,'backupvalue':backupvalue,'settinglabel':settinglabel, 'settingvalue':settingvalue, 'catid':catId, 'groupid':groupId,'moreinfo':str(moreinfo).lower(),'settinginfo':settinginfo,'backupinfo':backupinfo,'addoninfo':addoninfo})
			for k,v in i.items():
				li.setProperty(k,str(v))
			if i.get('id') in self.selectedforchange:
				li.setProperty('selected','true')
			Log(settinginfo)
			Log(addoninfo)
			Log(backupinfo)
			self.setlistctr.addItem(li)


	def ContainerPostion(self,container):
		return int(xbmc.getInfoLabel(f'Container({container}).Position'))

	def UpdateSelected(self,item):
		Log(self.selectedforchange)
		key = item.getProperty('id')
		value = item.getProperty('backupvalue')
		if key in self.selectedforchange:
			self.selectedforchange.pop(key)
		else:
			self.selectedforchange.update({key:value})
		Log(self.selectedforchange)

	def ReLoadSetCtrl(self,item,pos):
		if item.getProperty('id') in self.selectedforchange:
			item.setProperty('selected','true')
		elif item.getProperty('id') not in self.selectedforchange:
			item.setProperty('selected','false')


	def ApplySettings(self):
		for k,v in self.selectedforchange.items():
			if type(v) == str and not v in ['true','false']:
				self.__ADDON__.setSettingString(k,v)
			elif v in ['true','false'] :
				v = json.loads(v)
				self.__ADDON__.setSettingBool(k,v)
			elif type(v) == int:
				self.__ADDON__.setSettingInt(k,v)
			elif type(v) == float:
				self.__ADDON__.setSettingNumber(k,v)
			else:
				continue
		self.selectedforchange.clear()

	def ResetList(self):
		Log(self.selectedforchange)
		self.selectedforchange.clear()
		Log(self.selectedforchange)