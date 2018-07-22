#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import commentparser
import datetime

#FILE_NAME = "test/test_commentparser.html"
#with open(FILE_NAME, 'r') as fileObject:
#	fileContent = fileObject.read()

PARAMETER_BLOGTITLE =  "blogtitle"
PARAMETER_BLOGCREATED = "blogcreated"
PARAMETER_BLOGCHANGED = "blogchanged"
PARAMETER_BLOGKEYWORDS = "blogkeywords"
DEFAULT_VALUE_NOKEYWORD = "no_keyword"


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
		self.parameters[PARAMETER_BLOGTITLE] = 'Peter Pan'
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_reset(self):
		commentText = """<!-- blogtitle: Mauris -->"""
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGTITLE] = 'Mauris'
		self.assertDictEqual(parser.get_parameter(), self.parameters)
	
		parser.reset()
		self.init_parameters()
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_shallow_reset(self):
		commentText = """<!-- blogtitle: pig -->"""
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGTITLE] = 'pig'
		self.assertDictEqual(parser.get_parameter(), self.parameters)
	
		commentText = """<!-- blogtitle: otto -->"""
		parser.feed(commentText)
		self.init_parameters()
		self.parameters[PARAMETER_BLOGTITLE] = 'otto'
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()


	def test_keywords_empty_list_1(self):
		commentText = "<!-- blogkeywords: -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGKEYWORDS] = [ DEFAULT_VALUE_NOKEYWORD ]
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_keywords_empty_list_2(self):
		commentText = "<!-- blogkeywords: , ,  ,  -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGKEYWORDS] = [ DEFAULT_VALUE_NOKEYWORD ]
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_keywords_mixed_uppercase_lowercase(self):
		commentText = "<!-- blogkeywords: GROSS, kLeiN, 122N , PfannKucheN  -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGKEYWORDS] = [ "gross", "klein", "122n", "pfannkuchen" ]
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_blogcreated_nodate(self):
		commentText = "<!-- blogcreated :  -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGCREATED] = datetime.datetime(2018, 1, 1, 1, 0)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_blogcreated_baddate_1(self):
		commentText = "<!-- blogcreated : 20180705 -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGCREATED] = datetime.datetime(2018, 1, 1, 1, 0, 0)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_blogcreated_baddate_2(self):
		commentText = "<!-- blogcreated : 20180230-010000 -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGCREATED] = datetime.datetime(2018, 1, 1, 1, 0, 0)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()

	def test_blogcreated_gooddate(self):
		commentText = "<!-- blogcreated : 20180705-130011 -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGCREATED] = datetime.datetime(2018, 7, 5, 13, 0, 11)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_blogchanged_nodate(self):
		commentText = "<!-- blogchanged : aaa -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGCHANGED] = datetime.datetime(2018, 1, 1, 1, 0)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_blogchanged_baddate_1(self):
		commentText = "<!-- blogchanged : 20180705-240101 -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGCHANGED] = datetime.datetime(2018, 1, 1, 1, 0, 0)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
	
	
	def test_blogchanged_baddate_2(self):
		commentText = "<!-- blogchanged : 20180228-000060 -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGCHANGED] = datetime.datetime(2018, 1, 1, 1, 0, 0)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()

	def test_blogchanged_gooddate(self):
		commentText = "<!-- blogchanged : 20180705-130011 -->"
		parser = commentparser.CommentParser()
		parser.feed(commentText)
		self.parameters[PARAMETER_BLOGCHANGED] = datetime.datetime(2018, 7, 5, 13, 0, 11)
		self.assertDictEqual(parser.get_parameter(), self.parameters)
		parser.close()
