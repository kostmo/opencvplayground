#!/usr/bin/python
from opencv import cv, highgui

from pygtk import require
require('2.0')
import gtk, gobject

from pipeline import FilterStage

# ==================================

class ImageFilter(FilterStage):

	def __init__(self):



