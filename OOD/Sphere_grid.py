import OOD.PolarGrid as PolarGrid
import numpy as np
import matplotlib.pyplot as plt


class HemisphereCell(PolarGrid.PolarCell):
    def __init__(self, hemisphere, row, column):
        self.hemisphere = hemisphere
        super().__init__(row, column)


class HemispereGrid(PolarGrid.PolarGrid):
    def __init__(self, id, row):
        self.id = id
        self.row = row
        super().__init__("", row)

        self.grid = self.prepare_grid()
        self.configure_cells()
        self.distances = None

    def size(self, row):
        return len(self.grid[row])

    def prepare_grid(self):
        grid = ["" for _ in range(self.row)]

        angular_height = np.pi / (2 * self.row)

        grid[0] = [HemisphereCell(self.id, 0, 0)]

        for _row in range(1, self.row):
            # theta = (_row + 1) / angular_height
            # radius = np.sin(theta)

            radius = _row / self.row
            circumference = 2 * np.pi * radius

            previous_count = len(grid[_row - 1])
            estimated_cell_width = circumference / previous_count
            ratio = int(estimated_cell_width / angular_height)

            # print(previous_count, ratio, estimated_cell_width, circumference, previous_count)
            cells = int(previous_count * ratio)
            # print(cells)
            grid[_row] = [HemisphereCell(self.id, _row, col) for col in range(cells)]

        return grid


class SphereGrid(PolarGrid.Grid):

    def __init__(self, rows):
        self.equator = rows // 2
        super().__init__(rows, 1)
        return

    def prepare_grid(self):
        return [HemispereGrid(i, self.equator) for i in range(2)]

    def configure_cells(self):
        belt = self.equator - 1

        for idx in range(self.size(belt)):
            a, b = self.grid[0].grid[belt][idx], self.grid[1].grid[belt][idx]

            a.outward.append(b)
            b.outward.append(a)

    def size(self, row):
        return self.grid[0].size(row)

    def each_cell(self):

        total_cell = []

        for hemi in self.grid:
            for cell in hemi.each_cells():
                total_cell.append(cell)

        return total_cell

    def to_png(self, ideal_size=10):

        img_height = ideal_size * self.row
        img_width = self.grid[0].size(self.equator - 1) * ideal_size

        wall_color = "k"

        plt.plot([0, img_width], [0, 0], wall_color)
        plt.plot([0, img_width], [img_height, img_height], wall_color)

        for cell in self.each_cell():
            row_size = self.size(cell.row)
            cell_width = img_width / row_size

            x1 = cell.col * cell_width
            x2 = x1 + cell_width

            y1 = cell.row * ideal_size
            y2 = y1 + ideal_size

            if cell.hemisphere > 0:
                y1 = img_height - y1
                y2 = img_height - y2

            # x1 = int(x1)
            # x2 = int(x2)
            #
            # y1 = int(y1)
            # y2 = int(y2)

            if cell.row > 0:
                if not cell.linked(cell.cw):
                    plt.plot([x2, x2], [y1, y2], wall_color)

                if not cell.linked(cell.inward):
                    plt.plot([x1, x2], [y1, y1], wall_color)

            if cell.hemisphere == 0 and cell.row == self.equator - 1:
                if not cell.linked(cell.outward[0]):
                    plt.plot([x1, x2], [y2, y2], wall_color)

        print([(cell.row, cell.col) for cell in self.each_cell()])
        plt.show()

    def to_color_png(self, ideal_size=10):

        img_height = ideal_size * self.row
        img_width = self.grid[0].size(self.equator - 1) * ideal_size

        wall_color = "k"

        max_d = max(self.distances.cells.values())

        fig, ax = plt.subplots()

        plt.plot([0, img_width], [0, 0], wall_color)
        plt.plot([0, img_width], [img_height, img_height], wall_color)

        for cell in self.each_cell():
            row_size = self.size(cell.row)
            cell_width = img_width / row_size

            x1 = cell.col * cell_width
            x2 = x1 + cell_width

            y1 = cell.row * ideal_size
            y2 = y1 + ideal_size

            if cell.hemisphere > 0:
                y1 = img_height - y1
                y2 = img_height - y2

            curr_d = self.distances.cells[cell]
            intensity = (max_d - curr_d) / max_d
            dark = intensity
            bright = (128 + 127 * intensity) / 255

            ax.fill_between([x1, x2], [y1] * 2, [y2] * 2, color=(dark, dark, bright))

            if cell.row > 0:
                if not cell.linked(cell.cw):
                    plt.plot([x2, x2], [y1, y2], wall_color)

                if not cell.linked(cell.inward):
                    plt.plot([x1, x2], [y1, y1], wall_color)

            if cell.hemisphere == 0 and cell.row == self.equator - 1:
                if not cell.linked(cell.outward[0]):
                    plt.plot([x1, x2], [y2, y2], wall_color)

        print([(cell.row, cell.col) for cell in self.each_cell()])
        plt.show()
