#Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/midi-remote-scripts/Launchpad_Pro/SkinDefault.py
from _Framework.Skin import Skin
from .Colors import Rgb

class Colors:

	class DefaultButton:
		On = Rgb.GREEN
		Off = Rgb.GREEN_HALF
		Disabled = Rgb.BLACK

	class Session:
		SceneTriggered = Rgb.GREEN_BLINK
		NoScene = Rgb.BLACK
		ClipStarted = Rgb.GREEN_PULSE
		ClipRecording = Rgb.RED_PULSE
		ClipTriggeredPlay = Rgb.GREEN_BLINK
		ClipTriggeredRecord = Rgb.RED_BLINK
		ClipEmpty = Rgb.BLACK
		RecordButton = Rgb.RED_HALF
		StopClip = Rgb.RED
		StopClipTriggered = Rgb.RED_BLINK
		StoppedClip = Rgb.RED_HALF
		Enabled = Rgb.GREEN
		Off = Rgb.GREEN_HALF

	class Zooming:
		Selected = Rgb.AMBER
		Stopped = Rgb.RED
		Playing = Rgb.GREEN
		Empty = Rgb.BLACK

	class Mixer:
		ArmOn = Rgb.RED
		ArmOff = Rgb.RED_HALF
		SoloOn = Rgb.BLUE
		SoloOff = Rgb.BLUE_HALF
		MuteOn = Rgb.YELLOW_HALF
		MuteOff = Rgb.YELLOW
		Selected = Rgb.LIGHT_BLUE
		Unselected = Rgb.LIGHT_BLUE_HALF
		Volume = Rgb.GREEN
		Pan = Rgb.ORANGE
		Sends = Rgb.WHITE

	class Sends:
		A = Rgb.DARK_BLUE
		AAvail = Rgb.DARK_BLUE_HALF
		B = Rgb.BLUE
		BAvail = Rgb.BLUE_HALF
		C = Rgb.LIGHT_BLUE
		CAvail = Rgb.LIGHT_BLUE_HALF
		D = Rgb.MINT
		DAvail = Rgb.MINT_HALF
		E = Rgb.DARK_YELLOW
		EAvail = Rgb.DARK_YELLOW_HALF
		F = Rgb.YELLOW
		FAvail = Rgb.YELLOW_HALF
		G = Rgb.ORANGE
		GAvail = Rgb.ORANGE_HALF
		H = Rgb.RED
		HAvail = Rgb.RED_HALF

	class Device:
		class Lock:
			Empty = Rgb.PURPLE
			Set = Rgb.RED_HALF
			Locked = Rgb.RED
		class Slider:
			On = Rgb.PURPLE
			Off = Rgb.PURPLE_HALF
		class PrecisionSlider:
			On = Rgb.PURPLE
			Off = Rgb.PURPLE_HALF
		class Enum:
			On = Rgb.ORANGE
			Off = Rgb.ORANGE_HALF
		class BigEnum:
			On = Rgb.YELLOW
			Off = Rgb.YELLOW_HALF
		class Toggle:
			On = Rgb.RED
			Off = Rgb.RED_HALF
	
	class StepSequencer:
		class Scale:
			On = Rgb.RED
			Off = Rgb.RED_HALF
		class Octave:
			On = Rgb.RED
			Off = Rgb.RED_HALF
		class Mute:
			On = Rgb.RED
			Off = Rgb.RED_HALF
		class Mode:
			On = Rgb.AMBER
			Off = Rgb.AMBER_HALF
		class Lock:
			class ToTrack:
				On = Rgb.RED
				Off =  Rgb.RED_HALF
			class ToClip:
				On =  Rgb.PURPLE
				Off = Rgb.PURPLE_HALF
		class LoopSelector:
			SelectedPlaying = Rgb.PURPLE
			Playing = Rgb.PURPLE_HALF
			Selected = Rgb.AMBER
			InLoop = Rgb.GREEN
		class Quantization:
			One=Rgb.BLACK
			Two=Rgb.GREEN_HALF
			Three=Rgb.GREEN
			Four=Rgb.GREEN
		class NoteSelector:
			class Octave:
				On = Rgb.GREEN
				Off = Rgb.GREEN_HALF
			Selected = Rgb.ORANGE
			Playing = Rgb.RED
		class NoteEditor:
			class VelocityShifted:
				On = Rgb.ORANGE
				Off = Rgb.ORANGE_HALF
			Velocity1 = Rgb.BLACK
			Velocity2 = Rgb.GREEN_HALF
			Velocity3 = Rgb.GREEN
			Muted = Rgb.AMBER
			Playing = Rgb.RED
			Metronome = Rgb.BLUE
				
	class StepSequencer2:
		class Pitch:
			On = Rgb.GREEN
			Off = Rgb.BLACK
			OnDim = Rgb.GREEN_HALF
			OffDim = Rgb.BLACK
		class Octave:
			On = Rgb.RED
			Off = Rgb.BLACK
			OnDim = Rgb.RED_HALF
			OffDim = Rgb.BLACK
		class Velocity:
			On = Rgb.AMBER
			Off = Rgb.BLACK
			OnDim = Rgb.AMBER_HALF
			OffDim = Rgb.BLACK
		class Length:
			On = Rgb.AMBER
			Off = Rgb.BLACK
			OnDim = Rgb.AMBER_HALF
			OffDim = Rgb.BLACK
			MetronomeInPage = Rgb.RED
			MetronomeInOtherPage = Rgb.RED_HALF
		class Random:
			On = Rgb.GREEN
			Off = Rgb.GREEN_HALF
		class NoteEditor:
			MetronomeInPage = Rgb.BLUE
			MetronomeInOtherPage = Rgb.BLUE_HALF
			PlayInPage = Rgb.RED
			PlayInOtherPage = Rgb.RED_HALF
			
	class Recording:
		On = Rgb.RED
		Off = Rgb.RED_HALF
		Transition = Rgb.RED_BLINK

	class DrumGroup:
		PadEmpty = Rgb.BLACK
		PadFilled = Rgb.YELLOW
		PadSelected = Rgb.LIGHT_BLUE
		PadSelectedNotSoloed = Rgb.LIGHT_BLUE
		PadMuted = Rgb.DARK_ORANGE
		PadMutedSelected = Rgb.LIGHT_BLUE
		PadSoloed = Rgb.DARK_BLUE
		PadSoloedSelected = Rgb.LIGHT_BLUE
		PadInvisible = Rgb.BLACK
		PadAction = Rgb.RED
		class Mute:
			On = Rgb.ORANGE
			Off = Rgb.DARK_ORANGE
		class Solo:
			On = Rgb.BLUE
			Off = Rgb.DARK_BLUE
	class Instrument:
		FeedbackRecord = Rgb.RED
		Feedback = Rgb.GREEN
		
		class Note:
			Root = Rgb.BLUE
			InScale = Rgb.LIGHT_BLUE_HALF
			Highlight = Rgb.LIGHT_BLUE
			OutOfScale = Rgb.BLACK
			Invalid = Rgb.BLACK
			
	class Scale:
		AbsoluteRoot = Rgb.RED
		RelativeRoot = Rgb.RED_HALF
		RelativeScale = Rgb.BLUE_HALF
		CircleOfFifths = Rgb.BLUE_HALF
		class QuickScale:
			On = Rgb.RED
			Off = Rgb.RED_HALF
		class Mode:
			On = Rgb.RED
			Off = Rgb.RED_HALF
		class Octave:
			On = Rgb.RED
			Off = Rgb.RED_HALF
		class Modus:
			On = Rgb.BLUE
			Off = Rgb.BLUE_HALF
		class Key:		
			On = Rgb.GREEN
			Off = Rgb.GREEN_HALF

	class Mode:

		class Session:
			On = Rgb.GREEN
			Off = Rgb.GREEN_HALF

		class Chromatic:
			On = Rgb.LIGHT_BLUE
			Off = Rgb.LIGHT_BLUE_HALF

		class Note:
			On = Rgb.LIGHT_BLUE
			Off = Rgb.LIGHT_BLUE_HALF

		class Drum:
			On = Rgb.YELLOW
			Off = Rgb.YELLOW_HALF

		class Device:
			On = Rgb.PURPLE
			Off = Rgb.PURPLE_HALF
		
		class StepSequencer:
			On = Rgb.MINT
			Off = Rgb.MINT_HALF
			
		class StepSequencer2:
			On = Rgb.ORANGE
			Off = Rgb.ORANGE_HALF
			
		class User:
			On = Rgb.DARK_BLUE
			Off = Rgb.DARK_BLUE_HALF

		class RecordArm:
			On = Rgb.RED
			Off = Rgb.RED_HALF

		class TrackSelect:
			On = Rgb.LIGHT_BLUE
			Off = Rgb.LIGHT_BLUE_HALF

		class Mute:
			On = Rgb.YELLOW
			Off = Rgb.YELLOW_HALF

		class Solo:
			On = Rgb.BLUE
			Off = Rgb.BLUE_HALF

		class Volume:
			On = Rgb.GREEN
			Off = Rgb.GREEN_HALF

		class Pan:
			On = Rgb.ORANGE
			Off = Rgb.ORANGE_HALF

		class Sends:
			On = Rgb.WHITE
			Off = Rgb.DARK_GREY

		class StopClip:
			On = Rgb.RED
			Off = Rgb.RED_HALF

	class Scrolling:
		Enabled = Rgb.YELLOW_HALF
		Pressed = Rgb.YELLOW
		Disabled = Rgb.BLACK

	class Misc:
		UserMode = Rgb.DARK_BLUE
		Shift = Rgb.DARK_GREY
		ShiftOn = Rgb.WHITE


def make_default_skin():
	return Skin(Colors)