#!/usr/bin/python
from opencv import cv, highgui

from pygtk import require
require('2.0')
import gtk, gobject

from webcam import WebcamManager, VideoWindow

import filters
from filters import FilterStage

# ==================================

class FilterPipeline(gtk.HBox):

	def __init__(self, main_window):
		gtk.HBox.__init__(self)

		self.main_window = main_window
		self.active_filters = []

		filter_toolbar = gtk.Toolbar()
		filter_toolbar.set_orientation( gtk.ORIENTATION_VERTICAL )
		filter_toolbar.set_style( gtk.TOOLBAR_ICONS )


		filter_menu = gtk.Menu()
		filter_options = [filters.Threshold, filters.Laplacian, filters.Passthrough, filters.Blobs]

		for my_filter in filter_options:

			filter_name = my_filter.filter_label

			menu_item = gtk.MenuItem( filter_name )
			menu_item.connect("activate", self.cb_add_filter, my_filter)
			menu_item.show()
			filter_menu.append( menu_item )


		add_button = gtk.MenuToolButton( gtk.STOCK_ADD )
		add_button.set_label("Add filter")
		add_button.set_menu( filter_menu )
#		add_button.connect("clicked", self.cb_add_camera)
		filter_toolbar.insert( add_button, 0 )





		self.pack_start(filter_toolbar, False, False)






		self.filter_tray = gtk.HBox()
		self.pack_start(self.filter_tray, False, False)

		self.show_all()

		self.cb_add_camera( None )

	# ===============================

	def propagate_filter_refresh(self):
		for my_filter in self.active_filters:
			my_filter.redraw_filter_frame()

	# ===============================

	def cb_add_filter(self, widget, data):

		connector = gtk.Image()
		connector.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_LARGE_TOOLBAR)
		connector.show()
		self.filter_tray.pack_start(connector, False, False)

		filter_object = data( self )
		self.active_filters.append( filter_object )
		self.filter_tray.pack_start(filter_object, False, False)
		filter_object.show_all()

		self.main_window.status_bar.push(0, "Added " + filter_object.filter_label + " filter")

	# ===============================

	def cb_add_camera(self, widget, cam_index=1):

		self.video_source = VideoWindow( cam_index, self )

		self.filter_tray.pack_start(self.video_source, False, False)
		self.video_source.show_all()

		self.main_window.status_bar.push(0, "New video source")

