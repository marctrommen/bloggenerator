#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import commentparser

#FILE_NAME = "test/test_commentparser.html"
#with open(FILE_NAME, 'r') as fileObject:
#	fileContent = fileObject.read()

PARAMETER_BLOGTITLE =  "blogtitle"
PARAMETER_BLOGCREATED = "blogcreated"
PARAMETER_BLOGCHANGED = "blogchanged"
PARAMETER_BLOGKEYWORDS = "blogkeywords"


class CommentParserTest(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		self.defaultParameters = ( PARAMETER_BLOGTITLE
			, PARAMETER_BLOGCREATED
			, PARAMETER_BLOGCHANGED
			, PARAMETER_BLOGKEYWORDS )
		self.parameters = {}
		super(CommentParserTest, self).__init__(*args, **kwargs)
	
	def init_parameters(self):
		for key in self.defaultParameters:
			self.parameters[key] = ""
	
	
	def setUp(self):
		self.init_parameters()

	
	def test_no_comment(self):
		commentText = """ """
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_any_comment(self):
		commentText = """<!-- =====================
     das ist ein Test
     ===================== -->"""
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_blogtitle(self):
		commentText = """<!-- blogtitle: Peter Pan -->"""
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters['blogtitle'] = 'Peter Pan'
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_reset(self):
		commentText = """<!-- blogtitle: Mauris -->"""
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters['blogtitle'] = 'Mauris'
		self.assertDictEqual(parser.get_parameter(), self.parameters)
	
		parser.reset()
		self.init_parameters()
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_shallow_reset(self):
		commentText = """<!-- blogtitle: pig -->"""
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters['blogtitle'] = 'pig'
		self.assertDictEqual(parser.get_parameter(), self.parameters)
	
		commentText = """<!-- blogtitle: otto -->"""
		parser.feed(commentText)
		self.init_parameters()
		self.parameters['blogtitle'] = 'otto'
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		
		parser.close()
