#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk
import sys

# ==================================

class ApplicationFrame(gtk.Assistant):

	padding = 5

	def __init__(self):

		gtk.Assistant.__init__(self)
#		self.set_resizable( False )	# This "shrink-wraps" the window.

		self.set_title("Interactive Calibration Tool")
		self.set_icon_from_file("my_icon.png")


		self.connect("delete_event", self.cb_clean_quit)

		self.connect("close", self.cb_clean_quit, None)	# This is a method of gtk.Assistant
		self.connect("cancel", self.cb_clean_quit, None)	# This is a method of gtk.Assistant


		page_widget = gtk.Button("Foo!")
		self.append_page( page_widget )
		self.set_page_title(page_widget, "foobar")
		self.set_page_type(page_widget, gtk.ASSISTANT_PAGE_INTRO)

		page_widget.connect("clicked", self.cb_complete_intro, page_widget)	# This is kinda wierd, 'cause the button is also the page






		page_widget2 = gtk.HBox(False, 5)


		left_side = gtk.VBox(False, 5)
		page_widget2.pack_start(left_side, False, False)

		right_side = gtk.VBox(False, 5)
		page_widget2.pack_start(right_side, False, False)


		self.image_placeholder = gtk.Image()
		right_side.pack_start(self.image_placeholder, False, False)


		liststore = gtk.ListStore( str )
		self.treeview = gtk.TreeView(liststore)
		self.treeview.set_tooltip_text("Extrinsic camera parameters")
		self.treeview.set_rules_hint(True)	# alternates row coloring automatically


		for i, new_col_label in enumerate(["Filename"]):
			cell = gtk.CellRendererText()

			tvcolumn = gtk.TreeViewColumn(new_col_label, cell, text=i)
			tvcolumn.set_sort_column_id(i)	# This is abusing the purpose of the sort ID for later
			tvcolumn.set_clickable(True)
			self.treeview.append_column(tvcolumn)

		self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_VERTICAL)
		self.treeview.get_selection().set_mode( gtk.SELECTION_MULTIPLE )

		left_side.pack_start(self.treeview, False, False)


		bottom_row = gtk.HBox(False, 5)
		left_side.pack_start(bottom_row, False, False)

		add_button = gtk.Button(stock=gtk.STOCK_ADD)
		add_button.connect("clicked", self.cb_file_dialog_open)
		bottom_row.pack_start(add_button, False, False)



		remove_button = gtk.Button(stock=gtk.STOCK_REMOVE)
		bottom_row.pack_start(remove_button, False, False)



		self.append_page( page_widget2 )
		self.set_page_title(page_widget2, "foobar2")
		self.set_page_type(page_widget2, gtk.ASSISTANT_PAGE_SUMMARY)

		self.show_all()

	# --------------------------------

	def cb_complete_intro(self, button_widget, page_widget):

		self.set_page_complete(page_widget, True)

	# --------------------------------
	def cb_file_dialog_open(self, widget):

		f = gtk.FileChooserDialog( "Select images..." )
#		f.set_local_only(False)
		f.set_select_multiple(True)
		f.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)

		file_filter = gtk.FileFilter()
		file_filter.add_pattern("*.jpg")
		file_filter.set_name("JPEG files")
		f.add_filter(file_filter)

		file_filter = gtk.FileFilter()
		file_filter.add_pattern("*")
		file_filter.set_name("All files")
		f.add_filter(file_filter)

		response = f.run()
		prompted_filenames = f.get_filenames()


		f.destroy()


		if response == gtk.RESPONSE_OK:
			for filename in prompted_filenames:
				self.treeview.get_model().append( [filename] )

        # --------------------------------
        def cb_fullscreen(self, widget):

		if widget.get_active():

			self.set_resizable( True )
			while gtk.events_pending():
				gtk.main_iteration(False)

			self.fullscreen()
		else:
			self.unfullscreen()
			self.set_resizable( False )


        # --------------------------------
        def cb_clean_quit(self, widget, delete_event):
                gtk.main_quit()

        # --------------------------------
        def cb_about(self, widget):
		a = gtk.AboutDialog()

		img = gtk.Image()
		img.set_from_file("my_icon.png")
		a.set_logo(img.get_pixbuf())
		a.set_authors(["Karl Ostmo"])
		a.set_name( self.get_title() )
		a.set_transient_for( self )
		a.run()
		a.destroy()

# ==================================

if __name__ == '__main__':

	f = ApplicationFrame()
	gtk.main()

