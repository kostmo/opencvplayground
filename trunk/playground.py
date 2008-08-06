#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk, gobject

from webcam import VideoWindow

class Playground:

	# ===============================

	def __init__(self):


		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("OpenCV Playground")
#		self.window.set_icon_from_file("")

		self.window.connect("delete_event", self.delete_event)
#		self.window.connect("key_press_event", self.handle_keyboard_press_event)
#		self.window.connect("key_release_event", self.handle_keyboard_release_event)
#		self.window.set_events(gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)

		self.window.connect("destroy", self.destroy)

		vbox = gtk.VBox(False, 5)
		self.window.add(vbox)

		top_menu = gtk.MenuBar()
		vbox.pack_start(top_menu, False, False)


		view_menu = gtk.MenuItem("_View")
		view_submenu = gtk.Menu()
		view_menu.set_submenu( view_submenu )
		view_submenu.append( gtk.MenuItem("Camera") )

		help_menu = gtk.MenuItem("_Help")
		help_submenu = gtk.Menu()

		help_menu.set_submenu( help_submenu )
		about_item = gtk.MenuItem("About")
		about_item.connect("activate", self.cb_about_dialog)
		help_submenu.append( about_item )

		top_menu.append( help_menu )
		top_menu.append( view_menu )


		# ----------------------------


		self.video = VideoWindow()
		vbox.pack_start(self.video, False, False)

		self.window.show_all()

	# ===============================

	def cb_about_dialog(self, widget):

		about_dialog = gtk.AboutDialog()
		about_dialog.set_version("0.1")
		about_dialog.set_copyright("2008")
		about_dialog.set_website("")
#		about_dialog.set_logo( gtk.gdk.pixbuf_new_from_file("") )
		about_dialog.set_copyright(u"\u00A92008 Karl Ostmo")
		about_dialog.set_authors(["Karl Ostmo"])
		about_dialog.set_website("http://kostmo.ath.cx/")

		about_dialog.run()
		about_dialog.destroy()

	# ===============================

	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()

	# ===============================

	def delete_event(self, widget, event, data=None):

		# Change FALSE to TRUE and the main window will not be destroyed
		# with a "delete_event".
		return False

	# ===============================

	def destroy(self, widget, data=None):

		if self.video:
			self.video.stop_capture()

		gtk.main_quit()


	# ===============================

if __name__ == "__main__":

	import sys, os
	# This is for loading the images
	pathname = os.path.dirname(sys.argv[0])
	fullpath =  os.path.abspath(pathname)
	os.chdir(fullpath)

	application = Playground()
	application.main()

