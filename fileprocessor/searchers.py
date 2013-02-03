"""Contains all built-in Searcher classes."""

import os

from .abstracts import Searcher

class FileSearcher(Searcher):
	
	"""Searches the filesystem for files, either recursively and non-recursively."""

	def __init__(self, recurse = False):
		"""Construct instance of FileSearcher.

		Keyword arguments:
		recurse -- If set to True, then the searcher will recursively
				   search through the given directory's sub-directories
				   for files.

		"""
		self.recurse = recurse

	def search(self, rootDirectory):
		"""Return a list containing the absolute paths of all files found.

		All files found are returned, regardless of name or type.		

		Arguments:
		rootDirectory -- Path to directory ot start searching from

		"""
		if not isinstance(rootDirectory, str):
			raise TypeError("Path to root directory to start search from should be a string")
		if not os.path.isdir(rootDirectory):
			raise IOError("Root directory '{}' does not exist".format(rootDirectory))

		fileListing = []
		if self.recurse:
			for root, directories, files in os.walk(rootDirectory):
				for filename in files:
					path = os.path.join(root, filename)
					fileListing.append( os.path.abspath(path) )
		else:
			for filename in os.listdir(rootDirectory):
				path = os.path.join(rootDirectory, filename)
				if os.path.isfile(path):
					fileListing.append( os.path.abspath(path) )

		return fileListing