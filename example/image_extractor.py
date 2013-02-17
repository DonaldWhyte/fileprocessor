"""Recursviely searches through directory and displays any image URLs
inside web pages.

Created to provide an example of how to use the fileprocessor module.

"""

import sys
import re
sys.path.append(".") # TODO: remove
from fileprocessor import FileProcessor, searchers, filterers, extractors

class ImageURLExtractor(extractors.TextExtractor):

	"""Extract image URLs from a web page."""

	# Pre-compiled regexes that are used to 
	IMAGE_TAG_REGEX = re.compile( r"<img.*?src=([\"\'])(.*?)\1.*?/>" )
	CSS_URL_REGEX = re.compile( r"url\( ?([\"\'])(.*?)\1 ?\)" )

	def extractFromString(self, data):
		"""Return list of found image URls in a web page.

		Arguments:
		data -- The full web page to scan as a string

		"""
		# Search for all occurrences of JavaScript
		matches = [ match for match in self.IMAGE_TAG_REGEX.finditer(data) ]
		matches += [ match for match in self.CSS_URL_REGEX.finditer(data) ]
		# Extract the found image URLs
		imageURLs = []
		for match in matches:
			imageURLs.append( match.group(2) )
		return imageURLs

def main(directory, showAll):
	"""Run image resource extraction process.

	Arguments:
	directory -- Directory containing web page soure code
	showAll -- If set to True, then all scanned files will
			   be displayed, even if no image URLs were
			   extracted from them. This means if this is
			   False, then any files where no data was
			   found are omitted.

	"""
	# Build components to use for file processor
	searcher = searchers.FileSearcher(True)
	filterer = filterers.ExtensionFilterer( ["html", "htm", "shtml", "php", "css", "js"] )
	extractor = ImageURLExtractor()
	processor = FileProcessor(searcher, [ filterer ], extractor)
	# Perform the URL extraction and display findings
	extractedURLs = processor.process(directory)
	for filename, imageURLs in extractedURLs.items():
		# If nothing was found in this file and the
		# approrpiate flag is set, skip this file
		if len(imageURLs) == 0 and not showAll:
			continue

		imageURLLines = ""
		for url in imageURLs:
			imageURLLines += "\t{}\n".format(url)
		# Remove last newline
		if len(imageURLLines) > 0:
			imageURLLines = imageURLLines[:-1]
		print("{}\n{}".format(filename, imageURLLines))



if __name__ == "__main__":
	# Parse command line arguments
	if len(sys.argv) < 2:
		sys.exit("Usage: python {} <directory> {-a}".format(sys.argv[0]))
	showAll = ("-a" in sys.argv)
	main(sys.argv[1], showAll)