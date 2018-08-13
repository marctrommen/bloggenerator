# -*- coding: utf-8 -*-


import os
import shutil
import datetime
import locale
import markdown

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


def markdown_to_html(filepath, filename):
	md_content = None
	html_content = None

	md_file = os.path.join(filepath, filename)
	with open(md_file, 'r') as fileObject:
		md_content = fileObject.read()
	
	html_content = markdown.markdown(md_content, 
		extensions=['markdown.extensions.extra'],
		output_format = "html5", 
		tab_length = 4,
		smart_emphasis = True
	)
	
	html_filename = filename.replace(".md", ".html")
	html_file = os.path.join(filepath, html_filename)
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
					filename = markdown_to_html(blogpostDir, filename)
					generatorParameters['blogPostList'].append(filename)
					filepath = os.path.join(blogpostDir, filename)
					shutil.copy(filepath, generatorParameters['blogArchiveDir'])
				elif filename.endswith(".html"):
					generatorParameters['blogPostList'].append(filename)
				else:
					shutil.copy(filepath, generatorParameters['blogArchiveDir'])
	print("createBlogpostFileList()")


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
	print("createBlogposts()")



if __name__ == '__main__':
	init()
	cleanup()
	blogBuildDirLayout()
	createBlogpostFileList()
	createBlogposts()
	print("main() done")