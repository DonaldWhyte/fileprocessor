# Example - Image Link Extraction #

`image_extractor.py` illustrates the use of fileprocessor by extracting the URLs of all images reference by HTML `<img>` tags and CSS `url(...)` directives. It recursively searches through one or more directories for files with the extensions `html`, `htm`, `shtml`, `php`, `css` and `js`.

This uses `fileprocessor.searchers.FileSearcher` to find all files within a directory, `fileprocessor.filterers.ExtensionFilterer` to remove non-web files and a custom extractor which subclasses `fileprocessor.extractors.TextExtractor` to scan the files for links.

Source code:
```
"""Recursively searches through directory and displays any image URLs
inside web pages.

Created to provide an example of how to use the fileprocessor module.

"""

import sys
import re
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
	directoriesToSearch -- List containing all of the
						   directories containing web page
						   soure code that need to be scanned
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
	extractedURLs = processor.process(directoriesToSearch)
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
	if len(sys.argv) < 3:
		sys.exit("Usage: python {} {{ -d <directory> }} {{-a}}".format(sys.argv[0]))
	
	directoriesToSearch = [] # store all directories requesed 
	for i in range(1, len(sys.argv)):
		if sys.argv[i] == "-d" and i < (len(sys.argv) - 1):
			i += 1 # go to next argumentt, the actual directory
			directoriesToSearch.append( sys.argv[i] )
	showAll = ("-a" in sys.argv)

	if len(directoriesToSearch) == 0:
		sys.exit("No directories to search specified")

	main(directoriesToSearch, showAll)
```