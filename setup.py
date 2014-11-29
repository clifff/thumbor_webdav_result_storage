# coding: utf-8

from setuptools import setup, find_packages

setup(
	name = 'thumbor_webdav_result_storage',
	version = "1",
	description = 'Thumbor extension to use WebDAV for result storage',
	author = 'Clif Reeder',
	author_email = 'clifreeder@gmail.com',
	include_package_data = True,
	packages=find_packages(),
	requires=['thumbor','tornado']
)
