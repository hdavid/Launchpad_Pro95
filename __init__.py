from _Framework.Capabilities import CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, SYNC, REMOTE, controller_id, inport, outport
from Launchpad_Pro95 import Launchpad_Pro95

def create_instance(c_instance):
	""" Creates and returns the Launchpad script """
	return Launchpad_Pro95(c_instance)

def get_capabilities():
	return {
		CONTROLLER_ID_KEY: controller_id(
			vendor_id = 4661, 
			product_ids = [81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96], 
			model_name = 
			[
				'Launchpad Pro',
				'Launchpad Pro 2',
				'Launchpad Pro 3',
				'Launchpad Pro 4',
			 	'Launchpad Pro 5',
				'Launchpad Pro 6',
				'Launchpad Pro 7',
				'Launchpad Pro 8',
				'Launchpad Pro 9',
				'Launchpad Pro 10',
				'Launchpad Pro 11',
				'Launchpad Pro 12',
				'Launchpad Pro 13',
				'Launchpad Pro 14',
				'Launchpad Pro 15',
				'Launchpad Pro 16'
			]
		),
		PORTS_KEY: 
			[
				inport(props = [NOTES_CC, SCRIPT, REMOTE]), 
				outport(props = [NOTES_CC, SCRIPT, SYNC, REMOTE])
			]
	}