#!/usr/bin/python

from pygtk import require
require('2.0')
import gtk
import sys

from correspondence_tool import PointPickerWindow

# ==================================

class ApplicationFrame(gtk.Window):

	padding = 5

	def __init__(self):

		gtk.Window.__init__(self)
		self.set_resizable( False )	# This "shrink-wraps" the window.

		self.set_title("Point Correspondence Tool")
		self.set_icon_from_file("my_icon.png")


		self.set_reallocate_redraws(True)
		self.connect("delete_event", self.cb_clean_quit)



		main_vbox = gtk.VBox(False, 2*self.padding)
		main_vbox.set_border_width( self.padding )
		self.add( main_vbox )

		# ~~~~~~~~~~~~~~~~~~~~~

		arrangement_stock_items = [gtk.STOCK_ZOOM_100, gtk.STOCK_ZOOM_OUT, gtk.STOCK_ZOOM_FIT]
		arrangement_style_labels = ["Top and Bottom", "Tri-panel", "Quad-panel"]

		h_toolbar = gtk.Toolbar()
		h_toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
		h_toolbar.set_style(gtk.TOOLBAR_ICONS)

		if False:
			last_radio = None
			for i, label in enumerate(arrangement_style_labels):
				radio = gtk.RadioToolButton(last_radio, arrangement_stock_items[i] )
				radio.set_tooltip_text( label )
#				radio.connect("toggled", lambda w: self.update_preview_window())
				h_toolbar.insert(radio, -1)
				last_radio = radio

			h_toolbar.insert(gtk.SeparatorToolItem(), -1)


		button = gtk.ToggleToolButton( gtk.STOCK_FULLSCREEN )
		button.set_tooltip_text( "Make Fullscreen" )
		button.connect("clicked", self.cb_fullscreen)
		h_toolbar.insert(button, -1)

		button = gtk.ToolButton( gtk.STOCK_ABOUT )
		button.set_tooltip_text( "About" )
		button.connect("clicked", self.cb_about)
		h_toolbar.insert(button, -1)





		button = gtk.ToolButton( gtk.STOCK_QUIT )
		button.set_tooltip_text( "Quit" )
		button.connect("clicked", self.cb_clean_quit, None)
		h_toolbar.insert(button, -1)


		main_vbox.pack_start(h_toolbar, False, False)


		main_hbox = gtk.HBox(False, 2*self.padding)
		main_vbox.pack_start(main_hbox, False, False)


		self.notebooks = []
		for i in range(1):
			nb = gtk.Notebook()
			nb.set_group_id(0)	# Arbitrary, so long as it is not -1
			self.notebooks.append(nb)

			main_hbox.pack_start(nb, False, False)

			nb.connect("page-removed", self.cb_page_removed)
			nb.connect("create-window", self.cb_page_window_created)




		# ~~~~~~~~~~~~~~~~~~~~~~~


		right_vbox = gtk.VBox(False, self.padding)
		main_hbox.pack_start(right_vbox, False, False)




		open_button = gtk.Button( stock=gtk.STOCK_OPEN )
		open_button.connect("clicked", self.cb_file_dialog_open)
		right_vbox.pack_start(open_button, False, False)


		open_button = gtk.Button( stock=gtk.STOCK_PRINT )
		open_button.connect("clicked", self.cb_print_correspondences)
		right_vbox.pack_start(open_button, False, False)


		# ~~~~~~~~~~~~~~~~~~~~~~~

		mini_hbox = gtk.HBox(False, self.padding)
		mini_hbox.pack_start( gtk.Label("Font Size:"), False, False)
		right_vbox.pack_start(mini_hbox, False, False)

		adj = gtk.Adjustment(0.6, 0, 5, 0.2, 1, 0)
		self.font_size = gtk.SpinButton(adj)
		self.font_size.set_digits(1)
		self.font_size.connect("value_changed", self.cb_redraw_all_images)
		mini_hbox.pack_start(self.font_size , False, False)


		self.numbering_checkbutton = gtk.CheckButton("Number")
		self.numbering_checkbutton.set_active(True)
		self.numbering_checkbutton.connect("toggled", self.cb_redraw_all_images)
		mini_hbox.pack_start(self.numbering_checkbutton, False, False)

		# ~~~~~~~~~~~~~~~~~~~~~~~


		mini_hbox = gtk.HBox(False, self.padding)
		mini_hbox.pack_start( gtk.Label("Border Size:"), False, False)
