#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

import templatehandler

class TemplateHandlerTest(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TemplateHandlerTest, self).__init__(*args, **kwargs)

	def test_getPage(self):
		th = templatehandler.TemplateHandler()
		self.assertEqual(len(th.getPage()), 1913, "incorrect file size")

	def test_getBlogpost(self):
		th = templatehandler.TemplateHandler()
		self.assertEqual(len(th.getBlogpost()), 656, "incorrect file size")

	def test_getBlogpostKeyword(self):
		th = templatehandler.TemplateHandler()
		self.assertEqual(len(th.getBlogpostKeyword()), 79, "incorrect file size")
