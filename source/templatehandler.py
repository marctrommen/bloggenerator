#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

class TemplateHandler(object):

	def __init__(self):
		aPath = os.path.realpath(__file__)
		aPath = os.path.dirname(aPath)
		aPath = os.path.join(aPath, "..")
		aPath = os.path.normpath(aPath)
		self.templatePath = os.path.join(aPath, "templates")
		self.loadTemplates()
	
	def loadTemplates(self):
		fileName = os.path.join(self.templatePath, "blogpost_keyword_template.html")
		with open(fileName, 'r') as fileObject:
			self.blogpostKeyword = fileObject.read()
		
		fileName = os.path.join(self.templatePath, "blogpost_template.html")
		with open(fileName, 'r') as fileObject:
			self.blogpost = fileObject.read()
		
		fileName = os.path.join(self.templatePath, "page_template.html")
		with open(fileName, 'r') as fileObject:
			self.page = fileObject.read()
		
		fileName = os.path.join(self.templatePath, "listpage_template.html")
		with open(fileName, 'r') as fileObject:
			self.listpage = fileObject.read()
		
		fileName = os.path.join(self.templatePath, "pageitem_template.html")
		with open(fileName, 'r') as fileObject:
			self.pageitem = fileObject.read()
		
		fileName = os.path.join(self.templatePath, "simpleitem_template.html")
		with open(fileName, 'r') as fileObject:
			self.simpleitem = fileObject.read()
		
	def getPage(self):
		return self.page
	
	def getBlogpost(self):
		return self.blogpost
	
	def getBlogpostKeyword(self):
		return self.blogpostKeyword

	def getListpage(self):
		return self.listpage
	
	def getPageitem(self):
		return self.pageitem
	
	def getSimpleitem(self):
		return self.simpleitem
	
