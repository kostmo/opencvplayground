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
		self.next_stage = None

		gtk.Frame.__init__(self, title)


		self.master_vbox = gtk.VBox(False, 5)
		self.master_vbox.set_border_width( 5 )
		self.add( self.master_vbox )


		video_frame = gtk.Frame()
		self.video_image = gtk.Image()

		self.master_vbox.pack_start(video_frame, False, False)
		video_frame.add(self.video_image)

	# --------------------------------------

	def redraw_filter_frame(self, widget=None):

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

		# Here we must signal ahead to the next filter in the pipeline, propagating the update
		if self.next_stage:
			self.next_stage.redraw_filter_frame()


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

	filter_label = "Simple Threshold"
        value_range_parameters = (128, 0, 255, 1, 5, 0)

	def __init__(self, pipeline):

		FilterStage.__init__(self, pipeline, self.filter_label + " filter")

		input_frame = self.pipeline.video_source.display_frame
		size = cv.cvGetSize(input_frame)
                self.display_frame = cv.cvCreateImage(size, cv.IPL_DEPTH_8U, 3)
		self.my_grayscale = cv.cvCreateImage (size, 8, 1)


		adj = gtk.Adjustment( *self.value_range_parameters )
		self.lower_bound = gtk.HScale(adj)
		self.lower_bound.set_value_pos(gtk.POS_RIGHT)
		self.lower_bound.set_digits(0)

		adj = gtk.Adjustment( *self.value_range_parameters )
		self.upper_bound = gtk.HScale(adj)
		self.upper_bound.set_value_pos(gtk.POS_RIGHT)
		self.upper_bound.set_digits(0)
		self.upper_bound.set_value(255)


		mini_hbox = gtk.HBox(False, 5)
		mini_hbox.pack_start(gtk.Label("Lower threshold:"), False, False)
		mini_hbox.pack_start(self.lower_bound, True, True)
		self.master_vbox.pack_start(mini_hbox, False, False)

		mini_hbox = gtk.HBox(False, 5)
		mini_hbox.pack_start(gtk.Label("Upper threshold:"), False, False)
		mini_hbox.pack_start(self.upper_bound, True, True)
		self.master_vbox.pack_start(mini_hbox, False, False)

		self.lower_bound.connect('value_changed', self.redraw_filter_frame)
		self.upper_bound.connect('value_changed', self.redraw_filter_frame)

	# --------------------------------------

	def recalculate_filter( self, input_frame, output_frame ):

		cv.cvCvtColor(input_frame, self.my_grayscale, cv.CV_RGB2GRAY);
		cv.cvThreshold(self.my_grayscale, self.my_grayscale, self.lower_bound.get_value(), self.upper_bound.get_value(), cv.CV_THRESH_BINARY)
		cv.cvCvtColor(self.my_grayscale, output_frame, cv.CV_GRAY2RGB);

# ==================================

class Laplacian(FilterStage):

	filter_label = "Laplacian"

	def __init__(self, pipeline):

		FilterStage.__init__(self, pipeline, self.filter_label + " filter")

		input_frame = self.pipeline.video_source.display_frame
                self.display_frame = cv.cvCreateImage( cv.cvGetSize(input_frame), cv.IPL_DEPTH_8U, 3)

	# --------------------------------------

	def recalculate_filter( self, input_frame, output_frame ):

		cv.cvCopy( input_frame, output_frame )

# ==================================

class Blobs(FilterStage):

	filter_label = "Blobs"

        value_range_parameters = (1000, 0, 320*240, 1, 5, 25)

	def __init__(self, pipeline):

		FilterStage.__init__(self, pipeline, self.filter_label + " filter")

		input_frame = self.pipeline.video_source.display_frame
		size = cv.cvGetSize(input_frame)
                self.display_frame = cv.cvCreateImage(size, cv.IPL_DEPTH_8U, 3)
		self.my_grayscale = cv.cvCreateImage (size, 8, 1)
		self.mask = cv.cvCreateImage (size, 8, 1)
		cv.cvSet(self.mask, 1)








		adj = gtk.Adjustment( *self.value_range_parameters )
		self.lower_bound = gtk.HScale(adj)
		self.lower_bound.set_value_pos(gtk.POS_RIGHT)
		self.lower_bound.set_digits(0)

		adj = gtk.Adjustment( *self.value_range_parameters )
		self.upper_bound = gtk.HScale(adj)
		self.upper_bound.set_value_pos(gtk.POS_RIGHT)
		self.upper_bound.set_digits(0)
		self.upper_bound.set_value(100000)


		mini_hbox = gtk.HBox(False, 5)
		mini_hbox.pack_start(gtk.Label("Lower threshold:"), False, False)
		mini_hbox.pack_start(self.lower_bound, True, True)
		self.master_vbox.pack_start(mini_hbox, False, False)

		mini_hbox = gtk.HBox(False, 5)
		mini_hbox.pack_start(gtk.Label("Upper threshold:"), False, False)
		mini_hbox.pack_start(self.upper_bound, True, True)
		self.master_vbox.pack_start(mini_hbox, False, False)

		self.lower_bound.connect('value_changed', self.redraw_filter_frame)
		self.upper_bound.connect('value_changed', self.redraw_filter_frame)




		self.pass_original_frame = gtk.CheckButton("Pass original frame")
		self.master_vbox.pack_start(self.pass_original_frame, False, False)


	# --------------------------------------

	def recalculate_filter( self, input_frame, output_frame ):

		from blobs.BlobResult import CBlobResult
		from blobs.Blob import CBlob




		cv.cvCvtColor(input_frame, self.my_grayscale, cv.CV_RGB2GRAY);
		cv.cvThreshold(self.my_grayscale, self.my_grayscale, 128, 255, cv.CV_THRESH_BINARY)

		if self.pass_original_frame.get_active():
			cv.cvCopy( input_frame, output_frame )
		else:
			cv.cvCvtColor(self.my_grayscale, output_frame, cv.CV_GRAY2RGB);


		myblobs = CBlobResult(self.my_grayscale, self.mask, 100, True)

		myblobs.filter_blobs(10, 10000)
		blob_count = myblobs.GetNumBlobs()


		from color_helpers import hsv2rgb
		for i in range(blob_count):

			my_enumerated_blob = myblobs.GetBlob(i)
			my_enumerated_blob.FillBlob(output_frame, hsv2rgb( i*180.0/blob_count ), 0, 0)



