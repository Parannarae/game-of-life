from typing import List
from unittest import TestCase

from src.life import CellIndex, Life

class TestGetNeighbors(TestCase):
    def setUp(self):
        self.game = Life()
        # for the test purpose, change the min size
        self.game.MIN_GRID_HEIGHT = 2
        self.game.MIN_GRID_WIDTH = 2
        self.game.init_grid(5, 5, [])

    def test_get_neighbors(self):
        """Check if neighbor cells are returned.
        """
        neighbors = self.game.get_neighbors(CellIndex(1, 1))

        exp_res = [
            CellIndex(0, 0), CellIndex(0, 1), CellIndex(0, 2),
            CellIndex(1, 0), CellIndex(1, 2),
            CellIndex(2, 0), CellIndex(2, 1), CellIndex(2, 2),
        ]

        # order of list can be differ
        self.assertEqual(len(neighbors), len(exp_res))
        for cell in exp_res:
            self.assertTrue(cell in neighbors)

    def test_get_neighbors_target_cell_at_top_right_corner(self):
        """Check if neighbor cells are returned if the target cell is placed at the top right corner of the grid.
        """
        neighbors = self.game.get_neighbors(CellIndex(0, 4))

        exp_res = [            
            CellIndex(0, 3),
            CellIndex(1, 3), CellIndex(1, 4),
        ]
                
        # order of list can be differ
        self.assertEqual(len(neighbors), len(exp_res))
        for cell in exp_res:
            self.assertTrue(cell in neighbors)

    def test_get_neighbors_target_cell_at_bottom_left_corner(self):
        """Check if neighbor cells are returned if the target cell is placed at the bottom left corner of the grid.
        """
        neighbors = self.game.get_neighbors(CellIndex(4, 0))

        exp_res = [            
            CellIndex(3, 0), CellIndex(3, 1),
            CellIndex(4, 1),
        ]
        
        # order of list can be differ
        self.assertEqual(len(neighbors), len(exp_res))
        for cell in exp_res:
            self.assertTrue(cell in neighbors)


class TestGetNumberOfAliveNeighbors(TestCase):
    def setUp(self):
        self.game = Life()
        # for the test purpose, change the min size
        self.game.MIN_GRID_HEIGHT = 2
        self.game.MIN_GRID_WIDTH = 2
        self.game.init_grid(5, 5, [])

    def test_get_number_of_alive_neighbors_single_alive_cell(self):
        """Check all surrounding cells of an alive cell get the count of 1.
        """
        alive_cells = [CellIndex(2, 2)]
        for cur_cell in alive_cells:
            self.game.grid[cur_cell.row][cur_cell.column] = True
        self.game.alive_cells = alive_cells

        alive_neighbor_counter = self.game.get_number_of_alive_neighbors()

        exp_dict = {
            CellIndex(1, 1): 1,
            CellIndex(1, 2): 1,
            CellIndex(1, 3): 1,
            CellIndex(2, 1): 1,
            CellIndex(2, 3): 1,
            CellIndex(3, 1): 1,
            CellIndex(3, 2): 1,
            CellIndex(3, 3): 1,
        }

        self.assertEqual(alive_neighbor_counter, exp_dict)

    def test_get_number_of_alive_neighbors_two_alive_cells(self):
        """Check all surrounding cells of two alive cells.
        """
        alive_cells = [CellIndex(2, 2), CellIndex(3, 3)]
        for cur_cell in alive_cells:
            self.game.grid[cur_cell.row][cur_cell.column] = True
        self.game.alive_cells = alive_cells

        alive_neighbor_counter = self.game.get_number_of_alive_neighbors()

        exp_dict = {
            # neighbor of 2,2
            CellIndex(1, 1): 1,
            CellIndex(1, 2): 1,
            CellIndex(1, 3): 1,
            CellIndex(2, 1): 1,
            CellIndex(3, 1): 1,            
            CellIndex(3, 3): 1,
            
            # overlapping neighbor
            CellIndex(2, 3): 2,     
            CellIndex(3, 2): 2,

            # neighbor of 3,3
            CellIndex(2, 2): 1,
            CellIndex(2, 4): 1,
            CellIndex(3, 4): 1,
            CellIndex(4, 2): 1,
            CellIndex(4, 3): 1,            
            CellIndex(4, 4): 1,
        }

        self.assertEqual(alive_neighbor_counter, exp_dict)


class TestIsSurviveForTheNextGeneration(TestCase):
    def setUp(self):
        self.game = Life()
        # for the test purpose, change the min size
        self.game.MIN_GRID_HEIGHT = 2
        self.game.MIN_GRID_WIDTH = 2
        self.game.init_grid(5, 5, [])

    def setup_data_and_check_result(
            self, 
            is_alive: bool, 
            num_of_alive_neighbors: int, 
            exp_res: bool):
        """Set up the board, and check the result of `is_survive_for_the_next_generation`.
        
        Args:
            is_alive: whether the cell is alive in the current generation
            num_of_alive_neighbors: total number of alive neighbors in the current generation
            exp_res: status of the cell in the next generation
        """
        # position of the cell is not a big deal
        cell_to_check = CellIndex(2, 2)
        if is_alive:            
            self.game.grid[cell_to_check.row][cell_to_check.column] = True
            self.game.alive_cells = [cell_to_check]
        
        self.assertEqual(
            self.game.is_survive_for_the_next_generation(cell_to_check, num_of_alive_neighbors),
            exp_res
        )

    def test_is_survive_for_the_next_generation_live_cell_with_n_alive_neighbor(self):
        """Check the status of the alive cell for the next generation.        
        """        
        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=0,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=1,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=2,
            exp_res=True
        )

        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=3,
            exp_res=True
        )

        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=4,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=5,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=6,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=7,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=True,
            num_of_alive_neighbors=8,
            exp_res=False
        )

    def test_is_survive_for_the_next_generation_dead_cell_with_n_alive_neighbor(self):
        """Check the status of the dead cell for the next generation.        
        """        
        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=0,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=1,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=2,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=3,
            exp_res=True
        )

        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=4,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=5,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=6,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=7,
            exp_res=False
        )

        self.setup_data_and_check_result(
            is_alive=False,
            num_of_alive_neighbors=8,
            exp_res=False
        )
    

