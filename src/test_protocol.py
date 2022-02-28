from opentrons import protocol_api

# metadata
metadata = {
	'protocolName': 'Pipette Printer',
    'author': 'Alex Hadik <ahadik@mit.edu>',
    'description': 'A simple protocol template for the pipette printing lab.',
    'apiLevel': '2.11'
}

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    palette = protocol.load_labware('usascientific_12_reservoir_22ml', '2')
    canvas = protocol.load_labware('nest_96_wellplate_200ul_flat', '5')

    # pipettes
    left_pipette = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])

    # commands
    left_pipette.pick_up_tip()
    left_pipette.aspirate(100, palette['A1'])
    left_pipette.dispense(100, canvas['A1'])
    left_pipette.drop_tip()

    left_pipette.pick_up_tip()
    left_pipette.aspirate(100, palette['A2'])
    left_pipette.dispense(100, canvas['A2'])
    left_pipette.drop_tip()