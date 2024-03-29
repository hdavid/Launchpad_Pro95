from __future__ import with_statement
from functools import partial
import Live
from _Framework.Util import const
from _Framework.Dependency import inject
from _Framework.SubjectSlot import subject_slot
from _Framework.Layer import Layer
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.IdentifiableControlSurface import IdentifiableControlSurface
from _Framework.ModesComponent import ModesComponent, LayerMode, AddLayerMode, ReenterBehaviour
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_CC_TYPE
from _Framework.ComboElement import ComboElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from .Colors import CLIP_COLOR_TABLE, RGB_COLOR_TABLE
from .SkinMK2 import make_skin
from .SpecialMidiMap import SpecialMidiMap, make_button, make_multi_button, make_slider
from .BackgroundComponent import ModifierBackgroundComponent, BackgroundComponent
from .ActionsComponent import ActionsComponent
from .ClipActionsComponent import ClipActionsComponent
#NEW from .LedLightingComponent import LedLightingComponent
from .TranslationComponent import TranslationComponent
from .TargetTrackComponent import TargetTrackComponent
#NEW from .SpecialDeviceComponent import SpecialDeviceComponent
#NEW from .DeviceNavigationComponent import DeviceNavigationComponent
from .SpecialSessionRecordingComponent import SpecialSessionRecordingComponent
from .DrumGroupFinderComponent import DrumGroupFinderComponent
from .DeviceComponent import DeviceComponent
from .StepSequencerComponent import StepSequencerComponent
from .StepSequencerComponent2 import StepSequencerComponent2
from .DrumGroupComponent import DrumGroupComponent
from .SpecialMixerComponent import SpecialMixerComponent
from .SpecialSessionComponent import SpecialSessionComponent as SessionComponent, SpecialClipSlotComponent, SpecialSessionZoomingComponent as SessionZoomingComponent, SessionZoomingManagerComponent
from .SpecialModesComponent import SpecialModesComponent, SpecialReenterBehaviour, CancelingReenterBehaviour
from .InstrumentComponent import InstrumentComponent
#NEW from .UserMatrixComponent import UserMatrixComponent
from .consts import *
try:
    xrange
except NameError:
    xrange = range
NUM_TRACKS = 8
NUM_SCENES = 8

