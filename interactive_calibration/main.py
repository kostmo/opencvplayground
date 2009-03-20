#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk
import sys


from opencv import cv, highgui


from mini_chessboard_calibration_test import ChessboardDataContainer, try_calibration

# ==================================

class ApplicationFrame(gtk.Assistant):

	padding = 5
	tile_count_adjustment_default_parameter_list = (4, 4, 8, 1, 1, 0)

	def __init__(self):

		gtk.Assistant.__init__(self)
#		self.set_resizable( False )	# This "shrink-wraps" the window.

		self.set_title("Interactive Calibration Tool")
		self.set_icon_from_file("my_icon.png")


		self.connect("delete_event", self.cb_clean_quit)

		self.connect("close", self.cb_clean_quit, None)	# This is a method of gtk.Assistant
		self.connect("cancel", self.cb_clean_quit, None)	# This is a method of gtk.Assistant


		page_widget = gtk.Button("Foo!")
		self.append_page( page_widget )
		self.set_page_title(page_widget, "foobar")
		self.set_page_type(page_widget, gtk.ASSISTANT_PAGE_INTRO)

		page_widget.connect("clicked", self.cb_complete_intro, page_widget)	# This is kinda wierd, 'cause the button is also the page


		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



		self.second_page_widget = gtk.HBox(False, 5)
		self.append_page( self.second_page_widget )
		self.set_page_title(self.second_page_widget, "Calibration Image Selection")
		self.set_page_type(self.second_page_widget, gtk.ASSISTANT_PAGE_CONTENT)


		left_side = gtk.VBox(False, 5)
		self.second_page_widget.pack_start(left_side, False, False)

		right_side = gtk.VBox(False, 5)
		self.second_page_widget.pack_start(right_side, True, True)





		liststore = gtk.ListStore( str, str, gtk.gdk.Pixbuf )
		self.treeview = gtk.TreeView(liststore)
		self.treeview.set_tooltip_text("Extrinsic camera parameters")
		self.treeview.set_rules_hint(True)	# alternates row coloring automatically


		for i, new_col_label in enumerate(["Filename"]):
			cell = gtk.CellRendererText()

			tvcolumn = gtk.TreeViewColumn(new_col_label, cell, text=i)
			tvcolumn.set_sort_column_id(i)	# This is abusing the purpose of the sort ID for later
			tvcolumn.set_clickable(True)
			self.treeview.append_column(tvcolumn)

		self.treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_VERTICAL)
		self.treeview.get_selection().set_mode( gtk.SELECTION_MULTIPLE )

		left_side.pack_start(self.treeview, False, False)





		bottom_row = gtk.HBox(False, 5)
		left_side.pack_start(bottom_row, False, False)

		add_button = gtk.Button(stock=gtk.STOCK_ADD)
		add_button.connect("clicked", self.cb_file_dialog_open)
		bottom_row.pack_start(add_button, False, False)

		remove_button = gtk.Button(stock=gtk.STOCK_REMOVE)
		remove_button.connect("clicked", self.cb_files_remove)	# TODO
		bottom_row.pack_start(remove_button, False, False)




		left_side.pack_start( self.make_tiles_controls(), False, False)







		self.iconview = gtk.IconView(self.treeview.get_model())

		self.iconview.set_text_column( 0 )
		self.iconview.set_pixbuf_column( 2 )
#		self.iconview.set_item_width( 100 )
		right_side.pack_start(self.iconview, True, True)
















		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		self.third_page_widget = gtk.HBox(False, 5)
		self.append_page( self.third_page_widget )
		self.set_page_title(self.third_page_widget , "Calibration Results")
		self.set_page_type(self.third_page_widget, gtk.ASSISTANT_PAGE_SUMMARY)


#		self.image_placeholder = gtk.Image()
#		right_side.pack_start(self.image_placeholder, False, False)













		treestore = gtk.TreeStore(str, float)

		last_parent = treestore.append(None, ["Translation", 0])
		for i in range(3):
			treestore.append(last_parent, [chr(ord("X") + i), 0])

		last_parent = treestore.append(None, ["Axis/Angle", 0])
		for i in range(3):
			treestore.append(last_parent, [chr(ord("X") + i), 0])


		self.coord_treeview = gtk.TreeView(treestore)
		self.coord_treeview.set_tooltip_text("Extrinsic camera parameters")
		self.coord_treeview.set_rules_hint(True)	# alternates row coloring automatically
		self.coord_treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_VERTICAL)
		self.coord_treeview.expand_row((0), True)



		for i, new_col_label in enumerate(["Axis", "Value"]):
			cell = gtk.CellRendererText()

			cell.set_property('editable', True)

			if i<3:
				tvcolumn = gtk.TreeViewColumn(new_col_label, cell, text=i)
			else:
				tvcolumn = gtk.TreeViewColumn(new_col_label, cell)

			tvcolumn.set_sort_column_id(i)	# This is abusing the purpose of the sort ID for later
			tvcolumn.set_expand(True)
			tvcolumn.set_clickable(True)
			if i>0:
				tvcolumn.set_cell_data_func(cell, self.simple_float_format)

			self.coord_treeview.append_column(tvcolumn)



		self.third_page_widget.pack_start(self.coord_treeview, False, False)



		calibrate_button = gtk.Button("Perform Calibration")
		calibrate_button.connect("clicked", self.cb_perform_calibration)
		self.third_page_widget.pack_start(calibrate_button, False, False)





		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		self.show_all()





	# -------------------------------------------
	def cb_perform_calibration(self, widget):

		chessboard_dimensions = [w.get_value_as_int()-1 for w in self.chessboard_tiles_controls]
		chessboard_dim = cv.cvSize( chessboard_dimensions[1], chessboard_dimensions[0] )
