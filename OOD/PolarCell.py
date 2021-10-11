from .Cell import Cell as Cell


class PolarCell(Cell):
    def __init__(self, row, col=0):

        self.row = row
        self.col = col

        self.cw = ""
        self.ccw = ""
        self.inward = ""
        self.outward = []

        self.accessor = ""
        self.links = {}
        self.north = ""
        self.south = ""
        self.east = ""
        self.west = ""

    def neighbors(self):
        arr = []
        if self.cw:
            arr.append(self.cw)

        if self.ccw:
            arr.append(self.ccw)

        if self.inward:
            arr.append(self.inward)

        arr += self.outward

        return arr
