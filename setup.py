#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import mulder

def setup_package():
	metadata = dict()
	metadata['name'] = mulder.__package__
	metadata['version'] = mulder.__version__
	metadata['description'] = mulder.description_
	metadata['url'] = mulder.url_
	metadata['entry_points'] = {
		'console_scripts': [
			'mulder = mulder.mulder:main',
		],
	}
	metadata['packages'] = find_packages()
	metadata['include_package_data'] = False
	setup(**metadata)

if __name__ == "__main__":
	setup_package()
