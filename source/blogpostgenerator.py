#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import locale


PARAMETER_BLOGTITLE =  "blogtitle"
PARAMETER_BLOGCREATED = "blogcreated"
PARAMETER_BLOGCHANGED = "blogchanged"
PARAMETER_BLOGKEYWORDS = "blogkeywords"

class BlogPostGenerator:

	def __init__(self, pageTemplate = '', blogpostTemplate = '', keywordTemplate = ''):
		locale.setlocale(locale.LC_ALL, '')
		self.page = pageTemplate
		self.blogpost = pageTemplate
		self.keyword = keywordTemplate
	
	
	def get_html(self, parameterDictionary, content, blogtitle):
		keywordSnippet = get_keywordSnippet(parameterDictionary[PARAMETER_BLOGKEYWORDS])
		return ""
	
	
	def get_pageSnippet(self, 
			pageTitle = '', 
			content = '', 
			generatedDate = datetime.datetime(2018, 1, 1, 1, 0, 0)):
		pageSnippet = self.page
		parameters = dict(
			BLOGTITLE = pageTitle,
			CONTENT = content,
			BLOGCURRENTYEAR = generatedDate.strftime('%Y'),
			BLOGGENERATED = generatedDate.strftime('%d.%m.%Y %H:%M:%S')
		)
		return pageSnippet.format(**parameters)
	
	
	def get_keywordSnippet(self, keywords):
		htmlSnippets = []
		for key in keywords:
			keywordSnippet = self.keyword
			htmlSnippets.append(keywordSnippet.format(KEYWORD=key))
		return ", ".join(htmlSnippets)