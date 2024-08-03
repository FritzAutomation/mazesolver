import unittest
from mazesolver import Maze, Cell

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)

    def test_maze_different_dimensions(self):
        num_cols = 8
        num_rows = 8
        m2 = Maze(0, 0, num_rows, num_cols, 20, 20)
        self.assertEqual(len(m2._cells), num_rows)
        self.assertEqual(len(m2._cells[0]), num_cols)

        num_cols = 5
        num_rows = 15
        m3 = Maze(0, 0, num_rows, num_cols, 30, 30)
        self.assertEqual(len(m3._cells), num_rows)
        self.assertEqual(len(m3._cells[0]), num_cols)

    def test_break_entrance_and_exit(self):
        num_cols = 5
        num_rows = 5
        m4 = Maze(0, 0, num_rows, num_cols, 20, 20)

        # Initially, all walls should exist
        self.assertTrue(m4._cells[0][0].has_top_wall)
        self.assertTrue(m4._cells[num_rows - 1][num_cols - 1].has_bottom_wall)

        # Break the entrance and exit walls
        m4._break_entrance_and_exit()

        # The top wall of the entrance should be gone
        self.assertFalse(m4._cells[0][0].has_top_wall)
        # The bottom wall of the exit should be gone
        self.assertFalse(m4._cells[num_rows - 1][num_cols - 1].has_bottom_wall)
        
    # def test_break_entrance_and_exit(self):
    #     num_cols = 5
    #     num_rows = 5
    #     m4 = Maze(0, 0, num_rows, num_cols, 20, 20)

    #     # Debugging output: Check all initial walls
    #     for i, row in enumerate(m4._cells):
    #         for j, cell in enumerate(row):
    #             print(f"Cell ({i}, {j}) - Top: {cell.has_top_wall}, Bottom: {cell.has_bottom_wall}, Left: {cell.has_left_wall}, Right: {cell.has_right_wall}")

    #     # Ensure all walls are initially present
    #     self.assertTrue(m4._cells[0][0].has_top_wall, "Initial top wall should exist")
    #     self.assertTrue(m4._cells[num_rows - 1][num_cols - 1].has_bottom_wall, "Initial bottom wall should exist")

    #     # Break the entrance and exit walls
    #     m4._break_entrance_and_exit()

    #     # The top wall of the entrance should be removed
    #     self.assertFalse(m4._cells[0][0].has_top_wall, "Entrance wall should be removed")
    #     # The bottom wall of the exit should be removed
    #     self.assertFalse(m4._cells[num_rows - 1][num_cols - 1].has_bottom_wall, "Exit wall should be removed")

if __name__ == "__main__":
    unittest.main()
