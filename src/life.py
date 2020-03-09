import random

from typing import Dict, List, Optional, Tuple

class CellIndex:
    """A class for a cell's coordinate
    """
    row = None
    column = None

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.row == other.row and self.column == other.column
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.row == other.row or not self.column == other.column
        return NotImplemented

    def __hash__(self):
        return hash((self.row, self.column))

    def __repr__(self):
        return 'CellIndex({}, {})'.format(self.row, self.column)

class Life:
    """A class containing the game of life.
    
    Attributes:
        grid: status for each cell in the current generation
        grid_width: a width of the grid
        grid_height: a height of the grid
        alive_cells: list of indices of alive cells in the current generation
        generation: current generation number
        MIN_GRID_WIDTH: minimum width of the grid
        MIN_GRID_HEIGHT minimum height of the grid
        MAX_GRID_SIZE: maximum width|height of the grid
    """
    grid = None
    grid_width = None
    grid_height = None
    alive_cells = None
    generation = None

    MIN_GRID_WIDTH = 5
    MIN_GRID_HEIGHT = 5
    MAX_GRID_SIZE = 500    # set a cap for the random generation

    def __init__(self):
        self.generation = 0

    def init_grid(self, width: int, height: int, init_alive_cells: List[CellIndex]):
        """Initialize the grid.
        
        Args:
            width: the grid width
            height the grid height
            init_alive_cells: list of initial alive cells
        """
        if width < self.MIN_GRID_WIDTH or height < self.MIN_GRID_HEIGHT:
            raise ValueError(
                "A grid should have the minimum size of {} (Given: {}".format((
                    self.MIN_GRID_WIDTH, self.MIN_GRID_HEIGHT), 
                    (width, height)))

        self.grid = [[False for _ in range(width)] for _ in range(height)]
        self.grid_width = width
        self.grid_height = height

        self.alive_cells = init_alive_cells
        for cur_cell in self.alive_cells:
            self.grid[cur_cell.row][cur_cell.column] = True

    @staticmethod
    def get_random_init_states(grid_width: int, grid_height: int, max_count=5) -> List[CellIndex]:
        """Return the list of randomly initialized alive cells.
        
        Args:
            grid_width: the grid's width 
            grid_height: the grid's height
        
        Returns:
            list of index of alive cells
        """
        # TODO: implement random assignment
        res = [CellIndex(1, 1), CellIndex(1, 3), CellIndex(2, 1), CellIndex(2, 2), CellIndex(2, 3)]
        return res

    def start_game(self,
                   grid_width: Optional[int] = None, 
                   grid_height: Optional[int] = None, 
                   init_alive_cells:Optional[List[CellIndex]] = None):
        """Initialize the game board.

        If parmeters are not given, they are randomly assigned.
        
        Args:
            grid_width: the grid width
            grid_height the grid height
            init_alive_cells: list of initial alive cells
        """
        if not grid_width:
            grid_width = random.randint(self.MIN_GRID_WIDTH, self.MAX_GRID_SIZE)

        if not grid_height:
            grid_height = random.randint(self.MIN_GRID_HEIGHT, self.MAX_GRID_SIZE)

        if not init_alive_cells:
            init_alive_cells = self.get_random_init_states(grid_width, grid_height)

        self.init_grid(grid_width, grid_height, init_alive_cells)

    def get_neighbors(self, center: CellIndex) -> List[CellIndex]:
        """Return cells which are the neighbor of center.
        
        Args:
            center: an index of the center cell to find its neighbors
        
        Returns:
            list of indices of neighbors (exclude center)
        """
        res = []
        for i in range(-1, 2):
            cur_row = center.row + i
            for j in range(-1, 2):
                cur_col = center.column + j       
                if ((0 <= cur_row < self.grid_height and 0 <= cur_col < self.grid_width) 
                        and (CellIndex(cur_row, cur_col) != center)):
                    res.append(CellIndex(cur_row, cur_col))
        
        return res

    def get_number_of_alive_neighbors(self) -> Dict[CellIndex, int]:
        """For each cell which has at least one alive neighbor, Get the total number of alive neighbors.

        A cell with no alive neighbor would not be in the returning dict.
        
        Returns:
            total number of alive neighbors for each target cell
        """
        alive_neighbor_counter = {}     # number of alive neighbor cells
        
        # for each alive cell, set its neighbor cell to have one live cell
        for cur_alive_cell in self.alive_cells:            
            cur_neighbors = self.get_neighbors(cur_alive_cell)

            for neighbor in cur_neighbors:
                alive_neighbor_counter[neighbor] = alive_neighbor_counter.get(neighbor, 0) + 1
        
        return alive_neighbor_counter

    def is_survive_for_the_next_generation(self, cell: CellIndex, num_of_alive_neighbors: int) -> bool:
        """Check if cell will be alive for the next generation.

        A cell will not be alive unless 
            1) a live cell with 2 or 3 neighbors 
            2) a dead cell with 3 neighbors
        
        Args:
            cell: a cell to check
            num_of_alive_neighbors: number of alive neighbor cells for the current generation
        
        Returns:
            True if cell will be alive for the next generation
        """
        is_alive = self.grid[cell.row][cell.column]

        return (
            (is_alive and (2 <= num_of_alive_neighbors <= 3)) 
            or (not is_alive and num_of_alive_neighbors == 3)
        )

    def proceed_generation(self):
        """Proceed one generation according to the following rule:

        - A live cell with with two or three live neighbors stay alive for the next generation
        - A dead cell with three live neighbors becomes alive for the next generation
        - Any other cells become dead for the next generation

        https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        """
        alive_neighbor_counter = self.get_number_of_alive_neighbors()

        # note that cells not in `alive_neighbor_counter` has no alive neighbors meaning dead for the next
        next_alive_cells = []
        for cur_cell, num_of_alive_neighbors in alive_neighbor_counter.items():
            if self.is_survive_for_the_next_generation(cur_cell, num_of_alive_neighbors):
                next_alive_cells.append(cur_cell)

        # change to the next generation
        cur_alive_cells_set = set(self.alive_cells)
        next_alive_cells_set = set(next_alive_cells)

        cell_to_die = cur_alive_cells_set - next_alive_cells_set
        cell_to_live = next_alive_cells_set - cur_alive_cells_set

        for cur_cell in cell_to_die:
            self.grid[cur_cell.row][cur_cell.column] = False

        for cur_cell in cell_to_live:
            self.grid[cur_cell.row][cur_cell.column] = True
        
        self.alive_cells = next_alive_cells
        self.generation += 1
