# i consider all the nodes to have weight of 1
# the goal of this algorithm is to find the shortest path

# About the algorithms 
# A star is an informed search algorithm so it wont consider irrelevant nodes 
# there's a priority queue/open set that keeps track of the nodes we are gonna go to 
# it determines what's going next by distance, F(n) = G(n) + H(n) 
# H(n) is the manhattan or euclidean distance from that node to destination (guess) 
# G(n) is the current shortest distance from start to current node 
# also it stores the node it came from\n 
# Dijkstra's algorithm is more inefficient but doesn't require any information, the priority queue just stores the distance 

print("Instructions:")
print("right click: to place start, end, and barriers")
print("left click: remove")
print("r: generate a random maze")
print("m: A* path finding algorithm w/Manhattan distance")
print("e: A* path finding algorithm w/Euclidean distance")
print("d: Dijkstra's algorithm/BFS")
print("c: clear all")
print("s: soft reset")

import pygame
import math 
import random
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithms")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED 
    
    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED 
    
    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self,grid):
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # down neighbor
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # up neighbor
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # right neighbor
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row > 0 and not grid[self.row][self.col - 1].is_barrier(): # left neighbor
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other): # for priority queue, doesn't rly matter too much
        return False
    
def h(p1, p2): #heuristic function
    # Adding euclidean distance to heuristic function, #addition 5
    if euclidean == 1:
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
    current.make_start()

def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # priority, tiebreaker, data
    came_from = {} # for reconstructing path
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

# dijkstra's algorithm, addition #4
def dijkstra(draw, grid, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start)) 
    came_from = {} 
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[1]
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_f_score = f_score[current] + 1
            if temp_f_score < f_score[neighbor]:
                came_from[neighbor] = current
                f_score[neighbor] = temp_f_score
                open_set.put((f_score[neighbor], neighbor))
                neighbor.make_open()
                

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# fills barriers on the sides of the window, addition #1
def fill_edges(win, grid):
    for i in range(0, len(grid)):
        grid[0][i].make_barrier()
        grid[len(grid[0]) - 1][i].make_barrier()
        grid[i][0].make_barrier()
        grid[i][len(grid[0]) - 1].make_barrier()

# keeps barriers, start, and end; addition #3
def soft_reset(win, grid, rows, width):
    win.fill(WHITE)

    for i in range(rows):
        for j in range(rows):
            spot = grid[i][j]
            if not spot.is_barrier() and not spot.is_start() and not spot.is_end():
                grid[i][j].reset()    
            spot.neighbors = []
            grid[i][j].draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

# made a random maze generator addition #6
def randMaze(grid):
    for row in grid:
        for spot in row:
            if random.randint(1, 10) < 3:
                spot.make_barrier()

def main(win, width):
    global euclidean
    euclidean = 0
    ROWS = 50
    grid = make_grid(ROWS, width)
    fill_edges(win, grid)

    start = None
    end = None
    
    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # left mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                # if click is out of range, addition #2
                if row < 0 or col < 0 or row > len(grid) - 1 or col > len(grid[0]) - 1:
                    continue
                spot = grid[row][col]
                if not start and spot != end:
                   start = spot
                   start.make_start()
                elif not end and spot != start:
                   end = spot
                   end.make_end()
                elif spot != end and spot != start:
                   spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]: # right mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if row < 0 or col < 0 or row > len(grid) - 1 or col > len(grid[0]) - 1:
                    continue
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e or event.key == pygame.K_d or event.key == pygame.K_m and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if event.key == pygame.K_e:
                        euclidean = 1
                    if event.key == pygame.K_m or event.key == pygame.K_e:
                        astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        euclidean = 0

                    if event.key == pygame.K_d:
                        dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c or event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    fill_edges(win, grid)
                    if event.key == pygame.K_r:
                        randMaze(grid)
                        draw(win, grid, ROWS, width)
                        start = grid[random.randint(1,ROWS-2)][random.randint(1,ROWS-2)]
                        start.make_start()
                        end = grid[random.randint(1,ROWS-2)][random.randint(1,ROWS-2)]
                        end.make_end()

                if event.key == pygame.K_s:
                    soft_reset(win, grid, ROWS, width)
            
    pygame.quit()

main(WIN, WIDTH)
