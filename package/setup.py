#    Setup script for ConvertQC
#    Copyright (C) 2019  Harry Adams (convertqc@gmail.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>

from distutils.core import setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='ConvertQC',
    version='0.1dev',
    license='LICENSE.txt',

    author='Harry Adams',
    author_email='convertqc@gmail.com',
    description="Tool for converting between quantum computing toolkits",
    long_description=long_description,

    entry_points={
        'console_scripts': [
            'convertqc = convertqc.convertqc:main',
        ],
    },

    packages=['convertqc'],
    install_requires=['autopep8>=1.4.4', 'qutip>=4.3.1', 'projectq>=0.4.2', 'argcomplete>=1.9.2', ],
)
