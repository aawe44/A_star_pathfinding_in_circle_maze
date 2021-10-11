class Distances:
    def __init__(self, root):
        self.root = root
        self.cells = {}
        self.cells[self.root] = 0

    def root_to_cell(self, cell):
        return self.cells[cell]

    def add_cell_dist(self, cell, distance):
        self.cells[cell] = distance

    def get_cells_key(self):
        return self.cells.keys()
