from distutils.core import setup
import os
import fileprocessor


currentFileDirectory = os.path.dirname(__file__)
with open(os.path.join(currentFileDirectory, "README"), "r") as f:
	readme = f.read()

setup(
	name="fileprocessor",
	version=fileprocessor.VERSION,
	description="Harness that makes bulk processing files quick and easy",
	long_description=readme,
	author="Donald Whyte",
	author_email="donaldwhyte0@gmail.com",
	url="http://code.google.com/p/fileprocessor",
	classifiers=[
		"Development Status :: 3 - Alpha Development Status"
		"Intended Audience :: Developers",
		"Programming Language :: Python 3",
		"Programming Language :: Python 3.2",
		"Programming Language :: Python 3.3",
	],
	keywords="batch file processing generic filesystem component lightweight utility",
	license="MIT",
	packages=("fileprocessor",),
	data_files=[ (".", ["LICENCE"]) ]
)