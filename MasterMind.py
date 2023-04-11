from flask import Flask, request
from random import randint
import copy


class Game:
    allGames = dict()  # contains all game id's

    def __init__(self):
        self.board = ""
        self.cnt = 0
        self.result = ""
        self.pattern = []  # list
        self.id = randint(100000, 999999)  # makes a random id
        while self.id in self.allGames:  # makes sure that id isn’t already used
            self.id = randint(100000, 999999)
        self.allGames[self.id] = self  # adds id to dictionary

    def getboard(self):
        print(str(self.board))
        return str(self.board)

    def checkpatterns(self, p):
        if str(p).isnumeric() == False:
            return "Invalid input"
        check = list(map(int, str(p)))
        print(check, " self.pattern: ", self.pattern)
        if self.pattern == check:
            return "bbbb"
        checkp = copy.deepcopy(check)
        new_pattern = copy.deepcopy(self.pattern)
        cntSamePos = 0
        cntSame = 0
        for i in range(0, len(check)):
            if str(self.pattern[i]) == str(check[i]):
                cntSamePos += 1
                checkp[i] = -1
                new_pattern[i] = -1
            print(checkp, " -> ", self.pattern)
        print(cntSamePos, " b's ")
        for i in range(0, len(check)):
            if checkp[i] != -1:
                for j in range(0, len(check)):
                    if checkp[i] == new_pattern[j] and new_pattern[j] != -1:
                        cntSame += 1
                        checkp[i] = -1
                        new_pattern[j] = -1
                        print(checkp, " -> ", self.pattern)

        print(cntSame, " w ")
        self.result = ""
        for _ in range(0, cntSamePos):
            self.result += 'b'
        for _ in range(0, cntSame):
            if (len(self.result) < 5):
                self.result += 'w'
        for _ in range(0, 4 - len(self.result)):
            self.result += '0'
        if self.board == "":
            self.board += p + " " + self.result
            self.board = str(self.board)
        else:
            self.board += "," + p + " " + self.result
            self.board = str(self.board)
        return self.result


app = Flask(__name__)


def checkpattern(num):
    if str(num).isnumeric() == False:
        return False
    l = list(map(int, str(num)))
    for i in range(0, len(l)):
        if str(l[i]).isnumeric() == False or int(l[i]) < 0 or int(l[i]) > 6:
            return False
    return True


def get_game(game_id):  # get the current game object
    if game_id is None or not game_id.isnumeric():
        return "game parameter is required and must be a number."
    try:
        return Game.allGames[int(game_id)]
    except KeyError:
        return "No such game"


def generatepattern():
    s = []
    for _ in range(0, 4):
        s.append(randint(0, 6))
    return s


@app.route("/newgame")
def newgame():
    print("new game")
    g = Game()
    p = request.args['pattern']
    if str(p).isnumeric() and checkpattern(int(p)) == True:
        g.pattern = list(map(int, str(p)))
    elif p == "random":
        g.pattern = generatepattern()
        print(g.pattern)
    return str(g.id)


@app.route("/restart")
def restart():
    getboard = request.args['game']
    g = get_game(getboard)
    if type(g) is str:
        return g
    p = request.args['newpattern']
    if p.isnumeric() and checkpattern(int(p)):
        g.cnt = 0
        g.board = ""
        g.pattern = list(map(int, str(p)))
        return "OK"
    elif p == "random":
        g.cnt = 0
        g.board = ""
        g.pattern = generatepattern()
        print(g.pattern)
        return "OK"
    return "Invalid"


@app.route("/play")
def guess():
    getboard = request.args['game']
    g = get_game(getboard)
    if type(g) is str:
        return g
    p = request.args['pattern']
    if g.cnt >= 10 or checkpattern(str(p)) == False:
        return "Invalid"
    g.cnt += 1
    turnsLeft = str(10 - int(g.cnt))
    resultPattern = g.checkpatterns(p)
    return resultPattern + " " + turnsLeft


@app.route('/getBoard')
def getBoard():
    getboard = request.args['game']
    g = get_game(getboard)
    if type(g) is str:
        return g
    return str(g.board)


# if __name__ == "__main__":
# app.run(host='0.0.0.0', port='0000', debug=True)