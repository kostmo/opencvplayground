#!/usr/bin/python
from opencv import cv, highgui

from pygtk import require
require('2.0')
import gtk, gobject


# ==================================

class FilterStage(gtk.Frame):

	filter_label = "Generic"

	def __init__(self, pipeline, title=""):

		self.pipeline = pipeline

		gtk.Frame.__init__(self, title)


		self.master_vbox = gtk.VBox(False, 5)
		self.master_vbox.set_border_width( 5 )
		self.add( self.master_vbox )


		video_frame = gtk.Frame()
		self.video_image = gtk.Image()

		self.master_vbox.pack_start(video_frame, False, False)
		video_frame.add(self.video_image)

	# --------------------------------------

	def redraw_filter_frame(self):

		input_frame = self.pipeline.video_source.display_frame

		self.recalculate_filter( input_frame, self.display_frame )

		self.webcam_pixbuf = gtk.gdk.pixbuf_new_from_data(
			self.display_frame.imageData,
			gtk.gdk.COLORSPACE_RGB,
			False,
			8,
			self.display_frame.width,
			self.display_frame.height,
			self.display_frame.widthStep)
		self.video_image.set_from_pixbuf(self.webcam_pixbuf)

# ==================================

class Passthrough(FilterStage):

	filter_label = "Passthrough"

	def __init__(self, pipeline):

		FilterStage.__init__(self, pipeline, self.filter_label + " filter")

		input_frame = self.pipeline.video_source.display_frame
                self.display_frame = cv.cvCreateImage( cv.cvGetSize(input_frame), cv.IPL_DEPTH_8U, 3)

	# --------------------------------------

	def recalculate_filter( self, input_frame, output_frame ):

		cv.cvCopy( input_frame, output_frame )


# ==================================

class Threshold(FilterStage):

	filter_label = "Threshold"

	def __init__(self, pipeline):

		FilterStage.__init__(self, pipeline, self.filter_label + " filter")

		input_frame = self.pipeline.video_source.display_frame
                self.display_frame = cv.cvCreateImage( cv.cvGetSize(input_frame), cv.IPL_DEPTH_8U, 3)

	# --------------------------------------

	def recalculate_filter( self, input_frame, output_frame ):

		cv.cvCopy( input_frame, output_frame )

# ==================================

class Laplacian(FilterStage):

	filter_label = "Laplacian"

	def __init__(self):

		FilterStage.__init__(self, pipeline, self.filter_label + " filter")

		input_frame = self.pipeline.video_source.display_frame
                self.display_frame = cv.cvCreateImage( cv.cvGetSize(input_frame), cv.IPL_DEPTH_8U, 3)

	# --------------------------------------

	def recalculate_filter( self, input_frame, output_frame ):

		cv.cvCopy( input_frame, output_frame )

# ==================================

class Blobs(FilterStage):

	filter_label = "Blobs"

	def __init__(self):

		FilterStage.__init__(self, pipeline, self.filter_label + " filter")

		input_frame = self.pipeline.video_source.display_frame
                self.display_frame = cv.cvCreateImage( cv.cvGetSize(input_frame), cv.IPL_DEPTH_8U, 3)

	# --------------------------------------

	def recalculate_filter( self, input_frame, output_frame ):

		cv.cvCopy( input_frame, output_frame )
