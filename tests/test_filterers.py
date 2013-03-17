import unittest
import sys
import os
sys.path.append(os.environ.get("PROJECT_ROOT_DIRECTORY", "."))

from fileprocessor.filterers import *

class TestExcludeListFilterer(unittest.TestCase):

	def setUp(self):
		self.originalFileListing = [
			# Stuff that should be filtered
			"/exact_filename_path.txt",
			"/root/hello/something.txt", "/root/hello/other.txt",
			"test_fileprocessor.py",
			"/root/hello.txt",
			# Stuff that should be allowed
			"/root/test_something.py", 
			"/root/byebye.txt~",
			"/root/stuff/five.cpp",
			"/root/toto/test.db"
		]
		self.excludeList = [
			"/exact_filename_path.txt", # exact path
			"/root/hello/*", # wildcard at end
			"test_*.py", # wildcard in middle
			"*.txt", # wildcard at the beginning
		]
		self.emptyListFilterer = ExcludeListFilterer([])
		self.listFilterer = ExcludeListFilterer(self.excludeList)

	def tearDown(self):
		self.originalFileListing = None
		self.excludeList = None
		self.emptyListFilterer = None
		self.listFilterer = None

	def test_construction(self):
		# Test invalid type
		with self.assertRaises(TypeError):
			ExcludeListFilterer(4543)
		# Test properties were assigned correctly
		self.assertEqual(self.emptyListFilterer.excludeList, [])
		self.assertEqual(self.listFilterer.excludeList, self.excludeList)

	def test_filter(self):
		FILTERED_LISTING = [ 
			"/root/test_something.py",  "/root/byebye.txt~",
			"/root/stuff/five.cpp", "/root/toto/test.db"
		]

		# Test with invalid type
		with self.assertRaises(TypeError):
			self.emptyListFilterer.filter(543)
		# Test different filterers
		self.assertEqual(self.emptyListFilterer.filter(self.originalFileListing),
			self.originalFileListing)
		self.assertEqual(self.listFilterer.filter(self.originalFileListing),
			FILTERED_LISTING)

class TestIncludeListFilterer(unittest.TestCase):

	def setUp(self):
		self.originalFileListing = [
			# Stuff that should be allowed
			"/exact_filename_path.txt",
			"/root/hello/something.txt", "/root/hello/other.txt",
			"test_fileprocessor.py",
			"/root/hello.txt",
			# Stuff that should be filtered
			"/root/test_something.py", 
			"/root/byebye.txt~",
			"/root/stuff/five.cpp",
			"/root/toto/test.db"
		]
		self.includeList = [
			"/exact_filename_path.txt", # exact path
			"/root/hello/*", # wildcard at end
			"test_*.py", # wildcard in middle
			"*.txt", # wildcard at the beginning
		]
		self.emptyListFilterer = IncludeListFilterer([])
		self.listFilterer = IncludeListFilterer(self.includeList)

	def tearDown(self):
		self.originalFileListing = None
		self.includeList = None
		self.emptyListFilterer = None
		self.listFilterer = None

	def test_construction(self):
		# Test invalid type
		with self.assertRaises(TypeError):
			IncludeListFilterer(4543)
		# Test properties were assigned correctly
		self.assertEqual(self.emptyListFilterer.includeList, [])
		self.assertEqual(self.listFilterer.includeList, self.includeList)

	def test_filter(self):
		FILTERED_LISTING = [ 
			"/exact_filename_path.txt",
			"/root/hello/something.txt", "/root/hello/other.txt",
			"test_fileprocessor.py",
			"/root/hello.txt"
		]

		# Test with invalid type
		with self.assertRaises(TypeError):
			self.emptyListFilterer.filter(543)
		# Test different filterers
		self.assertEqual(self.emptyListFilterer.filter(self.originalFileListing), [])
		self.assertEqual(self.listFilterer.filter(self.originalFileListing), FILTERED_LISTING)

class TestExtensionFilterer(unittest.TestCase):

	def setUp(self):
		self.originalFileListing = [
			# Stuff that shouldn't be allowed
			"hello.txt~", "stuff.bin", "binary file",
			"Huh?", "C:/something.win32", "/var/lib/python3.3",
			".hgignore",
			# Stuff that should be allowed
			"test_something.py", "haha.py.py",
			"/var/lib/python/LICENSE.txt"
			".txt", "final.txt"
		]
		self.emptyExtensionFilterer = ExtensionFilterer([])
		self.extensionFilterer = ExtensionFilterer(["py", "txt"])

	def tearDown(self):
		self.originalFileListing = None
		self.emptyExtensionFilterer = None
		self.extensionFilterer = None

	def test_construction(self):
		# Test invalid type for extension
		with self.assertRaises(TypeError):
			ExtensionFilterer(44)
		# Test stub filterers was constructed correctly
		self.assertEqual(self.emptyExtensionFilterer.allowedExtensions, [])
		self.assertEqual(self.extensionFilterer.allowedExtensions, ["py", "txt"])

	def test_filter(self):
		FILTERED_LISTING = [ 
			"test_something.py", "haha.py.py",
			"/var/lib/python/LICENSE.txt"
			".txt", "final.txt"
		]
		# Test having no extensions allowed
		self.assertEqual(self.emptyExtensionFilterer.filter(self.originalFileListing), [])
		# Test having some extensions allowed
		self.assertEqual(self.extensionFilterer.filter(self.originalFileListing), FILTERED_LISTING)