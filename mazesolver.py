import time
from tkinter import Tk, BOTH, Canvas

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.start_point.x, self.start_point.y,
            self.end_point.x, self.end_point.y,
            fill=fill_color, width=2
        )

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Tkinter Window")
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_cell(self, cell):
        cell.draw(self.__canvas)

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False  # Track if the cell has been visited
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win

    def draw(self, canvas):
        background_color = "#d9d9d9"
        if self.has_left_wall:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="black")
        else:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill=background_color)
        if self.has_top_wall:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="black")
        else:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill=background_color)
        if self.has_right_wall:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="black")
        else:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill=background_color)
        if self.has_bottom_wall:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="black")
        else:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill=background_color)
            
    def draw_move(self, to_cell, undo=False):
        # Calculate the centers of the current and target cells
        current_center_x = (self._x1 + self._x2) / 2
        current_center_y = (self._y1 + self._y2) / 2
        target_center_x = (to_cell._x1 + to_cell._x2) / 2
        target_center_y = (to_cell._y1 + to_cell._y2) / 2

        # Determine the color of the move
        fill_color = "red" if not undo else "gray"

        # Draw the line representing the move
        if self._win:
            self._win.draw_line(Line(Point(current_center_x, current_center_y), 
                                     Point(target_center_x, target_center_y)), fill_color)



import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)  # Start breaking walls from the top-left corner
        self._reset_cells_visited()  # Reset the visited property for all cells

    def _create_cells(self):
        for row in range(self.num_rows):
            row_cells = []
            for col in range(self.num_cols):
                cell_x1 = self.x1 + col * self.cell_size_x
                cell_y1 = self.y1 + row * self.cell_size_y
                cell_x2 = cell_x1 + self.cell_size_x
                cell_y2 = cell_y1 + self.cell_size_y
                cell = Cell(cell_x1, cell_y1, cell_x2, cell_y2, self.win)
                row_cells.append(cell)
            self._cells.append(row_cells)
        if self.win:
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    self._draw_cell(row, col)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        if self.win:
            self.win.draw_cell(cell)
            self._animate()

    def _animate(self):
        if self.win:
            self.win.redraw()
            time.sleep(0.05)
            
    def _break_entrance_and_exit(self):
        # Remove the top wall of the top-left cell (entrance)
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        # Remove the bottom wall of the bottom-right cell (exit)
        self._cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)
        
    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            directions = []

            # Check each direction for unvisited neighbors
            if i > 0 and not self._cells[i - 1][j].visited:
                directions.append(("up", i - 1, j))
            if i < self.num_rows - 1 and not self._cells[i + 1][j].visited:
                directions.append(("down", i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                directions.append(("left", i, j - 1))
            if j < self.num_cols - 1 and not self._cells[i][j + 1].visited:
                directions.append(("right", i, j + 1))

            if len(directions) == 0:
                self._draw_cell(i, j)
                return

            direction, ni, nj = random.choice(directions)

            if direction == "up":
                current_cell.has_top_wall = False
                self._cells[ni][nj].has_bottom_wall = False
            elif direction == "down":
                current_cell.has_bottom_wall = False
                self._cells[ni][nj].has_top_wall = False
            elif direction == "left":
                current_cell.has_left_wall = False
                self._cells[ni][nj].has_right_wall = False
            elif direction == "right":
                current_cell.has_right_wall = False
                self._cells[ni][nj].has_left_wall = False

            self._draw_cell(i, j)
            self._draw_cell(ni, nj)
            self._animate()

            self._break_walls_r(ni, nj)
            
    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
                
    def solve(self):
        return self._solve_r(0, 0)
                
    def _solve_r(self, i, j):
        # Call the animate method to visualize the solving process
        self._animate()

        current_cell = self._cells[i][j]
        current_cell.visited = True

        # If at the end cell (bottom-right corner), return True
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        # Possible moves: (direction, next_i, next_j)
        directions = [
            ("up", i - 1, j),
            ("down", i + 1, j),
            ("left", i, j - 1),
            ("right", i, j + 1)
        ]

        # For each possible direction
        for direction, ni, nj in directions:
            # Check boundaries and wall existence
            if 0 <= ni < self.num_rows and 0 <= nj < self.num_cols:
                next_cell = self._cells[ni][nj]

                if not next_cell.visited:
                    # Check if there's no wall blocking the way
                    if (direction == "up" and not current_cell.has_top_wall and not next_cell.has_bottom_wall) or \
                       (direction == "down" and not current_cell.has_bottom_wall and not next_cell.has_top_wall) or \
                       (direction == "left" and not current_cell.has_left_wall and not next_cell.has_right_wall) or \
                       (direction == "right" and not current_cell.has_right_wall and not next_cell.has_left_wall):

                        # Draw move (you can customize the drawing logic as needed)
                        current_cell.draw_move(next_cell)

                        # Recursively attempt to solve from the next cell
                        if self._solve_r(ni, nj):
                            return True

                        # Undo move if not successful
                        current_cell.draw_move(next_cell, undo=True)

        return False

# Main function
if __name__ == "__main__":
    win = Window(800, 600)
    maze = Maze(50, 50, 7, 7, 100, 100, win)  # Create a 5x5 maze

    solved = maze.solve()  # Attempt to solve the maze
    if solved:
        print("The maze was solved!")
    else:
        print("No solution found.")

    win.wait_for_close()
