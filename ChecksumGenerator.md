# Example - Checksum Generator #

This example goes through all the files within the given directories recursively and generates a SHA-1 checksum for each file.

This uses `fileprocessor.searchers.FileSearcher` to find all the files and a custom extractor derived from `fileprocessor.extractors.ByteStreamExtractor` to generate the checksum. **Every** file is chosen, so no filterer is used for this particular example.

Source code:
```
"""Generates checksums for every file within a directory (recursively),
displaying those checksums through stdout.

Created to provide an example of how to use the fileprocessor module.

"""

import sys
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
					 memory. (default: 65536)

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

def main(directoriesToSearch):
	"""Run checksum generation process.

	Arguments:
	directoriesToSearch -- List containing all of the
						   directories containing files
						   to generate checksums for

	"""
	# Build components to use for file processor
	searcher = searchers.FileSearcher(True)
	extractor = ChecksumGenerator()
	processor = FileProcessor(searcher, [], extractor)
	# Perofrm checksum generation and display every checksum
	generatedChecksums = processor.process(directoriesToSearch)
	for filename, checksum in generatedChecksums.items():
		print("{}\n\t{}".format(filename, checksum))

if __name__ == "__main__":
	# Parse command line arguments
	if len(sys.argv) < 3:
		sys.exit("Usage: python {} {{-d <directory> }}".format(sys.argv[0]))
	directoriesToSearch = [] # store all directories requesed 
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == "-d" and i < (len(sys.argv) - 1):
			i += 1 # go to next argumnet, the actual directory
			directoriesToSearch.append( sys.argv[i] )

	if len(directoriesToSearch) == 0:
		sys.exit("No directories to search specified")

	main(directoriesToSearch)
```