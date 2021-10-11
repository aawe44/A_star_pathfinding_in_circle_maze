import sys

import pygame
import time
import os
import numpy as np
import random
import ch03
import matplotlib.pyplot as plt
import heapq
import collections

from OOD.PolarGrid import PolarGrid as  PolarGrid
from OOD.Distances import Distances as Distances

PI = np.pi
IS_DRAW_CARVE = False

WIDTH = 800
HEIGHT = 800

n = 64
cell_size = WIDTH // n // 2

# set up pygame window
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
RED = (255, 200, 200)

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

GREEN_BLUE = (0, 255, 255)
RED_BLUE = (255, 0, 255)


def idx_to_pos(grid, row, col):
    img_size = 2 * n * cell_size

    center = img_size // 2 + WIDTH * 0.025

    theta = 2 * PI / len(grid[row])

    inner_radius = row * cell_size
    outer_radius = inner_radius + cell_size

    theta_ccw = col * theta
    theta_cw = theta_ccw + theta

    ax = center + (inner_radius * np.cos(theta_ccw))
    ay = center + (inner_radius * np.sin(theta_ccw))

    bx = center + (outer_radius * np.cos(theta_ccw))
    by = center + (outer_radius * np.sin(theta_ccw))

    cx = center + (inner_radius * np.cos(theta_cw))
    cy = center + (inner_radius * np.sin(theta_cw))

    dx = center + (outer_radius * np.cos(theta_cw))
    dy = center + (outer_radius * np.sin(theta_cw))

    ex, ey = None, None
    if row + 1 == len(grid) or len(grid[row]) != len(grid[row + 1]):
        ex = center + (outer_radius * np.cos(theta_ccw + theta / 2))
        ey = center + (outer_radius * np.sin(theta_ccw + theta / 2))

    if ex is not None:
        xs = [ax, bx, ex, dx, cx]
        ys = [ay, by, ey, dy, cy]

    else:
        xs = [ax, bx, dx, cx]
        ys = [ay, by, dy, cy]

    return [xs, ys, ax, ay, bx, by, cx, cy, dx, dy]


def draw_wall(grid, w):
    row, col, t = w.key

    xs, ys, ax, ay, bx, by, cx, cy, dx, dy = idx_to_pos(grid, row, col)

    if t == "r":
        pygame.draw.line(bg, BLACK, (ax, ay), (cx, cy), 1)
    else:
        pygame.draw.line(bg, BLACK, (cx, cy), (dx, dy), 1)


def draw_cell(grid, cell, d, max_d, c=None):
    row, col = cell.row, cell.col

    if cell.row == 0:
        return

    xs, ys, ax, ay, bx, by, cx, cy, dx, dy = idx_to_pos(grid, row, col)

    points = [(x, y) for x, y in zip(xs, ys)]

    curr_d = d
    intensity = (max_d - curr_d) / (max_d + 1)

    dark = intensity * 255
    bright = (128 + 127 * intensity)

    red = (bright, dark, dark)
    green = (0, bright, 0)
    blue = (dark, dark, bright)

    if c == "r":
        c = red
    elif c == "b":
        c = BLUE
    elif c == "g":
        c = green
    else:
        c = red

    pygame.draw.polygon(bg, c, points)
    return


def cell_to_pos(grid, cell):
    img_size = 2 * n * cell_size
    theta = 2 * PI / len(grid[cell.row])
    center = img_size // 2 + WIDTH * 0.025
    # center = 0
    inner_radius = cell.row * cell_size
    theta_ccw = cell.col * theta
    ax = center + (inner_radius * np.cos(theta_ccw))
    ay = center + (inner_radius * np.sin(theta_ccw))
    return ax, ay


def calculate(grid, x, y, nx, ny):
    x, y = cell_to_pos(grid, grid[x][y])
    nx, ny = cell_to_pos(grid, grid[nx][ny])
    dx = abs(x - nx)
    dy = abs(y - ny)
    return dx + dy


