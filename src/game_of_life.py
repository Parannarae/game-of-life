from enum import Enum

from life import Life

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
            pass
        elif chosen ==Menu.QUIT.value:
            return False
        else:
            print("Unknown number has chosen.")

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

    def start_new_game(self):
        """Start the new game of life.
        """
        self.cur_game = Life()
        self.cur_game.start_game(5, 5)
        self.print_board()
        self.select_menu()


if __name__ == '__main__':
    interface = StdoutInterface()
    interface.start_new_game()
