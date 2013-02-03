"""Contains the abstract classes for the major components of the library."""

class Searcher:

	"""Searches directory for files to process."""

	def search(self, rootDirectory):
		"""Search directory for files and return list of absolute paths to those files.

		Arguments:
		rootDirectory -- Root directory to start searching in.

		"""
		raise NotImplementedError

class Filterer:

	"""Filters lists of files based on some criteria."""

	def filter(self, fileListing):
		"""Filter list of files and return a NEW list containing only the files that passed the filter.

		NOTE: This should not alter the original list given.

		Arguments:
		fileListing -- A list containing the absolute paths of the
					   files to filter."""
		raise NotImplementedError

class Extractor:

	"""Extracts data from files."""

	def extract(self, filename):
		"""Extract data from the file with the given filename.

		What this returns depends on what data is to be extracted.
		This is determined by the concrete subclass of Extractor.

		Arguments:
		filename -- Name of the file to extract data from

		"""
		raise NotImplementedError