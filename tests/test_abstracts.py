import unittest
import sys
import os
sys.path.append(os.environ.get("PROJECT_ROOT_DIRECTORY", "."))

from fileprocessor.abstracts import *

class TestAbstractClasses(unittest.TestCase):

	def test_searcher(self):
		searcher = Searcher()
		with self.assertRaises(NotImplementedError):
			searcher.search("dir")

	def test_filterer(self):
		filterer = Filterer()
		with self.assertRaises(NotImplementedError):
			filterer.filter(["test.txt"])

	def test_extractor(self):
		extractor = Extractor()
		with self.assertRaises(NotImplementedError):
			extractor.extract("test.txt")