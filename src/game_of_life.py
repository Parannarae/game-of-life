from life import Life

class StdoutInterface:
    """An interface for the game of life on Stdout
    """
    cur_game = None

    def start_new_game(self):
        """Start the new game of life.
        """
        self.cur_game = Life()
        self.cur_game.start_game(5, 5)

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
        for _ in range(num_of_generation):
            self.cur_game.proceed_generation()


if __name__ == '__main__':
    interface = StdoutInterface()
    interface.start_new_game()
    interface.print_board()
    interface.process_generation()
    interface.print_board()
