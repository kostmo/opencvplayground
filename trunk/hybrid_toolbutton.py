#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk

class Playground(gtk.Window):
	def __init__(self):
		gtk.Window.__init__( self, gtk.WINDOW_TOPLEVEL )
		vbox = gtk.VBox(False)
		self.add(vbox)
		vbox.set_size_request(200, -1)
		toolbar = gtk.Toolbar()
		toolbutton = gtk.ToolButton()
		toolbutton.set_label("Add")

		# ATTEMPT NUMBER ONE
		toolbutton_icon_widget = gtk.HBox()
		img = gtk.Image()
		img.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_SMALL_TOOLBAR)
		toolbutton_icon_widget.pack_start(img, False, False)
		arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_NONE)
		toolbutton_icon_widget.pack_start(arrow, False, False)
		toolbutton.set_icon_widget(toolbutton_icon_widget)
		toolbar.insert(toolbutton, -1)

		# ATTEMPT NUMBER TWO
		menu_button = gtk.MenuToolButton( gtk.STOCK_ADD )
		menu = gtk.Menu()
		[menu.append(gtk.MenuItem(video_source)) for video_source in ["Peas", "Carrots"]]
		menu.show_all()
		menu_button.set_menu(menu)
		toolbar.insert(menu_button, -1)


		# ATTEMPT NUMBER THREE
		toggle_button = gtk.ToggleToolButton(gtk.STOCK_ADD)
		toolbutton_icon_widget = gtk.HBox()
		img = gtk.Image()
		img.set_from_stock(gtk.STOCK_ADD, gtk.ICON_SIZE_SMALL_TOOLBAR)
		toolbutton_icon_widget.pack_start(img, False, False)
		arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_NONE)
		toolbutton_icon_widget.pack_start(arrow, False, False)
		toggle_button.set_icon_widget(toolbutton_icon_widget)
		toolbar.insert(toggle_button, -1)
		menu = gtk.Menu()
		[menu.append(gtk.MenuItem(video_source)) for video_source in ["Milk", "Cookies"]]
		for i, child in enumerate(menu.get_children()):
			child.connect("activate", self.cb_menu_activate, i)
		menu.show_all()
		toggle_button.connect( "clicked", self.popup_cb, menu )
		menu.connect( "deactivate", self.deactivate_cb, toggle_button )

		vbox.pack_start(toolbar, False, False)


		# ATTEMPT NUMBER FOUR
		add_button = gtk.Button( "Add pipeline", gtk.STOCK_ADD )
		add_button.set_relief( gtk.RELIEF_NONE )
		container = add_button.get_children()[0].get_children()[0]
		arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_NONE)
#		container.reorder_child(arrow, -1)	# doesn't put the arrow at the end :(
		container.pack_start( arrow, False, False )
		vbox.pack_start(add_button, False, False)

		self.show_all()

	def cb_menu_activate(self, menu, child_index):
		print "Activated item", child_index

	def deactivate_cb(self, menu, button):
#		print "Menu deactivated."	# Why is this called twice?
		button.set_active(False)

	def popup_cb(self, widget, menu):
		menu.popup(None, None, None, 1, 0)

if __name__ == "__main__":

	application = Playground()
	gtk.main()

