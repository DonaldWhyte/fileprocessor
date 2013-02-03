import unittest
import sys
import os
sys.path.append(os.environ.get("PROJECT_ROOT_DIRECTORY", "."))

import shutil

from fileprocessor.searchers import *

class TestFileSearcher(unittest.TestCase):

	def setUp(self):
		# Create both kinds of file searchers
		self.nonRecursiveSearcher = FileSearcher()
		self.recursiveSearcher = FileSearcher(recurse=True)
		# Set up a test directory tree
		self.basePath = os.getcwd() # done for testing results later
		os.mkdir(".test_dir")
		os.mkdir(".test_dir/sub_dir")
		os.mkdir(".test_dir/sub_dir/sub_dir2")
		os.mkdir(".test_dir/sub_dir/sub_dir3")
		with open(".test_dir/one.txt", "w") as f:
			f.write("TEST_FILE")
		with open(".test_dir/two.txt", "w") as f:
			f.write("TEST_FILE")
		with open(".test_dir/sub_dir/three.txt", "w") as f:
			f.write("TEST_FILE")
		with open(".test_dir/sub_dir/sub_dir2/four.txt", "w") as f:
			f.write("HAHA")

	def tearDown(self):
		# Cleanup searchers and test directory tree
		self.nonRecursiveSearcher = None
		self.recursiveSearcher = None
		shutil.rmtree(".test_dir")

	def test_construction(self):
		# Test flags for both searchers were set cotrrectly
		self.assertTrue(self.recursiveSearcher.recurse)
		self.assertFalse(self.nonRecursiveSearcher.recurse)

	def test_search(self):
		NONRECURSIVE_RESULT = [
			os.path.join(self.basePath, ".test_dir", "one.txt"),
			os.path.join(self.basePath, ".test_dir", "two.txt")
		]
		RECURSIVE_RESULT = [
			os.path.join(self.basePath, ".test_dir", "one.txt"),
			os.path.join(self.basePath, ".test_dir", "two.txt"),
			os.path.join(self.basePath, ".test_dir", "sub_dir", "three.txt"),
			os.path.join(self.basePath, ".test_dir", "sub_dir", "sub_dir2", "four.txt")
		]

		# Test invalid type for argument
		with self.assertRaises(TypeError):
			self.nonRecursiveSearcher.search(46435)
		# Test non-existent directory
		with self.assertRaises(IOError):
			self.nonRecursiveSearcher.search("04378485678576875876857738")
		# Test valid directory with a NON-RECURSIVE search
		self.assertEqual(self.nonRecursiveSearcher.search(".test_dir"), NONRECURSIVE_RESULT)
		# Test valid directory with a RECURSIVE search
		self.assertEqual(self.recursiveSearcher.search(".test_dir"), RECURSIVE_RESULT)