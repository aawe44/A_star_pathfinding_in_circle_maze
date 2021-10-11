import  time
import numpy as np
import random
from .Grid import Grid as Grid
from .PolarCell import PolarCell as PolarCell
from .Wall import Wall as Wall
import matplotlib.pyplot as plt
import pygame

PI = np.pi


class PolarGrid(Grid):
    def __init__(self, distances, row, col=0):
        self.row = row
        self.col = row
        self.distances = distances
        self.walls = []
        super().__init__(row, self.col)

    def prepare_grid(self):
        rows = ["" for _ in range(self.row)]

        row_height = 1 / self.row
        rows[0] = [PolarCell(0, 0)]

        for row in range(1, self.row):
            radius = row / self.row
            circumference = 2 * PI * radius

            previous_count = len(rows[row - 1])
            estimated_cell_width = circumference / previous_count

            ratio = int(estimated_cell_width / row_height)

            cells = previous_count * ratio

            rows[row] = [PolarCell(row, col) for col in range(cells)]

        return rows

    def configure_cells(self):
        for cell in self.each_cells():
            row, col = cell.row, cell.col

            if row > 0:
                cell.cw = self.grid[row][(col + 1) % len(self.grid[row])]
                cell.ccw = self.grid[row][(col - 1) % len(self.grid[row])]

                ratio = len(self.grid[row]) / len(self.grid[row - 1])

                parent = self.grid[row - 1][int(col // ratio)]

                parent.outward.append(cell)
                cell.inward = parent

                wall = Wall(row, col, "s")
                wall.neighbor = [cell, cell.cw]
                self.walls.append(wall)

                wall = Wall(row, col, "r")
                wall.neighbor = [cell, parent]
                self.walls.append(wall)

        return

    def random_cell(self):
        row = random.randint(0, self.row - 1)
        col = random.randint(0, self.col - 1)
        return self.grid[row][col]

    def to_png(self, cell_size=10):

        img_size = 2 * self.row * cell_size

        center = img_size // 2

        fig, axs = plt.subplots()

        walls = []

        max_d = max(self.distances.cells.values())

        for cell in self.each_cells():
            if cell.row == 0:
                continue

            theta = 2 * PI / len(self.grid[cell.row])

            inner_radius = cell.row * cell_size
            outer_radius = inner_radius + cell_size

            theta_ccw = cell.col * theta
            theta_cw = theta_ccw + theta

            ax = center + (inner_radius * np.cos(theta_ccw))
            ay = center + (inner_radius * np.sin(theta_ccw))

            bx = center + (outer_radius * np.cos(theta_ccw))
            by = center + (outer_radius * np.sin(theta_ccw))

            cx = center + (inner_radius * np.cos(theta_cw))
            cy = center + (inner_radius * np.sin(theta_cw))

            dx = center + (outer_radius * np.cos(theta_cw))
            dy = center + (outer_radius * np.sin(theta_cw))

            if not cell.linked(cell.inward):
                walls.append([[ax, cx], [ay, cy]])

            if not cell.linked(cell.cw):
                walls.append([[cx, dx], [cy, dy]])

            ex, ey = None, None
            if cell.row + 1 == self.row or len(self.grid[cell.row]) != len(self.grid[cell.row + 1]):
                ex = center + (outer_radius * np.cos(theta_ccw + theta / 2))
                ey = center + (outer_radius * np.sin(theta_ccw + theta / 2))

            curr_d = self.distances.cells[cell]
            intensity = (max_d - curr_d) / (max_d)

            dark = intensity
            bright = (128 + 127 * intensity) / 255

            if ex is not None:
                xs = [ax, bx, ex, dx, cx]
                ys = [ay, by, ey, dy, cy]

            else:
                xs = [ax, bx, dx, cx]
                ys = [ay, by, dy, cy]

            plt.fill(xs, ys, color=(bright, dark, dark))

        for x, y in walls:
            plt.plot(x, y, "k")

        theta = np.arange(0, 2 * np.pi, 0.01)
        X = center + center * np.sin(theta)
        Y = center + center * np.cos(theta)
        plt.plot(X, Y, "k")

        axs.set_aspect('equal')
        plt.show()

    def to_ani(self, bg, cell_size=10):

        img_size = 2 * self.row * cell_size

        center = img_size // 2

        fig, axs = plt.subplots()

        walls = []

        max_d = max(self.distances.cells.values())

        for cell in self.each_cells():
            if cell.row == 0:
                continue

            theta = 2 * PI / len(self.grid[cell.row])

            inner_radius = cell.row * cell_size
            outer_radius = inner_radius + cell_size

            theta_ccw = cell.col * theta
            theta_cw = theta_ccw + theta

            ax = center + (inner_radius * np.cos(theta_ccw))
            ay = center + (inner_radius * np.sin(theta_ccw))

            bx = center + (outer_radius * np.cos(theta_ccw))
            by = center + (outer_radius * np.sin(theta_ccw))

            cx = center + (inner_radius * np.cos(theta_cw))
            cy = center + (inner_radius * np.sin(theta_cw))

            dx = center + (outer_radius * np.cos(theta_cw))
            dy = center + (outer_radius * np.sin(theta_cw))

            if not cell.linked(cell.inward):
                walls.append([[ax, cx], [ay, cy]])

            if not cell.linked(cell.cw):
                walls.append([[cx, dx], [cy, dy]])

            ex, ey = None, None
            if cell.row + 1 == self.row or len(self.grid[cell.row]) != len(self.grid[cell.row + 1]):
                ex = center + (outer_radius * np.cos(theta_ccw + theta / 2))
                ey = center + (outer_radius * np.sin(theta_ccw + theta / 2))

            curr_d = self.distances.cells[cell]
            intensity = (max_d - curr_d) / (max_d)

            dark = intensity
            bright = (128 + 127 * intensity) / 255

            if ex is not None:
                xs = [ax, bx, ex, dx, cx]
                ys = [ay, by, ey, dy, cy]

            else:
                xs = [ax, bx, dx, cx]
                ys = [ay, by, dy, cy]

            # plt.fill(xs, ys, color=(bright, dark, dark))
            pygame.draw.polygon(bg, (bright, dark, dark), [(x, y) for x in xs for y in ys])

        pygame.display.update()
        time.sleep(0.1)
        # for x, y in walls:
        #     plt.plot(x, y, "k")

        theta = np.arange(0, 2 * np.pi, 0.01)
        X = center + center * np.sin(theta)
        Y = center + center * np.cos(theta)
        plt.plot(X, Y, "k")

        axs.set_aspect('equal')
        # plt.show()
