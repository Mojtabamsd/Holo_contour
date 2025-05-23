import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'holocontour'
author = 'Mojtaba Masoudi'
copyright = '2025, Mojtaba Masoudi'
release = '0.1.1'

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

# Enable parsing of Markdown
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

# HTML output options
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
