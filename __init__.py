#!/usr/bin/env python2

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2015'

from calibre.customize import EditBookToolPlugin


class DemoPlugin(EditBookToolPlugin):

    name = 'Remove Base font-family'
    version = (1, 0, 0)
    author = 'ywzhaiqi'
    supported_platforms = ['windows', 'osx', 'linux']
    description = 'Remove Base font-family'
    minimum_calibre_version = (1, 46, 0)
