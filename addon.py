#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from resources.lib.modules.utils import Log,DateTimeNow,PathTranslate
import sys
from   urllib.parse import parse_qs,urlparse,urlencode
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs


base_url      = sys.argv[0]
addon_handle  = int(sys.argv[1])
args          = parse_qs(sys.argv[2][1:])
mode          = args.get('mode', None)

addon         = xbmcaddon.Addon('plugin.program.addonadministrator')
addon_icon    = addon.getAddonInfo('icon')
addon_name    = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')

xbmcvfs.mkdirs(os.path.join(xbmcvfs.translatePath('special://userdata'),'addon_data','plugin.program.addonadministrator','backup'))

def AddDir(name,mode,iconimage,isFolder=True):
	u=BuildUrl({'name':name,'mode':mode,'iconimage':iconimage})
	liz=xbmcgui.ListItem(name)
	liz.setArt({'icon':'DefaultFolder.png','thumb':iconimage})
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)

def BackUp():
	selection = [BuildListItem('All')]
	from resources.lib.modules import getaddons
	results = getaddons.GetAddonsWithSettings()
	for res in results:
		if not res.get('addon_enabled') and addon.getSettingBool('backup.ignore.disabled'):
			continue
		else:
			selection.append(BuildListItem(res.get('addon_name'),thumb=res.get('addon_thumb'),properties={'addon_id':res.get('addon_id')}))
	ret = xbmcgui.Dialog().multiselect(addon.getLocalizedString(30008), selection)
	if ret and isinstance(ret,list):
		from resources.lib.modules import backup
		if ret[0] == 0:
			selection.pop(0)
			for i in selection:
				backup.BackUp(i.getProperty('addon_id'),addon.getSettingString('backup.store.path'))
		else:
			for n in ret:
				backup.BackUp(selection[n].getProperty('addon_id'),addon.getSettingString('backup.store.path'))
	else:
		xbmcgui.Dialog().notification(addon_name,addon.getLocalizedString(30052),addon_icon)	




def BuildListItem(name,thumb=None,properties=None):
	li = xbmcgui.ListItem(name)
	if thumb:
		li.setArt({'icon':'DefaultAddon.png','thumb':thumb})
	else:
		li.setArt({'icon':'DefaultAddon.png','thumb':'DefaultAddon.png'})
	if properties:
		li.setProperties(properties)
	return li

def BuildUrl(query):
	return base_url + '?' + urlencode(query)

def Compare():
	from resources.lib.modules import getaddons
	from resources.lib.modules.guicontrol import SettingCompare
	from resources.lib.modules import backupfile
	selection = []
	choice = []
	sysaddons = getaddons.GetSysAddons()
	pathselect = xbmcgui.Dialog().yesnocustom(addon.getLocalizedString(30058), addon.getLocalizedString(30028),customlabel=addon.getLocalizedString(30035), nolabel=addon.getLocalizedString(30030), yeslabel=addon.getLocalizedString(30029))
	if pathselect == 1:
		backuppath = os.path.join(addon.getSettingString('backup.store.path'),'addonsettings.buk')
	elif pathselect == 0:
		backuppath = xbmcgui.Dialog().browse(1, addon.getLocalizedString(30059), 'local', mask='buk')
	else:
		return
	if xbmcvfs.exists(backuppath):
		backedup_addons = backupfile.ReadAddons(backuppath)
		if backedup_addons != None:
			for a in sysaddons:
				aid = a['addonid']
				if aid in backedup_addons:
					selection.append(BuildListItem(xbmcaddon.Addon(aid).getAddonInfo('name'),properties=a))
			ret = xbmcgui.Dialog().select(addon.getLocalizedString(30056),selection)
			selected = selection[ret].getProperty('addonid')
			Log(selected)
			choices = backupfile.ReadChoices(backuppath,selected)
			# choices = choices.reverse()
			for c in choices:
				choice.insert(0,BuildListItem(c))
			ret2 = xbmcgui.Dialog().select(f"{addon.getLocalizedString(30057)} {xbmcaddon.Addon(selected).getAddonInfo('name')}",choice)
			Log(ret2)
			xbmc.executebuiltin('Dialog.Close(all,true)')
			# Dialog.Close(dialog[,force])
			d = SettingCompare(backuppath,selected,choice[ret2].getLabel())
			d.doModal()
			del d

