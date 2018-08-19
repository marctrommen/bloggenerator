#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import shutil
import datetime
import locale
import markdown
import pprint

import cloudsync
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
	generatorParameters['blogTitle'] = "techBlog"
	
	generatorParameters['blogPostList'] = []
	generatorParameters['blogPostMetaData'] = {}
	generatorParameters['keywordMetaData'] = {}
	generatorParameters['archiveMetaData'] = {}
	print("init()")

def cleanup():
	aPath = generatorParameters['blogRootDir']
	if os.path.isdir(aPath):
		shutil.rmtree(aPath)
	print("cleanup()")


def blogBuildDirLayout():
	shutil.copytree(generatorParameters['projectStaticDir'], generatorParameters['blogRootDir'])
	os.makedirs(generatorParameters['blogArchiveDir'])
	print("blogBuildDirLayout()")


def isValidFilename(name):
	filename = name.split(".")[0]
	if len(filename) > 14:
		datepart = filename[:15]
		try:
			datetime.datetime.strptime(datepart, DATE_PARSE_FORMAT)
			return True
		except ValueError:
			print("ERROR - isValidFilename():", name)
			return False
	else:
		print("ERROR - isValidFilename():", name)
		return False


def markdown_to_html(filename):
	md_content = None
	html_content = None

	md_file = os.path.join(generatorParameters['projectBlogpostDir'], filename)
	with open(md_file, 'r') as fileObject:
		md_content = fileObject.read()
	
	html_content = markdown.markdown(md_content, 
		extensions=['markdown.extensions.extra'],
		output_format = "html5", 
		tab_length = 4,
		smart_emphasis = True
	)
	
	html_filename = filename.replace(".md", ".html")
	html_file = os.path.join(generatorParameters['blogArchiveDir'], html_filename)
	with open(html_file, 'w') as fileObject:
		fileObject.write(html_content)
	
	print("markdown_to_html()")
	return html_filename
	

def createBlogpostFileList():
	"""get file list of "content" directory and check if file in list hits
	against the file naming pattern and starts with "yyyymmdd_hhMMSS".
	If this test is successfuly passed handle the file as follows:
	
	*   if file content is of type Markdown, then translate it into HTML5, 
	    add it to the blog candidate list for further blog generation processing
		copy the Markdown file to the blog destination folder
		
	*   if file content is of type HTML5, then add it to the blog candidate
	    list for further blog generation processing.
		
	*   any other files just copy them to the blog destination folder as a 
	    linked file of the blog post
	"""
	blogpostDir = generatorParameters['projectBlogpostDir']
	files = os.listdir(blogpostDir)
	for filename in files:
		filepath = os.path.join(blogpostDir, filename)
		if os.path.isfile(filepath):
			if isValidFilename(filename):
				if filename.endswith(".md"):
					filename = markdown_to_html(filename)
					generatorParameters['blogPostList'].append(filename)
				elif filename.endswith(".html"):
					generatorParameters['blogPostList'].append(filename)
				
				# copy any mathing file
				shutil.copy(filepath, generatorParameters['blogArchiveDir'])
	
	if len(generatorParameters['blogPostList']) > 0:
		generatorParameters['blogPostList'].sort()
		generatorParameters['blogPostList'].reverse()
	
	print("createBlogpostFileList()")


def createBlogposts():
	th = templatehandler.TemplateHandler()
	blogGenerator = blogpostgenerator.BlogPostGenerator(
		th, 
		generatorParameters['blogTitle'], 
		generatorParameters['generatorStarted'])
	parser = commentparser.CommentParser()
	
	for item in generatorParameters['blogPostList']:
		inFileName = os.path.join(generatorParameters['blogArchiveDir'], item)
		with open(inFileName, 'r') as fileObject:
			content = fileObject.read()
		parser.feed(content)
		generatorParameters['blogPostMetaData'][item] = parser.get_parameter()
		#print(generatorParameters['blogPostMetaData'][item])
		html = blogGenerator.get_html(
			generatorParameters['blogPostMetaData'][item], 
			content)
		outFileName = os.path.join(generatorParameters['blogArchiveDir'], item)
		with open(outFileName, 'w') as fileObject:
			fileObject.write(html)
	print("createBlogposts()")


def create_keyword_structure():
	"""Iterate over the meta information of all blogarticles and gather a list 
	of distinct keywords. Then find for each keyword all blogarticles which
	refer to these keywords. Store it then as dictionary into local datastrcture
	below 'keywordMetaData'."""
	# iterate over all blogposts
	for blogpost in generatorParameters['blogPostList']:
		blogpost_keywords = generatorParameters['blogPostMetaData'][blogpost]['blogkeywords']
		# iterate over blogpost's keywords
		for keyword in blogpost_keywords:
			if keyword not in generatorParameters['keywordMetaData'].keys():
				generatorParameters['keywordMetaData'][keyword] = []
			
			generatorParameters['keywordMetaData'][keyword].append(blogpost)
	print("create_keyword_structure()")


def create_archive_structure():
	"""Iterate over the meta information of all blogarticles and gather a list 
	of years the articles were created. Then find for each year all blogarticles 
	which match with their creation date to this. Store it then as dictionary
	into local datastrcture below 'archiveMetaData'."""
	# iterate over all blogposts
	for blogpost in generatorParameters['blogPostList']:
		blogcreated = generatorParameters['blogPostMetaData'][blogpost]['blogcreated']
		archive_year = blogcreated.year
		if archive_year not in generatorParameters['archiveMetaData'].keys():
			generatorParameters['archiveMetaData'][archive_year] = []
		generatorParameters['archiveMetaData'][archive_year].append(blogpost)
	print("create_archive_structure()")


if __name__ == '__main__':
	init()
	
	sync_object = cloudsync.CloudSync()
	hasBlogChanges = sync_object.sync(
		"blogposts", 
		generatorParameters['projectBlogpostDir']
	)
	
	if hasBlogChanges:
		cleanup()
		blogBuildDirLayout()
		createBlogpostFileList()
		createBlogposts()
		create_keyword_structure()
		create_archive_structure()
	
	print("main() done")	
	
	print(pprint.pformat(generatorParameters))
