#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import locale


PARAMETER_BLOGTITLE =  "blogtitle"
PARAMETER_BLOGCREATED = "blogcreated"
PARAMETER_BLOGCHANGED = "blogchanged"
PARAMETER_BLOGKEYWORDS = "blogkeywords"
PARAMETER_BLOGFILENAME = "blogfilename"
SNIPPET_SEPERATOR = ", "

class ListpageGenerator(object):

	def __init__(self, templateHandler, pageTitle, pageSubtitle, pageGenerated):
		locale.setlocale(locale.LC_ALL, '')
		self.templateHandler = templateHandler
		self.pageParameters = dict (
			BLOGTITLE = pageTitle,
			PAGESTYLE = "listpage",
			PATHLOCATION = ".", 
			PAGETITLE = pageSubtitle,
			PAGETITLE_ID = pageSubtitle,
			CONTENT = "",
			PAGECONTENT = "",
			BLOGCURRENTYEAR = pageGenerated.strftime('%Y'),
			BLOGGENERATED = pageGenerated.strftime('%Y%m%d %H%M%S'),
			BLOGGENERATED_HUMANREADABLE = pageGenerated.strftime('%d.%m.%Y %H:%M:%S')
		)
	
	
	def get_html(self, itemList, parameterDictionary):
		listcontent = []
		for item in itemList:
			keywordSnippet = self.get_keywordSnippet(parameterDictionary[item][PARAMETER_BLOGKEYWORDS])
	
			itemParameters = dict(
				BLOGPOSTID = parameterDictionary[item][PARAMETER_BLOGCREATED].strftime('%Y%m%d%H%M%S'),
				BLOGPOSTTITLE = parameterDictionary[item][PARAMETER_BLOGTITLE],
				BLOGPOSTCREATED = parameterDictionary[item][PARAMETER_BLOGCREATED].strftime('%Y%m%d %H%M%S'),
				BLOGPOSTCREATED_HUMANREADABLE = parameterDictionary[item][PARAMETER_BLOGCREATED].strftime('%d.%m.%Y %H:%M:%S'),
				BLOGPOSTKEYWORDS = keywordSnippet,
				BLOGPOSTCHANGED = parameterDictionary[item][PARAMETER_BLOGCHANGED].strftime('%Y%m%d %H%M%S'),
				BLOGPOSTCHANGED_HUMANREADABLE = parameterDictionary[item][PARAMETER_BLOGCHANGED].strftime('%d.%m.%Y %H:%M:%S'),
				BLOGPOSTFILENAME = item
			)
	
			listcontent.append(self.get_itemSnippet(itemParameters))
		
		return self.get_pageSnippet('\n'.join(listcontent))
	
	
	def get_pageSnippet(self, listcontent):
		listpageSnippet = self.templateHandler.getListpage()
		self.pageParameters['PAGECONTENT'] = listcontent
		self.pageParameters['CONTENT'] = listpageSnippet.format(**self.pageParameters)

		pageSnippet = self.templateHandler.getPage()
		return pageSnippet.format(**self.pageParameters)
	
	
	def get_itemSnippet(self, itemParameters):
		itemSnippet = self.templateHandler.getPageitem()
		return itemSnippet.format(**itemParameters)
	
	
	def get_keywordSnippet(self, keywords):
		htmlSnippets = []
		for key in keywords:
			keywordSnippet = self.templateHandler.getBlogpostKeyword()
			htmlSnippets.append(keywordSnippet.format(KEYWORD=key, PATHLOCATION = "."))
		return SNIPPET_SEPERATOR.join(htmlSnippets)