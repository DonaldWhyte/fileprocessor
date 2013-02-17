"""Contains all built-in Extractor classes."""

from fileprocessor.abstracts import Extractor

class ByteExtractor(Extractor):

	"""Extractor used for extracting data from a binary file.

	If the files being read are large, then it may be worth
	using ByteStreamExtractor to read the file bit-by-bit.
	Otherwise, a lot of memory will be used up as the entire
	contents of the large file is loaded in one go.

	"""

	def extract(self, filename):
		"""Read entire contents of binary file and extract data from it.

		What this returns depends on what data is to be extracted.
		This is determined by the concrete subclasses of Extractor.

		Arguments:
		filename -- Name of the file to extract data from.
					TypeError is raised if this is not a string.

		"""
		if not isinstance(filename, str):
			raise TypeError("Filename must be a string")
		# Open file as BINARY and read it all in at once
		with open(filename, "rb") as f:
			data = f.read()
		return self.extractFromBytes(data)

	def extractFromBytes(self, data):
		"""Extract information from byte data and return that information.

		Raises a NotImplementedError . This method should be
		overriden by subclasses.

		Arguments:
		data -- a bytes object that contains all of the data to process

		"""
		raise NotImplementedError


class ByteStreamExtractor(Extractor):

	"""Extractor used for extracting data from a binary file.

	This class streams the binary file, so it can be read
	incrementally rather than reading the entire file in one go.

	"""

	def extract(self, filename):
		"""Open binary file stream and extract data from it.

		What this returns depends on what data is to be extracted.
		This is determined by the concrete subclasses of Extractor.

		Arguments:
		filename -- Name of the file to extract data from
					TypeError is raised if this is not a string.

		"""
		if not isinstance(filename, str):
			raise TypeError("Filename must be a string")
		# Open file and read it all in at once
		with open(filename, "rb") as f:
			return self.extractFromStream(f)

	def extractFromStream(self, stream):
		"""Extract information from a byte stream and return that information.

		Raises a NotImplementedError. This method should be
		overriden by subclasses.

		Arguments:
		data -- a binary stream that can be used to access data
				to process

		"""
		raise NotImplementedError


class TextExtractor(Extractor):

	"""Extractor used for extracting data from a text file.

	If the files being read are large, then it may be worth
	using TextStreamExtractor to read the file bit-by-bit.
	Otherwise, a lot of memory will be used up as the entire
	contents of the large file is loaded in one go.

	"""

	def extract(self, filename):
		"""Read entire contents of text file and extract data from it.

		What this returns depends on what data is to be extracted.
		This is determined by the concrete subclasses of Extractor.

		Arguments:
		filename -- Name of the file to extract data from
					TypeError is raised if this is not a string.

		"""
		if not isinstance(filename, str):
			raise TypeError("Filename must be a string")
		# Open file as TEXT and read it all in at once
		with open(filename, "r") as f:
			data = f.read()
		return self.extractFromString(data)

	def extractFromString(self, data):
		"""Extract information from text data and return that information.

		Raises a NotImplementedError. This method should be
		overriden by subclasses.

		Arguments:
		data -- a string that contains all of the data to process

		"""
		raise NotImplementedError


class TextStreamExtractor(Extractor):

	"""Extractor used for extracting data from a text file.

	This class streams the text file, so it can be read
	incrementally rather than reading the entire file in one go.

	"""

	def extract(self, filename):
		"""Open text file stream and extract data from it.

		What this returns depends on what data is to be extracted.
		This is determined by the concrete subclasses of Extractor.

		Arguments:
		filename -- Name of the file to extract data from
					TypeError is raised if this is not a string.

		"""
		if not isinstance(filename, str):
			raise TypeError("Filename must be a string")
		# Open file and read it all in at once
		with open(filename, "r") as f:
			return self.extractFromStream(f)

	def extractFromStream(self, stream):
		"""Extract information from a text stream and return that information.

		Raises a NotImplementedError. This method should be
		overriden by subclasses.

		Arguments:
		data -- a text stream that can be used to access data
				to process

		"""
		raise NotImplementedError		