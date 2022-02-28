import matplotlib.pyplot as plt
from multipledispatch import dispatch
import numpy as np
from opentrons import protocol_api
from sklearn.datasets import load_digits

# metadata
metadata = {
	"protocolName": "Pipette Printer",
    "author": "Rico Meinl <dev@rmeinl.com>",
    "description": "A simple protocol template for the pipette printing lab.",
    "apiLevel": "2.11"
}


class Canvas:
    def __init__(self, well_rows=8, well_cols=12, depth=4, depth_map={}):
        self._wells = well_rows*well_cols
        self._well_rows = well_rows
        self._well_cols = well_cols
        self._row_map = {chr(65+i): i for i in range(well_rows)}
        self._rev_row_map = {v:k for k,v in self._row_map.items()}
        self._col_map = {i+1: i for i in range(well_cols)}
        self._rev_col_map = {v:k for k,v in self._col_map.items()}
        self._depth = depth
        self._depth_map = {i+1: i for i in range(depth)} if not depth_map else depth_map
        self._board = np.zeros((well_rows, well_cols, depth))

    @dispatch(int, int, int, float)
    def set(self, row, col, depth, amount):
        _depth = self._depth_map.get(depth, depth)
        self._board[row][col][_depth] += amount

    @dispatch(str, int, float)
    def set(self, well, depth, amount):
        row, col = self.well_to_array_idx(well)
        self.set(row, col, depth, amount)

    def well_to_array_idx(self, well: str):
        row, col = well[0], int(well[1:])
        return self._row_map[row], self._col_map[col]

    def array_idx_to_well(self, row: int, col: int):
        row_char = self._rev_row_map[row]
        col_int = self._rev_col_map[col]
        return row_char+str(col_int)

    def draw(self, cmap_name=None):
        plt.figure(figsize=(self._well_rows, self._well_cols))
        plt.imshow(self._board)
        plt.xticks(list(self._col_map.values()), list(self._col_map.keys()))
        plt.yticks(list(self._row_map.values()), list(self._row_map.keys()))
        if cmap_name:
            plt.set_cmap(cmap_name)
        plt.savefig("test.png")
        plt.close()


def rgb2gray(r, g, b):
    return 0.299 * r + 0.587 * b + 0.114 * g


def run(protocol: protocol_api.ProtocolContext):
    # labware
    # tiprack_p20 = protocol.load_labware("opentrons_96_tiprack_20ul", "1")
    palette = protocol.load_labware("usascientific_12_reservoir_22ml", "2")
    tiprack_p300 = protocol.load_labware("opentrons_96_tiprack_300ul", "4")
    canvas = protocol.load_labware("nest_96_wellplate_200ul_flat", "5")
    
    # pipettes
    # left_pipette = protocol.load_instrument(
    #     "p20_single_gen2", "left", tip_racks=[tiprack_p20]
    # )
    right_pipette = protocol.load_instrument(
        "p300_single_gen2", "right", tip_racks=[tiprack_p300]
    )

    digits = load_digits()
    # We only have 4 colors so we divide each pixel by 4 to end up with 4 values
    depth = 1
    data = digits.images // depth
    digit = data[0]
    sim_canvas = Canvas(depth=depth)
    # depth_map = {i:f"A{i+1}" for i in range(depth)}

    # commands
    for iy, ix in np.ndindex(digit.shape):
        depth_val = digit[iy, ix]
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
        canvas_well = sim_canvas.array_idx_to_well(iy, ix_shifted)
        right_pipette.dispense(amount, canvas[canvas_well])
        # Simulate canvas in Canvas obj
        sim_canvas.set(canvas_well, 1, amount)
        right_pipette.drop_tip()

    sim_canvas.draw(cmap_name="Reds")