def Export():
	#Qa use existing backup or create new
	Qa = xbmcgui.Dialog().yesnocustom(addon_name,addon.getLocalizedString(30044),addon.getLocalizedString(30046),addon.getLocalizedString(30045),addon.getLocalizedString(30035))
	Log(Qa)
	if Qa == 0:
		pass
	elif Qa == 2:
		BackUp()
	else:
		xbmcgui.Dialog().notification(addon_name,addon.getLocalizedString(30051),addon_icon)
		return
	#Qb use setting export path or browse 
	Qb = xbmcgui.Dialog().yesnocustom(addon_name,addon.getLocalizedString(30028),addon.getLocalizedString(30030),addon.getLocalizedString(30029),addon.getLocalizedString(30035))
	Log(Qb)
	if Qb == 0:
		path = addon.getSettingString('export.path')
	elif Qb == 2:
		path = xbmcgui.Dialog().browseSingle(0,addon.getLocalizedString(30050),'')
		Log(path)
	else:
		xbmcgui.Dialog().notification(addon_name,addon.getLocalizedString(30051),addon_icon)
		return
	if path:
		raw_path = addon.getSettingString('backup.store.path')
		if raw_path.startswith('special'):
			raw_path = xbmcvfs.translatePath(raw_path)
		source = os.path.join(raw_path,'addonsettings.buk')
		dest = os.path.join(path,f"export_addonsettings_{DateTimeNow(fmt='%Y%m%d%H%M')}.buk")
		success = xbmcvfs.copy(source, dest)
		if success:
			txt = f'{addon.getLocalizedString(30048)} {source} {xbmc.getLocalizedString(19160)} {dest}'
			xbmcgui.Dialog().notification(addon_name,txt,addon_icon)
			Log(txt)
		else:
			txt = f'{addon.getLocalizedString(30049)} {source} {xbmc.getLocalizedString(19160)} {dest}'
			xbmcgui.Dialog().notification(addon_name,txt,addon_icon)
			Log(txt)
	else:
		xbmcgui.Dialog().notification(addon_name,addon.getLocalizedString(30051),addon_icon)
		return
	


def Import():
	file = None
	path = addon.getSettingString('import.path')
	if path:
		ret = xbmcgui.Dialog().yesnocustom(addon_name,addon.getLocalizedString(30028),addon.getLocalizedString(30030),addon.getLocalizedString(30029),addon.getLocalizedString(30035))
		Log(ret)
		if ret == 0:
			file = xbmcgui.Dialog().browseSingle(1,addon.getLocalizedString(30031),'',defaultt=path)
		elif ret == 2:
			file = xbmcgui.Dialog().browseSingle(1,addon.getLocalizedString(30031),'')
		else:
			xbmcgui.Dialog().notification(addon_name,addon.getLocalizedString(3055))
	else:
		ret = xbmcgui.Dialog().yesno(addon_name,addon.getLocalizedString(30043))
		if ret:
			path = xbmcgui.Dialog().browseSingle(0,addon.getLocalizedString(30015),'')
			addon.setSettingString('import.path',path)
			file = xbmcgui.Dialog().browseSingle(1,addon.getLocalizedString(30031),'',defaultt=path)
		else:
			file = xbmcgui.Dialog().browseSingle(1,addon.getLocalizedString(30031),'')
	Log(file)
	if file:
		Restore(file)

def MainMenu():
	AddDir(addon.getLocalizedString(30032),'settings',None)
	AddDir(addon.getLocalizedString(30033),'userdata',None)

def Restore(backuppath):
	selection = [BuildListItem('All')]
	from resources.lib.modules import getaddons
	from resources.lib.modules import restore
	from resources.lib.modules import backupfile
	sysaddons = getaddons.GetSysAddons()
	# backuppath = os.path.join(addon.getSettingString('backup.store.path'),'addonsettings.buk')
	backedup_addons = backupfile.ReadAddons(backuppath)
	if backedup_addons != None:
		for a in sysaddons:
			aid = a['addonid']
			if aid in backedup_addons:
				selection.append(BuildListItem(xbmcaddon.Addon(aid).getAddonInfo('name'),properties=a))
	if len(selection) >1:
		ret = xbmcgui.Dialog().multiselect(addon.getLocalizedString(30013), selection)
		if ret and isinstance(ret,list):
			if ret[0]==0:
				selection.pop(0)
				for sel in selection:
					aid = sel.getProperty('addonid')
					restore.Restore(aid,backuppath)
			else:
				for r in ret:
					aid = selection[r].getProperty('addonid')
					restore.Restore(aid,backuppath)
		else:
			xbmcgui.Dialog().notification(addon_name,addon.getLocalizedString(30053),addon_icon)
			return
	else:
		xbmcgui.Dialog().notification(addon_name,addon.getLocalizedString(30054),addon_icon)
		return


				
def SettingsMenu():
	AddDir(addon.getLocalizedString(30002),'backup', None)
	AddDir(addon.getLocalizedString(30003),'restore',None)
	AddDir(addon.getLocalizedString(30004),'import', None)
	AddDir(addon.getLocalizedString(30005),'export', None)
	AddDir(addon.getLocalizedString(30006),'compare',None)

def UserDataMenu():
	pass
	

Log(str(sys.argv))
if mode is None:
	Log('Opening main menu')
	MainMenu()
	xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'settings':
	SettingsMenu()
	xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'userdata':
	UserDataMenu()
	xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'backup':
	Log('Opening backup')
	BackUp()
	# xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'restore':
	Log('Opening restore')
	Restore(os.path.join(addon.getSettingString('backup.store.path'),'addonsettings.buk'))
	# xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'import':
	Log('Opening import')
	Import()
	# xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'export':
	Log('Opening export')
	Export()
	# xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'compare':
	Log('Opening compare')
	Compare()
	# xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'settings.general.hidden.files':
	Log('Opening settings.general.hidden.files')
	from resources.lib.scripts import settings
	settings.HiddenFiles()
elif mode[0] == 'settings.import.import.path':
	Log('Opening settings.import.import.path')
	from resources.lib.scripts import settings
	settings.ImportPath()