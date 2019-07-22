=========
ConvertQC
=========

A Python command-line tool to convert quantum computing scripts between different toolkits (currently only supporting QuTiP and ProjectQ).

Author - Harry Adams

Date - 03/05/19

Email - convertqc@gmail.com

Dependencies
------------

* qutip (Dependencies - http://qutip.org/docs/4.1/installation.html)
* projectq
* autopep8

Installation
------------

* Download the source repository (GitHub link to add once released).
* Navigate to the root directory of the project:  
 
  ``cd convertqc``
* Run ``pip3 install -e .`` to install

Running
-------

* ``convertqc <input_filename> <input_format> <output_format>``

* Formats: projectq, qutip

Examples
--------

* To display the help window

    ``convertqc -h``

* To translate a file (``example.py``) from ProjectQ to QuTiP

    ``convertqc example.py projectq qutip``

* To translate a file (``example.py``) from QuTiP to ProjectQ

    ``convertqc examply.py qutip projectq``
  
* To specify an output filename, use the -f flag (without the file extension)

    ``convertqc example.py -f output_file projectq qutip``
  
* To disable comments in code which identify untranslated lines, use the -m flag

    ``convertqc example.py -m projectq qutip``


File Structure
--------------

* Current directory: Root directory which contains the license, readme, and setup script.

* /convertqc/: Contains the scripts for running ConvertQC. Copied to user directory when installed using above method.

* /stress/: Contains files with large numbers of repetitive lines to be used as part of stress testing

* /test/: Contains test scripts which can be run using the command

    ``python3 -m unittest``

License
-------

This software is shared under the GNU GPL v3.0 License. Please view the LICENSE.txt file to view.