import random

from typing import List, Optional, Tuple

class Life:
    """A class containing the game of life.
    
    Attributes:
        grid: status for each cell in the current generation
        alive_cells: list of indices of alive cells in the current generation
        generation: current generation number
        MIN_GRID_WIDTH: minimum width of the grid
        MIN_GRID_HEIGHT minimum height of the grid
        MAX_GRID_SIZE: maximum width|height of the grid
    """
    grid = None
    alive_cells = None
    generation = None

    MIN_GRID_WIDTH = 5
    MIN_GRID_HEIGHT = 5
    MAX_GRID_SIZE = 500    # set a cap for the random generation

    def __init__(self):
        self.generation = 0

    def init_grid(self, width: int, height: int, init_alive_cells: List[Tuple[int, int]]):
        """Initialize the grid.
        
        Args:
            width: The grid width
            height The grid height
            init_alive_cells: List of initial alive cells
        """
        if width < self.MIN_GRID_WIDTH or height < self.MIN_GRID_HEIGHT:
            raise ValueError(
                "A grid should have the minimum size of {} (Given: {}".format((
                    self.MIN_GRID_WIDTH, self.MIN_GRID_HEIGHT), 
                    (width, height)))

        self.grid = [[False for _ in range(width)] for _ in range(height)]

        self.alive_cells = init_alive_cells
        for cur_cell in self.alive_cells:
            cur_row = cur_cell[0]
            cur_col = cur_cell[1]

            self.grid[cur_row][cur_col] = True

    def start_game(self, 
                   grid_width: Optional[int] = None, 
                   grid_height: Optional[int] = None, 
                   init_alive_cells:Optional[List[Tuple[int, int]]] = None):
        """Initialize the game board

        If parmeters are not given, they are randomly assigned.
        
        Args:
            grid_width: The grid width
            grid_height The grid height
            init_alive_cells: List of initial alive cells
        """
        if not grid_width:
            grid_width = random.randint(self.MIN_GRID_WIDTH, self.MAX_GRID_SIZE)

        if not grid_height:
            grid_height = random.randint(self.MIN_GRID_HEIGHT, self.MAX_GRID_SIZE)

        if not init_alive_cells:
            init_alive_cells = self.get_random_init_states(grid_width, grid_height)

        self.init_grid(grid_width, grid_height, init_alive_cells)
    
    @staticmethod
    def get_random_init_states(grid_width: int, grid_height: int, max_count=5) -> List[Tuple[int, int]]:
        """Return the list of randomly initialized alive cells.
        
        Args:
            grid_width: the grid's width 
            grid_height: the grid's height
        
        Returns:
            List of index of alive cells
        """
        # TODO: implement random assignment
        res = [(1,3), (2, 4), (4, 2)]
        return res
