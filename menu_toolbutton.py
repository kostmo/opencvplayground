#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk

class Playground(gtk.Window):
	def __init__(self):
		gtk.Window.__init__( self, gtk.WINDOW_TOPLEVEL )
		vbox = gtk.VBox(False)
		self.add(vbox)
		vbox.set_size_request(100, -1)
		toolbar = gtk.Toolbar()
		toolbutton = gtk.ToolButton()

		toggle_button = gtk.ToggleToolButton(gtk.STOCK_ADD)
		toolbar.insert(toggle_button, -1)

		menu = gtk.Menu()
		video_source_options = ["Milk", "Cookies"]
		[menu.append(gtk.MenuItem(video_source)) for video_source in video_source_options]
		for i, child in enumerate(menu.get_children()):
			child.connect("activate", self.cb_menu_activate, video_source_options[i])
		menu.show_all()
		toggle_button.connect( "clicked", self.popup_cb, menu )
		menu.connect( "deactivate", self.deactivate_cb, toggle_button )

		vbox.pack_start(toolbar, False, False)
		self.show_all()

	def cb_menu_activate(self, menu, child_index):

		import opencv
#		import cairo
		print "Activated item", child_index

	def deactivate_cb(self, menu, button):
		print "Button object:", button
		button.set_active(False)

	def popup_cb(self, widget, menu):
		menu.popup(None, None, None, 1, 0)

if __name__ == "__main__":
	application = Playground()
	gtk.main()

