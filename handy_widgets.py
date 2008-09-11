from pygtk import require
require('2.0')
import gtk

def make_menu_button(toolbar, stock_id, label_text=""):
	menu_button = gtk.MenuToolButton(None, None)

	hbox = menu_button.get_child()
	button, toggle_button = hbox.get_children()
	hbox.remove(button)
	img = gtk.image_new_from_stock(stock_id, gtk.ICON_SIZE_SMALL_TOOLBAR)
	arrow = toggle_button.get_child()
	toggle_button.remove(arrow)
	hbox = gtk.HBox()
	hbox.pack_start(img, False, False)
	if label_text:
		hbox.pack_start(gtk.Label(label_text), False, False)
	hbox.pack_start(arrow, False, False)
	toggle_button.add(hbox)

	toolbar.insert(menu_button, -1)

	return menu_button

