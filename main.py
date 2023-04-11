import dixit
import chess
import Tictactoe
import boggle
import MasterMind


def play_game():
    game = input("enter game, enter exact spelling: dixit, chess, Tictactoe, boggle, MasterMind: ")
    if game == "dixit":
        dixit.run_game()
    elif game == "chess":
        chess.run_game()
    elif game == "Tictactoe":
        Tictactoe.run_game()
    elif game == "boggle":
        boggle.run_game()
    elif game == "MasterMind":
        MasterMind.run_game()
    elif game == "exit":
        exit()
    else:
        print("error: enter game name or type exit to finish program")
        return "rerun"
    return "done"

if __name__ == '__main__':
    status = play_game()