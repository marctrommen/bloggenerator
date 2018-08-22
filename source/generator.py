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
import listpagegenerator
import simplelistpagegenerator
import simplepagegenerator

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
	generatorParameters['blogRootDir'] = os.path.join(generatorParameters['projectRootDir'], "_site")
	generatorParameters['blogArchiveDir'] = os.path.join(generatorParameters['blogRootDir'], "archive")
	
	locale.setlocale(locale.LC_ALL, '')
	generatorParameters['generatorStarted'] = datetime.datetime.now()
	generatorParameters['blogTitle'] = "techBlog"
	
	generatorParameters['templateHandler'] = templatehandler.TemplateHandler()
	
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
	
	# copy .htaccess file if any exists
	filepath = os.path.join(generatorParameters['projectRootDir'], '.htaccess')
	if os.path.exists(filepath):
		shutil.copy(filepath, generatorParameters['blogRootDir'])
	
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


def markdown_to_html(filename, destination):
	md_content = None
	html_content = None

	md_file = os.path.join(generatorParameters['projectContentDir'], filename)
	with open(md_file, 'r') as fileObject:
		md_content = fileObject.read()
	
	html_content = markdown.markdown(md_content, 
		extensions=['markdown.extensions.extra'],
		output_format = "html5", 
		tab_length = 4,
		smart_emphasis = True
	)
	
	html_filename = filename.replace(".md", ".html")
	html_file = os.path.join(destination, html_filename)
	with open(html_file, 'w') as fileObject:
		fileObject.write(html_content)
	
	print("markdown_to_html()")
	return html_filename
	

def createBlogpostFileList():
	"""get file list of "content" directory and check if file in list hits
	against the file naming pattern and starts with "yyyymmdd_hhMMSS".
	If this test passes successfuly handle the file as follows:
	
	*   if file content is of type Markdown, then translate it into HTML5, 
	    add it to the blog candidate list for further blog generation processing
		copy the Markdown file to the blog destination folder
		
	*   if file content is of type HTML5, then add it to the blog candidate
	    list for further blog generation processing.
		
	*   any other files just copy them to the blog destination folder as a 
	    linked file of the blog post
	"""
	blogpostDir = generatorParameters['projectContentDir']
	files = os.listdir(blogpostDir)
	for filename in files:
		filepath = os.path.join(blogpostDir, filename)
		if os.path.isfile(filepath):
			if isValidFilename(filename):
				if filename.endswith(".md"):
					filename = markdown_to_html(filename, generatorParameters['blogArchiveDir'])
					generatorParameters['blogPostList'].append(filename)
				elif filename.endswith(".html"):
					generatorParameters['blogPostList'].append(filename)
				
				# copy any matching file
				shutil.copy(filepath, generatorParameters['blogArchiveDir'])
	
	if len(generatorParameters['blogPostList']) > 0:
		generatorParameters['blogPostList'].sort()
		generatorParameters['blogPostList'].reverse()
	
	print("createBlogpostFileList()")