class TestProceedGeneration(TestCase):
    def setUp(self):
        self.game = Life()
        # for the test purpose, change the min size
        self.game.MIN_GRID_HEIGHT = 2
        self.game.MIN_GRID_WIDTH = 2

    def print_board(self):
        """Show the board's status to Stdout
        
        Args:
            cur_life: Current game status instance
        """
        print("==========Gen {}==========".format(self.game.generation))
        
        for cur_row in self.game.grid:
            print("  ".join(['o' if cur_col else 'x' for cur_col in cur_row]))
        
        print("====================")

    def check_result(self, 
                     num_of_rows: int, 
                     num_of_cols: int, 
                     exp_alive_cells: List[CellIndex],
                     generation: int):
        """Check the result of `proceed_generation`.
        
        Args:
            num_of_rows: total number of rows of the game board
            num_of_cols: total number of columns of the game board
            exp_alive_cells: list of alive cells in the next generation
            generation: generation number
        """
        # order of list can be differ
        self.assertEqual(len(self.game.alive_cells), len(exp_alive_cells))
        for cell in exp_alive_cells:
            self.assertTrue(cell in self.game.alive_cells)
        
        self.assertEqual(self.game.generation, generation)
        
        # check all grid
        for row in range(num_of_rows):
            for col in range(num_of_cols):
                cur_ind = CellIndex(row, col)
                cur_status = self.game.grid[cur_ind.row][cur_ind.column]
                if cur_ind in exp_alive_cells:
                    self.assertTrue(cur_status)
                else:
                    self.assertFalse(cur_status)
    
    def test_proceed_generation(self):
        """Check the game board after one generation.
        """
        num_of_rows = 5
        num_of_cols = 6
        self.game.init_grid(
            width=num_of_cols,
            height=num_of_rows,            
            init_alive_cells=[CellIndex(1, 1), CellIndex(2, 1), CellIndex(2, 2), CellIndex(2, 3)]
        )

        self.print_board()
        self.game.proceed_generation()        
        self.print_board()

        exp_alive_cells = [
            CellIndex(1, 1),
            CellIndex(2, 1),
            CellIndex(2, 2),
            CellIndex(3, 2),
        ]

        self.check_result(num_of_rows=num_of_rows, 
                          num_of_cols=num_of_cols, 
                          exp_alive_cells=exp_alive_cells,
                          generation=1)

    def test_proceed_generation_no_survival(self):
        """Check the game board where no cell survives after one generation.
        """
        num_of_rows = 5
        num_of_cols = 6
        self.game.init_grid(
            width=num_of_cols,
            height=num_of_rows,            
            init_alive_cells=[CellIndex(1, 1), CellIndex(2, 1)]
        )

        self.game.proceed_generation()

        exp_alive_cells = []

        self.check_result(num_of_rows=num_of_rows, 
                          num_of_cols=num_of_cols, 
                          exp_alive_cells=exp_alive_cells,
                          generation=1)

    def test_proceed_generation_twice(self):
        """Check the game board after two generation.
        """
        num_of_rows = 5
        num_of_cols = 6
        self.game.init_grid(
            width=num_of_cols,
            height=num_of_rows,            
            init_alive_cells=[CellIndex(1, 1), CellIndex(2, 1), CellIndex(2, 2), CellIndex(2, 3)]
        )

        self.game.proceed_generation()
        self.print_board()
        self.game.proceed_generation()
        self.print_board()

        exp_alive_cells = [
            CellIndex(1, 1),
            CellIndex(1, 2),
            CellIndex(2, 1),
            CellIndex(2, 2),
            CellIndex(3, 1),
            CellIndex(3, 2),
        ]

        self.check_result(num_of_rows=num_of_rows, 
                          num_of_cols=num_of_cols, 
                          exp_alive_cells=exp_alive_cells,
                          generation=2)

    def test_proceed_generation_with_corner_cells(self):
        """Check the game board after one generation which has alive cells on the corner of the grid.
        """
        num_of_rows = 5
        num_of_cols = 6
        self.game.init_grid(
            width=num_of_cols,
            height=num_of_rows,            
            init_alive_cells=[CellIndex(1, 0), CellIndex(2, 0), CellIndex(3, 0)]
        )

        self.print_board()
        self.game.proceed_generation()        
        self.print_board()

        exp_alive_cells = [
            CellIndex(2, 0),
            CellIndex(2, 1),
        ]

        self.check_result(num_of_rows=num_of_rows, 
                          num_of_cols=num_of_cols, 
                          exp_alive_cells=exp_alive_cells,
                          generation=1)