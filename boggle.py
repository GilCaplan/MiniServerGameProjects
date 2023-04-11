from flask import Flask, request
from random import randint


class Game:
    allGames = dict()  # contains all game id's

    def __init__(self):
        self.allplayers = []
        self.player_name = dict()
        self.playerletters = ""
        self.id = randint(100000, 999999)  # makes a random id
        while self.id in self.allGames:  # makes sure that id isn’t already used
            self.id = randint(100000, 999999)
        self.allGames[self.id] = self  # adds id to dictionary

    def register(self, name):
        id = randint(100000, 999999)
        while id in self.allplayers:
            id = randint(100000, 999999)
        self.allplayers.append(id)
        self.player_name[str(id)] = name
        return str(id)


app = Flask(__name__)


def randStr():
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']
    s = ''
    for _ in range(0, 16):
        s += a[randint(0, 25)]
    return s.upper()


def get_game(game_id):  # get the current game object
    if game_id is None or not game_id.isnumeric():
        return "game parameter is required and must be a number."
    try:
        return Game.allGames[int(game_id)]
    except KeyError:
        return "No such game"


@app.route('/newgame')
def newGame():
    g = Game()
    g.letters = randStr()
    print("new game created")
    return str(g.id)


@app.route('/register')
def register():
    g = request.args['game']
    if type(get_game(g)) is str:
        return get_game(g)
    g = get_game(g)
    p = request.args['newPlayer']
    print("new player created")
    return g.register(p)


@app.route('/getLetters')
def getLetters():
    g = request.args['game']
    if type(get_game(g)) is str:
        return get_game(g)
    g = get_game(g)
    p = request.args['player']
    return g.letters


@app.route('/newLetters')
def newLetters():
    g = request.args['game']
    if type(get_game(g)) is str:
        return get_game(g)
    g = get_game(g)
    g.letters = randStr()
    p = request.args['player']
    return g.letters


def run_game():
    app.run(host='0.0.0.0', port='9999', debug=True)