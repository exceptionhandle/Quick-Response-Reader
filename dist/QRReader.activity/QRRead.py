# Copyright (C) 2008, One Laptop per Child
# Author: Keshav Sharma <keshav7890@gmail.com> & Vaibhav Sharma
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

from __future__ import division
import pygtk
import gtk
from gtk import gdk
import gobject
import sys
from PIL import Image,ImageEnhance,ImageFont,ImageFilter,ImageOps,ImageDraw
import math
from math import *
import Image

import StringIO
import logging
import random
from sugar import mime
import gst, pygame, sys, time
from random import *
from qrcode import *

class QRReader(gtk.DrawingArea):
    __gsignals__ = {
        'expose-event' : ('override'),
        'zoom-changed' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, []),
        'angle-changed': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, []),
                   }

    __gproperties__ = {
        'zoom': (gobject.TYPE_FLOAT, 'Zoom Factor', 'Factor of zoom',0, 4, 1, gobject.PARAM_READWRITE),
        'angle': (gobject.TYPE_INT, 'Angle', 'Angle of rotation',0, 360, 0, gobject.PARAM_READWRITE),
        'file_location':( gobject.TYPE_STRING, 'File Location', 'Location of the image file',
        '', gobject.PARAM_READWRITE),
        }
  
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.set_app_paintable(True)
        self.pixbuf              = None
        self.zoom                = None
        self.input_text          = "text to edit"
        self._tempfile           = None
        self.file_location       = None
        self._temp_pixbuf        = None
        self.im                  = None
        self._image_changed_flag = True
        self._optimal_zoom_flag  = True
        self.angle = 0

    def do_get_property(self, pspec):
        if pspec.name == 'zoom'          :    return self.zoom
        elif pspec.name == 'angle'       :    return self.angle
        elif pspec.name == 'file_location':   return self.file_location
        else:            raise AttributeError('unknown property %s' % pspec.name)

    def do_set_property(self, pspec, value):
        if pspec.name == 'zoom':            self.set_zoom(value)
        elif pspec.name == 'angle':            self.set_angle(value)
        elif pspec.name == 'file_location'  :      self.set_file_location(value)
        else:        raise AttributeError('unknown property %s' % pspec.name)

    def calculate_optimal_zoom(self, width=None, height=None, pixbuf=None):
        # This tries to figure out a best fit model
        # If the image can fit in, we show it in 1:1,
        # in any other case we show it in a fit to screen way

        if pixbuf == None:
            pixbuf = self.pixbuf

        if width == None or height == None:
            rect = self.parent.get_allocation()
            width = rect.width
            height = rect.height

        if width < pixbuf.get_width() or height < pixbuf.get_height():
            # Image is larger than allocated size
            zoom = min(width / pixbuf.get_width(),
                    height / pixbuf.get_height())
        else:            zoom = 1

        self._optimal_zoom_flag = True

        return zoom - 0.018 #XXX: Hack

    def set_pixbuf( self , pixbuf ):
        self.pixbuf              = pixbuf
        self.zoom                = None
        self._image_changed_flag = True
        if self.window:
            alloc       = self.get_allocation()
            rect        = gdk.Rectangle( alloc.x , alloc.y , alloc.width ,alloc.height )
            self.window.invalidate_rect( rect , True )
            self.window.process_updates( True )

    #def do_size_request(self, requisition):
    #    requisition.width = self.pixbuf.get_width()
    #    requisition.height = self.pixbuf.get_height()

    def do_expose_event(self, event):
        ctx = self.window.cairo_create()
        ctx.rectangle(event.area.x, event.area.y,
            event.area.width, event.area.height)
        ctx.clip()
        self.draw(ctx)

    def draw(self, ctx):
        if not self.pixbuf:
            return
        if self.zoom == None:
            self.zoom = self.calculate_optimal_zoom()

        if self._temp_pixbuf == None or self._image_changed_flag == True:
            width, height = self.rotate()
            self._temp_pixbuf = self._temp_pixbuf.scale_simple(width, height, gtk.gdk.INTERP_TILES)
            self._image_changed_flag = False

        rect = self.get_allocation()
        x = rect.x
        y = rect.y

        width = self._temp_pixbuf.get_width()
        height = self._temp_pixbuf.get_height()

        if self.parent:
            rect = self.parent.get_allocation()
            if rect.width > width:
                x = int(((rect.width - x) - width) / 2)

            if rect.height > height:
                y = int(((rect.height - y) - height) / 2)

        self.set_size_request(self._temp_pixbuf.get_width(),
                self._temp_pixbuf.get_height())

        ctx.set_source_pixbuf(self._temp_pixbuf, x, y)

        ctx.paint()

    def set_zoom(self, zoom):
        self._image_changed_flag = True
        self._optimal_zoom_flag = False
        self.zoom = zoom

        if self.window:
            alloc = self.get_allocation()
            rect = gdk.Rectangle(alloc.x, alloc.y,alloc.width, alloc.height)
            self.window.invalidate_rect(rect, True)
            self.window.process_updates(True)

        self.emit('zoom-changed')

    def set_angle(self, angle):
        self._image_changed_flag = True
        self._optimal_zoom_flag = True

        self.angle = angle

        if self.window:
            alloc = self.get_allocation()
            rect = gdk.Rectangle(alloc.x, alloc.y,
                alloc.width, alloc.height)
            self.window.invalidate_rect(rect, True)
            self.window.process_updates(True)

        self.emit('angle-changed')

    def rotate(self):
        if self.angle == 0:
            rotate = gtk.gdk.PIXBUF_ROTATE_NONE
        elif self.angle == 90:
            rotate = gtk.gdk.PIXBUF_ROTATE_COUNTERCLOCKWISE
        elif self.angle == 180:
            rotate = gtk.gdk.PIXBUF_ROTATE_UPSIDEDOWN
        elif self.angle == 270:
            rotate = gtk.gdk.PIXBUF_ROTATE_CLOCKWISE
        elif self.angle == 360:
            self.angle = 0
            rotate = gtk.gdk.PIXBUF_ROTATE_NONE
        else:
            logging.warning('Got unsupported rotate angle')

        self._temp_pixbuf = self.pixbuf.rotate_simple(rotate)
        width = int(self._temp_pixbuf.get_width() * self.zoom)
        height = int(self._temp_pixbuf.get_height() * self.zoom)

        return (width, height)


    def grey(self,value):
        import urllib2
        pixbuf = self.pixbuf
        im = self.pixbuftoImage(pixbuf)
