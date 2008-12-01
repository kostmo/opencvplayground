#!/usr/bin/python
from opencv import cv, highgui

from pygtk import require
require('2.0')
import gtk, gobject

# ==================================

class PointPickerWindow(gtk.HBox):

	def __init__(self, main_window, idx, filename):

		self.main_window = main_window
		self.img_idx = idx

		self.pane_title = "Image " + `idx`
		self.correspondence_points = []


		gtk.HBox.__init__(self, False, self.main_window.padding)
		self.set_border_width( self.main_window.padding )

		preview_frame = gtk.Frame()
		self.preview_image = gtk.Image()
		self.source_img = highgui.cvLoadImage( filename )
		self.prepare_image(self.source_img)

		event_box = gtk.EventBox()
		event_box.connect("motion_notify_event", self.cb_motion_notify_event)
		event_box.connect("button_press_event", self.cb_button_press_event)

		event_box.set_events(gtk.gdk.EXPOSURE_MASK			# are each of these MASKS necessary?
		#		| gtk.gdk.LEAVE_NOTIFY_MASK
				| gtk.gdk.BUTTON_PRESS_MASK
				| gtk.gdk.BUTTON_RELEASE_MASK
				| gtk.gdk.POINTER_MOTION_MASK
				| gtk.gdk.POINTER_MOTION_HINT_MASK)

		event_box.add( self.preview_image )
		preview_frame.add( event_box )

		wrapper_box = gtk.HBox()
		wrapper_box.pack_start(preview_frame, False, False)
		self.pack_start(wrapper_box, False, False)

		# -----------------------------------

		if False:
			v_toolbar = gtk.Toolbar()
			v_toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)
			v_toolbar.set_style(gtk.TOOLBAR_ICONS)


			self.enable_feature_points = gtk.ToggleToolButton(gtk.STOCK_ABOUT)
			self.enable_feature_points.set_active(True)
			self.enable_feature_points.set_tooltip_text("Mark features")
	#		self.enable_feature_points.connect("toggled", lambda w: self.update_preview_window())
			v_toolbar.insert(self.enable_feature_points, -1)


			self.enable_sobel = gtk.ToggleToolButton(gtk.STOCK_NEW)
			self.enable_sobel.set_tooltip_text("Edge finder")
	#		self.enable_sobel.connect("toggled", lambda w: self.update_preview_window())
			v_toolbar.insert(self.enable_sobel, -1)


			self.pack_start(v_toolbar, False, False)

		self.show_all()

	# -------------------------------------------

	def paint_points(self, drawing_target):

		cv.cvCopy(self.source_img, drawing_target)

		for extrema in self.correspondence_points:
			cv_point = cv.cvPoint( int(extrema[0]), int(extrema[1]) )
			cv.cvCircle( drawing_target, cv_point, 3, cv.CV_RGB(255, 255, 0), 1, cv.CV_AA )


		if self.main_window.numbering_checkbutton.get_active():
			border_size = self.main_window.border_size.get_value_as_int()

			font_size = self.main_window.font_size.get_value()
			myfont = cv.cvInitFont( cv.CV_FONT_HERSHEY_COMPLEX, font_size, font_size, 0, border_size, cv.CV_AA)
			myfont_big = cv.cvInitFont( cv.CV_FONT_HERSHEY_COMPLEX, font_size, font_size, 0, 3*border_size, cv.CV_AA)

			for i, extrema in enumerate(self.correspondence_points):
				cv_point = cv.cvPoint( int(extrema[0]), int(extrema[1]) )

				cv.cvPutText( drawing_target, `i`, cv_point, myfont_big, cv.CV_RGB(0, 0, 0) )
				cv.cvPutText( drawing_target, `i`, cv_point, myfont, cv.CV_RGB(255, 255, 255) )


		self.update_image()

	# -------------------------------------------

	def prepare_image(self, iplimg):

		highgui.cvConvertImage(iplimg, iplimg, highgui.CV_CVTIMG_SWAP_RB)

		self.preview_pixbuf = gtk.gdk.pixbuf_new_from_data(
			iplimg.imageData,
			gtk.gdk.COLORSPACE_RGB,
			False,
			8,
			iplimg.width,
			iplimg.height,
			iplimg.widthStep)
		self.preview_image.set_from_pixbuf(self.preview_pixbuf)
		self.display_img = cv.cvCreateImage( cv.cvSize(iplimg.width, iplimg.height), cv.IPL_DEPTH_8U, 3 )

	# -------------------------------------------
	def update_image(self):

		# Finally, push the image onto the screen
		incoming_pixbuf = gtk.gdk.pixbuf_new_from_data(
			self.display_img.imageData,
			gtk.gdk.COLORSPACE_RGB,
			False,
			8,
			self.display_img.width,
			self.display_img.height,
			self.display_img.widthStep)
		incoming_pixbuf.copy_area(0, 0, self.display_img.width, self.display_img.height, self.preview_pixbuf, 0, 0)
		self.preview_image.queue_draw()

	# -------------------------------------------
	def add_standard_file_filters(self, widget):

		mydict = {	"PNG" : "*.png",
				"JPG" : "*.jpg",
				"All files" : "*"
		}

		for key, val in mydict.iteritems():
			file_filter = gtk.FileFilter()
			file_filter.add_pattern( val )
			file_filter.set_name( key )
			widget.add_filter(file_filter)

	# -------------------------------------------
	def cb_button_press_event(self, widget, event):

		x = int(event.x)
		y = int(event.y)


		if event.button == 1:

			self.correspondence_points.append( (x, y) )
			self.paint_points( self.display_img )
			self.main_window.refresh_list_display()

		self.main_window.notebooks[0].set_current_page( (self.img_idx + 1) % len(self.main_window.preview_panes) )

		return True

	# -------------------------------------------
	def cb_motion_notify_event(self, widget, event):
                
		if event.is_hint:
			x, y, state = event.window.get_pointer()
		else:
			x = event.x
			y = event.y
			state = event.state	# Unnecessary, for now


		if state & gtk.gdk.BUTTON1_MASK:
			pass

		elif state & gtk.gdk.BUTTON3_MASK:
			pass


		return True

