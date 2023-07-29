#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs


from.utils import Log

from .getsettings import GetSettingsCats,GetSettingLabel,GetSettingsInfo,GetSettingsGrp,GetSettings

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
		# from.getsettings import GetSettingsInfo,GetSettingLabel
		self.settinginfo  = GetSettingsInfo(addonid)
		# Log(self.settinginfo)
		from.backupfile  import ReadAddonInfo,ReadSavedSettings
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

	def __new__(cls,backup_file,addonid,bckupdt):
		return super(SettingCompare,cls).__new__(cls,'Setting_Compare.xml', __addonpath__,'Default', '720p')

	def __init__(self,backup_file,addonid,bckupdt):
		super(SettingCompare,self).__init__()
		self.backup_file = backup_file
		self.addonid = addonid
		self.bckupdt = bckupdt
		# from .getsettings import GetSettingsCats,GetSettingLabel
		self.cat = GetSettingsCats(self.addonid)
		self.selectedforchange = []

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
				pos = self.ContainerPostion(self.CATLIST)
				self.LoadGroupCtrl(self.catlistcontr.getListItem(pos))
			elif focusid == self.GROUPLIST:
				pos = self.ContainerPostion(self.GROUPLIST)
				self.LoadSetCtrl(self.grplistctr.getListItem(pos))
		elif action.getId() in [ACTION_DOWN]:
			if focusid == self.CATLIST:
				pos = self.ContainerPostion(self.CATLIST)
				self.LoadGroupCtrl(self.catlistcontr.getListItem(pos))
			elif focusid == self.GROUPLIST:
				pos = self.ContainerPostion(self.GROUPLIST)
				self.LoadSetCtrl(self.grplistctr.getListItem(pos))
		elif action.getId() in [ACTION_SELECT_ITEM]:
			if focusid == self.SETTINGLIST:
				pass

	def onFocus(self,controlId):
		if controlId == self.CATLIST:
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
		addsetting = xbmcaddon.Addon(self.addonid).getSettings()
		Log(items)
		for i in items:
			li = xbmcgui.ListItem(GetSettingLabel(self.addonid,i.get('label')),xbmcaddon.Addon(self.addonid).getSetting(i.get('id')))
			self.setlistctr.addItem(li)


	def ContainerPostion(self,container):
		return int(xbmc.getInfoLabel(f'Container({container}).Position'))