#		right_vbox.pack_start(mini_hbox, False, False)

		adj = gtk.Adjustment(1, 0, 5, 1, 2, 0)
		self.border_size = gtk.SpinButton(adj)
		self.border_size.connect("value_changed", self.cb_redraw_all_images)
		mini_hbox.pack_start(self.border_size , False, False)

		# ~~~~~~~~~~~~~~~~~~~~~~~



		treestore = gtk.ListStore( *([int]*5) )
		self.coord_treeview = gtk.TreeView(treestore)
		self.coord_treeview.set_tooltip_text("Extrinsic camera parameters")
		self.coord_treeview.set_rules_hint(True)	# alternates row coloring automatically



		for i, new_col_label in enumerate(["Pair", "X", "Y", "X'", "Y'"]):
			cell = gtk.CellRendererText()

			tvcolumn = gtk.TreeViewColumn(new_col_label, cell, text=i)
			tvcolumn.set_sort_column_id(i)	# This is abusing the purpose of the sort ID for later
			tvcolumn.set_clickable(True)
			self.coord_treeview.append_column(tvcolumn)

		self.coord_treeview.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_VERTICAL)
		self.coord_treeview.get_selection().set_mode( gtk.SELECTION_MULTIPLE )
		self.coord_treeview.set_rubber_banding(True)

		right_vbox.pack_start(self.coord_treeview, False, False)


		# ~~~~~~~~~~~~~~~~~~~~~~~


		delete_button = gtk.Button( stock=gtk.STOCK_DELETE )
		delete_button.connect("clicked", self.cb_remove_point)
		right_vbox.pack_start(delete_button, False, False)




		clear_button = gtk.Button("Clear All Points")
		clear_button.connect("clicked", self.cb_clear_all)
		right_vbox.pack_start(clear_button, False, False)

		# ~~~~~~~~~~~~~~~~~~~~~~~
		'''
		self.preview_panes = []
		for i in range(2):
			self.preview_panes.append( PointPickerWindow( self, i ) )

		for page in self.preview_panes:
			self.notebooks[0].append_page(page, gtk.Label(page.pane_title))
			self.notebooks[0].set_tab_reorderable(page, True)
			self.notebooks[0].set_tab_detachable(page, True)
		'''

		self.show_all()


		self.cb_file_dialog_open(None)


	# --------------------------------
	def cb_remove_point(self, widget):

		liststore, rowpaths = self.coord_treeview.get_selection().get_selected_rows()

		points_to_delete = []
		for rowpath in rowpaths:
			points_to_delete.append( liststore.get_value(liststore.get_iter(rowpath), 0) )

		points_to_delete.sort()
		points_to_delete.reverse()

		for i in points_to_delete:
			for pane in self.preview_panes:
				pane.correspondence_points.pop(i)

		self.cb_redraw_all_images(widget)
		self.refresh_list_display()

	# --------------------------------
	def cb_redraw_all_images(self, widget):

		for pane in self.preview_panes:
			pane.paint_points(pane.display_img)

	# --------------------------------
	def cb_print_correspondences(self, widget):

		matching_number = len(self.preview_panes[0].correspondence_points)
		for pane in self.preview_panes:
			if matching_number != len(pane.correspondence_points):
				print "Not all the images have the same number of points specified."
				return

		model = self.coord_treeview.get_model()
		model.clear()


		correspondence_list = []
		for pane in self.preview_panes:
			correspondence_list.append( pane.correspondence_points )

		print correspondence_list

		c_string = str(correspondence_list)

		c_string = c_string.replace("[", "{")
		c_string = c_string.replace("]", "}")
		c_string = c_string.replace("(", "{")
		c_string = c_string.replace(")", "}")

		print "C syntax:"
		print c_string

	# --------------------------------
	def restock_images(self, prompted_filenames):

		# delete all old columns
		for column in self.coord_treeview.get_columns():
			self.coord_treeview.remove_column(column)

		treestore = gtk.ListStore( *([int]*(1+2*len(prompted_filenames))) )
		self.coord_treeview.set_model( treestore )

		column_labels = ["Pair"]
		for i in range( len(prompted_filenames) ):
			prime_string = "'"*i
			column_labels.append( "X"+prime_string )
			column_labels.append( "Y"+prime_string )

		for i, new_col_label in enumerate( column_labels ):
			cell = gtk.CellRendererText()

			tvcolumn = gtk.TreeViewColumn(new_col_label, cell, text=i)
			tvcolumn.set_sort_column_id(i)	# This is abusing the purpose of the sort ID for later
			tvcolumn.set_clickable(True)
			self.coord_treeview.append_column(tvcolumn)


		while self.notebooks[0].get_n_pages():
			self.notebooks[0].remove_page( 0 )

		self.preview_panes = []
		for i, filename in enumerate(prompted_filenames):
			pane = PointPickerWindow( self, i, filename )
			self.preview_panes.append( pane )

		for page in self.preview_panes:
			self.notebooks[0].append_page(page, gtk.Label(page.pane_title))
