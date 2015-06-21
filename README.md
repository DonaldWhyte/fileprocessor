# fileprocessor

This very simple Python pacakge provides a framework for batch processing of files. Exactly how the files are processed and what data is extracted from them is up to the developer. fileprocessor just provides a harness that eases the process of getting/setting the data you want from files.

### Install

**NOTE**: fileprocessor only supports Python 3.0.0+. There is *no* Python 2 support!

Clone the repository and execute the setup file:

```
python setup.py install
```

### Design Overview

fileprocessor aims to streamline the task of generating or extracting data from a large collection of files by providing a standard harness which can easily be extended to meet the user's specific requirements.

This is achieved by separating each step of this process into distinct components that has a defined place within the chain of actions. Below is a diagram which shows the harness' components and where they fit in the data extraction process.

![fileprocessor Process Diagram](https://raw.github.com/DonaldWhyte/fileprocessor/master/docs/fileprocessor_design.png)

Note that `source` is a generic term which refers to a location which contains. For most use cases, `source` means directories and `resource` means files. However, this may not always be the case. For example, `source` could be a URL and `resource` could be data found within that URL.

##### Process:

1. User inputs list of sources
2. `Searcher` component constructs a list of resources contained within the sources
3. Found sources are filtered by zero or more `Filterer` components, resulting in a list only containing resources the user wishes to process
4. Each resource is ran through an `Extractor`, which reads the resource data, extracts/processes the data and then returns some output for each resource
5. The names and extracted/processed data of each resource is then returned to the user

##### Component Summary:

* `FileProcessor` -- high-level interface which starts the data extraction process. The sources to search for resources in is given to this.
* `Searcher` -- components which search for resources within the given sources
* `Filterer` -- components which remove some resources from the extraction process, based on some criteria
* `Extractor` -- component which actually reads, extracts and processes a resource to produce some kind of output to give back to the user

### Usage

#### Running the Processor

The high-level class `FileProcessor` is used to start the file processing. This class has a single method `process()` which takes a list of `sources`, which is a list of strings whose contents represent the names of the `sources`. `process()` returns a dictionary, where the *keys* are the names of any processed `resources` and the *values* are the corresponding data extracted/processed from the content of the `resource`.

How exactly `FileProcessor` scans the given `source` names or extracts data from `resources` depends on the components (described in DesignOverview) passed to the `FileProcessor`'s constructor. Below is a basic example of how fileprocessor is used.

```
from fileprocessor import FileProcessor

# Create components to use in processing here
searcher = ???
filterers = ???
extractor = ???
# Construct the actual processor, passing in the individual components
processor = fileprocessor.Processor(searcher, filterers, extractor)
# Define the sources to process, start processing and store the results
sources = [ "source1", "source" ]
processedData = processor.process(sources)
```

Note how the creation of searchers, filterers and extractors has not been defined yet. These three components are classes defined by the user.

The abstract classes in `fileprocessor.abstracts` must be used to define `Searchers`, `Filterers` and  `Extractors`. These classes are `fileprocessor.abstracts.Searcher`, `fileprocessor.abstracts.Filterer` and `fileprocessor.abstracts.Extractor` respectively.

#### Defining a Searcher

`fileprocessor.abstracts.Searcher` has a single abstract method which must be overriden by subclasses called `search()`. This takes a string containing the name of a `source` and returns a list of `resources` found inside that source.

There are two built-in `Searchers`:

* `fileprocessor.searchers.FileSearcher` -- Searches directories on a filesystem, treating files as `resources`
* `fileprocessor.searchers.CompositeSearcher` -- Uses multiple searchers on the same `source}} and returns a combined list of resources

#### Defining a Filterer

`fileprocessor.abstracts.Filterer` has a single abstract method which must be overriden by subclasses called `filter()`. This takes a list of `resource` names and returns a filtered list of those `resources`.

There are three built-in `Filterers`:

* `fileprocessor.filterers.ExclusionListFilterer` -- Uses glob patterns to exclude `resources`. If a `resource` name matches one of the patterns specified, it is removed from the list.
* `fileprocessor.filterers.InclusionListFilterer` -- Uses glob patterns to select `resources`. If a `resource` name *does not match* one of the patterns specified, it is removed from the list.
* `fileprocessor.filterers.ExtensionFilterer` -- Filters `resources` whose names do not end with one of the specified extensions

#### Defining an Extractor

`fileprocessor.abstracts.Extractor` has a single abstract method which must be overriden by subclasses called `extract()`. This takes the *name* of a single `resource` and returns the data extracted from the resource.

There are four built-in `Extractors`:

* `fileprocessor.extractors.ByteExtractor` -- Treats `resources` as binary files. This loads the entire binary file into memory before processing it.
* `fileprocessor.extractors.ByteStreamExtractor` -- Treats `resources` as binary files. This opens the binary file as a stream, so the entire file is not loaded into memory at once. Good if you're processing very large files.
* `fileprocessor.extractors.TextExtractor` -- Treats `resources` as textfiles. This loads the entire text file into memory before processing it.
* `fileprocessor.extractors.TextStreamExtractor` -- Treats `resources` as textfiles. This opens the text file as a stream, so the entire file is not loaded into memory at once. Good if you're processing very large files.

#### Putting It All Together

Suppose we wanted to extract the filesize of each PNG or GIF image file within two directories. First, we need a `Searcher` which recursively searchers through directories. The built-in class `fileprocessor.searchers.FileSearcher` can be used for this.

Then, we need a way of filtering out non PNG/GIF files. A built-in filterer also already exists for this -- `fileprocessor.filterers.ExtensionFilterer`.

Finally, we need to count the number of bytes contained within each file. There does not an exist an extractor for this, so we need to define it ourselves. Reading binary files is functionality already defined by a built-in `Extractor`, so we subclass that (`filesearcher.extractors.ByteFileExtractor`).

```
from fileprocessor import FileProcessor
from fileprocessor.searchers import FileSearcher
from fileprocessor.filterers import ExtensionFilterer
from fileprocessor.extractors import ByteExtractor

class FilesizeExtractor(ByteExtractor): # customer extractor

    def extractFromBytes(self, data):
        return len(data) # number of bytes (filesize!)

# Create components to use in processing here
searcher = FileSearcher(recurse=True) # recursively search directories
extensionFilterer =  ExtensionFilterer( ["png", "gif"] ) # only PNG or GIF 
filterers = [ extensionFilterer ] # we can have more than one filterer
extractor = FilesizeExtractor()

# Construct the actual processor, passing in the individual components
processor = fileprocessor.Processor(searcher, filterers, extractor)
# Define the sources to process, start processing and store the results
sources = [ "." ] # recursively search CURRENT DIRECTORY
processedData = processor.process(sources)
```

After running this script, `processedData` would contain a dicitonary where the keys are the filenames of found PNG/GIF files and the value would be the number of bytes the respective files contain.

### Examples

For concrete examples on how this design is used to process directories of files, check out of the "examples" folder of this repo.

### Tests

Unit tests are provided in the 'tests' directory. To run all the unit tests simply navigate into the 'tests' directory and invoke the following command:

```
python run_test.py -d .. -w .
```

To run a single test file, invoke the following command in the 'tests' directory:

```
python run_test.py -d .. -w . -t "[TEST_NAME]"
```

where `[TEST_NAME]` is the name of the test file without the "test_" prefix or ".py" suffix. For example, if `[TEST_NAME] = filterers`, then the test file "test_filterers.py" will be executed.

### Source Code

Git repository can be accessed here: https://github.com/DonaldWhyte/fileprocessor

### License

fileprocess is licensed under the MIT License. See LICENCE for more information.
