import dixit
import chess
import Tictactoe
import boggle
import MasterMind

if __name__ == '__main__':
    Game = "play"
    while Game == "play":
        Game = input("enter game, enter exact spelling: dixit, chess, Tictactoe, boggle, MasterMind: ")
        if Game == "dixit":
            dixit.run_game()
            Game = "stop"
            break
        elif Game == "chess":
            chess.run_game()
            Game = "stop"
            break
        elif Game == "Tictactoe":
            Tictactoe.run_game()
            Game = "stop"
            break
        elif Game == "boggle":
            boggle.run_game()
            Game = "stop"
            break
        elif Game == "MasterMind":
            MasterMind.run_game()
            Game = "stop"
            break
        elif Game == "exit":
            exit()
        else:
            print("error: enter game name or type exit to finish program")
