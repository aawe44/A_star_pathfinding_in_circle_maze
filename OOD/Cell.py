from .Distances import  Distances as Distances

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.accessor = ""
        self.links = {}
        self.north = ""
        self.south = ""
        self.east = ""
        self.west = ""

    def link(self, cell, bidi=True):
        self.links[cell] = True
        if bidi:
            cell.link(self, False)

    def unlink(self, cell, bidi=True):
        del self.links[cell]
        if bidi:
            cell.unlink(self, False)

    def linked(self, cell):
        return self.links.get(cell, None)

    def neighbors(self):
        list = []

        if self.north:
            list.append(self.north)

        if self.south:
            list.append(self.south)

        if self.east:
            list.append(self.east)

        if self.west:
            list.append(self.west)

        return list

    def distances(self):

        distances = Distances(self)

        frontier = [self]

        while frontier:
            new_frontier = []

            for cell in frontier:

                for linked in cell.links:
                    if linked in distances.cells:
                        continue

                    distances.cells[linked] = distances.cells[cell] + 1
                    new_frontier.append(linked)

            frontier = new_frontier

        return distances
