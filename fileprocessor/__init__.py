"""Main import for fileprocessing library. Contains main class for
processing files."""

import sys
import os
import collections


# Done so importing modules from library is easier
def getSubModulesAndPackages():
	"""Return list of all modules and packages contained within current package."""
	modulesToImport = []

	# Add all Python files in directory
	directoryName = os.path.dirname(__file__)
	for filename in os.listdir(directoryName):
		# Ignore filenames in exclude list
		if filename in ["__pycache__"]:
			continue
		# If filename ends with .py, we assume it's a Python module
		elif filename.endswith(".py"):
			modulesToImport.append(filename[:-3])
		# If filename is actually a directory, we assume it's a subpackage
		else:
			absolutePath = os.path.abspath( os.path.join(directoryName, filename) )
			if os.path.isdir(absolutePath):
				modulesToImport.append(filename)

	return modulesToImport
__all__ = getSubModulesAndPackages()


class FileProcessor:

	"""Harness for searching, filtering and extracting data from files."""

	def __init__(self, searcher, filterers, extractor):
		"""Construct new instance of FileProcessor.

		Arguments:
		searcher -- Object which searches the file system and returns
					a list of all the files found. Should be an instance
					of Searcher.
		filterers -- List of objects which filter the file listing based
					 on some criteria. Objects should be instances of
					 Filterer.
		extractor -- Object which processes a single file and returns the
					 desired data from it. Should be an instance of
					 Extractor.
		"""
		self.searcher = searcher
		self.filterers = filterers
		self.extractor = extractor

	def process(self, rootDirectories):
		"""Process one or more directories of files in some way.

		Return a dictionary where the keys are the absolute paths
		to the files and values are the data extracted from the
		corresponding files.

		Exactly how it searches for files to process and what data
		it extracts from the files is determined by the objects
		given to the FileProcessor instance in the constructor.

		Arguments:
		rootDirectories -- Either a string containing the path to one
						  directory or a list containing multiple
						  directories to process

		"""
		if isinstance(rootDirectories, str): # wrap single directory in a list
			rootDirectories = [ rootDirectories ]
		elif not isinstance(rootDirectories, collections.Iterable):
			raise TypeError("Path to root directory must be a string or collection of strings")

		# Now process each directory, keepinga global dictionary of extracted data
		data = {}
		for directory in rootDirectories:
			# If directory doesn't exist, report the issue and skip to the next one
			if not os.path.isdir(directory):
				print("Directory '{}' does not exist".format(directory), file=sys.stderr)
				continue
			# Search for the files in the directory, filter the resultant list
			# and then extract data from the files
			fileListing = self.searcher.search(directory)
			for filterer in self.filterers:
				fileListing = filterer.filter(fileListing)
			for path in fileListing:
				data[path] = self.extractor.extract(path)

		return data