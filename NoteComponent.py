from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ModesComponent import ModesComponent
from .ScaleComponent import ScaleComponent
from _Framework.ToggleComponent import ToggleComponent
from _Framework.Control import PlayableControl, ButtonControl, ToggleButtonControl, control_matrix
from .consts import ACTION_BUTTON_COLORS

class NoteComponent(ControlSurfaceComponent):
	
	matrix = control_matrix(PlayableControl)

	def __init__(self, control_surface = None, feedback_channels = [0,1,2], non_feedback_channel = 15, get_pattern = None, *a, **k):
		self._get_pattern = get_pattern
		self._control_surface = control_surface
		self._layout_set = False
		self._non_feedback_channel = non_feedback_channel
		self._feedback_channels = feedback_channels
		super(NoteComponent, self).__init__(*a, **k)
	
	
	def update_matrix_mapping(self, playable = False):
		pattern =  self._get_pattern()
		max_j = 8 -1#self.matrix.width - 1
		note_channel = [0 for i in range(128)]
		
		lala = 1
		for index, button in enumerate(self.matrix):
			row, col = button.coordinate
			note_info = pattern.note(col, max_j - row)
			if note_info.index != None and note_info.index<128:
				if note_info.root:
					button.color = "Note.Pads.Root"
				elif note_info.highlight:
					button.color = "Note.Pads.Highlight"
				elif note_info.in_scale:
					button.color = "Note.Pads.InScale"
				elif note_info.valid:
					button.color = "Note.Pads.OutOfScale"
				else:
					button.color = "Note.Pads.Invalid"
				button.identifier = note_info.index
				button.channel = self._feedback_channels[note_channel[note_info.index]]
				button.set_playable(not playable)
				note_channel[note_info.index] = note_channel[note_info.index] + 1
			else:
				button.identifier = lala
				lala = lala + 1
				button.channel = self._non_feedback_channel
				button.color = "Note.Pads.Invalid"
				button.set_playable(False)
			
			
			
	def set_matrix(self, matrix):
		if not matrix or not self._layout_set:
			self.matrix.set_control_element(matrix)
			self.update_matrix_mapping()
			self._layout_set = bool(matrix)
	
	# def set_scene_buttons(self, matrix):
	# 		if not matrix or not self._layout_set_scene:
	# 			self.scene_buttons.set_control_element(matrix)
	# 			self._layout_set_scene = bool(matrix)
	
	@matrix.pressed
	def drum_matrix(self, pad):
		pass
		# selected_drum_pad = self._coordinate_to_pad_map[pad.coordinate]
		# 		if self.mute_button.is_pressed:
		# 			selected_drum_pad.mute = not selected_drum_pad.mute
		# 		if self.solo_button.is_pressed:
		# 			selected_drum_pad.solo = not selected_drum_pad.solo
		# 		if self.quantize_button.is_pressed:
		# 			pad.color = 'DrumGroup.PadAction'
		# 			self.quantize_pitch(selected_drum_pad.note)
		# 		if self.delete_button.is_pressed:
		# 			pad.color = 'DrumGroup.PadAction'
		# 			self.delete_pitch(selected_drum_pad)
		# 		if self.select_button.is_pressed:
		# 			self._drum_group_device.view.selected_drum_pad = selected_drum_pad
		# 			self.select_drum_pad(selected_drum_pad)
		# 			self._selected_pads.append(selected_drum_pad)
		# 			if len(self._selected_pads) == 1:
		# 				self._update_control_from_script()
		# 			self.notify_pressed_pads()
		# 		if self.mute_button.is_pressed or self.solo_button.is_pressed:
		# 			self._update_led_feedback()
		
	@matrix.released
	def drum_matrix(self, pad):
		pass
		# selected_drum_pad = self._coordinate_to_pad_map[pad.coordinate]
		# if selected_drum_pad in self._selected_pads:
		# 	self._selected_pads.remove(selected_drum_pad)
		# 	if not self._selected_pads:
		# 		self._update_control_from_script()
		# 	self.notify_pressed_pads()
		# self._update_led_feedback()


