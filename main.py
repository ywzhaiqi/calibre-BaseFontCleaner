#!/usr/bin/env python2
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)


import re
from PyQt5.Qt import QAction, QInputDialog
from cssutils.css import CSSRule

# The base class that all tools must inherit from
from calibre.gui2.tweak_book.plugin import Tool

from calibre import force_unicode
from calibre.gui2 import error_dialog
from calibre.ebooks.oeb.polish.container import OEB_DOCS, OEB_STYLES, serialize

class DemoTool(Tool):

    #: Set this to a unique name it will be used as a key
    name = 'base-font-cleaner'

    #: If True the user can choose to place this tool in the plugins toolbar
    allowed_in_toolbar = True

    #: If True the user can choose to place this tool in the plugins menu
    allowed_in_menu = True

    isChanged = False

    def create_action(self, for_toolbar=True):
        # Create an action, this will be added to the plugins toolbar and
        # the plugins menu
        #ac = QAction(get_icons('images/icon.png'), 'Clean Base fonts', self.gui)  # noqa
        ac = QAction(get_icons('images/icon.png'), '移除基础字体', self.gui)  # noqa
        if not for_toolbar:
            # Register a keyboard shortcut for this toolbar action. We only
            # register it for the action created for the menu, not the toolbar,
            # to avoid a double trigger
            self.register_shortcut(ac, 'clean-base-fonts', default_keys=('Ctrl+Shift+Alt+F',))
        ac.triggered.connect(self.ask_user)
        return ac

    def ask_user(self):
        # Ensure any in progress editing the user is doing is present in the container
        self.boss.commit_all_editors_to_container()
        try:
            self.clean_base_fonts()
        except Exception:
            # Something bad happened report the error to the user
            import traceback
            error_dialog(self.gui, _('Failed to clean base fonts'), _(
                'Failed to clean base fonts, click "Show details" for more info'),
                det_msg=traceback.format_exc(), show=True)
            # Revert to the saved restore point
            self.boss.revert_requested(self.boss.global_undo.previous_container)
        else:
            if self.isChanged:
                # Show the user what changes we have made, allowing her to revert them if necessary
                self.boss.show_current_diff()
                # Update the editor UI to take into account all the changes we have made
                self.boss.apply_container_update_to_gui()

    def clean_base_fonts(self):
        # Magnify all font sizes defined in the book by the specified factor
        # First we create a restore point so that the user can undo all changes
        # we make.
        self.boss.add_savepoint('Before: Clean base fonts')

        container = self.current_container  # The book being edited as a container object

        # Iterate over all style declarations in the book, this means css
        # stylesheets, <style> tags and style="" attributes
        for name, media_type in container.mime_map.iteritems():
            if media_type in OEB_STYLES:
                # A stylesheet. Parsed stylesheets are cssutils CSSStylesheet
                # objects.
                self.magnify_stylesheet(container.parsed(name))
                if self.isChanged:
                    container.dirty(name)  # Tell the container that we have changed the stylesheet

    def magnify_stylesheet(self, sheet):
        # Magnify all fonts in the specified stylesheet by the specified
        for rule in sheet.cssRules.rulesOfType(CSSRule.STYLE_RULE):
            self.magnify_declaration(rule)

        # 另一种方法
        # sheet.cssText

    def magnify_declaration(self, rule):
        style = rule.style
        if rule.selectorText in ['body', 'div', 'p']:
            val = style.getPropertyValue('font-family')
            if val == u'"zw", "宋体", "明体", "明朝", serif':
                style.setProperty('font-family', '')
                self.isChanged = True

    def magnify_csstext(self, cssText):
        pass