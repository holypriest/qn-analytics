# qn-analytics

The main goal of this project is to be a set of tools to extract data from SciELO analytics for Química Nova Journal (several parts can be adapted to other SciELO journals, though, considering they use the same structure for a great number of their journals).

*dump.py*

This file contains a script to extract all QN access data from SciELO Analytics, using requests. Raw data in JSON format is saved using separate files for every article. These files are used later to compose a structured source of data.

*article.py*

This class implements the 'Article' objects, that will contain the data extracted from the files dumped above in a structured manner, together with some methods to aid further statistics on accesses.

*tools.py*

This is a simple script to get the title and the authors' names for an article, given its SciELO code.

*hotpapers.py*

This is a script that uses Article objects to get a list of the most accessed articles in a given time range, with their access counts.

This is an ongoing project. This code is just a draft to satisfy an urgency and will be improved. More features will be added in the future.
