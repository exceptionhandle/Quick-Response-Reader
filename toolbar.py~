# Copyright (C) 2006, Red Hat, Inc.
#Author: Keshav Sharma <keshav7890@gmail.com> & Vaibhav Sharma
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
from gettext import gettext as _
import re

import pango
import gobject
import gtk
import evince

try:
    import epubadapter
except:
    pass

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.toggletoolbutton import ToggleToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.graphics import iconentry
from sugar.activity import activity
from sugar.graphics.icon import Icon
from sugar.graphics.xocolor import XoColor
class waterToolbar(gtk.Toolbar):
    __gtype_name__ = 'waterToolbar'

    __gsignals__ = {        'watermark_tl': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'watermark_tile': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'watermark_scale': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'left_top': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'right_top': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'left_bottom': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'right_bottom': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([]))
                      }

    def __init__(self):
        gtk.Toolbar.__init__(self)
            
            
        self.left_top = ToolButton('left_top')
        self.left_top.set_tooltip(_('left_top'))
        self.left_top.connect('clicked', self.left_top_cb)
        self.insert(self.left_top, -1)
        self.left_top.show()

        self.right_top = ToolButton('right_top')
        self.right_top.set_tooltip(_('right_top'))
        self.right_top.connect('clicked', self.right_top_cb)
        self.insert(self.right_top, -1)
        self.right_top.show()
            
        self.left_bottom = ToolButton('left_bottom')
        self.left_bottom.set_tooltip(_('left_bottom'))
        self.left_bottom.connect('clicked', self.left_bottom_cb)
        self.insert(self.left_bottom, -1)
        self.left_bottom.show()
            
        self.right_bottom = ToolButton('right_bottom')
        self.right_bottom.set_tooltip(_('right_bottom'))
        self.right_bottom.connect('clicked', self.right_bottom_cb)
        self.insert(self.right_bottom, -1)
        self.right_bottom.show()
            
        self.watermark_tl = ToolButton('watermark_tl')
        self.watermark_tl.set_tooltip(_('mark image top left'))
        self.watermark_tl.connect('clicked', self.watermark_tl_cb)
        self.insert(self.watermark_tl, -1)
        self.watermark_tl.show()
            
        self.watermark_til = ToolButton('watermark_tile')
        self.watermark_til.set_tooltip(_('mark image tile form'))
        self.watermark_til.connect('clicked', self.watermark_tile_cb)
        self.insert(self.watermark_til, -1)
        self.watermark_til.show()
            
        self.watermark_scale = ToolButton('watermark_scale')
        self.watermark_scale.set_tooltip(_('mark scale form'))
        self.watermark_scale.connect('clicked', self.watermark_scale_cb)
        self.insert(self.watermark_scale, -1)
        self.watermark_scale.show()
           
    def watermark_tl_cb(self, button):
        self.emit('watermark_tl')
    def watermark_tile_cb(self, button):
        self.emit('watermark_tile')
    def watermark_scale_cb(self, button):
        self.emit('watermark_scale')
    def ambross_cb(self, button):
        self.emit('ambross')
    def left_top_cb(self, button):
        self.emit('left_top')
    def right_top_cb(self, button):
        self.emit('right_top')
    def left_bottom_cb(self, button):
        self.emit('left_bottom')
    def right_bottom_cb(self, button):
        self.emit('right_bottom')
    def sharpen_cb(self, button):
        self.emit('sharpen')

    
