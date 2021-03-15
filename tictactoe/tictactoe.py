from dataclasses import dataclass
from typing import List, Union, Tuple


@dataclass
class TicTacToe(object):
    """
    TicTacToe game object.
    """

    def __init__(self):
        """
        Constructor for the TicTacToe game object.
        Initialize all the global variables.
        """
        self._VALUES = [' ' for x in range(9)]
        self._PLAYER_POS = {'X': [], 'O': []}
        self._PLAYER_CHOICE = {'X': "", 'O': ""}
        self._CUR_PLAYER_NAME = ''

    def initial_setup(self) -> List[str]:
        """
        Initialize the game by taking player names and setting them to player 1 and player 2 variables. Set Player 1 to the first one playing

        :return: list of player 1,2 and current player.
        """
        print("Player 1")
        player1 = input("Enter the name : ")
        print("\n")

        print("Player 2")
        player2 = input("Enter the name : ")
        print("\n")

        self._CUR_PLAYER_NAME = player1
        return [player1, player2]

    def player_menu(self, player1, player2):
        """
        Sets up the Tic Tac Toe game. Let the player 1 and player 2 choose between X and O.

        :param player1: Player 1 of the game.
        :param player2: Player 2 of the game.

        :return: False if the player choice is valid. True if the player input is invalid.
        """
        while True:
            print("Turn to choose for", self._CUR_PLAYER_NAME)
            print("Enter 1 for X")
            print("Enter 2 for O")

            try:
                choice = int(input())
            except ValueError:
                print("Please enter 1 or 2 \n")
                continue

            if choice == 1:
                self._PLAYER_CHOICE['X'] = self._CUR_PLAYER_NAME
                if self._CUR_PLAYER_NAME == player1:
                    self._PLAYER_CHOICE['O'] = player2
                else:
                    self._PLAYER_CHOICE['O'] = player1
                return False

            elif choice == 2:
                self._PLAYER_CHOICE['O'] = self._CUR_PLAYER_NAME
                if self._CUR_PLAYER_NAME == player1:
                    self._PLAYER_CHOICE['X'] = player2
                else:
                    self._PLAYER_CHOICE['X'] = player1
                return False

            else:
                print("Invalid Choice!!!! Try Again\n")
                continue

    def get_player_choices(self):
        return self._PLAYER_CHOICE

    def get_player_list(self, player1, player2) -> List[str]:
        return [player1, player2]

    def get_player_pos(self):
        return self._PLAYER_POS

    def get_current_player(self):
        return self._CUR_PLAYER_NAME

    def current_sign(self):
        """
        Gets the symbol of the current player.

        :return: Symbol of the current player
        """
        for key, value in self._PLAYER_CHOICE.items():
            if value == self._CUR_PLAYER_NAME:
                curr_sign = key
                return curr_sign

    def print_tic_tac_toe(self):
        """
        Prints the Tic Tac Toe board. Additional functions are used to update the board.

        :return: Tic Tac Toe board
        """
        print("\n")
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self._VALUES[0], self._VALUES[1], self._VALUES[2]))
        print('\t_____|_____|_____')

        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self._VALUES[3], self._VALUES[4], self._VALUES[5]))
        print('\t_____|_____|_____')

        print("\t     |     |")

        print("\t  {}  |  {}  |  {}".format(self._VALUES[6], self._VALUES[7], self._VALUES[8]))
        print("\t     |     |")
        print("\n")

    def player_move_req(self, curr_sign) -> int:
        """
        Request input from the player on which grid is chosen to place the symbol.
        If a player enters a non-integer, the program requests to input a number between 1 and 9.

        :param curr_sign: Sign of the current player.
        :return: grid number that player chooses
        """
        while True:
            try:
                print(f"Player: {self._CUR_PLAYER_NAME} with '{curr_sign}'. It is your turn. Which box? : ", end="")
                move = int(input())
                return move
            except ValueError:
                print("Please input a number between 1 and 9. Try again!! \n")
                continue

    def player_move_check(self, move) -> bool:
        """
        Checks whether the player input for the move is valid or not.

        :param move: grid number that player chooses
        :return: True if move is valid. False if move is invalid.
        """
        if move < 1 or move > 9:
            return False
        if self._VALUES[move - 1] != ' ':
            return False
        else:
            return True

    def update_board(self, move, curr_sign) -> Tuple[List[str], dict]:
        """
        Updates the game board with the player move.

        :param move: grid number that player chooses
        :param curr_sign: sign of the current player

        :return: the Tic Tac Toe board with the updated move.
        """
        self._VALUES[move - 1] = curr_sign
        self._PLAYER_POS[curr_sign].append(move)
        self.print_tic_tac_toe()
        return self._VALUES, self._PLAYER_POS

    def player_move_exe(self, move, curr_sign):
        """
        Gets the user input for where to place the symbol and check if the input is valid or not.
        If the move is valid, the move is executed and board is updated.


        :param curr_sign: Sign of the current player.
        :param move: Move requested by the player.

        :return: Updates the game board with player move.
        """
        while True:
            if self.player_move_check(move) == True:
                self.update_board(move, curr_sign)
                return False
            elif self.player_move_check(move) == False:
                print("Invalid Input!! Try again!!")

    def switch_player(self, player1, player2) -> Tuple[str, str]:
        """
        Switches turn to the other player.

        :param player1: Player 1 of the game.
        :param player2: Player 2 of the game.

        :return: Name of the next player and the sign the player has chosen.
        """
        if self._CUR_PLAYER_NAME == player1:
            self._CUR_PLAYER_NAME = player2
        else:
            self._CUR_PLAYER_NAME = player1
        curr_sign = self.current_sign()
        return curr_sign, self._CUR_PLAYER_NAME

    def check_draw(self):
        """
        Check if the game is a draw game.

        :return: True if the game is draw. False if the game is not a draw game.
        """
        if len(self._PLAYER_POS['X']) + len(self._PLAYER_POS['O']) == 9:
            return True
        return False

    def check_win(self, curr_sign):
        """
        Checks if the player has won the game or not by checking the player's position combinations with the iterating
        of win conditions.

        :param curr_sign: Sign of the current player.

        :return: True if the player has won the game. False if there's no winner yet.
        """
        win_cond = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        for x in win_cond:
            if all(y in (self._PLAYER_POS[curr_sign]) for y in x):
                return True
        return False


    def run(self):
        """
        Goes through the sequence of the game in a loop until a player wins or the game is drawn.

        :return: null if the game hasn't finished yet. Win or draw message if the conditions are met.
        """
        player1, player2 = self.initial_setup()
        self.player_menu(player1, player2)
        self.print_tic_tac_toe()
        curr_sign = self.current_sign()
        while True:
            move = self.player_move_req(curr_sign)
            self.player_move_exe(move, curr_sign)
            if self.check_win(curr_sign):
                print(f"Player: {self._CUR_PLAYER_NAME} with '{curr_sign} has won the game!!\n")
                break
            if self.check_draw():
                print("Game Drawn \n")
                break
            curr_sign, self._CUR_PLAYER_NAME = self.switch_player(player1, player2)
        return


def main():
    play_another = True
    while play_another:
        the_game = TicTacToe()
        the_game.run()
        play_another_input = input("Play Again? Enter 'y' to play again. Enter any key to exit: \n")
        print("\n")
        if play_another_input != 'y':
            play_another = False
    return False


if __name__ == "__main__":
    main()
