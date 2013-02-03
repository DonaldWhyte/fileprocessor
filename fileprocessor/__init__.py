"""Main import for fileprocessing library. Contains main class for
processing files."""

import os


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

	def __init__(self, searcher, filterer, extractor):
		"""Construct new instance of FileProcessor.

		Arguments:
		searcher -- Object which searches the file system and returns
					a list of all the files found. Should be an instance
					of Searcher.
		filterer -- Object which filters the file listing based on some
					criteria. Should be an instance of Filterer.
		extractor -- Object which processes a single file and returns the
					 desired data from it. Should be an instance of
					 Extractor.
		"""
		self.searcher = searcher
		self.filterer = filterer
		self.extractor = extractor

	def process(self, rootDirectory):
		"""Process a given directory of files in some way.

		Return a dictionary where the keys are the absolute paths
		to the files and values are the data extracted from the
		corresponding files.

		Exactly how it searches for files to process and what data
		it extracts from the files is determined by the objects
		given to the FileProcessor instance in the constructor.

		Arguments:
		rootDirectory -- Path to directory to search files in.

		"""
		if not isinstance(rootDirectory, str):
			raise TypeError("Path to root directory must be a string")
		if not os.path.isdir(rootDirectory):
			raise IOError("Directory '{}' does not exist".format(rootDirectory))

		fileListing = self.searcher.search(rootDirectory)
		fileListing = self.filterer.filter(fileListing)
		data = {}
		for path in fileListing:
			data[path] = self.extractor.extract(path)
		return data