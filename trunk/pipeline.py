#!/usr/bin/python
from opencv import cv, highgui

from pygtk import require
require('2.0')
import gtk, gobject

# ==================================

class FilterStage(gtk.Frame):

	def __init__(self):

		gtk.Frame.__init__(self, "Filter")


		self.master_vbox = gtk.VBox(False, 5)
		self.master_vbox.set_border_width( 5 )
		self.add( self.master_vbox )


		video_frame = gtk.Frame()
		self.video_image = gtk.Image()

		self.master_vbox.pack_start(video_frame, False, False)
		video_frame.add(self.video_image)
