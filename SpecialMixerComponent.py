#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/midi-remote-scripts/Launchpad_Pro/SpecialMixerComponent.py
from functools import partial
from _Framework.Util import clamp
from _Framework.Dependency import depends
from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.Control import RadioButtonControl, RadioButtonGroup, ControlList
from .consts import FADER_TYPE_STANDARD, FADER_TYPE_BIPOLAR, VOLUME_MAP_CHANNEL, PAN_MAP_CHANNEL, SENDS_MAP_CHANNEL, FADER_LAYOUT_SYSEX_BYTE
SEND_COLORS = (('Sends.A', 'Sends.AAvail'),
 ('Sends.B', 'Sends.BAvail'),
 ('Sends.C', 'Sends.CAvail'),
 ('Sends.D', 'Sends.DAvail'),
 ('Sends.E', 'Sends.EAvail'),
 ('Sends.F', 'Sends.FAvail'),
 ('Sends.G', 'Sends.GAvail'),
 ('Sends.H', 'Sends.HAvail'))

#fix for python3
try:
	xrange
except NameError:
	xrange = range

class SpecialRadioButtonGroup(ControlList, RadioButtonControl):

	class State(RadioButtonGroup.State):

		def _make_control(self, index):
			control = self._control_type(checked_color=SEND_COLORS[index][0], unchecked_color=SEND_COLORS[index][1])
			control._event_listeners = self._event_listeners
			control._get_state(self._manager).index = index
			control_state = control._get_state(self._manager)
			control_state._on_checked = partial(self._on_checked, control_state)
			control_state.is_checked = index == self._checked_index
			return control

	def __init__(self, *a, **k):
		super(SpecialRadioButtonGroup, self).__init__(RadioButtonControl, *a, **k)


class SpecialMixerComponent(MixerComponent):
	send_select_buttons = SpecialRadioButtonGroup()

	@depends(layout_setup=None)
	def __init__(self, num_tracks = 0, num_returns = 0, auto_name = False, invert_mute_feedback = False, layout_setup = None, *a, **k):
		self._layout_setup = layout_setup
		super(SpecialMixerComponent, self).__init__(num_tracks, num_returns, auto_name, invert_mute_feedback, *a, **k)
		self.on_num_sends_changed()

	def _create_strip(self):
		return SpecialChanStripComponent()

	def set_volume_controls(self, controls):
		#for strip, control in map(None, self._channel_strips, controls or []):
		i=0
		for strip in self._channel_strips:
			if controls!=None and controls[i]:
				controls[i].set_channel(VOLUME_MAP_CHANNEL)
				controls[i].set_light_and_type('Mixer.Volume', FADER_TYPE_STANDARD)
				strip.set_volume_control(controls[i])
			else:
				strip.set_volume_control(None)
			i=i+1
		
	def set_pan_controls(self, controls):
		#for strip, control in map(None, self._channel_strips, controls or []):
		i=0
		for strip in self._channel_strips:
			if controls!=None and controls[i]:
				controls[i].set_channel(PAN_MAP_CHANNEL)
				controls[i].set_light_and_type('Mixer.Pan', FADER_TYPE_BIPOLAR)
				strip.set_pan_control(controls[i])
			else:
				strip.set_pan_control(None)
			i=i+1

	def set_send_controls(self, controls):
		self._send_controls = controls
		#for strip, control in map(None, self._channel_strips, controls or []):
		i=0
		for strip in self._channel_strips:
			if self.send_index is None or self.send_index not in xrange(8):
				strip.set_send_controls(None)
			else:
				if controls!=None and controls[i]:
					controls[i].set_channel(SENDS_MAP_CHANNEL)
					controls[i].set_light_and_type(SEND_COLORS[self.send_index][0], FADER_TYPE_STANDARD)
					strip.set_send_controls((None,) * self._send_index + (controls[i],))
				else:
					strip.set_send_controls(None)
			i=i+1

	def set_arm_buttons(self, buttons):	
		#for strip in self._channel_strips:#, button in map(None, self._channel_strips, buttons or []):
		i=0
		for strip in self._channel_strips:
			if buttons!=None and buttons[i]:
				buttons[i].reset_state()
				buttons[i].set_on_off_values('Mixer.ArmOn', 'Mixer.ArmOff')
				strip.set_arm_button(buttons[i])
			else:
				strip.set_arm_button(None)
			i=i+1

	def set_solo_buttons(self, buttons):
		#for strip, button in map(None, self._channel_strips, buttons or []):
		i=0
		for strip in self._channel_strips:
			if buttons!=None and buttons[i]:
				buttons[i].reset_state()
				buttons[i].set_on_off_values('Mixer.SoloOn', 'Mixer.SoloOff')
				strip.set_solo_button(buttons[i])
			else:
				strip.set_solo_button(None)
			i=i+1
			
	def set_mute_buttons(self, buttons):
		#for strip, button in map(None, self._channel_strips, buttons or []):
		i=0
		for strip in self._channel_strips:
			if buttons!=None and buttons[i]:
				buttons[i].reset_state()
				buttons[i].set_on_off_values('Mixer.MuteOff', 'Mixer.MuteOn')
				strip.set_mute_button(buttons[i])
			else:
				strip.set_mute_button(None)
			i=i+1

	def set_track_select_buttons(self, buttons):
		#for strip, button in map(None, self._channel_strips, buttons or []):
		i=0
		for strip in self._channel_strips:
			if buttons!=None and buttons[i]:
				buttons[i].reset_state()
				buttons[i].set_on_off_values('Mixer.Selected', 'Mixer.Unselected')
				strip.set_select_button(buttons[i])
			else:
				strip.set_select_button(None)
			i=i+1

	@send_select_buttons.checked
	def send_select_buttons(self, button):
		self.send_index = button.index

	def on_num_sends_changed(self):
		self.send_select_buttons.control_count = clamp(self.num_sends, 0, 8)

	def on_send_index_changed(self):
		if self._layout_setup is not None and self._send_controls is not None:
			self._layout_setup(FADER_LAYOUT_SYSEX_BYTE)
		if self.send_index is None:
			self.send_select_buttons.control_count = 0
		elif self.send_index < self.send_select_buttons.control_count:
			for slider in self._send_controls:
				slider.set_light(SEND_COLORS[self.send_index][0])

			self.send_select_buttons[self.send_index].is_checked = True
		else:
			for button in self.send_select_buttons:
				button.is_checked = False


class SpecialChanStripComponent(ChannelStripComponent):

	def __init__(self, *a, **k):
		super(SpecialChanStripComponent, self).__init__(*a, **k)
		self.empty_color = 'DefaultButton.Disabled'

	def _arm_value(self, value):
		super(SpecialChanStripComponent, self)._arm_value(value)
		if self.is_enabled() and value and self._track and self._track.can_be_armed and self.song().view.selected_track != self._track:
			self.song().view.selected_track = self._track

	def _select_value(self, value):
		super(SpecialChanStripComponent, self)._select_value(value)
		if self.is_enabled() and value and self._track:
			view = self.application().view
			if view.is_view_visible('Detail') and not view.is_view_visible('Detail/DeviceChain'):
				view.show_view('Detail/DeviceChain')