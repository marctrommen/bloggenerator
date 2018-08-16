#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import locale


PARAMETER_BLOGTITLE =  "blogtitle"
PARAMETER_BLOGCREATED = "blogcreated"
PARAMETER_BLOGCHANGED = "blogchanged"
PARAMETER_BLOGKEYWORDS = "blogkeywords"
SNIPPET_SEPERATOR = ", "

class BlogPostGenerator(object):

	def __init__(self, templateHandler, pageTitle, pageGenerated):
		locale.setlocale(locale.LC_ALL, '')
		self.templateHandler = templateHandler
		self.pageParameters = dict (
			BLOGTITLE = pageTitle,
			PAGESTYLE = "blogpost",
			CONTENT = "",
			BLOGCURRENTYEAR = pageGenerated.strftime('%Y'),
			BLOGGENERATED = pageGenerated.strftime('%Y%m%d %H%M%S'),
			BLOGGENERATED_HUMANREADABLE = pageGenerated.strftime('%d.%m.%Y %H:%M:%S')
		)
	
	
	def get_html(self, parameterDictionary, content):
		keywordSnippet = self.get_keywordSnippet(parameterDictionary[PARAMETER_BLOGKEYWORDS])
		
		blogpostParameters = dict(
			BLOGPOSTID = parameterDictionary[PARAMETER_BLOGCREATED].strftime('%Y%m%d%H%M%S'),
			BLOGPOSTTITLE = parameterDictionary[PARAMETER_BLOGTITLE],
			BLOGPOSTCREATED = parameterDictionary[PARAMETER_BLOGCREATED].strftime('%Y%m%d %H%M%S'),
			BLOGPOSTCREATED_HUMANREADABLE = parameterDictionary[PARAMETER_BLOGCREATED].strftime('%d.%m.%Y %H:%M:%S'),
			BLOGPOSTKEYWORDS = keywordSnippet,
			BLOGPOSTCHANGED = parameterDictionary[PARAMETER_BLOGCHANGED].strftime('%Y%m%d %H%M%S'),
			BLOGPOSTCHANGED_HUMANREADABLE = parameterDictionary[PARAMETER_BLOGCHANGED].strftime('%d.%m.%Y %H:%M:%S'),
			BLOGPOSTCONTENT = content
		)
		
		blogpostSnippet = self.get_blogpostSnippet(blogpostParameters)
		
		return self.get_pageSnippet(blogpostSnippet)
	
	
	def get_pageSnippet(self, content):
		pageSnippet = self.templateHandler.getPage()
		self.pageParameters['CONTENT'] = content
		return pageSnippet.format(**self.pageParameters)
	
	
	def get_blogpostSnippet(self, blogpostParameters):
		blogpostSnippet = self.templateHandler.getBlogpost()
		return blogpostSnippet.format(**blogpostParameters)
	
	
	def get_keywordSnippet(self, keywords):
		htmlSnippets = []
		for key in keywords:
			keywordSnippet = self.templateHandler.getBlogpostKeyword()
			htmlSnippets.append(keywordSnippet.format(KEYWORD=key))
		return SNIPPET_SEPERATOR.join(htmlSnippets)