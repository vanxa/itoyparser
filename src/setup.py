from distutils.core import setup
import py2exe
import os


setup(windows=[os.path.join(os.getcwd(),"main\parser.py")])