from unittest import TestCase

from src.life import CellIndex, Life

class TestGetNeighbors(TestCase):
    def setUp(self):
        self.game = Life()
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
        self.assertEqual(neighbors, exp_res)

    def test_get_neighbors_target_cell_at_top_right_corner(self):
        """Check if neighbor cells are returned if the target cell is placed at the top right corner of the grid.
        """
        neighbors = self.game.get_neighbors(CellIndex(0, 4))

        exp_res = [            
            CellIndex(0, 3),
            CellIndex(1, 3), CellIndex(1, 4),
        ]
        self.assertEqual(neighbors, exp_res)

    def test_get_neighbors_target_cell_at_bottom_left_corner(self):
        """Check if neighbor cells are returned if the target cell is placed at the bottom left corner of the grid.
        """
        neighbors = self.game.get_neighbors(CellIndex(4, 0))

        exp_res = [            
            CellIndex(3, 0), CellIndex(3, 1),
            CellIndex(4, 1),
        ]
        self.assertEqual(neighbors, exp_res)


class TestGetNumberOfAliveNeighbors(TestCase):
    def setUp(self):
        self.game = Life()
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
    