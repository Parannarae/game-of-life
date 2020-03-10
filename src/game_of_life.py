from enum import Enum
from typing import List

from life import CellIndex, Life


FILE_FOLDER = 'shared_folder'


class Menu(Enum):
    NEXT = 1
    NEXT_N = 2
    DUMP_RESULT = 3
    QUIT = 4

    @staticmethod
    def get_text_description(value: 'Menu') -> str:
        """Get human friendly description of each menu.
        
        Args:
            value: menu to get a description
        
        Returns:
            description of value
        """
        if value == Menu.NEXT:
            return "Proceed to the next generation"
        elif value == Menu.NEXT_N:
            return "Proceed to next N generations"
        elif value == Menu.DUMP_RESULT:
            return "Dump the current generation to a file"
        elif value == Menu.QUIT:
            return "Quit"
        else:
            raise ValueError("{} is not an option".format(value))


class FileParser:
    """A class to parse the file input/output

    A file has the following format (every value is separated by the white space):
    `
    grid_height grid_width
    total_number_of_alive_cells
    row_index_of_first_alive_cell column_index_of_first_alive_cell
    row_index_of_second_alive_cell column_index_of_second_alive_cell
    ...
    `
    """
    grid_width = None
    grid_height = None
    alive_cells = None

    def __init__(self, grid_width: int = None, grid_height: int = None, alive_cells: List[CellIndex] = None):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.alive_cells = alive_cells

    def dump_grid_to_file(self, file_name: str = 'result_dump.txt'):
        """Write the information to a file
        
        Args:
            file_name (str): name of the file        
        """
        if (self.grid_width is None or self.grid_height is None or self.alive_cells is None):
            raise Exception(
                "All attributes must be set: (grid_width: {}, grid_height: {}, alive_cells: {})".format(
                    self.grid_width, self.grid_height, self.alive_cells))

        if file_name.split('.')[-1] != 'txt':
            file_name = file_name + '.txt'

        with open(FILE_FOLDER + '/{}'.format(file_name), 'w') as fp:
            fp.write("{} {}\n".format(self.grid_height, self.grid_width))
            fp.write("{}\n".format(len(self.alive_cells)))
            for cell in self.alive_cells:
                fp.write("{} {}\n".format(cell.row, cell.column))

    def parse_from_file(self, file_name: str = 'input.txt'):
        """Set attributes' values from the file `file_name`.
        
        Args:
            file_name: a name of the file to read from
        """
        with open(FILE_FOLDER + '/{}'.format(file_name)) as fp:
            contents = fp.readlines()

        num_of_initial_alive_cells = -1
        alive_cells = []
        for content in contents:
            tokens = content.strip().split(' ')
            if tokens:                
                if self.grid_width is None:
                    if not len(tokens) == 2:
                        raise Exception("The first data line is not in the correct format ({}).".format(content[:-1]))

                    try:
                        self.grid_height = int(tokens[0])
                        self.grid_width = int(tokens[1])
                    except ValueError:
                        raise Exception("The first data line is not in the correct format ({}).".format(content[:-1]))
                
                elif num_of_initial_alive_cells == -1:
                    if not len(tokens) == 1:
                        raise Exception("The second data line is not in the correct format ({}).".format(content[:-1]))

                    try:
                        num_of_initial_alive_cells = int(tokens[0])
                    except ValueError:
                        raise Exception("The second data line is not in the correct format ({}).".format(content[:-1]))

                else:
                    if not len(tokens) == 2:
                        raise Exception(
                            "The initial alive cell index data line is not in the correct format ({}).".format(
                                content[:-1]))

                    try:
                        alive_cells.append(CellIndex(int(tokens[0]),int(tokens[1])))
                    except ValueError:
                        raise Exception(
                            "The initial alive cell index data line is not in the correct format ({}).".format(
                                content[:-1]))

                    if len(alive_cells) == num_of_initial_alive_cells:
                        self.alive_cells = alive_cells
                        # ignore the rest of lines
                        return

        
class StdoutInterface:
    """An interface for the game of life on Stdout
    """
    cur_game = None
    valid_menu = None

    def __init__(self):
        self.valid_menu = set(v.value for v in Menu.__members__.values())

    def print_board(self):
        """Show the board's status to Stdout
        
        Args:
            cur_life: Current game status instance
        """
        print("==========Gen {}==========".format(self.cur_game.generation))
        
        for cur_row in self.cur_game.grid:
            print("  ".join(['o' if cur_col else 'x' for cur_col in cur_row]))
        
        print("====================")

    def process_generation(self, num_of_generation: int = 1):
        """Process the game for num_of_generation
        
        Args:
            num_of_generation: total number of generation to go
        """
        for _ in range(num_of_generation):
            self.cur_game.proceed_generation()
            self.print_board()

    def process_menu(self, chosen: int) -> bool:
        """Given chosen, execute the appropriate process.
        
        Args:
            chosen: menu number
        
        Returns:
            True if the program needs to be quit
        """
        if chosen == Menu.NEXT.value:
            self.process_generation()
        
        elif chosen == Menu.NEXT_N.value:
            user_input = input("Number of generations to proceed:")
            
            try:
                num_of_generation = int(user_input.strip())
            except ValueError:
                print("Unknown menu has chosen.")
                return True
            
            self.process_generation(num_of_generation=num_of_generation)
            
        elif chosen == Menu.DUMP_RESULT.value:
            fp = FileParser(grid_width=self.cur_game.grid_width,
                            grid_height=self.cur_game.grid_height,
                            alive_cells=self.cur_game.alive_cells)
            file_name = 'result_dump.txt'
            fp.dump_grid_to_file(file_name)
            print("Alive cells for the {}th generation are recorded on {}".format(self.cur_game.generation, file_name))

        elif chosen ==Menu.QUIT.value:
            return False
        
        else:
            print("Unknown menu has chosen.")

        return True

    def select_menu(self):
        """Print the menu, and execute the appropriate process.
        """
        keep_looping = True
        while keep_looping:
            # print menus
            print("Current generation: {}".format(self.cur_game.generation))
            for v in Menu.__members__.values():
                print("{}: {}".format(v.value, Menu.get_text_description(v)))

            user_input = input("Select number:")
            try:
                chosen = int(user_input.strip())
            except ValueError:
                print("Unknown menu has chosen.")
                print()
                continue

            if chosen in self.valid_menu:
                keep_looping = self.process_menu(chosen)

            print()

    def start_new_game(self, 
                       grid_width: int = None, 
                       grid_height: int = None, 
                       alive_cells: List[CellIndex] = None):
        """Start the new game of life.

        Args:
            grid_width: the grid width
            grid_height the grid height
            init_alive_cells: list of initial alive cells
        """
        self.cur_game = Life()
        self.cur_game.start_game(grid_width=grid_width, grid_height=grid_height, init_alive_cells=alive_cells)
        self.print_board()
        self.select_menu()


if __name__ == '__main__':
    interface = StdoutInterface()
    interface.start_new_game()