class ViewToolbar(gtk.Toolbar):
    __gtype_name__ = 'ViewToolbar'

    __gsignals__ = {
        'zoom_in': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'zoom_out': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'zoom_to_fit': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'zoom_original': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'rotate_clockwise': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'rotate_anticlockwise': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'undo': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'redo': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'save': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,
                              ([])),
        'paste': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,

                              ([])),
        'original': (gobject.SIGNAL_RUN_FIRST,
                              gobject.TYPE_NONE,

                              ([])),
    }

    def __init__(self):
        gtk.Toolbar.__init__(self)

        self._zoom_out_button = None
        self._zoom_in_button = None

        self._zoom_out_button = ToolButton('zoom-out')
        self._zoom_out_button.set_tooltip(_('Zoom out'))
        self._zoom_out_button.connect('clicked', self.zoom_out_cb)
        self.insert(self._zoom_out_button, -1)
        self._zoom_out_button.show()

        self._zoom_in_button = ToolButton('zoom-in')
        self._zoom_in_button.set_tooltip(_('Zoom in'))
        self._zoom_in_button.connect('clicked', self.zoom_in_cb)
        self.insert(self._zoom_in_button, -1)
        self._zoom_in_button.show()
 
        zoom_tofit_button = ToolButton('zoom-best-fit')
        zoom_tofit_button.set_tooltip(_('Fit to window'))
        zoom_tofit_button.connect('clicked', self.zoom_to_fit_cb)
        self.insert(zoom_tofit_button, -1)
        zoom_tofit_button.show()

        zoom_original_button = ToolButton('zoom-original')
        zoom_original_button.set_tooltip(_('Original size'))
        zoom_original_button.connect('clicked', self.zoom_original_cb)
        self.insert(zoom_original_button, -1)
        zoom_original_button.show()

        spacer = gtk.SeparatorToolItem()
        spacer.props.draw = False
        self.insert(spacer, -1)
        spacer.show()

        rotate_anticlockwise_button = ToolButton('rotate_anticlockwise')
        rotate_anticlockwise_button.set_tooltip(_('Rotate anticlockwise'))
        rotate_anticlockwise_button.connect('clicked',
                self.rotate_anticlockwise_cb)
        self.insert(rotate_anticlockwise_button, -1)
        rotate_anticlockwise_button.show()

        rotate_clockwise_button = ToolButton('rotate_clockwise')
        rotate_clockwise_button.set_tooltip(_('Rotate clockwise'))
        rotate_clockwise_button.connect('clicked', self.rotate_clockwise_cb)
        self.insert(rotate_clockwise_button, -1)
        rotate_clockwise_button.show()

        self.undo_button = ToolButton('undo')
        self.undo_button.set_tooltip(_('undo'))
        self.undo_button.connect('clicked', self.undo_cb)
        self.insert(self.undo_button, -1)
        self.undo_button.show()

        self.redo_button = ToolButton('redo')
        self.redo_button.set_tooltip(_('redo'))
        self.redo_button.connect('clicked', self.redo_cb)
        self.insert(self.redo_button, -1)
        self.redo_button.show()


        self.save_button = ToolButton('copy')
        self.save_button.set_tooltip(_('save image'))
        self.save_button.connect('clicked', self.save_cb)
        self.insert(self.save_button, -1)
        self.save_button.show()


        self.paste_button = ToolButton('paste')
        self.paste_button.set_tooltip(_('paste back saved'))
        self.paste_button.connect('clicked', self.paste_cb)
        self.insert(self.paste_button, -1)
        self.paste_button.show()
        
        self.original_button = ToolButton('original')
        self.original_button.set_tooltip(_('original pic'))
        self.original_button.connect('clicked', self.original_cb)
        self.insert(self.original_button, -1)
        self.original_button.show()

    def original_cb(self, button):
        self.emit('original')

    def zoom_in_cb(self, button):
        self.emit('zoom_in')
    
    def zoom_out_cb(self, button):
        self.emit('zoom_out')

    def zoom_to_fit_cb(self, button):
        self.emit('zoom_to_fit')
    def zoom_original_cb(self, button):
        self.emit('zoom_original')
    def rotate_clockwise_cb(self, button):
        self.emit('rotate_clockwise')
    def rotate_anticlockwise_cb(self, button):
        self.emit('rotate_anticlockwise')
    def undo_cb(self, button):
        self.emit('undo')
    def redo_cb(self, button):
        self.emit('redo')
    def save_cb(self, button):
        self.emit('save')
    def paste_cb(self, button):
        self.emit('paste')
   
    def set_activity(self, activity):
        self.activity = activity

