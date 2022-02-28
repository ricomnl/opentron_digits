from opentrons import protocol_api

# metadata
metadata = {
	"protocolName": "Pipette Printer",
    "author": "Rico Meinl <dev@rmeinl.com>",
    "description": "A simple protocol template for the pipette printing lab.",
    "apiLevel": "2.11"
}

well_rows=8
well_cols=12
_row_map = {chr(65+i): i for i in range(well_rows)}
_rev_row_map = {v:k for k,v in _row_map.items()}
_col_map = {i+1: i for i in range(well_cols)}
_rev_col_map = {v:k for k,v in _col_map.items()}


def array_idx_to_well(row: int, col: int):
    row_char = _rev_row_map[row]
    col_int = _rev_col_map[col]
    return row_char+str(col_int)


def run(protocol: protocol_api.ProtocolContext):
    # labware
    tiprack_p20 = protocol.load_labware("opentrons_96_tiprack_20ul", "1")
    tiprack_p300 = protocol.load_labware("opentrons_96_tiprack_300ul", "4")
    palette = protocol.load_labware("usascientific_12_reservoir_22ml", "2")
    canvas = protocol.load_labware("nest_96_wellplate_200ul_flat", "5")
    
    # pipettes
    left_pipette = protocol.load_instrument(
        "p20_single_gen2", "left", tip_racks=[tiprack_p20]
    )
    right_pipette = protocol.load_instrument(
        "p300_single_gen2", "right", tip_racks=[tiprack_p300]
    )

    digit = [
        [ 0.,  0.,  5., 13.,  9.,  1.,  0.,  0.],
        [ 0.,  0., 13., 15., 10., 15.,  5.,  0.],
        [ 0.,  3., 15.,  2.,  0., 11.,  8.,  0.],
        [ 0.,  4., 12.,  0.,  0.,  8.,  8.,  0.],
        [ 0.,  5.,  8.,  0.,  0.,  9.,  8.,  0.],
        [ 0.,  4., 11.,  0.,  1., 12.,  7.,  0.],
        [ 0.,  2., 14.,  5., 10., 12.,  0.,  0.],
        [ 0.,  0.,  6., 13., 10.,  0.,  0.,  0.]
    ]
    # commands
    for iy in range(len(digit)):
        for ix in range(len(digit[iy])):
            depth_val = digit[iy][ix]
            # We shift the x because the letters are quadratic
            ix_shifted = ix + 2
            if depth_val == 0.:
                continue
            amount = depth_val * 10.
            # Pick up the tip
            right_pipette.pick_up_tip()
            # Aspirate from palette with index of depth
            right_pipette.aspirate(amount, palette["A1"])
            # Dispense the amount onto the canvas at given well
            canvas_well = array_idx_to_well(iy, ix_shifted)
            right_pipette.dispense(amount, canvas[canvas_well])
            # Simulate canvas in Canvas obj
            right_pipette.drop_tip()