#		chessboard_dim = cv.cvSize( *chessboard_dimensions )


		ts = self.treeview.get_model()
		myiter = ts.get_iter_first()
		

		chessboard_data_set = []
		img = None
		while myiter:

			filename = ts.get_value(myiter, 1)
			myiter = ts.iter_next(myiter)


			img = highgui.cvLoadImage(filename, highgui.CV_LOAD_IMAGE_COLOR)
			found_all, corners = cv.cvFindChessboardCorners( img, chessboard_dim )
			chessboard_data_set.append( ChessboardDataContainer(corners, chessboard_dimensions) )

		try_calibration(chessboard_data_set, chessboard_dimensions, cv.cvGetSize(img))


		print "Done."


	# -------------------------------------------
	def simple_float_format(self, column, cell_renderer, tree_model, iter):

		col_number = column.get_sort_column_id()
		number = tree_model.get_value(iter, col_number)
		cell_renderer.set_property("text", "%.2f" % (number))

	# --------------------------------
	def make_tiles_controls(self):


		from chain_link import LinkableAdjustments

		tile_controls_vbox = gtk.VBox(False, self.padding)
		tile_controls_vbox.set_border_width(5)
		tile_controls_frame = gtk.Frame("Chessboard Dimensions")
		tile_controls_frame.set_tooltip_text("Specify properties of Fiducial Marker")
#		master_vbox.pack_start(tile_controls_frame, False, False)
		tile_controls_frame.add(tile_controls_vbox)


		tile_count_controls_hbox = gtk.HBox(False, self.padding)
		tile_controls_vbox.pack_start( tile_count_controls_hbox, False, False)

		tile_count_vbox = gtk.VBox(False, self.padding)
		tile_count_controls_hbox.pack_start( tile_count_vbox, True, True)

		self.chessboard_tiles_controls = []
		for txt in ["Horizontal:", "Vertical:"]:
			lil_hbox = gtk.HBox(False, self.padding)
			tile_count_vbox.pack_start( lil_hbox, False, False)

			lil_hbox.pack_start( gtk.Label(txt), True, True)

			adj = gtk.Adjustment( *self.tile_count_adjustment_default_parameter_list )
			spin_button = gtk.SpinButton(adj)
			self.chessboard_tiles_controls.append( spin_button )
			lil_hbox.pack_start( spin_button, False, False)

		self.chessboard_tiles_controls[0].set_value(6)	# TODO

		# ~~~~~~~~~~~~~~~~~~~

		linker_box = LinkableAdjustments( self.chessboard_tiles_controls )
		tile_count_controls_hbox.pack_start( linker_box, False, False)

		# ~~~~~~~~~~~~~~~~~~~

		lil_hbox = gtk.HBox(False, self.padding)
		tile_controls_vbox.pack_start( lil_hbox, False, False)
		lil_hbox.pack_start( gtk.Label("Tile size:"), True, True)
		adj = gtk.Adjustment(1, 0.25, 5, 0.25, 1, 0)
		self.board_tile_size = gtk.SpinButton(adj)
		self.board_tile_size.set_digits(2)
#		adj.connect('value_changed', self.update_scene_parms)
		lil_hbox.pack_start( self.board_tile_size, False, False)
		lil_hbox.pack_start( gtk.Label("in."), False, False)


		return tile_controls_frame






	# --------------------------------
	def cb_files_remove(self, button_widget):

		print "TODO"

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
		prompted_filenames = f.get_filenames()


		f.destroy()

		import os

		if response == gtk.RESPONSE_OK:
			for filename in prompted_filenames:


				thumbnail_size = 64
				pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
				aspect = 1.0 * pixbuf.get_width() / pixbuf.get_height()

				new_width = 0
				new_height = 0
				if pixbuf.get_width() > pixbuf.get_height():
					new_width = thumbnail_size
					new_height = int(new_width / aspect)
				else:
					new_height = thumbnail_size
					new_width = int(new_height * aspect)

				thumbnail = pixbuf.scale_simple(new_width, new_height, gtk.gdk.INTERP_BILINEAR)


				self.treeview.get_model().append( [os.path.basename(filename), filename, thumbnail] )


		if len(self.treeview.get_model()) >= 3:
			self.set_page_complete(self.second_page_widget, True)


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