class EditToolbar(gtk.Toolbar):
    __gtype_name__ = 'EditToolbar'

    __gsignals__ = {
        'grey': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),
        'blur': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),
        'transpose': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),
        'offset': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),
        'ambross': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'contour': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),
        'text': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),
        'finedges': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'solarize': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'invert': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'sharpen': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'contrast': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'bright': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'dcontrast': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([])),        
        'dbright': (gobject.SIGNAL_RUN_FIRST,
                          gobject.TYPE_NONE,
                          ([]))        

    }

    def __init__(self):
        gtk.Toolbar.__init__(self)
            
        self.grey = ToolButton('grey')
        self.grey.set_tooltip(_('grey'))
        self.grey.connect('clicked', self.grey_cb)
        self.insert(self.grey, -1)
        self.grey.show()
            
        self.blur = ToolButton('blur')
        self.blur.set_tooltip(_('blur'))
        self.blur.connect('clicked', self.blur_cb)
        self.insert(self.blur, -1)
        self.blur.show()
            
        self.transpose = ToolButton('mirror')
        self.transpose.set_tooltip(_('mirror'))
        self.transpose.connect('clicked', self.transpose_cb)
        self.insert(self.transpose, -1)
        self.transpose.show()
            
        self.offset = ToolButton('offset')
        self.offset.set_tooltip(_('Divide n transpose'))
        self.offset.connect('clicked', self.offset_cb)
        self.insert(self.offset, -1)
        self.offset.show()
            
        self.contour = ToolButton('contour')
        self.contour.set_tooltip(_('contour'))
        self.contour.connect('clicked', self.contour_cb)
        self.insert(self.contour, -1)
        self.contour.show()
            
        self.finedges = ToolButton('finedges')
        self.finedges.set_tooltip(_('findedges'))
        self.finedges.connect('clicked', self.finedges_cb)
        self.insert(self.finedges, -1)
        self.finedges.show()
      
        self.solarize = ToolButton('solarize')
        self.solarize.set_tooltip(_('solarize'))
        self.solarize.connect('clicked', self.solarize_cb)
        self.insert(self.solarize, -1)
        self.solarize.show()
            
        self.invert = ToolButton('invert')
        self.invert.set_tooltip(_('invert'))
        self.invert.connect('clicked', self.invert_cb)
        self.insert(self.invert, -1)
        self.invert.show()
    
        self.ambross = ToolButton('embross')
        self.ambross.set_tooltip(_('emboss'))
        self.ambross.connect('clicked', self.ambross_cb)
        self.insert(self.ambross, -1)
        self.ambross.show()
            
        self.sharpen = ToolButton('sharpen')
        self.sharpen.set_tooltip(_('sharpen'))
        self.sharpen.connect('clicked', self.sharpen_cb)
        self.insert(self.sharpen, -1)
        self.sharpen.show()
            
        self.contrast = ToolButton('contrast')
        self.contrast.set_tooltip(_('increase contrast'))
        self.contrast.connect('clicked', self.contrast_cb)
        self.insert(self.contrast, -1)
        self.contrast.show()
            
        self.dcontrast = ToolButton('dcontrast')
        self.dcontrast.set_tooltip(_('decrease contrast'))
        self.dcontrast.connect('clicked', self.dcontrast_cb)
        self.insert(self.dcontrast, -1)
        self.dcontrast.show()
            
        self.bright = ToolButton('bright')
        self.bright.set_tooltip(_('increase brightness'))
        self.bright.connect('clicked', self.bright_cb)
        self.insert(self.bright, -1)
        self.bright.show()
            
        self.dbright = ToolButton('dbright')
        self.dbright.set_tooltip(_('decrease brightness'))
        self.dbright.connect('clicked', self.dbright_cb)
        self.insert(self.dbright, -1)
        self.dbright.show()
           

    def grey_cb(self, button):
        self.emit('grey')
    def blur_cb(self, button):
        self.emit('blur')
    def transpose_cb(self, button):
        self.emit('transpose')
    def offset_cb(self, button):
        self.emit('offset')
    def contour_cb(self, button):
        self.emit('contour')
    def finedges_cb(self, button):
        self.emit('finedges')
    def solarize_cb(self, button):
        self.emit('solarize')
    def invert_cb(self, button):
        self.emit('invert')
    def watermark_tl_cb(self, button):
        self.emit('watermark_tl')
    def watermark_tile_cb(self, button):
        self.emit('watermark_tile')
    def watermark_scale_cb(self, button):
        self.emit('watermark_scale')
    def ambross_cb(self, button):
        self.emit('ambross')
    def left_top_cb(self, button):
        self.emit('left_top')
    def right_top_cb(self, button):
        self.emit('right_top')
    def left_bottom_cb(self, button):
        self.emit('left_bottom')
    def right_bottom_cb(self, button):
        self.emit('right_bottom')
    def sharpen_cb(self, button):
        self.emit('sharpen')
    def contrast_cb(self, button):
        self.emit('contrast')
    def bright_cb(self, button):
        self.emit('bright')
    def dcontrast_cb(self, button):
        self.emit('dcontrast')
    def dbright_cb(self, button):
        self.emit('dbright')

    
