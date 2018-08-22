#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import locale


class SimplePageGenerator(object):

	def __init__(self, templateHandler, siteTitle, pageGenerated):
		locale.setlocale(locale.LC_ALL, '')
		self.templateHandler = templateHandler
		self.pageParameters = dict (
			BLOGTITLE = siteTitle,
			PAGESTYLE = "simplepage",
			PATHLOCATION = ".", 
			PAGETITLE = "",
			PAGETITLE_ID = "",
			CONTENT = "",
			PAGECONTENT = "",
			BLOGCURRENTYEAR = pageGenerated.strftime('%Y'),
			BLOGGENERATED = pageGenerated.strftime('%Y%m%d %H%M%S'),
			BLOGGENERATED_HUMANREADABLE = pageGenerated.strftime('%d.%m.%Y %H:%M:%S')
		)


	def get_html(self, pagetitle, html_content):
		listpage_snippet = self.templateHandler.getListpage()
		self.pageParameters['PAGETITLE'] = pagetitle
		self.pageParameters['PAGETITLE_ID'] = pagetitle
		self.pageParameters['PAGECONTENT'] = html_content
		self.pageParameters['CONTENT'] = listpage_snippet.format(**self.pageParameters)

		page_snippet = self.templateHandler.getPage()
		return page_snippet.format(**self.pageParameters)
