"""Generates checksums fore every file within a directory (recursively),
displaying those checksums through stdout.

Created to provide an example of how to use the fileprocessor module.

"""

import sys
sys.path.append(".") # TODO: remove
import hashlib
from fileprocessor import FileProcessor, searchers, filterers, extractors

class ChecksumGenerator(extractors.ByteStreamExtractor):

	"""Generates """

	def __init__(self, blockSize = 65536):
		"""Construct instance of ChecksumGenerator.

		Keyword arguments:
		blockSize -- Amount of data to read it at once when
					 generating checksum. Should be fairly
					 low if the machine does not have much
					 memory.

		"""
		self.blockSize = blockSize

	def extractFromStream(self, data):
		"""Generate and reutrn SHA-1 checksum from stream of byte data.

		Arguments:
		data -- Byte stream containing data to generate checksum for

		"""
		hasher = hashlib.sha1()
		buff = data.read(self.blockSize)
		while len(buff) > 0:
			hasher.update(buff)
			buff = data.read(self.blockSize)
		return hasher.hexdigest()

def main(directory, showAll):
	"""Run checksum generation process.

	Arguments:
	directory -- Directory containing files to generate
				 checksums for

	"""
	# Build components to use for file processor
	searcher = searchers.FileSearcher(True)
	extractor = ChecksumGenerator()
	processor = FileProcessor(searcher, [], extractor)
	# Perofrm checksum generation and display every checksum
	generatedChecksums = processor.process(directory)
	for filename, checksum in generatedChecksums.items():
		print("{}\n\t{}".format(filename, checksum))

if __name__ == "__main__":
	# Parse command line arguments
	if len(sys.argv) < 2:
		sys.exit("Usage: python {} <directory>".format(sys.argv[0]))
	main(sys.argv[1])