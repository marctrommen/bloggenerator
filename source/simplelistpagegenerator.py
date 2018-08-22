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

class SimpleListpageGenerator(object):

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
	
	
	def get_html(self, parameterDictionary, is_keywords_list = True):
		listcontent = []
		items = parameterDictionary.keys()
		items = list(items)
		items.sort()
		if not is_keywords_list:
			items.reverse()
		
		for item in items:
			if is_keywords_list:
				itemid = item
				itemtitle = item.replace('_', ' ')
				itemfilename = 'keyword_' + itemid + '.html'
			else:
				itemid = str(item)
				itemtitle = itemid
				if itemid == self.pageParameters['BLOGCURRENTYEAR']:
					itemfilename = 'index.html'
				else:
					itemfilename = 'archive_' + itemid + '.html'
			
			item_parameters = dict(
				ITEMID = itemid,
				ITEMFILENAME = itemfilename,
				ITEMTITLE = itemtitle,
				NUMBERITEMS = len(parameterDictionary[item])
			)
	
			listcontent.append(self.get_itemSnippet(item_parameters))
		
		return self.get_pageSnippet('\n'.join(listcontent))
	
	
	def get_pageSnippet(self, listcontent):
		listpage_snippet = self.templateHandler.getListpage()
		self.pageParameters['PAGECONTENT'] = listcontent
		self.pageParameters['CONTENT'] = listpage_snippet.format(**self.pageParameters)

		page_snippet = self.templateHandler.getPage()
		return page_snippet.format(**self.pageParameters)
	
	
	def get_itemSnippet(self, itemParameters):
		item_snippet = self.templateHandler.getSimpleitem()
		return item_snippet.format(**itemParameters)