#        im=Image.open("/home/keshav/Downloads/qrcode/life.png")
        strt=start(im)
        import urllib2
        from Tkinter import *
        
        if strt.words [0] == "h" and strt.words [1] == "t" and strt.words [2] == "t" and strt.words [3] == "p":
            roo = Tk()
            tex = Text(roo)
            tex.insert(INSERT,"masking used is "+"\""+str(strt.mask)+"\""+"\n\n")
            tex.insert(INSERT,"mode of the masked pattern is "+"\""+str(strt.mode)+"\""+"\n\n")
            tex.insert(INSERT,"Data decoded from the QR pattern is \""+strt.words+"\"")
            tex.pack()
            roo.mainloop()        
            data = urllib2.urlopen(strt.words)
            root = Tk()
            text = Text(root)
            text.insert(INSERT, data.read())
            text.pack()
            root.mainloop()        


    def pil_to_pixbuf(self,image):
        """Return a pixbuf created from the PIL <image>."""
        imagestr = image.tostring()
        IS_RGBA = image.mode == 'RGBA'
        return gtk.gdk.pixbuf_new_from_data(imagestr, gtk.gdk.COLORSPACE_RGB, IS_RGBA, 8, image.size[0], image.size[1], (IS_RGBA and 4 or 3) * image.size[0])

    def pixbuf_to_pil(self,pixbuf):
        """Return a PIL image created from <pixbuf>."""
        dimensions = pixbuf.get_width(), pixbuf.get_height()
        stride = pixbuf.get_rowstride()
        pixels = pixbuf.get_pixels()
        mode = pixbuf.get_has_alpha() and 'RGBA' or 'RGB'
        return Image.frombuffer(mode, dimensions, pixels, 'raw', mode, stride, 1)

    def pixbuftoImage(self,pb):
        width,height = pb.get_width(),pb.get_height()
        return Image.fromstring("RGB",(width,height),pb.get_pixels() )
    
    def imagetopixbuf(self,im):  
        file1 = StringIO.StringIO()  
        im.save(file1, "ppm")  
        contents = file1.getvalue()  
        file1.close()  
        loader = gtk.gdk.PixbufLoader("pnm")  
        loader.write(contents, len(contents))  
        pixbuf = loader.get_pixbuf()  
        loader.close()  
        return pixbuf        


    def original_cb(self,value):
        self.set_file_location(self.original)

    def set_file_location(self, file_location):
        self.original=file_location
        self.pixbuf = gtk.gdk.pixbuf_new_from_file(file_location)
        self.file_location = file_location
        self.zoom = None
        self._image_changed_flag = True
        if self.window:
            alloc = self.get_allocation()
            rect = gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
            self.window.invalidate_rect(rect, True)
            self.window.process_updates(True)

    def save_cb(self,file_path):
        pixbuf=self.pixbuf 
        pixbuf.save(file_path, 'png', {})
        
#check working of functions
def update(view_object):
    view.grey("g")
    return True


if __name__ == '__main__':
    window = gtk.Window()

    vadj = gtk.Adjustment()
    hadj = gtk.Adjustment()
    sw = gtk.ScrolledWindow(hadj, vadj)

    view = QRReader()

    view.set_file_location(sys.argv[1])


    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)


    sw.add_with_viewport(view)
    window.add(sw)

    window.set_size_request(800, 600)

    window.show_all()

    gobject.timeout_add(1000, update, view)

    gtk.main()
