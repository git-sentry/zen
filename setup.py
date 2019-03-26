#!/usr/bin/env python3

import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

version = '0.0.0'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='zen',
    version=version,
    install_requires=requirements,
    author='Dragos Dumitrache',
    author_email='dragosd2000@gmail.com.com',
    description='Github Zen utility tools',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'zen = zen.main.zen:main',
        ]
    },
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dragosdumitrache/zen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)
