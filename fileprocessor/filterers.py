"""Contains all built-in Filterer classes."""

import collections
import fnmatch
import os

from fileprocessor.abstracts import Filterer


class ExcludeListFilterer(Filterer):

	"""Filterer which filters files based on glob patterns."""

	def __init__(self, excludeList):
		"""Construct instance of ExcludeListFilterer.

		Arguments:
		excludeList -- List of glob patterns which will be used as
					   as a black list to remove files in the list
					   from the final listing.

		"""
		if not isinstance(excludeList, collections.Iterable):
			raise TypeError("Exclusion list should be an iterable collection of strings")
		self.excludeList = excludeList

	def filter(self, fileListing):
		"""Filter file listing based on stored glob patterns.

		Returns NEW list containing the the files which passed the filter.

		Arguments:
		fileListing -- A list containing the absolute paths of the
					   files to filter.

		"""
		if not isinstance(fileListing, collections.Iterable):
			raise TypeError("List of files to filter should be an iterable collection of strings")
		newListing = list(fileListing)

		# Go through each entry, checking if they match one of the
		# glob patterns. If an entry does, it is removed
		i = 0
		while i < len(newListing):
			filtered = False
			for exclusion in self.excludeList:
				if fnmatch.fnmatch(newListing[i], exclusion):
					filtered = True
					del newListing[i]
					break
			# If the current element was not deleted, increment
			# the index into the file listing. We don't do it if
			# an element was deleted as the next element would
			# have moved ot the delete elements's index
			if not filtered:
				i += 1

		return newListing


class IncludeListFilterer(Filterer):

	"""Filterer which filters files that don't match glob patterns."""

	def __init__(self, includeList):
		"""Construct instance of IncludeListFilterer.

		Arguments:
		includeList -- List of glob patterns which will be used as
					   as a white list to remove files NOT in the list
					   from the final listing.

		"""
		if not isinstance(includeList, collections.Iterable):
			raise TypeError("Inclusion list should be an iterable collection of strings")
		self.includeList = includeList

	def filter(self, fileListing):
		"""Filter file listing based on stored glob patterns.

		Returns NEW list containing the the files which passed the filter.

		Arguments:
		fileListing -- A list containing the absolute paths of the
					   files to filter.

		"""
		if not isinstance(fileListing, collections.Iterable):
			raise TypeError("List of files to filter should be an iterable collection of strings")

		# Add any files from the original listing which match
		# one of the whitelist patterns.
		newListing = []
		for elem in fileListing:
			for pattern in self.includeList:
				if fnmatch.fnmatch(elem, pattern):
					newListing.append(elem)
					break
		return newListing		


class ExtensionFilterer(Filterer):

	def __init__(self, allowedExtensions):
		"""Construct instance of ExtensionFilterer.

		Arguments:
		allowedExtensions -- List of allowed extensions (e.g. ["txt", "py"]).
							 Any files which don't have these extensions
							 will be removed.

		"""
		if not isinstance(allowedExtensions, collections.Iterable):
			raise TypeError("Allowed extension list should be an iterable collection of strings")
		self.allowedExtensions = allowedExtensions

	def filter(self, fileListing):
		"""Filter file listing based on stored extension whitelist.

		Returns NEW list containing the the files which passed the filter.

		Arguments:
		fileListing -- A list containing the absolute paths of the
					   files to filter.

		"""
		if not isinstance(fileListing, collections.Iterable):
			raise TypeError("List of files to filter should be an iterable collection of strings")
		newListing = list(fileListing)

		i = 0
		while i < len(newListing):
			name, extension = os.path.splitext(newListing[i])
			# Increment index and allow file if its extension is in
			# the white list
			if extension[1:] in self.allowedExtensions:
				i += 1
			else:
				del newListing[i]

		return newListing