#			self.notebooks[0].set_tab_reorderable(page, True)
#			self.notebooks[0].set_tab_detachable(page, True)

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
#		prompted_filename = f.get_filename()
		prompted_filenames = f.get_filenames()

		# This will be useful if/when we allow manipulating remote files (when set_local_only is False).
#		prompted_filename = f.get_uris()	# FIXME

		f.destroy()


		if response == gtk.RESPONSE_OK:
			self.restock_images(prompted_filenames)

        # --------------------------------
        def refresh_list_display(self):

		matching_number = len(self.preview_panes[0].correspondence_points)
		for pane in self.preview_panes:
			if matching_number != len(pane.correspondence_points):
				return

		model = self.coord_treeview.get_model()
		model.clear()

		for i in range( matching_number ):
			data_list = [i]
			for j in range( len(self.preview_panes) ):
				for k in range(2):
					data_list.append( self.preview_panes[j].correspondence_points[i][k] )

			last_parent = model.append(data_list)

        # --------------------------------
        def cb_clear_all(self, widget):
		for pane in self.preview_panes:
			pane.correspondence_points = []
			pane.paint_points(pane.display_img)

		self.refresh_list_display()

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
        def cb_page_removed(self, notebook, child, page_num):
		pass
#		print "A page was removed! There are", notebook.get_n_pages(), "more."

        # --------------------------------
        def cb_page_window_created(self, notebook, page, x, y):

		new_win = gtk.Window()
		page.satellite_window = new_win
#		new_win.move(x, y)
		new_win.set_position(gtk.WIN_POS_MOUSE)

		notebook.remove_page( notebook.page_num(page) )
		new_win.add(page)

		new_win.page_origin = notebook
		new_win.page_widget = page

		if False:
			new_win.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_UTILITY )
			new_win.set_transient_for(self)
		else:
			new_win.set_icon( self.get_icon() )
			new_win.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_NORMAL )

		new_win.set_title(page.pane_title)
		new_win.connect("delete-event", self.cb_satellite_window_deleted)

		new_win.show_all()

        # --------------------------------
	def cb_satellite_window_deleted(self, widget, delete_event):

		widget.remove( widget.page_widget )
		widget.page_origin.append_page( widget.page_widget, gtk.Label(widget.page_widget.pane_title) )
		widget.page_origin.set_tab_reorderable(widget.page_widget, True)
		widget.page_origin.set_tab_detachable(widget.page_widget, True)
		widget.page_widget.satellite_window = None

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

