#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import filecmp
import subprocess
import os
import shutil

class CloudSync(object):

	def __init__(self):
		self.__cloud_mountpoint = '/media/marco/gmx'


	def __mount_cloud(self):
		command = ['mount', self.__cloud_mountpoint]
		error_code = -1
		
		with subprocess.Popen(command) as process:
			error_code = process.wait()
		
		return error_code == 0


	def __unmount_cloud(self):
		command = ['umount', self.__cloud_mountpoint]
		error_code = -1
		
		with subprocess.Popen(command) as process:
			error_code = process.wait()
		
		return error_code == 0


	def sync(self, rel_cloud_dir, abs_local_dir):
		"""synchronise """
		has_changes = False
		
		if self.__mount_cloud():
			cloud_dir = os.path.join(self.__cloud_mountpoint, rel_cloud_dir)
			
			result = filecmp.dircmp(cloud_dir, abs_local_dir)
			
			# copy all new files from cloud_dir to local_dir
			for new_file in result.left_only:
				has_changes = True
				shutil.copy(
					os.path.join(cloud_dir, new_file),
					abs_local_dir
				)
			
			# copy all changed files from cloud_dir to local_dir
			for changed_file in result.diff_files:
				has_changes = True
				shutil.copy(
					os.path.join(cloud_dir, changed_file),
					abs_local_dir
				)
			
			has_changed = self.__unmount_cloud() and has_changes
		else:
			self.__unmount_cloud()
		
		return has_changes
