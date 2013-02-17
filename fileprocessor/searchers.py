"""Contains all built-in Searcher classes."""

import sys
import os
import collections

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

class CompositeSearcher(Searcher):

	"""Uses multiple searchers and combines their findings into a single listing of resources."""

	def __init__(self, searchers):
		if not isinstance(searchers, collections.Iterable):
			raise TypeError("Collection of searchers to use must be an iterable object")
		self.searchers = searchers

	def search(self, rootDirectory):
		"""Pass given directory to child searchers and combine their results.

		If a searcher raises an exception or returns an invalid value,
		then that searcher is simply ignored during the run. The findings
		of the other searchers will still be returned.

		Arguments:
		rootDirectory -- Path to directory to start searching from

		"""
		# All the resources found by the searchers. This is a set to
		# get rid of duplicate values
		allFindings = set()
		for searcher in self.searchers:
			try:
				# Get child searcher's findings as a set and merge it
				# with the set containing all the findings
				findings = set(searcher.search(rootDirectory))
				allFindings = allFindings.union(findings)
			except BaseException as e:
				print("Error searching for resources: {}".format(e), file=sys.stderr)

		return allFindings