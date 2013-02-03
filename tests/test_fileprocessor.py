import unittest
import sys
import os
sys.path.append(os.environ.get("PROJECT_ROOT_DIRECTORY", "."))

from fileprocessor import FileProcessor

class MockFileSearcher:

	def __init__(self):
		self.fileLists = {
			"root_dir" : [ "/path/to/stuff.txt", "/another_path/test.txt", "/programs/ls.bin" ],
			"empty_dir" : []
		}

	def search(rootDirectory):
		return self.fileList

class MockFilterer:

	def filter(fileList):
		# Just remove a single FIXED file for the test
		try:
			fileList.remove("/programs/ls.bin")
		except:
			pass
		return fileList

class MockDataExtractor:

	def extract(filePath):
		return self.filePath + ": PROCESSED"

class TestFileProcessor(unittest.TestCase):

	def setUp(self):
		self.mockSearcher = MockFileSearcher()
		self.mockFilterer = MockFilterer()
		self.mockExtractor = MockDataExtractor()
		self.fileProcessor = FileProcessor(self.mockSearcher,
			self.mockFilterer, self.mockExtractor)
		# Create empty directories just so the file processor
		# doesn't comaplin when we test process()
		os.mkdir("empty_dir")
		os.mkdir("root_dir")

	def tearDown(self):
		self.mockSearcher = None
		self.mockFilterer = None
		self.mockExtractor = None
		self.fileProcessor = None
		# Delete created directories
		os.rmdir("empty_dir")
		os.rmdir("root_dir")

	def test_constructor(self):
		# Test valid arguments (use constructed object in setUp())
		self.assertEqual(self.fileProcessor.searcher, self.mockSearcher)
		self.assertEqual(self.fileProcessor.searcher, self.mockSearcher)
		self.assertEqual(self.fileProcessor.searcher, self.mockSearcher)

	def test_process_failure(self):
		# Invalid directory (type)
		with self.assertRaises(TypeError):
			self.fileProcessor.process(5454)
		# Invalid directory (doesn't exist)
		with self.assertRaises(IOError):
			self.fileProcessor.process("non-existent")

	def test_process_success(self):
		EXPECTED_DATA = {
			"/path/to/stuff.txt" : "/path/to/stuff.txt: PROCESSED",
			"/another_path/test.txt" : "/another_path/test.txt: PROCESSED"
		}

		# Test with no files
		self.assertEqual(self.fileProcessor.process("empty_dir"), {})
		# Test with files
		self.assertEqual(self.fileProcessor.process("root_dir"), EXPECTED_DATA)
