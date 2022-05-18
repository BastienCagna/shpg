
import sphinx_bootstrap_theme

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

project = 'Static HTML Page Generator'
copyright = '2022, Bastien Cagna, Neurospin, CEA'
author = 'Bastien Cagna'

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'numpydoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    # 'nbsphinx',
    'sphinx_gallery.gen_gallery',
    # 'sphinxcontrib.fulltoc'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

release = "0.0.1"
# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_theme_options = {
    'navbar_title': 'Static HTML Page Generator',
    'bootswatch_theme': "flatly",
    'navbar_sidebarrel': False,
    'bootstrap_version': "3",
    # 'logo_only': False,
    # 'prev_next_buttons_location': 'bottom',
    # 'style_external_links': False,
    # 'vcs_pageview_mode': '',
    # 'style_nav_header_background': 'white',
    # # Toc options
    # 'collapse_navigation': True,
    # 'sticky_navigation': True,
    # 'includehidden': True,
    # 'titles_only': False
    'navbar_links': [
        ("Gallery", "auto_examples/index"),
        # ("API", "api"),
        # ("Tutorial", "tutorial"),
        # ("Installation", "install"),
        ("Github", "https://github.com/BastienCagna/shpg", True),
    ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# html_sidebars = {'**': ['localtoc.html', 'searchbox.html'],
#    'using/windows': ['windowssidebar.html', 'searchbox.html']}

# https://sphinx-gallery.github.io/stable/getting_started.html
sphinx_gallery_conf = {
     'examples_dirs': '../examples',   # path to your example scripts
     'gallery_dirs': 'auto_examples',  # path to where to save gallery generated output
}

