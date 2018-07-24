# -*- coding: utf-8 -*-


import os
import shutil
import datetime
import locale

import templatehandler
import commentparser
import blogpostgenerator

DATE_PARSE_FORMAT = "%Y%m%d_%H%M%S"

generatorParameters = {}

def init():
	aPath = os.path.realpath(__file__)
	aPath = os.path.dirname(aPath)
	aPath = os.path.join(aPath, "..")
	aPath = os.path.normpath(aPath)
	generatorParameters['projectRootDir'] = aPath
	generatorParameters['projectStaticDir'] = os.path.join(generatorParameters['projectRootDir'], "static")
	generatorParameters['projectContentDir'] = os.path.join(generatorParameters['projectRootDir'], "content")
	generatorParameters['projectBlogpostDir'] = os.path.join(generatorParameters['projectContentDir'], "blog")
	generatorParameters['blogRootDir'] = os.path.join(generatorParameters['projectRootDir'], "_site")
	generatorParameters['blogArchiveDir'] = os.path.join(generatorParameters['blogRootDir'], "archive")
	
	locale.setlocale(locale.LC_ALL, '')
	generatorParameters['generatorStarted'] = datetime.datetime.now()
	generatorParameters['blogTitle'] = ""
	
	generatorParameters['blogPostList'] = []
	generatorParameters['blogPostMetaData'] = {}

def cleanup():
	aPath = generatorParameters['blogRootDir']
	if os.path.isdir(aPath):
		shutil.rmtree(aPath)


def blogBuildDirLayout():
	shutil.copytree(generatorParameters['projectStaticDir'], generatorParameters['blogRootDir'])
	os.makedirs(generatorParameters['blogArchiveDir'])


def isValidFilename(name):
	filename = name.split(".")[0]
	if len(filename) > 14:
		datepart = filename[:15]
		try:
			datetime.datetime.strptime(datepart, DATE_PARSE_FORMAT)
			return True
		except ValueError:
			return False
	else:
		return False


def createBlogpostFileList():
	blogpostDir = generatorParameters['projectBlogpostDir']
	fileList = os.listdir(blogpostDir)
	for item in fileList:
		filepath = os.path.join(blogpostDir, item)
		if os.path.isfile(filepath):
			if isValidFilename(item):
				if item.endswith(".html"):
					generatorParameters['blogPostList'].append(item)
				else:
					shutil.copy(filepath, generatorParameters['blogArchiveDir'])


def createBlogposts():
	th = templatehandler.TemplateHandler()
	blogGenerator = blogpostgenerator.BlogPostGenerator(
		th, 
		generatorParameters['blogTitle'], 
		generatorParameters['generatorStarted'])
	parser = commentparser.CommentParser()
	
	for item in generatorParameters['blogPostList']:
		inFileName = os.path.join(generatorParameters['projectBlogpostDir'], item)
		with open(inFileName, 'r') as fileObject:
			content = fileObject.read()
		parser.feed(content)
		generatorParameters['blogPostMetaData'][item] = parser.get_parameter()
		html = blogGenerator.get_html(
			generatorParameters['blogPostMetaData'][item], 
			content)
		outFileName = os.path.join(generatorParameters['blogArchiveDir'], item)
		with open(outFileName, 'w') as fileObject:
			fileObject.write(html)



if __name__ == '__main__':
	init()
	cleanup()
	blogBuildDirLayout()
	createBlogpostFileList()
	createBlogposts()