def createBlogposts():
	blogGenerator = blogpostgenerator.BlogPostGenerator(
		generatorParameters['templateHandler'], 
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


def create_blog_list_pages():
	years = generatorParameters['archiveMetaData'].keys()
	current_year = generatorParameters['generatorStarted'].year
	
	for year in years:
		if year == current_year:
			filename = 'index.html'
		else:
			filename = 'archive_' + str(year) + '.html'

		list_page_generator = listpagegenerator.ListpageGenerator(
			generatorParameters['templateHandler'], 
			generatorParameters['blogTitle'], 
			str(year), 
			generatorParameters['generatorStarted']
		)
	
		html = list_page_generator.get_html(
			generatorParameters['archiveMetaData'][year], 
			generatorParameters['blogPostMetaData']
		)
		outFileName = os.path.join(generatorParameters['blogRootDir'], filename)
		with open(outFileName, 'w') as fileObject:
			fileObject.write(html)
	
	print('create_blog_list_pages()')


def create_keyword_list_pages():
	keywords = generatorParameters['keywordMetaData'].keys()
	
	for keyword in keywords:
		filename = 'keyword_' + keyword + '.html'
		
		list_page_generator = listpagegenerator.ListpageGenerator(
			generatorParameters['templateHandler'], 
			generatorParameters['blogTitle'], 
			'Tag: ' + keyword.replace("_", " ").upper(), 
			generatorParameters['generatorStarted']
		)

		html = list_page_generator.get_html(
			generatorParameters['keywordMetaData'][keyword], 
			generatorParameters['blogPostMetaData']
		)
			
		outFileName = os.path.join(generatorParameters['blogRootDir'], filename)
		with open(outFileName, 'w') as fileObject:
			fileObject.write(html)

	print('create_keyword_list_pages()')


def create_archive_page():
	years = generatorParameters['archiveMetaData'].keys()
	
	simple_list_page_generator = simplelistpagegenerator.SimpleListpageGenerator(
		generatorParameters['templateHandler'], 
		generatorParameters['blogTitle'], 
		'Jahresarchive', 
		generatorParameters['generatorStarted']
	)

	html = simple_list_page_generator.get_html(
		generatorParameters['archiveMetaData'],
		False
	)
		
	outFileName = os.path.join(generatorParameters['blogRootDir'], 'archive.html')
	with open(outFileName, 'w') as fileObject:
		fileObject.write(html)
	
	print('create_archive_page()')


def create_keyword_catalog_page():
	keywords = list(generatorParameters['keywordMetaData'].keys())
	keywords.sort()
	
	simple_list_page_generator = simplelistpagegenerator.SimpleListpageGenerator(
		generatorParameters['templateHandler'], 
		generatorParameters['blogTitle'], 
		'Verfügbare Keywords', 
		generatorParameters['generatorStarted']
	)

	html = simple_list_page_generator.get_html(
		generatorParameters['keywordMetaData'],
		True
	)
		
	outFileName = os.path.join(generatorParameters['blogRootDir'], 'keyword_catalog.html')
	with open(outFileName, 'w') as fileObject:
		fileObject.write(html)

	print('create_keyword_catalog_page()')


def create_special_page(pagename):
	if pagename == 'about':
		filename = pagename + '.md'
		pagetitle = 'About / Über'
	elif pagename == 'impressum':
		filename = pagename + '.md'
		pagetitle = 'Impressum'
	else:
		return
	
	# transform Markdown to HTML5
	md_filepath = os.path.join(generatorParameters['projectContentDir'], filename)
	# copy Markdown file
	shutil.copy(md_filepath, generatorParameters['blogRootDir'])

	html_filename = markdown_to_html(filename, generatorParameters['blogRootDir'])
	
	html_filepath = os.path.join(generatorParameters['blogRootDir'], html_filename)
	with open(html_filepath, 'r') as fileObject:
		html_snippet = fileObject.read()
	
	simple_page_generator = simplepagegenerator.SimplePageGenerator(
		generatorParameters['templateHandler'], 
		generatorParameters['blogTitle'], 
		generatorParameters['generatorStarted']
	)

	html = simple_page_generator.get_html(pagetitle, html_snippet)

	with open(html_filepath, 'w') as fileObject:
		fileObject.write(html)
	
	print('create_special_page()')


def sync_to_web_hoster():
	import subprocess
	
	command = ['doStratoSshSync.sh', 
		'--in', generatorParameters['blogRootDir'],
		'--out', 'www/techblog']
	error_code = -1
	
	with subprocess.Popen(command) as process:
		error_code = process.wait()	
	
	if not (error_code == 0):
		print('An error occured while file sync to web space via ssh tunnel!')
	print('sync_to_web_hoster()')


def website_build():
	init()
	
	sync_object = cloudsync.CloudSync()
	hasBlogChanges = sync_object.sync(
		"techBlog", 
		generatorParameters['projectContentDir']
	)
	
	if hasBlogChanges:
		cleanup()
		blogBuildDirLayout()
		createBlogpostFileList()
		createBlogposts()
		create_keyword_structure()
		create_archive_structure()
		create_blog_list_pages()
		create_keyword_list_pages()
		create_archive_page()
		create_keyword_catalog_page()
		create_special_page("about")
		create_special_page("impressum")
		sync_to_web_hoster()

	print('website_build()')

def test_website_build():
	init()
	cleanup()
	blogBuildDirLayout()
	createBlogpostFileList()
	createBlogposts()
	create_keyword_structure()
	create_archive_structure()
	create_blog_list_pages()
	create_keyword_list_pages()
	create_archive_page()
	create_keyword_catalog_page()
	create_special_page("about")
	create_special_page("impressum")


if __name__ == '__main__':
	website_build()
	#test_website_build()
	
	print("main() done")
	
	print(pprint.pformat(generatorParameters))