class MidiMap(SpecialMidiMap):

	def __init__(self, *a, **k):
		
		super(MidiMap, self).__init__(*a, **k)
		
		#left buttons
		left_button_names = (
			'Session_Record_Button',
			'Double_Loop_Button',
			'Duplicate_Button',
			'Quantize_Button',
			'Delete_Button',
			'Undo_Button',
			'Click_Button',
			'Shift_Button'
		)
		default_states = {True: 'DefaultButton.On', False: 'DefaultButton.Off'}
		rec_states = {True: 'Recording.On', False: 'Recording.Off'}
		shift_states = {True: 'Misc.ShiftOn', False: 'Misc.Shift'}
		
		for index, val in enumerate(left_button_names):
			if val in ('Session_Record_Button', 'Undo_Button', 'Click_Button'):
				self.add_button(val, 0, (index + 1) * 10, MIDI_CC_TYPE, default_states=rec_states if val == 'Session_Record_Button' else default_states)
			else:
				self.add_modifier_button(val, 0, (index + 1) * 10, MIDI_CC_TYPE, default_states=shift_states if val == 'Shift_Button' else default_states)
		
		#bottom buttons
		self.add_button('Record_Arm_Mode_Button', 0, 1, MIDI_CC_TYPE, default_states={True: 'Mode.RecordArm.On', False: 'Mode.RecordArm.Off'})
		self.add_button('Track_Select_Mode_Button', 0, 2, MIDI_CC_TYPE, default_states={True: 'Mode.TrackSelect.On', False: 'Mode.TrackSelect.Off'})
		self.add_button('Mute_Mode_Button', 0, 3, MIDI_CC_TYPE, default_states={True: 'Mode.Mute.On', False: 'Mode.Mute.Off'})
		self.add_button('Solo_Mode_Button', 0, 4, MIDI_CC_TYPE, default_states={True: 'Mode.Solo.On', False: 'Mode.Solo.Off'})
		self.add_button('Volume_Mode_Button', 0, 5, MIDI_CC_TYPE, default_states={True: 'Mode.Volume.On', False: 'Mode.Volume.Off'})
		self.add_button('Pan_Mode_Button', 0, 6, MIDI_CC_TYPE, default_states={True: 'Mode.Pan.On', False: 'Mode.Pan.Off'})
		self.add_button('Sends_Mode_Button', 0, 7, MIDI_CC_TYPE, default_states={True: 'Mode.Sends.On', False: 'Mode.Sends.Off'})
		self.add_button('Stop_Clip_Mode_Button', 0, 8, MIDI_CC_TYPE, default_states={True: 'Mode.StopClip.On', False: 'Mode.StopClip.Off'})

		#top buttons
		self._arrow_button_names = ['Arrow_Up_Button', 'Arrow_Down_Button','Arrow_Left_Button','Arrow_Right_Button']
		arrow_button_states = {'Pressed': 'DefaultButton.On', 'Enabled': 'DefaultButton.Off', True: 'DefaultButton.On', False: 'DefaultButton.Disabled'}
		for index, val in enumerate(self._arrow_button_names):
			self.add_button(val, 0, index + 91, MIDI_CC_TYPE, default_states=arrow_button_states)

		self.add_modifier_button('Session_Mode_Button', 0, 95, MIDI_CC_TYPE, default_states={True: 'Mode.Session.On', False: 'Mode.Session.Off'}, element_factory=make_multi_button)
		self.add_button('Note_Mode_Button', 0, 96, MIDI_CC_TYPE, element_factory=make_multi_button, default_states = {True: 'Mode.Drum.On', False: 'Mode.Drum.Off'})
		self.add_button('Device_Mode_Button', 0, 97, MIDI_CC_TYPE, default_states={True: 'Mode.Device.On', False: 'Mode.Device.Off'}, element_factory=make_multi_button)
		self.add_button('User_Mode_Button', 0, 98, MIDI_CC_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'}, element_factory=make_multi_button, color_slaves=True)
		
		#scene buttons
		self.add_matrix('Scene_Launch_Button_Matrix', make_button, 0, [[ identifier for identifier in xrange(89, 18, -10) ]], MIDI_CC_TYPE)
		
		self['Scene_Stop_Button_Matrix'] = self['Scene_Launch_Button_Matrix'].submatrix[:7, :]
		self['Scene_Stop_Button_Matrix'].name = 'Scene_Stop_Button_Matrix'
		self['Stop_All_Clips_Button'] = self['Scene_Launch_Button_Matrix_Raw'][0][7]
		
		#main matrix
		self.add_matrix('Main_Button_Matrix', make_button, 0, [ [ identifier for identifier in xrange(start, start + NUM_TRACKS) ] for start in xrange(81, 10, -10) ], MIDI_NOTE_TYPE)
		
		#User
		# self.add_matrix('User_Button_Matrix', make_button, 5, [ [ identifier for identifier in xrange(start, start + NUM_TRACKS) ] for start in xrange(81, 10, -10) ], MIDI_NOTE_TYPE)
		# self.add_button('User_Scene_1', 5, 99, MIDI_NOTE_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'})
		# self.add_button('User_Scene_2', 5, 100, MIDI_NOTE_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'})
		# self.add_button('User_Scene_3', 5, 101, MIDI_NOTE_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'})
		# self.add_button('User_Scene_4', 5, 102, MIDI_NOTE_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'})
		# self.add_button('User_Scene_5', 5, 103, MIDI_NOTE_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'})
		# self.add_button('User_Scene_6', 5, 104, MIDI_NOTE_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'})
		# self.add_button('User_Scene_7', 5, 105, MIDI_NOTE_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'})
		# self.add_button('User_Scene_8', 5, 106, MIDI_NOTE_TYPE, default_states={True: 'Mode.User.On', False: 'Mode.User.Off'})
		
		#mixer button matrix	
		self['Mixer_Button_Matrix'] = self['Main_Button_Matrix'].submatrix[:, 7:]
		self['Mixer_Button_Matrix'].name = 'Mixer_Button_Matrix'
		
		#matrix with session button pressed ?
		matrix_rows_with_session_button_raw = [ [ self.with_session_button(self['Main_Button_Matrix_Raw'][row][column]) for column in xrange(8) ] for row in xrange(8) ]
		self['Main_Button_Matrix_With_Session_Button'] = ButtonMatrixElement(rows=matrix_rows_with_session_button_raw, name='Main_Button_Matrix_With_Session_Button')
		
		#note matrix
		note_buttons_raw = []
		for identifier in xrange(128):
			if identifier not in self['Main_Button_Matrix_Ids']:
				button = make_button('Note_Button_' + str(identifier), 0, identifier, MIDI_NOTE_TYPE)
				button.set_enabled(False)
				button.set_channel(CHROM_MAP_CHANNEL)
				note_buttons_raw.append(button)
		self['Note_Button_Matrix'] = ButtonMatrixElement(rows=[note_buttons_raw], name='Note_Button_Matrix')

		def make_raw_drum_matrix():
			result = []
			for row in xrange(7, -1, -1):
				button_row = []
				row_offset = 8 + (7 - row) * 4
				for column in xrange(8):
					column_offset = 28 if column >= 4 else 0
					identifier = row * 8 + column + row_offset + column_offset
					# this Main_Button_Matrix_Ids seems not to be set anywhere....
					matrix_coords = self['Main_Button_Matrix_Ids'].get(identifier)
					if matrix_coords:
						button_row.append(self['Main_Button_Matrix_Raw'][matrix_coords[1]][matrix_coords[0]])
					else:
						button_row.append(make_button('Drum_Note_Button_' + str(identifier), 0, identifier, MIDI_NOTE_TYPE))

				result.append(button_row)

			return result
			
		# drum matrix
		self['Drum_Button_Matrix'] = ButtonMatrixElement(rows=make_raw_drum_matrix(), name='Drum_Button_Matrix')
		
		#slider matrix
		self.add_matrix('Slider_Button_Matrix', make_slider, 0, [[ identifier for identifier in xrange(21, 29) ]], MIDI_CC_TYPE)
		for index, slider in enumerate(self['Slider_Button_Matrix_Raw'][0]):
			slider.set_index(index)

	def with_shift(self, button_name):
		return ComboElement(self[button_name], modifiers=[self['Shift_Button']], name='Shifted_' + button_name)

	def with_session_button(self, button):
		return ComboElement(button, modifiers=[self['Session_Mode_Button']], name=button.name + '_With_Session_Button')


class Launchpad_Pro95(IdentifiableControlSurface, OptimizedControlSurface):
	identity_request = SYSEX_IDENTITY_REQUEST

	def __init__(self, c_instance, *a, **k):
		self._copied_slot = None
		product_id_bytes = MANUFACTURER_ID + DEVICE_CODE
		super(Launchpad_Pro95, self).__init__(c_instance=c_instance, product_id_bytes=product_id_bytes, *a, **k)
		#self.set_enabled(False)
		self._challenge = Live.Application.get_random_int(0, 400000000) & 2139062143
		live = Live.Application.get_application()
		self._live_major_version = live.get_major_version()
		self._live_minor_version = live.get_minor_version()
		self._live_bugfix_version = live.get_bugfix_version()
		with self.component_guard():
			self._skin = make_skin()
			with inject(skin=const(self._skin)).everywhere():
				self._midimap = MidiMap()
			self._target_track_component = TargetTrackComponent(name='Target_Track')
			self._create_background()
			self._create_global_component()
			self._last_sent_mode_byte = None
			with inject(layout_setup=const(self._layout_setup), should_arm=const(self._should_arm_track)).everywhere():
				self._create_session()
				self._create_recording()
				self._create_actions()
				self._create_drums()
				self._create_instrument_component()
				self._create_step_sequencer()
				self._create_step_sequencer2()
				self._create_mixer()
				self._create_device()
				self._create_modes()
				#self._create_m4l_interface()
		
			self._on_session_record_changed.subject = self.song()
		# do this in handshake successful. self.set_highlighting_session_component(self._session)
		self.set_device_component(self._device)
		self._device_selection_follows_track_selection = True
		self._on_session_record_changed()

	def disconnect(self):
		#self.set_highlighting_session_component(None)
		self._send_midi(TURN_OFF_LEDS)
		self._send_midi(QUIT_MESSAGE)
		super(Launchpad_Pro95, self).disconnect()

	def _create_background(self):
		self._modifier_background_component = ModifierBackgroundComponent(
			name='Background_Component', 
			is_enabled=False, 
			layer=Layer(shift_button=self._midimap['Shift_Button'])
		)
		self._shifted_background = BackgroundComponent(
			name='No_Op_Shifted_Buttons', 
			is_enabled=False, 
			layer=Layer(
				#click_button=self._midimap.with_shift('Click_Button'),
				delete_button=self._midimap.with_shift('Delete_Button'),
				duplicate_button=self._midimap.with_shift('Duplicate_Button'),
				double_button=self._midimap.with_shift('Double_Loop_Button'),
				session_record_button=self._midimap.with_shift('Session_Record_Button')
			)
		)

	def _create_global_component(self):
		self._actions_component = ActionsComponent(
			name='Global_Actions',
			is_enabled=False, 
			layer=Layer(
				undo_button=self._midimap['Undo_Button'],
				redo_button=self._midimap.with_shift('Undo_Button'),
				metronome_button=self._midimap['Click_Button'],
				tap_button=self._midimap.with_shift('Click_Button'),
				quantization_on_button=self._midimap.with_shift('Quantize_Button'),
				duplicate_button=self._midimap['Duplicate_Button']
			)
		)

	def _create_session(self):
		self._session = SessionComponent(
			NUM_TRACKS,
			NUM_SCENES,
			auto_name=True,
			is_enabled=False,
			enable_skinning=True,
			layer=Layer(
				track_bank_left_button=self._midimap['Arrow_Left_Button'],
				track_bank_right_button=self._midimap['Arrow_Right_Button'],
				scene_bank_up_button=self._midimap['Arrow_Up_Button'],
				scene_bank_down_button=self._midimap['Arrow_Down_Button']
			)
		)
		self._session.set_enabled(True)
		self._session.set_rgb_mode(CLIP_COLOR_TABLE, RGB_COLOR_TABLE)
		SpecialClipSlotComponent.quantization_component = self._actions_component
		for scene_index in xrange(NUM_SCENES):
			scene = self._session.scene(scene_index)
			scene.layer = Layer(
				select_button=self._midimap['Shift_Button'],
				delete_button=self._midimap['Delete_Button'],
				duplicate_button=self._midimap['Duplicate_Button']
			)
			for track_index in xrange(NUM_TRACKS):
				slot = scene.clip_slot(track_index)
				slot.layer = Layer(
					select_button=self._midimap['Shift_Button'],
					delete_button=self._midimap['Delete_Button'],
					duplicate_button=self._midimap['Duplicate_Button'],
					double_loop_button=self._midimap['Double_Loop_Button'],
					quantize_button=self._midimap['Quantize_Button']
				)

		self._session_zoom = SessionZoomingComponent(
			self._session, 
			name='Session_Overview', 
			is_enabled=True, 
			enable_skinning=True
		)

	def _create_recording(self):
		self._session_record = SpecialSessionRecordingComponent(
			self._target_track_component,
			name='Session_Recording',
			is_enabled=False, 
			layer=Layer(
				record_button=self._midimap['Session_Record_Button']
			)
		)

	def _create_actions(self):
		self._clip_actions_component = ClipActionsComponent(
			self._target_track_component, 
			name='Clip_Actions', 
			is_enabled=False, 
			layer=Layer(
				duplicate_button=self._midimap['Duplicate_Button'],
				double_button=self._midimap['Double_Loop_Button'],
				quantize_button=self._midimap['Quantize_Button']
			)
		)
		ClipActionsComponent.quantization_component = self._actions_component

	def _create_drums(self):
		self._drum_group_finder = DrumGroupFinderComponent(
			self._target_track_component, 
			name = 'Drum_Group_Finder', 
			is_enabled = False, 
			layer = None
		)
		self._on_drum_group_changed.subject = self._drum_group_finder
		self._drum_group_finder.set_enabled(True)
		self._drum_group = DrumGroupComponent(
			self._clip_actions_component,
			control_surface = self,
			name='Drum_Group_Control',
			translation_channel=DR_MAP_CHANNEL
		)
		self._drum_group.set_enabled(True)

	def _create_step_sequencer(self):
		self._step_sequencer = StepSequencerComponent(self)
	
	def _create_step_sequencer2(self):
		self._step_sequencer2 = StepSequencerComponent2(self)
	
	def _create_instrument_component(self):
		self._instrument_component = InstrumentComponent(self, self._drum_group)
		
	def _create_mixer(self):
		self._mixer = SpecialMixerComponent(
			NUM_TRACKS, 
			auto_name=True, 
			is_enabled=True, 
			invert_mute_feedback=True
		)
		self._mixer.name = 'Mixer_Control'
		self._session.set_mixer(self._mixer)

	def _create_device(self):
		#self._device = SpecialDeviceComponent(name='Device_Control', is_enabled=False)
		self._device = DeviceComponent(control_surface = self, name='Device_Control', is_enabled=False)
		#self._device_navigation = DeviceNavigationComponent(name='Device_Navigation')
		#self._device_background = BackgroundComponent(name='Device_Background_Component')

	def _setup_drum_group(self):
		self._drum_group.set_drum_group_device(self._drum_group_finder.drum_group)

	def _create_translation(self, comp_name, channel, button_layer, should_enable = True, should_reset = True):
			translation_component = TranslationComponent(
				name=comp_name,
				translated_channel=channel,
				should_enable=should_enable,
				should_reset=should_reset,
				is_enabled=False,
				layer=button_layer
			)
			setattr(self, '_' + comp_name.lower(), translation_component)
			return translation_component

	def _create_modes(self):
		self._modes = ModesComponent(name='Launchpad_Modes', is_enabled=False)
		self._session_layer_mode = AddLayerMode(
			self._session, 
			Layer(
				scene_launch_buttons=self._midimap['Scene_Launch_Button_Matrix'],
				clip_launch_buttons=self._midimap['Main_Button_Matrix'],
				delete_button=self._midimap['Delete_Button'],
				duplicate_button=self._midimap['Duplicate_Button'],
				double_button=self._midimap['Double_Loop_Button'],
				quantize_button=self._midimap['Quantize_Button']
			)
		)
		action_button_background = BackgroundComponent(name='No_Op_Buttons')
		self._action_button_background_layer_mode = LayerMode(
			action_button_background, 
			Layer(
				delete_button=self._midimap['Delete_Button'], 
				quantize_button=self._midimap['Quantize_Button'], 
				duplicate_button=self._midimap['Duplicate_Button'], 
				double_button=self._midimap['Double_Loop_Button']
			)
		)
		self._clip_delete_layer_mode = AddLayerMode(
			self._clip_actions_component, 
			layer=Layer(
				delete_button=self._midimap['Delete_Button']
			)
		)
		self._create_session_zooming_modes()
		self._create_session_mode()
		self._create_note_modes()
		self._create_device_mode()
		self._create_user_mode()
		self._create_record_arm_mode()
		self._create_track_select_mode()
		self._create_mute_mode()
		self._create_solo_mode()
		self._create_volume_mode()
		self._create_pan_mode()
		self._create_sends_mode()
		self._create_stop_clips_mode()
		self._modes.layer = Layer(
			session_mode_button=self._midimap['Session_Mode_Button'],
			note_mode_button=self._midimap['Note_Mode_Button'],
			device_mode_button=self._midimap['Device_Mode_Button'],
			user_mode_button=self._midimap['User_Mode_Button'],
			record_arm_mode_button=self._midimap['Record_Arm_Mode_Button'],
			track_select_mode_button=self._midimap['Track_Select_Mode_Button'],
			mute_mode_button=self._midimap['Mute_Mode_Button'],
			solo_mode_button=self._midimap['Solo_Mode_Button'],
			volume_mode_button=self._midimap['Volume_Mode_Button'],
			pan_mode_button=self._midimap['Pan_Mode_Button'],
			sends_mode_button=self._midimap['Sends_Mode_Button'],
			stop_clip_mode_button=self._midimap['Stop_Clip_Mode_Button']
		)
		self._modes.selected_mode = 'session_mode'
		self._on_layout_changed.subject = self._modes

	def _create_session_zooming_modes(self):
		session_zoom_layer = Layer(
			button_matrix=self._midimap['Main_Button_Matrix'], 
			nav_left_button=self._midimap['Arrow_Left_Button'], 
			nav_right_button=self._midimap['Arrow_Right_Button'], 
			nav_up_button=self._midimap['Arrow_Up_Button'], 
			nav_down_button=self._midimap['Arrow_Down_Button']
		)
		session_zooming_layer_mode = LayerMode(self._session_zoom, session_zoom_layer)
		self._session_zooming_manager = SessionZoomingManagerComponent(self._modes, is_enabled=False)
		session_zooming_button_layer_mode = LayerMode(
			self._session_zooming_manager, 
			Layer(session_zooming_button=self._midimap['Session_Mode_Button'])
		)
		self._prioritized_session_zooming_button_layer_mode = LayerMode(
			self._session_zooming_manager, 
			Layer(session_zooming_button=self._midimap['Session_Mode_Button'], priority=1)
		)
		self._session_zooming_background = BackgroundComponent(name='Session_Zooming_Background')
		session_zooming_background_layer_mode = LayerMode(
			self._session_zooming_background, 
			Layer(
				scene_launch_buttons=self._midimap['Scene_Launch_Button_Matrix'],
				delete_button=self._midimap['Delete_Button'],
				quantize_button=self._midimap['Quantize_Button'],
				duplicate_button=self._midimap['Duplicate_Button'],
				double_loop_button=self._midimap['Double_Loop_Button']
			)
		)
		self._modes.add_mode('session_zooming_mode', [self._session_zooming_manager,
			session_zooming_button_layer_mode,
		 	session_zooming_layer_mode,
		 	session_zooming_background_layer_mode])
		self._modes.add_mode('prioritized_session_zooming_mode',
 			[
				partial(self._layout_switch, SESSION_LAYOUT_SYSEX_BYTE),
		 		self._session_zooming_manager,
		 		self._prioritized_session_zooming_button_layer_mode,
		 		session_zooming_layer_mode,
		 		session_zooming_background_layer_mode,
		 		self.update
			]
		)

	def _create_session_mode(self):
		self._modes.add_mode(
			'session_mode', 
			[
				partial(self._layout_setup, SESSION_LAYOUT_SYSEX_BYTE),
				self._session_layer_mode, self._session.update_navigation_buttons],
				behaviour=CancelingReenterBehaviour('session_zooming_mode')
			)

	def _create_note_modes(self):
		#pass
		#note_mode_matrix_translation = self._create_translation(
		#	'Note_Mode_Matrix_Translation', 
		#	CHROM_MAP_CHANNEL, 
		#	Layer(
		#		button_matrix=self._midimap['Main_Button_Matrix'], 
		#		note_button_matrix=self._midimap['Note_Button_Matrix'], 
		#		drum_matrix=self._midimap['Drum_Button_Matrix'], 
		#		mixer_button_matrix=self._midimap['Mixer_Button_Matrix']
		#	), 
		#	should_enable=False
		#)
		# note_mode_scene_launch_translation = self._create_translation(
		# 	'Note_Mode_Scene_Launch_Translation', 
		# 	#CHROM_MAP_CHANNEL, 
		# 	DR_MAP_CHANNEL,
		# 	Layer(
		# 		scene_launch_buttons=self._midimap['Scene_Launch_Button_Matrix']
		# 	)
		# )
		#drum_mode_note_matrix_translation = self._create_translation(
		#	'Drum_Mode_Note_Button_Translation', 
		#	0, 
		#	Layer(note_button_matrix=self._midimap['Note_Button_Matrix']),
		#	should_enable=False,
		#	should_reset=False
		#)

		
		#self._note_modes = SpecialModesComponent(name='Note_Modes')
		#self._note_modes.add_mode(
		#	'chromatic_mode', 
		#	[
		#		partial(self._layout_setup, NOTE_LAYOUT_SYSEX_BYTE), 
		#		self._clip_delete_layer_mode,
		#		note_mode_matrix_translation
		#	]
		#)
		
		#self._note_modes.add_mode(
		#	'audio_mode', 
		#	[
		#		partial(self._layout_setup, AUDIO_LAYOUT_SYSEX_BYTE),
		#		self._clip_delete_layer_mode
		#	]
		#)
		#self._note_modes.set_enabled(False)
		#self._modes.add_mode(
		#	'note_mode', 
		#	[
		#		note_mode_scene_launch_translation,
		#		self._note_modes,
		#		self._select_note_mode,
		#		self._select_target_track,
		#		self._clip_actions_component,
		#		self._show_playing_clip,
		#		self._set_clip_actions_type
		#	],
		#	behaviour=ReenterBehaviour(self.toggle_detail_view)
		#)
		#self._drum_group = DrumGroupComponent(
		#	self._clip_actions_component, 
		#	name='Drum_Group_Control'#, 
		#	#translation_channel=DR_MAP_CHANNEL
		#)
		
		self._instrument_component._modes.set_enabled(False)
		self._instrument_component.set_layers(self._midimap)
		self._modes.add_mode(
			'note_mode', 
			[
				#note_mode_scene_launch_translation,
				self._instrument_component._modes,
				self._instrument_component._detect_mode,
				self._select_target_track,
				self._clip_actions_component,
				self._show_playing_clip,
				self._set_clip_actions_type
			],
			behaviour=ReenterBehaviour(self.toggle_detail_view)
		)
		
		self._session_record.set_modes_component(self._modes)
		self._session_record.set_note_mode_name('note_mode')

	def _create_device_mode(self):
		#device_mode_scene_launch_translation = self._create_translation(
		#	'Device_Mode_Scene_Launch_Translation', 
		#	DEVICE_MAP_CHANNEL, 
		#	Layer(scene_launch_buttons=self._midimap['Scene_Launch_Button_Matrix'])
		#)
		device_layer_mode = LayerMode(
			self._device, 
			#layer=Layer(parameter_controls=self._midimap['Slider_Button_Matrix'])
			layer=Layer(
				matrix = self._midimap['Main_Button_Matrix'],
				prev_track_button = self._midimap['Arrow_Left_Button'],
				next_track_button = self._midimap['Arrow_Right_Button'],
				prev_device_button = self._midimap['Arrow_Up_Button'],
				next_device_button = self._midimap['Arrow_Down_Button'],
				on_off_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][0],
				prev_bank_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][1],
				next_bank_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][2],
				precision_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][3],
				lock_button1 = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][4],
				lock_button2 = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][5],
				lock_button3 = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][6],
				lock_button4 = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][7]
			)
		)
		#device_nav_layer_mode = LayerMode(
		#	self._device_navigation, 
		#	layer=Layer(
		#		device_nav_left_button=self._midimap['Arrow_Left_Button'], 
		#		device_nav_right_button=self._midimap['Arrow_Right_Button']
		#	)
		#)
		#device_background_layer_mode = LayerMode(
		#	self._device_background, 
		#	layer=Layer(
		#		arrow_up_button=self._midimap['Arrow_Up_Button'],
		#		arrow_down_button=self._midimap['Arrow_Down_Button']
		#	)
		#)
		self._modes.add_mode(
			'device_mode', 
			[
				#partial(self._layout_switch, SESSION_LAYOUT_SYSEX_BYTE),
				#partial(self._layout_setup, FADER_LAYOUT_SYSEX_BYTE),
				partial(self._layout_setup, DRUM_LAYOUT_SYSEX_BYTE, SYSEX_PARAM_BYTE_STANDALONE_LAYOUT),
			 	self._device,
			 	device_layer_mode,
			 	#device_nav_layer_mode,
			 	#device_background_layer_mode,
			 	#self._clip_actions_component,
			 	#self._clip_delete_layer_mode,
			 	#device_mode_scene_launch_translation,
			 	self._show_playing_clip,
		 		self._set_clip_actions_type
			], 
			behaviour=ReenterBehaviour(self.toggle_detail_view)
		)

	def _create_user_mode(self):
		self._user_button_modes = ModesComponent(name='User_Button_Modes', is_enabled=False)
		
		self._user_button_modes.add_mode(
			'stepsequencer_mode',
			[
				partial(self._layout_switch, SESSION_LAYOUT_SYSEX_BYTE),
				partial(self._layout_setup, DRUM_LAYOUT_SYSEX_BYTE, SYSEX_PARAM_BYTE_STANDALONE_LAYOUT),
				LayerMode(
					self._step_sequencer, 
					Layer(
						matrix = self._midimap['Main_Button_Matrix'],
						prev_track_button = self._midimap['Arrow_Left_Button'],
						next_track_button = self._midimap['Arrow_Right_Button'],
						prev_scene_button = self._midimap['Arrow_Up_Button'],
						next_scene_button = self._midimap['Arrow_Down_Button'],
						scale_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][0],
						octave_up_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][1],
						octave_down_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][2],
						quantization_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][3],
						velocity_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][4],
						mode_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][5], #replaced with solo ??
						mute_shift_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][6],
						lock_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][7]
					)
				)
				#,self._step_sequencer.update()
			]
		)
		
		self._user_button_modes.add_mode(
			'stepsequencer2_mode',
			[
				partial(self._layout_switch, SESSION_LAYOUT_SYSEX_BYTE),
				partial(self._layout_setup, DRUM_LAYOUT_SYSEX_BYTE, SYSEX_PARAM_BYTE_STANDALONE_LAYOUT),
				LayerMode(
					self._step_sequencer2,
					Layer(
						matrix = self._midimap['Main_Button_Matrix'],
						prev_track_button = self._midimap['Arrow_Left_Button'],
						next_track_button = self._midimap['Arrow_Right_Button'],
						prev_scene_button = self._midimap['Arrow_Up_Button'],
						next_scene_button = self._midimap['Arrow_Down_Button'],
						scale_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][0],
						octave_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][1],
						pitch_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][2],
						quantization_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][3],
						velocity_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][4],
						length_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][5],
						random_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][6],
						lock_button = self._midimap['Scene_Launch_Button_Matrix_Raw'][0][7]
					)
				)
				#,self._step_sequencer2.update()
			]
		)
		
		self._user_button_modes.add_mode('user_mode', [
			partial(self._layout_switch, SESSION_LAYOUT_SYSEX_BYTE),
			partial(self._layout_setup, USER_LAYOUT_SYSEX_BYTE)
		])
		self._user_button_modes.selected_mode = "stepsequencer_mode"
		self._modes.add_mode(
				'user_mode', 
				[
					partial(self._layout_switch, SESSION_LAYOUT_SYSEX_BYTE),
					partial(self._layout_setup, DRUM_LAYOUT_SYSEX_BYTE, SYSEX_PARAM_BYTE_STANDALONE_LAYOUT),
					self._enable_user_button_modes,
					self._user_button_modes
					
				],
				behaviour=ReenterBehaviour(self._toggle_user_button_modes)
			)
			
	def _toggle_user_button_modes(self):
		self._user_button_modes.cycle_mode()
		button = self._midimap['User_Mode_Button']
		if self._user_button_modes.selected_mode == "stepsequencer_mode":
			button.default_states = {True: 'Mode.StepSequencer.On', False: 'Mode.StepSequencer.Off'}
			self.show_message("drum step sequencer")
		elif self._user_button_modes.selected_mode == "stepsequencer2_mode":
			button.default_states = {True: 'Mode.StepSequencer2.On', False: 'Mode.StepSequencer2.Off'}
			self.show_message("melodic step sequencer")
		elif self._user_button_modes.selected_mode == "user_mode":
			button.default_states = {True: 'Mode.User.On', False: 'Mode.User.Off'}
			self.show_message("user mode")
		button.reset_state()
		button.turn_on()
		self._enable_user_button_modes()
		self._step_sequencer.update()
		self._step_sequencer2.update()
	
	def _enable_user_button_modes(self):
		self._step_sequencer.set_enabled(self._user_button_modes.selected_mode == "stepsequencer_mode")
		self._step_sequencer2.set_enabled(self._user_button_modes.selected_mode == "stepsequencer2_mode")
		#self._step_sequencer.update()
		#self._step_sequencer2.update()
		
	def _create_record_arm_mode(self):
		arm_layer_mode = LayerMode(
			self._mixer, 
			layer=Layer(arm_buttons=self._midimap['Mixer_Button_Matrix'])
		)
		self._modes.add_mode(
			'record_arm_mode', 
			[
				partial(self._layout_setup, SESSION_LAYOUT_SYSEX_BYTE),
		 		self._session_layer_mode,
		 		arm_layer_mode,
		 		self._session_zooming_manager,
		 		self._prioritized_session_zooming_button_layer_mode,
		 		self._session.update_navigation_buttons
			],
			behaviour=SpecialReenterBehaviour('session_mode')
		)

	def _create_track_select_mode(self):
		track_select_layer_mode = LayerMode(self._mixer, layer=Layer(track_select_buttons=self._midimap['Mixer_Button_Matrix']))
		self._modes.add_mode(
			'track_select_mode',
			[
				partial(self._layout_setup, SESSION_LAYOUT_SYSEX_BYTE),
		 		self._session_layer_mode,
		 		track_select_layer_mode,
		 		self._session_zooming_manager,
		 		self._prioritized_session_zooming_button_layer_mode,
		 		self._session.update_navigation_buttons
			],
			behaviour=SpecialReenterBehaviour('session_mode')
		)

	def _create_mute_mode(self):
		mute_layer_mode = LayerMode(self._mixer, layer=Layer(mute_buttons=self._midimap['Mixer_Button_Matrix']))
		self._modes.add_mode(
			'mute_mode', 
			[
				partial(self._layout_setup, SESSION_LAYOUT_SYSEX_BYTE),
		 		self._session_layer_mode,
		 		mute_layer_mode,
		 		self._session_zooming_manager,
		 		self._prioritized_session_zooming_button_layer_mode,
		 		self._session.update_navigation_buttons
			],
			behaviour=SpecialReenterBehaviour('session_mode')
		)

	def _create_solo_mode(self):
		solo_layer_mode = LayerMode(
			self._mixer, 
			layer=Layer(solo_buttons=self._midimap['Mixer_Button_Matrix'])
		)
		self._modes.add_mode(
			'solo_mode', 
			[
				partial(self._layout_setup, SESSION_LAYOUT_SYSEX_BYTE),
		 		self._session_layer_mode,
		 		solo_layer_mode,
		 		self._session_zooming_manager,
		 		self._prioritized_session_zooming_button_layer_mode,
		 		self._session.update_navigation_buttons
			],
			behaviour=SpecialReenterBehaviour('session_mode')
		)

	def _create_volume_mode(self):
		volume_mode_scene_launch_translation = self._create_translation(
			'Volume_Mode_Scene_Launch_Translation', 
			VOLUME_MAP_CHANNEL, 
			Layer(scene_launch_buttons=self._midimap['Scene_Launch_Button_Matrix'])
		)
		volume_layer_mode = LayerMode(self._mixer, layer=Layer(volume_controls=self._midimap['Slider_Button_Matrix']))
		self._modes.add_mode(
			'volume_mode',
			[
				partial(self._layout_setup, FADER_LAYOUT_SYSEX_BYTE),
			 	volume_layer_mode,
			 	self._action_button_background_layer_mode,
			 	self._session_zooming_manager,
			 	self._prioritized_session_zooming_button_layer_mode,
			 	volume_mode_scene_launch_translation,
		 		self._session.update_navigation_buttons
		],
		behaviour=SpecialReenterBehaviour('session_mode')
	)

	def _create_pan_mode(self):
		pan_mode_scene_launch_translation = self._create_translation(
			'Pan_Mode_Scene_Launch_Translation', 
			PAN_MAP_CHANNEL, 
			Layer(scene_launch_buttons=self._midimap['Scene_Launch_Button_Matrix'])
		)
		pan_layer_mode = LayerMode(
			self._mixer, 
			layer=Layer(pan_controls=self._midimap['Slider_Button_Matrix'])
		)
		self._modes.add_mode(
			'pan_mode', 
			[
				partial(self._layout_setup, FADER_LAYOUT_SYSEX_BYTE),
		 		pan_layer_mode,
		 		self._action_button_background_layer_mode,
		 		self._session_zooming_manager,
		 		self._prioritized_session_zooming_button_layer_mode,
		 		pan_mode_scene_launch_translation,
		 		self._session.update_navigation_buttons
			],
			behaviour=SpecialReenterBehaviour('session_mode')
		)

	def _create_sends_mode(self):
		send_layer_mode = LayerMode(
			self._mixer, 
			layer=Layer(
				send_controls=self._midimap['Slider_Button_Matrix'],
				send_select_buttons=self._midimap['Scene_Launch_Button_Matrix']
			)
		)
		self._modes.add_mode(
			'sends_mode', 
			[
				partial(self._layout_setup, FADER_LAYOUT_SYSEX_BYTE),
		 		send_layer_mode,
		 		self._action_button_background_layer_mode,
		 		self._session_zooming_manager,
		 		self._prioritized_session_zooming_button_layer_mode,
		 		self._session.update_navigation_buttons
			],
			behaviour=SpecialReenterBehaviour('session_mode')
		)

	def _create_stop_clips_mode(self):
		stop_layer_mode = AddLayerMode(
			self._session, 
			Layer(
				stop_track_clip_buttons=self._midimap['Mixer_Button_Matrix'],
				stop_scene_clip_buttons=self._midimap['Scene_Stop_Button_Matrix'],
				stop_all_clips_button=self._midimap['Stop_All_Clips_Button']
			)
		)
		self._modes.add_mode(
			'stop_clip_mode',
			[
				partial(self._layout_setup, SESSION_LAYOUT_SYSEX_BYTE),
		 		self._session_layer_mode,
		 		stop_layer_mode,
		 		self._session_zooming_manager,
		 		self._prioritized_session_zooming_button_layer_mode,
		 		self._session.update_navigation_buttons
			],
			behaviour=SpecialReenterBehaviour('session_mode')
		)

	def _create_m4l_interface(self):
		#self._m4l_interface = M4LInterfaceComponent(controls=self.controls, component_guard=self.component_guard, priority=1)
		self.get_control_names = self._m4l_interface.get_control_names
		self.get_control = self._m4l_interface.get_control
		self.grab_control = self._m4l_interface.grab_control
		self.release_control = self._m4l_interface.release_control

	def toggle_detail_view(self):
		view = self.application().view
		if view.is_view_visible('Detail'):
			if view.is_view_visible('Detail/DeviceChain'):
				view.show_view('Detail/Clip')
			else:
				view.show_view('Detail/DeviceChain')

	@subject_slot('drum_group')
	def _on_drum_group_changed(self):
		self._instrument_component._detect_mode()
		if self._instrument_component._modes.selected_mode == 'drum_mode':	
			#self._drum_group.set_drum_group_device(self._drum_group_finder.drum_group)
			 self._setup_drum_group()
		if self._modes.selected_mode == 'note_mode':
			self._select_note_mode()
		else:
			self.release_controlled_track()
		#self._update_note_mode_button()

	def _select_note_mode(self):
		self._instrument_component._detect_mode()
		self._update_note_mode_button()
	# 			"""
	# 			Selects which note mode to use depending on the kind of
	# 			current target track and its device chain.  Will also
	# 			select the target if specified.
	# 			"""
		#track = self._target_track_component.target_track
		#drum_device = self._drum_group_finder.drum_group
		#if track is None or track.is_foldable or track in self.song().return_tracks or track == self.song().master_track or track.is_frozen or track.has_audio_input:
		#	self._note_modes.selected_mode = 'audio_mode'
		#elif drum_device:
		#	self._note_modes.selected_mode = 'drum_mode'
		#else:
		#	self._note_modes.selected_mode = 'note_mode'
		#self._modes.update()
		#if self._note_modes.selected_mode == 'audio_mode':
		#	self.release_controlled_track()
		#else:
		#	self.set_controlled_track(self._target_track_component.target_track)

	def _select_target_track(self):
		track = self._target_track_component.target_track
		if track != self.song().view.selected_track:
			self.song().view.selected_track = track

	def _update_note_mode_button(self):
		focused_track_is_drum_track = self._drum_group_finder.drum_group is not None
		button = self._midimap['Note_Mode_Button']
		if focused_track_is_drum_track:
			button.default_states = {True: 'Mode.Drum.On', False: 'Mode.Drum.Off'}
		else:
			button.default_states = {True: 'Mode.Note.On', False: 'Mode.Note.Off'}
		button.reset_state()
		self._modes.update()

	def _show_playing_clip(self):
		track = None
		if self._use_sel_track():
			track = self.song().view.selected_track
		else:
			track = self._target_track_component.target_track
		if track in self.song().tracks:
			slot_index = track.fired_slot_index
			if slot_index < 0:
				slot_index = track.playing_slot_index
			if slot_index >= 0:
				clip_slot = track.clip_slots[slot_index]
				self.song().view.highlighted_clip_slot = clip_slot
				

	def _set_clip_actions_type(self):
		self._clip_actions_component.use_selected_track(self._use_sel_track())
		self._clip_actions_component.update()

	def _use_sel_track(self):
		return self._modes.selected_mode == 'device_mode'

	def _should_arm_track(self):
		return self._modes.selected_mode == 'record_arm_mode'

	@subject_slot('selected_mode')
	def _on_layout_changed(self, mode):
		#if mode == 'note_mode':
		#	self.set_controlled_track(self._target_track_component.target_track)
		#else:
		#	self.release_controlled_track()
		self._session_record.set_enabled(mode != 'user_mode')

	@subject_slot('session_record')
	def _on_session_record_changed(self):
		status = self.song().session_record
		feedback_color = int(self._skin['Note.FeedbackRecord'] if status else self._skin['Note.Feedback'])
		self._c_instance.set_feedback_velocity(feedback_color)

	def _clear_send_cache(self):
		with self.component_guard():
			for control in self.controls:
				control.clear_send_cache()

	def _update_hardware(self):
		self._clear_send_cache()
		self.update()
		
	def _update_global_components(self):
		self._actions_component.update()
		self._session_record.update()
		self._modifier_background_component.update()

	def _layout_setup(self, mode, mode_type = SYSEX_PARAM_BYTE_LAYOUT):
		self._layout_switch(mode, mode_type)
		
		self._clear_send_cache()
		self._update_global_components()

	def _layout_switch(self, mode, mode_type = SYSEX_PARAM_BYTE_LAYOUT):
		prefix = SYSEX_STANDARD_PREFIX + mode_type
		suffix = SYSEX_STANDARD_SUFFIX
		self._send_midi(prefix + mode + suffix)
		self._last_sent_mode_byte = mode

	def _send_identity_request(self):
		if self._live_major_version >= 10:
			super(Launchpad_Pro95, self)._send_identity_request()
		else:
			self._send_midi(SYSEX_IDENTITY_REQUEST)

	def port_settings_changed(self):
		self.set_highlighting_session_component(None)
		super(Launchpad_Pro95, self).port_settings_changed()

        
	def on_identified(self):
		self._send_challenge()

	def _send_challenge(self):
		challenge_bytes = []
		for index in range(4):
			challenge_bytes.append(self._challenge >> 8 * index & 127)
			
		challenge = CHALLENGE_PREFIX + tuple(challenge_bytes) + (247,)
		self._send_midi(challenge)

	def _on_handshake_successful(self):
		self._do_send_midi(LIVE_MODE_SWITCH_REQUEST)
		#self.set_highlighting_session_component(self._session)
		
		with self.component_guard():
			self._modes.set_enabled(True)
			self._actions_component.set_enabled(True)
			self._session_record.set_enabled(True)
			self._modifier_background_component.set_enabled(True)
			self._shifted_background.set_enabled(True)
			self.release_controlled_track()
			self.set_feedback_channels(FEEDBACK_CHANNELS)
		if self._last_sent_mode_byte is not None:
			self._layout_setup(self._last_sent_mode_byte)
		self.set_highlighting_session_component(self._session)
		self.update()

	def _is_challenge_response(self, midi_bytes):
		return len(midi_bytes) == 10 and midi_bytes[:7] == SYSEX_STANDARD_PREFIX + SYSEX_CHALLENGE_RESPONSE_BYTE

	def _is_response_valid(self, midi_bytes):
		response = int(midi_bytes[7])
		response += int(midi_bytes[8] << 8)
		return response == Live.Application.encrypt_challenge2(self._challenge)

	def handle_sysex(self, midi_bytes):
		if len(midi_bytes) < 7:
			pass
		elif self._is_challenge_response(midi_bytes) and self._is_response_valid(midi_bytes):
			self._on_handshake_successful()
		elif midi_bytes[6] == SYSEX_STATUS_BYTE_LAYOUT and midi_bytes[7] == NOTE_LAYOUT_SYSEX_BYTE[0]:
			self._update_hardware()
		elif midi_bytes[6] in (SYSEX_STATUS_BYTE_MODE, SYSEX_STATUS_BYTE_LAYOUT):
			pass
		#if len(midi_bytes) < 7:
		#	pass
		#if self._is_challenge_response(midi_bytes) and self._is_response_valid(midi_bytes):
		#	self._on_handshake_successful()
		#	
		#elif False and midi_bytes[6] in (SYSEX_STATUS_BYTE_MODE, SYSEX_STATUS_BYTE_LAYOUT):
		#	self.log_message(str(midi_bytes))
		#	self.log_message(str(midi_bytes[5]))
		#	pass
		else:
			if midi_bytes[0]==240 and midi_bytes[1]==0 and midi_bytes[2]==32 and midi_bytes[3]==41:
				if midi_bytes[4]==0 and len(midi_bytes)==6:
					self.log_message("got sysex type 0")
				elif midi_bytes[4]==2 and len(midi_bytes)==9:
					self.log_message("got sysex type 2. data: "+str(midi_bytes[5])+"-"+str(midi_bytes[6])+"-"+str(midi_bytes[7]))
				else:
					super(Launchpad_Pro95, self).handle_sysex(midi_bytes)
			else:
				super(Launchpad_Pro95, self).handle_sysex(midi_bytes)
			
			
