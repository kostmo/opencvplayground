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

		self.set_title("Point Correspondence Tool")
		self.set_icon_from_file("my_icon.png")


		self.connect("delete_event", self.cb_clean_quit)

		self.connect("close", self.cb_clean_quit, None)	# This is a method of gtk.Assistant

		page_widget = gtk.Button("Foo!")
		self.append_page( page_widget )
		self.set_page_title(page_widget, "foobar")
		self.set_page_type(page_widget, gtk.ASSISTANT_PAGE_INTRO)

		page_widget.connect("clicked", self.cb_complete_intro, page_widget)	# This is kinda wierd, 'cause the button is also the page


		page_widget = gtk.Button("Bar!")
		self.append_page( page_widget )
		self.set_page_title(page_widget, "foobar2")
		self.set_page_type(page_widget, gtk.ASSISTANT_PAGE_SUMMARY)

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
#		prompted_filename = f.get_filename()
		prompted_filenames = f.get_filenames()

		# This will be useful if/when we allow manipulating remote files (when set_local_only is False).
#		prompted_filename = f.get_uris()	# FIXME

		f.destroy()


		if response == gtk.RESPONSE_OK:
			self.restock_images(prompted_filenames)

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

