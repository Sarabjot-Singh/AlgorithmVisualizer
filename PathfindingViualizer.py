from queue import PriorityQueue
import pygame
import win32api

# defining color constants
WHITE = (255, 255, 255) # White Color Code
RED = (255, 0, 0) # Red Color Code
GREEN = (0, 255, 0) # Green Color Code
BLUE = (0, 0, 255) # Blue Color Code
BLACK = (0, 0, 0) # Black Color Code
PURPLE = (128, 0, 128) # Purple Color Code
ORANGE = (255, 165, 0) # Orange Color Code
TURQUOISE = (64, 224, 208) # Turquoise Color Code

def make_grid(rows, width):
    '''Data structure to hold the nodes #backend'''
    gap = width // rows
    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(rows):
            node = Node(row, col, gap, rows)
            grid[row].append(node)

    return grid

def draw_grid(win, rows, width):
    # This function just draw the grid lines  on the pygame window
    gap = width // rows
    # Horizontal lines
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap),(width, i * gap))

    # vertical lines
    for i in range(rows):
        pygame.draw.line(win, BLACK, (i * gap, 0),(i * gap, width))

def get_clicked_position(rows, width, pos):
    # This function returns the row and coloumn of Node in pygame Window
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row,col

def fill_grid(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in  row:
            node.draw(win) # not recursion just draw the rectangle in windows representing the node

    draw_grid(win, rows, width) # drawing grid upon the rectangle node objects
    pygame.display.update() # updating the pygame display

def make_trace(path_dict, current, fill_grid):
    # This function create/draws optimal path
    while current in path_dict:
        current = path_dict[current]
        current.make_path()
        fill_grid()

class Node:
    def __init__(self,row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.color = WHITE
        self.x = row * width #actual position of x-coor in pygame window.
        self.y = col * width #actual position of y-coor in pygame window.
        self.total_rows = total_rows #just to avoid global variable.
        self.neighbour_nodes = [] # i.e top, left, right, bottom
    #
    #                     n2
    #                     |
    #               n3 -- n1 -- n4
    #                     |
    #                     n5
    #
    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == TURQUOISE

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == BLUE

    def reset_node(self):
        self.color = WHITE

    def make_close(self):
        self.color = TURQUOISE

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid): #just test if neighbouris barrier or not if not a barrier append the node to neighbours list
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
    #       CHECKING BOTTOM NODE OF CURRENT NODE
            self.neighbour_nodes.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
    #       CHECKING UPPER NODE OF CURRENT NODE
            self.neighbour_nodes.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
    #       CHECKING RIGHT NODE OF CURRENT NODE
            self.neighbour_nodes.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
    #       CHECKING LEFT NODE OF CURRENT NODE
            self.neighbour_nodes.append(grid[self.row][self.col - 1])
    def make_path(self):
        self.color = PURPLE

#ALGORITHM FUNCTIONS

def heuristics(node1_coor, node2_coor):
    x1, y1 = node1_coor
    x2, y2 = node2_coor
    return abs(x2 - x1) + abs(y2 - y1) # it gives us estimated distance bt current node and end node
    # uses manhattan distance to calculate the estimated distance

def main(win, width): #THIS IS HEART FUNCTION FOR ALL FUNCTIONS
    win32api.MessageBox(0, 'This is path finder visualizer please read before continue', 'ALERT')
    win32api.MessageBox(0, 'Contains three algorithms namely Dijkstras, A-star, Best-First', 'ALERT')
    win32api.MessageBox(0, 'First select start and end node and barrier nodes', 'ALERT')
    win32api.MessageBox(0, 'Press following to visualize\n'
                           'Press A for A-Star\n'
                           'Press D for Dijkstras\n'
                           'Press B for Best-First\n'
                           'Press C to reset Grid', 'ALERT')
    ROWS = 50 # 50 by 50 grid
    grid = make_grid(ROWS, width)

    start = None # setting start node to None in whole grid
    end = None # setting end node to None  in the grid

    run = True
    while run:
        fill_grid(win, grid, ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                # print(pos)
                row, col = get_clicked_position(ROWS, width, pos)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(ROWS, width, pos)
                node = grid[row][col]
                node.reset_node()

                if node == start:
                    start = None

                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                for row in grid:
                    for node in row:
                        node.update_neighbours(grid)
                if event.key == pygame.K_a and start and end: # checking f start and end are defined
                    A_star(lambda: fill_grid(win, grid, ROWS, width), start, end, grid)

                elif event.key == pygame.K_d and start and end:
                    Dijkstras(lambda: fill_grid(win, grid, ROWS, width), start, end, grid)

                elif event.key == pygame.K_b and start and end:
                    Best_First(lambda: fill_grid(win, grid, ROWS, width), start, end, grid)

                # RESETING THE GRID
                elif event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                else:
                    win32api.MessageBox(0, 'Press following to visualize\n'
                       'Press A for A-Star\n'
                       'Press D for Dijkstras\n'
                       'Press B for Best-First\n'
                       'Press C to Reset the grid', 'ALERT')


    pygame.quit() #if event type is quit then this is invoked


def A_star(function_draw, start, end, grid):
    ''' A-STAR ALGORITHM '''
    count = 0
    nodes_priority_wise = PriorityQueue() # always chooses node with least f_score
    nodes_priority_wise.put((0, count, start)) # (f_score, count, current_node)
    nodes_g_scores = {node: float("inf") for row in grid for node in row}
    nodes_g_scores[start] = 0
    nodes_f_scores = {node: float("inf") for row in grid for node in row}
    nodes_f_scores[start] = heuristics(start.get_position(), end.get_position())
    path_dict = {}

    node_set = {start} # initially only start in node set

    while not nodes_priority_wise.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = nodes_priority_wise.get()[2]
        node_set.remove(current)

        if current == end:
            make_trace(path_dict, current, function_draw)
            return

        for neighbor in current.neighbour_nodes:
            # checking every neighbor's g_score
            n_g_score = nodes_g_scores[current] + 1

            if n_g_score < nodes_g_scores[neighbor]:
                path_dict[neighbor] = current
                nodes_g_scores[neighbor] = n_g_score
                nodes_f_scores[neighbor] = n_g_score + heuristics(neighbor.get_position(), end.get_position())
                # updating f_score so that priority queue can work
                if neighbor not in node_set:
                    count += 1
                    node_set.add(neighbor)
                    nodes_priority_wise.put((nodes_f_scores[neighbor], count, neighbor))
                    neighbor.make_open()

        function_draw()

        if current != start:
            current.make_close() #making everynode visited node a close node
    pygame.quit()

def Dijkstras(function_draw, start, end, grid):
    ''' DIJKSTRA'S ALGORITHM '''
    count = 0
    nodes_priority_wise = PriorityQueue() # always chooses node with least f_score
    nodes_priority_wise.put((0, count, start)) # (f_score, count, current_node)
    nodes_g_scores = {node: float("inf") for row in grid for node in row}
    nodes_g_scores[start] = 0
    path_dict = {}

    node_set = {start} # initially only start in node set

    while not nodes_priority_wise.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # GETTING THE NODE WITH HIGHEST PRIORITY (F'SCORE)
        current = nodes_priority_wise.get()[2]
        node_set.remove(current)

        if current == end:
            make_trace(path_dict, current, function_draw)
            return

        for neighbor in current.neighbour_nodes:
            # checking every neighbor's g_score
            n_g_score = nodes_g_scores[current] + 1

            if n_g_score < nodes_g_scores[neighbor]:
                path_dict[neighbor] = current
                nodes_g_scores[neighbor] = n_g_score
                # updating f_score so that priority queue can work
                if neighbor not in node_set:
                    count += 1
                    node_set.add(neighbor)
                    nodes_priority_wise.put((nodes_g_scores[neighbor], count, neighbor))
                    neighbor.make_open()
        if current != start:
            current.make_close() #making start node a close node

        function_draw()


    pygame.quit()


def Best_First(function_draw, start, end, grid):
    ''' BEST-FIRST ALGORITHM '''
    count = 0
    nodes_priority_wise = PriorityQueue() # always chooses node with least f_score
    nodes_priority_wise.put((0, count, start)) # (f_score, count, current_node)
    nodes_g_scores = {node: float("inf") for row in grid for node in row}
    nodes_g_scores[start] = 0
    nodes_f_scores = {node: float("inf") for row in grid for node in row}
    nodes_f_scores[start] = heuristics(start.get_position(), end.get_position())
    path_dict = {}

    node_set = {start} # initially only start in node set

    while not nodes_priority_wise.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = nodes_priority_wise.get()[2]
        node_set.remove(current)

        if current == end:
            make_trace(path_dict, current, function_draw)
            return

        for neighbor in current.neighbour_nodes:
            # checking every neighbor's g_score
            n_g_score = nodes_g_scores[current] + 1

            if n_g_score < nodes_g_scores[neighbor]:
                path_dict[neighbor] = current
                nodes_g_scores[neighbor] = n_g_score
                nodes_f_scores[neighbor] = heuristics(neighbor.get_position(), end.get_position())
                # updating f_score so that priority queue can work
                if neighbor not in node_set:
                    count += 1
                    node_set.add(neighbor)
                    nodes_priority_wise.put((nodes_f_scores[neighbor], count, neighbor))
                    neighbor.make_open()

        function_draw()

        if current != start:
            current.make_close() #making start node a close node
    pygame.quit()

def run():

    win = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('PATH FINDING VISUALIZER')
    main(win, 800)

