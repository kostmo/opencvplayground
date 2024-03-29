#!/usr/bin/python
from opencv import cv, highgui

from pygtk import require
require('2.0')
import gtk, gobject

# ==================================

class WebcamManager:

	def __init__(self):

		self.webcams = []
		print "Scanning available cameras..."

		cam_index = 0
		while True:

			try:
				capture = highgui.cvCreateCameraCapture( cam_index )
			except e:
				print "Capture error:"
				print e

			if not capture:
				break

			try:
				webcam_frame = highgui.cvQueryFrame( capture )
			except e:
				print "Query error:"
				print e

			if not webcam_frame:
				break

			print "Camera %d: %dx%d" % (cam_index, webcam_frame.width, webcam_frame.height)

#			cv.cvReleaseCapture( capture )

		print "Finished scanning."


# ==================================


from filters import FilterStage

class VideoWindow(FilterStage):

	def __init__(self, device, pipeline):

		FilterStage.__init__(self, pipeline, "Webcam")

		# -----------------------------------

		self.video_enabled_button = gtk.ToggleButton("Enable Video")
		self.video_enabled_button.connect('clicked', self.cb_toggle_video)
		self.master_vbox.pack_start(self.video_enabled_button, False, False)

		# -----------------------------------

		hbox = gtk.HBox(False, 5)
		self.master_vbox.pack_start(hbox, False, False)

		self.inverted_video = gtk.CheckButton("Flip vertical")
		hbox.pack_start(self.inverted_video, False, False)

		self.flipped_video = gtk.CheckButton("Flip horizontal")
		hbox.pack_start(self.flipped_video, False, False)

		hbox.pack_end(gtk.Label("Framerate:"), False, False)

		# -----------------------------------


		self.capture = None

#		device = 0
		self.start_capture(device)

		if self.initialize_video():
			self.video_enabled_button.set_active(True)

	# -----------------------------------

	def start_capture(self, device):

#		video_dimensions = [176, 144]
		video_dimensions = [320, 240]

                if not self.capture:

			self.capture = highgui.cvCreateCameraCapture(device)
			
			highgui.cvSetCaptureProperty(self.capture, highgui.CV_CAP_PROP_FRAME_WIDTH, video_dimensions[0])
			highgui.cvSetCaptureProperty(self.capture, highgui.CV_CAP_PROP_FRAME_HEIGHT, video_dimensions[1])

	# -----------------------------------

	def stop_capture(self):
                if self.capture:
                        cv.cvReleaseCapture( self.capture )

	# -----------------------------------

	def initialize_video(self):

		webcam_frame = highgui.cvQueryFrame( self.capture )

		if not webcam_frame:
			return False

		self.webcam_pixbuf = gtk.gdk.pixbuf_new_from_data(
			webcam_frame.imageData,
			gtk.gdk.COLORSPACE_RGB,
			False,
			8,
			webcam_frame.width,
			webcam_frame.height,
			webcam_frame.widthStep)
		self.video_image.set_from_pixbuf(self.webcam_pixbuf)


                self.display_frame = cv.cvCreateImage( cv.cvSize(webcam_frame.width, webcam_frame.height), cv.IPL_DEPTH_8U, 3)

		return True

	# -----------------------------------

	def cb_toggle_video(self, widget):

		if widget.get_active():
			gobject.idle_add( self.run )

	# -------------------------------------------

	def run(self):
		if self.capture:	# Is this check necessary?
			webcam_frame = highgui.cvQueryFrame( self.capture )
		else:
			print "Capture error!"
			return False

		flip_parameter = self.flipped_video.get_active() | (self.inverted_video.get_active() << 1)
		if flip_parameter:
			cv.cvFlip (webcam_frame, None, 2 - flip_parameter)

		highgui.cvConvertImage(webcam_frame, self.display_frame, highgui.CV_CVTIMG_SWAP_RB)

		incoming_pixbuf = gtk.gdk.pixbuf_new_from_data(
				self.display_frame.imageData,
				gtk.gdk.COLORSPACE_RGB,
				False,
				8,
				self.display_frame.width,
				self.display_frame.height,
				self.display_frame.widthStep)
		incoming_pixbuf.copy_area(0, 0, self.display_frame.width, self.display_frame.height, self.webcam_pixbuf, 0, 0)

		self.video_image.queue_draw()
		self.pipeline.propagate_filter_refresh()

		return self.video_enabled_button.get_active()

