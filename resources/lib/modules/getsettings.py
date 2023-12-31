#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import xml.etree.ElementTree as ET

import xbmc
import xbmcaddon

from.utils import Log

def ParseXML(addonid):
	'''Reads xml file and returns root'''
	settingsfile = os.path.join(xbmcaddon.Addon(addonid).getAddonInfo('path'),'resources','settings.xml')
	tree = ET.parse(settingsfile)
	root = tree.getroot()
	return root

def GetSettingsCats(addonid) ->list:
	''' Returns list of dicts of all categorys from settings xml '''
	data = []
	root = ParseXML(addonid)
	for x in root.findall('.//category'):
		Log(x.attrib)
		data.append(x.attrib)
	return data

def GetSettingsGrp(addonid,catId)->list:
	'''Returns list of dicts of all settings groups that match a category'''
	data =[]
	root = ParseXML(addonid)
	for x in root.findall(f".//category[@id='{catId}']/group"):
		Log(x.attrib)
		data.append(x.attrib)
	return data

def GetSettingsInfo(addonid)->list:
	'''Returns all settings as a list of dicts'''
	data = []
	root = ParseXML(addonid)
	for x in root.findall('.//setting'):
		data.append(x.attrib)
	return data

def GetSettings(addonid,catId,groupId)->list:
	'''Returns a list of dicts of all settings that match a category and group'''
	data = []
	root = ParseXML(addonid)
	for x in root.findall(f".//category[@id='{catId}']/group[@id='{groupId}']/setting"):
		Log(x.attrib)
		data.append(x.attrib)
	return data

def GetSettingOptions(addonid,catId,groupId,settingId)->dict:
	'''Returns options list for a setting that has label in dict as option_value:label'''
	data = {}
	root = ParseXML(addonid)
	for x in root.findall(f".//category[@id='{catId}']/group[@id='{groupId}']/setting[@id='{settingId}']/constraints/options/option[@label]"):
		data.update({x.text:x.get('label')})
	Log(data)
	return data


def GetSettingLabel(addonid,label):
	'''Function to return a label in  string format 
	will check to see if is a digit and check language files for corresponding string''' 
	Log(label)
	t = type(label)
	if t == str:
		if label.isdigit():
			label = int(label)
			if label in range(30000,32999):
				label = xbmcaddon.Addon(addonid).getLocalizedString(label)
				Log(label)
				if len(label) >= 1:
					return label
			else:
				label = xbmc.getLocalizedString(label)
				Log(label)
				if len(label) >= 1:
					return label
		else:
			return label