def draw_dist_a_start(grid, start, end, is_draw=False, is_BFS=False):
    walls = grid.walls
    grid = grid.grid

    bg.fill(WHITE)
    img_size = 2 * n * cell_size
    pygame.draw.arc(bg, BLACK, [WIDTH * 0.025, WIDTH * 0.025, img_size, img_size], 0, 2.05 * PI, 1)

    for wall in walls:
        if wall.is_draw:
            draw_wall(grid, wall)

    screen.blit(bg, (0, 0))
    pygame.display.update()

    start, end = grid[start[0]][start[1]], grid[end[0]][end[1]]

    er = end.row
    ec = end.col

    heap = []
    visited = set()

    cell_to_g = collections.defaultdict(None)
    cell_to_h = collections.defaultdict(None)
    cell_to_f = collections.defaultdict(None)

    cell_to_g[start] = 0
    cell_to_h[start] = 0
    cell_to_f[start] = 0

    heapq.heappush(heap, (cell_to_f[start], start.row, start.col))

    curr_to_prev = {start: None}
    draw_cell(grid, start, 250, 500)
    draw_cell(grid, end, 250, 500)

    def update_grid():

        for i, (x, y) in enumerate(sorted(list(visited))):
            k = len(visited)
            draw_cell(grid, grid[x][y], i + k // 2, 2 * k, "g")

        for _, x, y in heap:
            draw_cell(grid, grid[x][y], 250, 500, "b")

        for wall in walls:
            if wall.is_draw:
                draw_wall(grid, wall)

        draw_cell(grid, start, 250, 500, "r")
        draw_cell(grid, end, 250, 500, "r")

        screen.blit(bg, (0, 0))
        pygame.display.update()
        return

    is_found = False
    while heap and not is_found:

        for _ in range(len(heap)):

            curr_f, x, y = heapq.heappop(heap)
            visited.add((x, y))

            if x == end.row and y == end.col:
                update_grid()
                is_found = True
                break

            curr = grid[x][y]
            for next_node in curr.links:

                if (next_node.row, next_node.col) in visited:
                    continue

                nx, ny = next_node.row, next_node.col

                ng = cell_to_g[curr] + calculate(grid, x, y, nx, ny)
                nh = 0 if is_BFS else calculate(grid, nx, ny, er, ec)
                nf = ng + nh

                if next_node in cell_to_f and nf >= cell_to_f[next_node]:
                    continue

                visited.add((next_node.row, next_node.col))
                heapq.heappush(heap, (nf, nx, ny))
                curr_to_prev[next_node] = curr

                cell_to_g[next_node] = ng
                cell_to_h[next_node] = nh
                cell_to_f[next_node] = nf

        if is_draw:
            update_grid()

    # build path
    path = []
    curr = end
    total = 0
    while curr is not None:
        if curr in curr_to_prev:
            prev = curr_to_prev[curr]
            if prev:
                total += calculate(grid, curr.row, curr.col, prev.row, prev.col)
        path.append(curr)
        curr = curr_to_prev[curr]

    if is_draw:
        draw_cell(grid, start, len(path) - 1, len(path))
        draw_cell(grid, end, len(path) // 2, len(path))
        k = len(path)

        path = path[::-1]
        path = [(i, p) for i, p in enumerate(path)]

        step = 5
        while path:
            curr = path[:step]
            path = path[step:]

            for i, cell in curr:
                draw_cell(grid, cell, i + k // 2, 2 * k, "r")

            for wall in walls:
                if wall.is_draw:
                    draw_wall(grid, wall)

            screen.blit(bg, (0, 0))
            pygame.display.update()

        time.sleep(5)
    return len(path)


def recursion(grid, walls):
    if IS_DRAW_CARVE:
        bg.fill(WHITE)
        img_size = 2 * n * cell_size
        pygame.draw.arc(bg, BLACK, [WIDTH * 0.025, WIDTH * 0.025, img_size, img_size], 0, 2.05 * PI, 1)

        for wall in walls:
            if wall.is_draw:
                draw_wall(grid, wall)

        screen.blit(bg, (0, 0))
        pygame.display.update()
        time.sleep(0.5)

    stack = [grid[0][0]]
    visited = set()
    visited.add(stack[0])

    while stack:
        cell = stack[-1]
        neighbors = []

        for nb in cell.neighbors():
            if nb not in visited:
                neighbors.append(nb)

        if neighbors:
            idx = random.randint(0, len(neighbors) - 1)
            neighbor = neighbors[idx]

            cell.link(neighbor)

            stack.append(neighbor)
            visited.add(neighbor)

            for w in walls:
                if cell in w.neighbor and neighbor in w.neighbor:
                    w.is_draw = False
        else:
            stack.pop()

        if IS_DRAW_CARVE:
            bg.fill(WHITE)
            pygame.draw.arc(bg, BLACK, [WIDTH * 0.025, WIDTH * 0.025, img_size, img_size], 0, 2.05 * PI, 1)

            for i, cell in enumerate(stack):
                draw_cell(grid, cell, i, len(stack))

            if stack:
                draw_cell(grid, stack[-1], len(stack), len(stack), (200, 255, 200))

            for wall in walls:
                if wall.is_draw:
                    draw_wall(grid, wall)

            screen.blit(bg, (0, 0))
            pygame.display.update()

    for cell in visited:
        cnt = 0
        neighbors = []
        for nb in cell.neighbors():
            if not cell.linked(nb):
                cnt += 1
                neighbors.append(nb)

        if cnt >= 3 and random.randint(1, 10) > 1:
            idx = random.randint(0, cnt - 1)
            neighbor = neighbors[idx]
            cell.link(neighbor)

            for w in walls:
                if cell in w.neighbor and neighbor in w.neighbor:
                    w.is_draw = False

    print("Done")
    # time.sleep(1)


class Pygrid(PolarGrid):
    def __init__(self, Distances, n, cell_size):
        PolarGrid.__init__(self, Distances, n, cell_size)



# initalise Pygame
xPos = 500
yPos = 0
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (xPos, yPos)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((int(WIDTH * 1.05), int(HEIGHT * 1.05)))
pygame.display.set_caption("Python Maze Generator")
clock = pygame.time.Clock()

bg = pygame.Surface(screen.get_size())
bg = bg.convert()
bg.fill(WHITE)

grid = Pygrid(Distances, n, cell_size)


def get_rand_pos():
    rows = len(grid.grid)
    x = random.randint(0, rows - 1)
    y = random.randint(0, len(grid.grid[x]) - 1)
    return x, y


rows = len(grid.grid)

char_to_pos = {
    "center": (1, 0),
    "left": (-1, len(grid.grid[-1]) // 2),
    "left_mid": (rows // 2, len(grid.grid[rows // 2]) // 2),
    "right": (-1, -1),
    "right_mid": (len(grid.grid) // 2, 0),
    "random": get_rand_pos()
}


def run_maze(start_type, end_type, cnt):
    start = char_to_pos[start_type] if start_type != "random" else get_rand_pos()
    end = char_to_pos[end_type] if end_type != "random" else get_rand_pos()

    if cnt == 0:
        recursion(grid.grid, grid.walls)

    is_draw = True
    draw_dist_a_start(grid, start, end, is_draw)
    draw_dist_a_start(grid, start, end, is_draw, True)



start_type = "center"
end_type = "right"

grid = Pygrid(Distances, n, cell_size)
recursion(grid.grid, grid.walls)

run_maze(start_type, end_type, 1)
run_maze(end_type, start_type, 1)

