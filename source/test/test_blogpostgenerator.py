#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import blogpostgenerator
import datetime

PARAMETER_BLOGTITLE =  "blogtitle"
PARAMETER_BLOGCREATED = "blogcreated"
PARAMETER_BLOGCHANGED = "blogchanged"
PARAMETER_BLOGKEYWORDS = "blogkeywords"


class BlogPostGeneratorTest(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		self.defaultParameters = ( PARAMETER_BLOGTITLE
			, PARAMETER_BLOGCREATED
			, PARAMETER_BLOGCHANGED
			, PARAMETER_BLOGKEYWORDS )
		self.parameters = {}
		super(BlogPostGeneratorTest, self).__init__(*args, **kwargs)
	
	def init_parameters(self):
		for key in self.defaultParameters:
			self.parameters[key] = ""
	
	
	def setUp(self):
		self.init_parameters()
	
	
	def test_get_keywordSnippet(self):
		FILE_NAME = "../templates/blogpost_keyword_template.html"
		with open(FILE_NAME, 'r') as fileObject:
			fileContent = fileObject.read()
		
		generator = blogpostgenerator.BlogPostGenerator(keywordTemplate = fileContent)
		keywords = ["fass", "hunde_trainer", "muckefuk"]
		html = generator.get_keywordSnippet(keywords)
		
		FILE_NAME = "test/keyword.html"
		with open(FILE_NAME, 'w') as fileObject:
			fileObject.write(html)
	
	
	def test_get_pageSnippet(self):
		FILE_NAME = "../templates/page_template.html"
		with open(FILE_NAME, 'r') as fileObject:
			fileContent = fileObject.read()
		
		generator = blogpostgenerator.BlogPostGenerator(pageTemplate = fileContent)
		html = generator.get_pageSnippet(pageTitle = 'my Blog', 
			content = '<p>nix</p>', 
			generatedDate = datetime.datetime(2018, 1, 1, 1, 0, 0))
			
		FILE_NAME = "test/page.html"
		with open(FILE_NAME, 'w') as fileObject:
			fileObject.write(html)
	