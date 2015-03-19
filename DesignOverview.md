# Design Overview #

fileprocessor aims to streamline the task of generating or extracting data from a large collection of files by providing a standard harness which can easily be extended to meet the user's specific requirements.

This is achieved by separating each step of this process into distinct components that has a defined place within the chain of actions. Below is a diagram which shows the harness' components and where they fit in the data extraction process.
![http://wiki.fileprocessor.googlecode.com/hg/fileprocessor_design.png](http://wiki.fileprocessor.googlecode.com/hg/fileprocessor_design.png)
Note that `source` is a generic term which refers to a location which contains. For most use cases, `source` means directories and `resource` means files. However, this may not always be the case. For example, `source` could be a URL and `resource` could be data found within that URL.

### Process ###
  1. User inputs list of sources
  1. `Searcher` component constructs a list of resources contained within the sources
  1. Found sources are filtered by zero or more `Filterer` components, resulting in a list only containing resources the user wishes to process
  1. Each resource is ran through an `Extractor`, which reads the resource data, extracts/processes the data and then returns some output for each resource
  1. The names and extracted/processed data of each resource is then returned to the user

### Summary of Components ###
  * **FileProcessor** -- high-level interface which starts the data extraction process. The sources to search for resources in is given to this.
  * **Searcher** -- components which search for resources within the given sources
  * **Filterer** -- components which remove some resources from the extraction process, based on some criteria
  * **Extractor** -- component which actually reads, extracts and processes a resource to produce some kind of output to give back to the user

### Examples ###
For concrete examples on how this design is used to process directories of files, see the ImageLinkExtraction and ChecksumGenerator examples.