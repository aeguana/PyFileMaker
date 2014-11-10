-------------------------------------------------------------------------------
PyFileMaker - Integrating FileMaker and Python 
(c) 2006-2008 Klokan Petr Pridal, klokan@klokan.cz 
(c) 2002-2006 Pieter Claerhout, pieter@yellowduck.be
 
http://code.google.com/p/pyfilemaker/
http://www.yellowduck.be/filemaker/
-------------------------------------------------------------------------------


TABLE OF CONTENTS

1. What is PyFileMaker?
2. Requirements
3. How to install PyFileMaker
4. How to set up your database
5. Where can I find more info
6. Changes


1. WHAT IS PYFILEMAKER?

PyFileMaker is a set of Python modules that makes it easy to access and modify
data stored in a FileMaker Pro/Server database. You can use it to query a FileMaker
database, but you can also use it to add data to a FileMaker database, you
can even use it to delete records and execute FileMaker scripts.

2. REQUIREMENTS

In order to use PyFileMaker, you will need to have the following software
installed on your computer:

PyFileMaker 1.2, 2.0:
- Python version 2.0 or higher
- The xml.parsers.expat Python module to parse XML data
- FileMaker Pro 6 with the WebCampanion and XML enabled 

This module was tested on Windows NT4, Windows 2000 and Windows XP. We also
tested the module on MacOS 9 and MacOS X version 10.1.5 and version 10.2.

Linux and Unix type of operating systems should work without any problems.

PyFileMaker:
- Python version 2.4 (includes expat by default) or higher
- FileMaker Server Advanced 7, 8 or 8.5 with XML sharing enabled

This module was developed and tested on Linux, should work elsewhere too.

3. HOW TO INSTALL PYFILEMAKER

There is nothing special to configure on PyFileMaker. Just make sure the
PyFileMaker directory, which contains the file FMPro.py/FMServer.py file is
somewhere in your Python path so that Python knows where to find the module.


4. HOW TO SET UP YOUR DATABASE

Since the PyFileMaker module relies on the FileMaker Pro Web Companion, you need
to have it turned on before you can use it. I normally configure it as follows:

   1. Open your database in FileMaker Pro
   2. Go to File -> Sharing and make sure Web Companion is selected
   3. Click on OK

You also might want to check the settings of the Web Companion plugin so that
you know the connection parameters. I always use the standard port 591.


5. WHERE CAN I FIND MORE INFO?

About Python: http://www.python.org
About FileMaker Pro: http://www.filemaker.com
About PyFileMaker 1.2: http://www.yellowduck.be/filemaker/
About PyFileMaker 2.0: http://www.yellowduck.be/filemaker/
About PyFileMaker: http://code.google.com/p/pyfilemaker/

6. CHANGES

Version 2.5 (based on 1.2a2, some features are not merged yet)
- Rewritten for FileMaker Server 7, 8 and 8.5 Advanced
- Support for interactivity using ipython
- Better data handling - Object Model which tracks changes itself, is useful for
  template engines (inspired by SQLAlchemy) 
- TODO: FileMaker Layouts, merge 1.2a2 -> 2.0 changes to this tree)

Version 2.0
- Changed the API funcion names to be more generic
- Added the script function that automatically executes a script
- The imageSave function can now automatically add the extension based on the
  image type of the image data which is being saved.

Version 1.2a3
- The clearDBParams and clearSortParams functions are now working
- When using the doImg function, it now resets the database parameters and
  the sort parameters before returning the result.

Version 1.2a2
- Now preserves newlines in field values

Version 1.2a1
- Add support for basic http authentication and password protected databases.
  The function setPassword can be used for this purpose.
- Fixed a bug where findall would only return 25 records.

Version 1.1
- Improved support for Macintosh OS X
- Now supports images
- Speed improvements thanks to switching from urllib to httplib

