import random
import matplotlib.pyplot as plt
from  .Cell import  Cell


class Grid:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.grid = self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self):
        grid = [[0] * self.col for _ in range(self.row)]

        for i in range(self.row):
            for j in range(self.col):
                grid[i][j] = Cell(i, j)

        return grid

    def configure_cells(self):
        for r in self.grid:
            for cell in r:
                row, col = cell.row, cell.col
                if row - 1 >= 0:
                    cell.north = self.grid[row - 1][col]

                if row + 1 < self.row:
                    cell.south = self.grid[row + 1][col]

                if col - 1 >= 0:
                    cell.west = self.grid[row][col - 1]

                if col + 1 < self.col:
                    cell.east = self.grid[row][col + 1]

    def random_cell(self):
        row = random.randint(0, self.row - 1)
        col = random.randint(0, self.col - 1)
        return self.grid[row][col]

    def size(self):
        return self.row * self.col

    def to_s(self):

        s = "+" + "---+" * self.col
        print(s)

        for r in self.grid:
            top = "|"
            bottom = "+"
            corner = "+"

            for cell in r:
                body = " " + self.contents_of(cell) + " "

                east_boundary = " " if cell.linked(cell.east) else "|"
                top += body + east_boundary

                sounth_boundary = "   " if cell.linked(cell.south) else "---"
                bottom += sounth_boundary + corner

            print(top)
            print(bottom)

    def each_cells(self):

        return [c for r in self.grid for c in r]

    def contents_of(self, cell):
        return " "

    def background_color_for(self, cell):
        return None

    def to_png(self, cell_size=25):

        img_width = cell_size * self.col
        img_height = cell_size * self.row

        background = "y"
        wall = "k"

        fig, ax = plt.subplots()

        walls = []

        for cell in self.each_cells():
            x1 = cell.col * cell_size
            y1 = img_height - cell.row * cell_size

            x2 = x1 + cell_size
            y2 = y1 - cell_size

            ax.fill_between([x1, x2], [y1] * 2, [y2] * 2, facecolor=background)

            line_width = 1

            if not cell.north:
                walls.append([[x1, x2], [y1] * 2, [y1 - line_width] * 2])

            if not cell.west:
                walls.append([[x1, x1 + line_width], [y1] * 2, [y2] * 2])

            if not cell.linked(cell.east):
                walls.append([[x2, x2 + line_width], [y1] * 2, [y2] * 2])

            if not cell.linked(cell.south):
                walls.append([[x1, x2], [y2] * 2, [y2 + line_width] * 2])

        for x, y1, y2 in walls:
            ax.fill_between(x, y1, y2, facecolor=wall)

        ax.set_aspect('equal')
        plt.show()
