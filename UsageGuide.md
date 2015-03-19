# Usage Guide #

### Running the Processor ###
The high-level class `FileProcessor` is used to start the file processing. This class has a single method `process()` which takes a list of `sources`, which is a list of strings whose contents represent the names of the `sources`. `process()` returns a dictionary, where the **keys** are the names of any processed `resources` and the **values** are the corresponding data extracted/processed from the content of the `resource`.

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

The abstract classes in `fileprocessor.abstracts}} must be used to define {{{Searchers`, `Filterers` and  `Extractors`. These classes are `fileprocessor.abstracts.Searcher`, `fileprocessor.abstracts.Filterer` and `fileprocessor.abstracts.Extractor` respectively.

### Defining a Searcher ###

`fileprocessor.abstracts.Searcher` has a single abstract method which must be overriden by subclasses called `search()`. This takes a string containing the name of a `source` and returns a list of `resources` found inside that source.

There are two built-in `Searchers`:
  * **`fileprocessor.searchers.FileSearcher`** -- Searches directories on a filesystem, treating files as `resources`
  * **`fileprocessor.searchers.CompositeSearcher`** -- Uses multiple searchers on the same {{{source}} and returns a combined list of resources

### Defining a Filterer ###

`fileprocessor.abstracts.Filterer` has a single abstract method which must be overriden by subclasses called `filter()`. This takes a list of `resource` names and returns a filtered list of those `resources`.

There are three built-in `Filterers`:
  * **`fileprocessor.filterers.ExclusionListFilterer`** -- Uses [glob](http://en.wikipedia.org/wiki/Glob_%28programming%29) patterns to **exclude** `resources`. If a `resource` name matches one of the patterns specified, it is removed from the list.
  * **`fileprocessor.filterers.InclusionListFilterer`** -- Uses [glob](http://en.wikipedia.org/wiki/Glob_%28programming%29) patterns to **select** `resources`. If a `resource` name **does not match** one of the patterns specified, it is removed from the list.
  * **`fileprocessor.filterers.ExtensionFilterer`** -- Filters`resources` whose names do not end with one of the specified extensions

### Defining an Extractor ###

`fileprocessor.abstracts.Extractor` has a single abstract method which must be overriden by subclasses called `extract()`. This takes the **name** of a single `resource` and returns the data extracted from the resource.

There are four built-in `Extractors`:
  * **`fileprocessor.extractors.ByteExtractor`** -- Treats `resources` as binary files. This loads the entire binary file into memory before processing it.
  * **`fileprocessor.extractors.ByteStreamExtractor`** -- Treats `resources` as binary files. This opens the binary file as a stream, so the entire file is not loaded into memory at once. Good if you're processing very large files.
  * **`fileprocessor.extractors.TextExtractor`** -- Treats `resources` as textfiles. This loads the entire text file into memory before processing it.
  * **`fileprocessor.extractors.TextStreamExtractor`** -- Treats `resources` as textfiles. This opens the text file as a stream, so the entire file is not loaded into memory at once. Good if you're processing very large files.

### Putting It All Together ###

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

For further examples, see ChecksumGenerator and ImageLinkExtraction.