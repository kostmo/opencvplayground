#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk, gobject
import gtk.glade

from webcam import WebcamManager, VideoWindow

class Playground:

	application_name = "OpenCV Playground"

	# ===============================

	def __init__(self):


		# create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title( self.application_name )
#		self.window.set_icon_from_file("")

		self.window.connect("delete_event", self.delete_event)
#		self.window.connect("key_press_event", self.handle_keyboard_press_event)
#		self.window.connect("key_release_event", self.handle_keyboard_release_event)
#		self.window.set_events(gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK)

		self.window.connect("destroy", self.destroy)

		vbox = gtk.VBox(False, 5)
		self.window.add(vbox)


		wTree = gtk.glade.XML("filter_menu.glade")
		main_menu = wTree.get_widget("menubar1")
		vbox.pack_start(main_menu, False, False)
		wTree.get_widget("imagemenuitem10").connect("activate", self.cb_about_dialog)

		# ----------------------------

#		self.webcam_manager = WebcamManager()

		# ----------------------------


		hbox = gtk.HBox(False, 5)
		vbox.pack_start(hbox, False, False)
		cam_add = gtk.Button(stock=gtk.STOCK_ADD)
		hbox.pack_start(cam_add, False, False)
		cam_index = gtk.SpinButton(gtk.Adjustment(0, 0, 7, 1))
		hbox.pack_start(cam_index, False, False)
		cam_add.connect("clicked", self.cb_add_camera, cam_index)


		self.video_window_list = []
		self.video_tray = gtk.HBox(False, 5)
		vbox.pack_start(self.video_tray, True, True)



		self.status_bar = gtk.Statusbar()
		self.status_bar.set_has_resize_grip(True)
		vbox.pack_start(self.status_bar, False, False)


		self.window.show_all()

	# ===============================

	def cb_add_camera(self, widget, index_widget):

		video = VideoWindow( index_widget.get_value_as_int() )
		self.video_window_list.append( video )
		self.video_tray.pack_start(video, False, False)
		video.show_all()

	# ===============================

	def cb_about_dialog(self, widget):

		about_dialog = gtk.AboutDialog()
		about_dialog.set_name( self.application_name )
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

		for video in self.video_window_list:
			video.stop_capture()

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

