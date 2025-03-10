import os
import sys
import time
from unittest.mock import MagicMock
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ME-405 Term Project'
copyright = '2025, Andrew Carr, Alain Kanadjian'
author = 'Andrew Carr, Alain Kanadjian'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon", # If using Google-style or NumPy-style docstrings
    "myst_parser",
]
if 'sphinx' in sys.modules:  # Check if the code is being run by Sphinx
    time.ticks_us = MagicMock(return_value=12345678)
    time.ticks_diff = MagicMock(return_value=12345678)
    time.ticks_add = MagicMock(return_value=12345678)
    time.ticks_ms = MagicMock(return_value=12345678)
autodoc_mock_imports = ['pyb','micropython','utime', 'time.ticks_us']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


sys.path.insert(0, os.path.abspath("../code"))  # Adjust path to 'code' folder

# if 'sphinx' in sys.modules:
#     sys.modules['pyb'] = MagicMock()
#     pyb = sys.modules['pyb']
#     pyb.Pin = MagicMock()
#     pyb.I2C = MagicMock()
