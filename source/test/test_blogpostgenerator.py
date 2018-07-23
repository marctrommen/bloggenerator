#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import blogpostgenerator
import templatehandler
import datetime

PARAMETER_BLOGTITLE =  "blogtitle"
PARAMETER_BLOGCREATED = "blogcreated"
PARAMETER_BLOGCHANGED = "blogchanged"
PARAMETER_BLOGKEYWORDS = "blogkeywords"


class BlogPostGeneratorTest(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(BlogPostGeneratorTest, self).__init__(*args, **kwargs)
	
	
	def setUp(self):
		th = templatehandler.TemplateHandler()
		title = "Blog-Test"
		dateGenerated = datetime.datetime(2018, 1, 1, 1, 0, 0)
		self.generator = blogpostgenerator.BlogPostGenerator(th, title, dateGenerated)
	
	
	def test_get_keywordSnippet(self):
		keywords = ["fass", "hunde_trainer", "muckefuk"]
		html = self.generator.get_keywordSnippet(keywords)
		self.assertEqual(len(html), 237, "incorrect snippet size")
	
	
	def test_get_pageSnippet(self):
		content = '<p>nix</p>'
		html = self.generator.get_pageSnippet(content)
		self.assertEqual(len(html), 1887, "incorrect snippet size")
	
	
	def test_get_blogpostSnippet(self):
		blogpostParameters = dict(
			BLOGPOSTID = 'aa',
			BLOGPOSTTITLE = 'bb',
			BLOGPOSTCREATED = 'cc',
			BLOGPOSTCREATED_HUMANREADABLE = 'dd',
			BLOGPOSTKEYWORDS = 'ee',
			BLOGPOSTCHANGED = 'ff',
			BLOGPOSTCHANGED_HUMANREADABLE = 'gg',
			BLOGPOSTCONTENT = 'hh'
		)
		html = self.generator.get_blogpostSnippet(blogpostParameters)
		self.assertEqual(len(html), 514, "incorrect snippet size")
	
	def test_get_html(self):
		parameters = {}
		parameters[PARAMETER_BLOGTITLE] = "aa"
		parameters[PARAMETER_BLOGCREATED] = datetime.datetime(2017, 1, 1, 1, 0, 0)
		parameters[PARAMETER_BLOGCHANGED] = datetime.datetime(2017, 1, 1, 1, 0, 0)
		parameters[PARAMETER_BLOGKEYWORDS] = ["bla"]
		
		content = '<p>nix</p>'
		html = self.generator.get_html(parameters, content)
		self.assertEqual(len(html), 2536, "incorrect snippet size")

