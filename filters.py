#!/usr/bin/python
from opencv import cv, highgui

from pygtk import require
require('2.0')
import gtk, gobject

from pipeline import FilterStage

# ==================================

class Laplacian(FilterStage):

	def __init__(self):


		FilterStage.__init__(self)

		print "Added Laplacian filter..."



