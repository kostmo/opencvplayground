#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk

class Playground(gtk.Window):

	def make_menu_button(self, toolbar):
		menu_button = gtk.MenuToolButton(None, None)

		hbox = menu_button.get_child()
		button, toggle_button = hbox.get_children()
		hbox.remove(button)
		img = gtk.image_new_from_stock(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_SMALL_TOOLBAR)
		arrow = toggle_button.get_child()
		toggle_button.remove(arrow)
		hbox = gtk.HBox()
		hbox.pack_start(img, False, False)
		hbox.pack_start(gtk.Label("Live Bookmarks"), False, False)
		hbox.pack_start(arrow, False, False)
		toggle_button.add(hbox)

		toolbar.insert(menu_button, -1)

		return menu_button

	def __init__(self):
		gtk.Window.__init__( self, gtk.WINDOW_TOPLEVEL )

		toolbar = gtk.Toolbar()
		self.add(toolbar)
		toolbar.set_size_request(200, -1)

		menu_button = self.make_menu_button(toolbar)
		menu = gtk.Menu()
		[menu.append(gtk.MenuItem(video_source)) for video_source in ["Peas", "Carrots"]]
		menu.show_all()
		menu_button.set_menu(menu)


		self.show_all()

if __name__ == "__main__":
	application = Playground()
	gtk.main()

