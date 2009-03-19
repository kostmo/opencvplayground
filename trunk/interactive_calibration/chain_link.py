from pygtk import require
require('2.0')
import gtk


class LinkableAdjustments(gtk.VBox):

	def __init__(self, control_set):

		self.control_set = control_set

		gtk.VBox.__init__(self, False)


		upper_bracket = gtk.DrawingArea()
		upper_bracket.connect("expose_event", self.cb_chain_bracket_expose_event)
		lower_bracket = gtk.DrawingArea()
		lower_bracket.connect("expose_event", self.cb_chain_bracket_expose_event, True)

		chain_button = gtk.ToggleButton()
		chain_button.set_relief( gtk.RELIEF_NONE )

		img = None
		if False:	# This doesn't work on Windows XP GTK+
			img = gtk.image_new_from_file("chain-broken_v.png")
		else:
			img = gtk.Image()
			img.set_from_file( "chain-broken_v.png" )

		chain_button.add( img )
		chain_button.connect('toggled', self.link_toggle_callback)

		self.pack_start( upper_bracket, True, True)
		self.pack_start( chain_button, False, False)
		self.pack_start( lower_bracket, True, True)

	# ===================================================

	def link_toggle_callback(self, widget):

		chain_options = ["chain-broken_v.png", "chain_v.png"]
		widget.get_child().set_from_file( chain_options[ int( widget.get_active() ) ] )

		# ~~~~~~~~~~~~~~~~~~

		old_value = self.control_set[0].get_value()

		temp = self.control_set[0].get_adjustment()
		if not widget.get_active():
			temp = gtk.Adjustment( temp.value, temp.lower, temp.upper, temp.step_increment, temp.page_increment, temp.page_size )

		for control in self.control_set[1:]:
			control.set_adjustment( temp )
			control.set_value( old_value )

	# -------------------------------------------

	def cb_chain_bracket_expose_event(self, widget, event, data=None):


		widget.window.draw_line(widget.style.fg_gc[gtk.STATE_NORMAL],
			widget.allocation.width/2,
			widget.allocation.height,
			widget.allocation.width/2,
			0
		)

		y_pos = 0
		if data:
			y_pos = widget.allocation.height-1


		widget.window.draw_line(widget.style.fg_gc[gtk.STATE_NORMAL],
			widget.allocation.width/2,
			y_pos,
			0,
			y_pos
		)

		return True


