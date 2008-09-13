#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk, gobject
import gtk.glade

class Playground(gtk.Window):

	application_name = "OpenCV Playground"

	# ===============================

	def __init__(self):

		# create a new window
		gtk.Window.__init__( self, gtk.WINDOW_TOPLEVEL )
		self.set_resizable( False )
		self.set_title( self.application_name )
		self.set_icon_from_file("slow_children.svg")


		self.connect("destroy", self.destroy)

		vbox = gtk.VBox(False)
		self.add(vbox)

		widget_name = "menubar1"
		wTree = gtk.glade.XML("filter_menu.glade", widget_name)
		main_menu = wTree.get_widget(widget_name)
		vbox.pack_start(main_menu, False, False)



		dic = {	"on_quit" : self.destroy,
			"on_about" : self.cb_about_dialog}

		wTree.signal_autoconnect(dic)


		# ----------------------------

#		self.webcam_manager = WebcamManager()

		# ----------------------------

		self.pipeline_list = []
		pipeline_toolbar = gtk.Toolbar()


		from handy_widgets import make_menu_button
		add_button = make_menu_button(pipeline_toolbar, gtk.STOCK_ADD, "Add Pipeline")

		source_menu = gtk.Menu()
		video_source_options = ["Webcam", "Image", "OpenGL"]
		for video_source_name in video_source_options:
			menu_item = gtk.MenuItem( video_source_name )
			menu_item.connect("activate", self.cb_add_pipeline, video_source_name)
			source_menu.append( menu_item )
		source_menu.show_all()
		add_button.set_menu(source_menu)




		vbox.pack_start(pipeline_toolbar, False, False)


		self.pipeline_tray = gtk.VBox(False, 5)
		vbox.pack_start(self.pipeline_tray, True, True)



		self.status_bar = gtk.Statusbar()
		self.status_bar.set_has_resize_grip(True)
		vbox.pack_start(self.status_bar, False, False)


		self.show_all()

	# ===============================

	def cb_add_pipeline(self, widget, data=None):

		from pipeline import FilterPipeline
		pipeline = FilterPipeline( self )
		self.pipeline_tray.pack_start(pipeline, False, False)
		self.pipeline_list.append( pipeline )

		self.status_bar.push(0, "Added filter pipeline")

	# ===============================

	def cb_about_dialog(self, widget):

		about_dialog = gtk.AboutDialog()
		about_dialog.set_name( self.application_name )
		about_dialog.set_version("0.1")
		about_dialog.set_copyright("2008")
		about_dialog.set_website("")
		about_dialog.set_logo( gtk.gdk.pixbuf_new_from_file("slow_children.svg") )
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

	def destroy(self, widget, data=None):

		print "Cleaning up and quitting..."

		for pipeline in self.pipeline_list:
			pipeline.video_source.stop_capture()

		gtk.main_quit()

if __name__ == "__main__":

	import sys, os
	# This is for loading the images
	pathname = os.path.dirname(sys.argv[0])
	fullpath =  os.path.abspath(pathname)
	os.chdir(fullpath)

	application = Playground()
	application.main()

