# -*- coding: utf-8 -*-

import sys, os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, '../../../src'))

import django_attendance
version = django_attendance.VERSION
release = django_attendance.RELEASE
project = django_attendance.PROJECT
copyright = django_attendance.COPYRIGHT
author = django_attendance.AUTHOR


# Source
master_doc = 'index'
templates_path = ['_templates']
source_suffix = '.rst'
exclude_trees = []
pygments_style = 'sphinx'

# html build settings
html_theme = 'default'
html_static_path = ['_static']

# htmlhelp settings
htmlhelp_basename = '%sdoc' %project

# latex build settings
latex_documents = [
    ('index', '%s.tex' % project, u'%s Documentation' % project,
    author, 'manual'),
]
