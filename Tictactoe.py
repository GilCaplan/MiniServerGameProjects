from flask import Flask, request
from random import randint


class Game:
    # how can i create so that each game has its own unique players and board?
    allGames = dict()  # contains all game id's

    def __init__(self):
        self.turn = "X"
        self.board = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
        self.allplayers = []  # list
        self.player_name = dict()  # dictionary
        self.id = randint(0, 10)  # makes a random id
        while self.id in self.allGames:  # makes sure that id isn’t already used
            self.id = randint(0, 1000)
        self.allGames[self.id] = self  # adds id to dictionary

    def register(self):
        id = randint(0, 100)
        while id in self.allplayers:
            id = randint(0, 100)
        self.allplayers.append(id)
        if len(self.allplayers) == 1:
            self.player_name[str(id)] = 'X'
            return str(id) + ' X'
        self.player_name[str(id)] = 'O'
        return str(id) + ' O'

    def play(self, p, pos):
        if self.board[pos] != 0:
            return "Invalid move"
        self.board[pos] = self.player_name[p]
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
        return "OK"

    def checkBoard(self, board):
        if board[0] == board[1] == board[4] != 0:
            return board[0]
        elif board[3] == board[4] == board[5] != 0:
            return board[4]
        elif board[6] == board[7] == board[8] != 0:
            return board[7]
        elif board[0] == board[3] == board[6] != 0:
            return board[0]
        elif board[1] == board[4] == board[7] != 0:
            return board[1]
        elif board[2] == board[5] == board[8] != 0:
            return board[2]
        elif board[0] == board[4] == board[8] != 0:
            return board[0]
        elif board[2] == board[4] == board[6] != 0:
            return board[2]
        else:
            cnt = 0
            for key in board.keys():
                if board[key] != 0:
                    cnt += 1
            if cnt == 9:
                return 0
        return -1

    def boardToString(self):
        board = ""
        for i in range(0, 9):
            board += str(self.board[i])
        return board


app = Flask(__name__)


def get_game(game_id):  # get the current game object
    if game_id is None or not game_id.isnumeric():
        return "game parameter is required and must be a number."
    try:
        return Game.allGames[int(game_id)]
    except KeyError:
        return "No such game"


@app.route("/newgame")
def register_Game():
    g = Game()
    return str(g.id)


@app.route("/register")
def register_player():  # two types of players X or Y or neither, how can i do it so a game can only have either?
    game = request.args['game']
    if type(get_game(game)) is str:
        return get_game(game)
    g = get_game(game)
    return g.register()


@app.route("/getBoard")
def getBoard():
    getboard = request.args['game']
    g = get_game(getboard)
    if type(g) is str:
        return g
    return g.boardToString()


@app.route("/play")
def play():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return g
    player = request.args['player']
    if not player.isnumeric():
        return "Invalid player"
    if int(player) not in g.allplayers:
        return "Invalid player"
    pos = request.args['pos']
    if pos.isnumeric():
        pos = int(pos)
        if pos >= 0 and pos < 9:
            g.play(player, pos)
    return "Invalid position"


@app.route("/stats")
def Gamestatus():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return g
    if len(g.allplayers) < 2:
        return 'Waiting for players'
    check = g.checkBoard(g.board)
    if check == 0:
        return "Tie"
    if check == 'X':
        return "Winner = X"
    if check == 'O':
        return "Winner = O"
    return "Turn = " + g.turn


def run_game():
    app.run(host='0.0.0.0', port='8888', debug=True)
