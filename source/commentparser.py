#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
import datetime
import locale

PARAMETER_BLOGTITLE =  "blogtitle"
PARAMETER_BLOGCREATED = "blogcreated"
PARAMETER_BLOGCHANGED = "blogchanged"
PARAMETER_BLOGKEYWORDS = "blogkeywords"
DEFAULT_DATETIME = "20180101_010000"
DATE_PARSE_FORMAT = "%Y%m%d-%H%M%S"

#FILE_NAME = "test/test_commentparser.html"
#with open(FILE_NAME, 'r') as fileObject:
#	fileContent = fileObject.read()


class CommentParser(HTMLParser):

	def __init__(self):
		locale.setlocale(locale.LC_ALL, '')
		self.defaultParameters = ( PARAMETER_BLOGTITLE
			, PARAMETER_BLOGCREATED
			, PARAMETER_BLOGCHANGED
			, PARAMETER_BLOGKEYWORDS )
		self.parameters = {}
		self.init_parameters()
		super(CommentParser, self).__init__()
	
	
	def init_parameters(self):
		for key in self.defaultParameters:
			self.parameters[key] = ""
	
	def feed(self, text):
		self.init_parameters()
		super(CommentParser, self).feed(text)
	
	def reset(self):
		self.init_parameters()
		super(CommentParser, self).reset()
	
	
	def handle_comment(self, data):
		try:
			(key, value) = data.split(':')
		except ValueError:
			return
		
		key = key.strip().lower()
		
		if key in self.defaultParameters:
			value = value.replace("\r", "")
			value = value.replace("\n", " ")
			value = value.replace("\t", " ")
			value = value.replace("  ", " ")
			value = value.strip()
			
			if key == PARAMETER_BLOGTITLE:
				self.parameters[key] = value
			elif key == PARAMETER_BLOGCREATED:
				self.parameters[key] = self.handle_date_parameter(value)
			elif key == PARAMETER_BLOGCHANGED:
				self.parameters[key] = self.handle_date_parameter(value)
			elif key == PARAMETER_BLOGKEYWORDS:
				self.parameters[key] = self.handle_list_parameter(value)
			else:
				pass
	
	
	def handle_date_parameter(self, datestring):
		try:
			date = datetime.datetime.strptime(datestring, DATE_PARSE_FORMAT)
		except ValueError:
			date = datetime.datetime.strptime(DEFAULT_DATETIME, DATE_PARSE_FORMAT)
		return date
	
	
	def handle_list_parameter(self, liststring):
		items = liststring.split(' ')
		for item in items:
			item = item.strip().lower()
		return items
	
	
	def get_parameter(self):
		return self.parameters

