from flask import Flask, request
import json
from random import randint
from pieces import Pawn, Queen, King, Knight, Bishop, Rook

a, b, c, d, e, f, g, h = 0, 1, 2, 3, 4, 5, 6, 7


class Game:
    allGames = dict()  # contains all game id's

    def __init__(self):
        self.status = "waiting"
        self.last_move = {"from": "", "to": ""}
        self.turn = 'w'
        self.flag = {'w': [True, True], 'b': [True,
                                              True]}  # in order to do king-rook casting, if rook or king is moved then it becomes False and option isn't available anymore
        self.casting = {'w': [False, False], 'b': [False, False]}
        self.bString = "RbNbBbQbKbBbNbRbPbPbPbPbPbPbPbPb0000000000000000000000000000000000000000000000000000000000000000PwPwPwPwPwPwPwPwRwNwBwQwKwBwNwRw"
        self.board = makeboard()
        self.player_name = dict()  # dictionary
        self.pname = dict()
        self.PlayerType = dict()  # whos turn it is
        self.id = 1  # randint(1000, 9999)  # makes a random id
        while self.id in self.allGames:  # makes sure that id isn’t already used
            self.id = randint(1000, 9999)
        self.allGames[self.id] = self  # adds id to dictionary

    def register(self, name):
        player_id = 1
        if str(player_id) in self.player_name:
            player_id = 2
        self.player_name[str(player_id)] = name
        if player_id == 1:
            self.PlayerType["1"] = 'w'
            self.pname[name] = "1"
        else:
            self.PlayerType["2"] = 'b'
            self.pname[name] = "2"

    def printmatrix(self):
        row = ""
        b = matrixflip(self.board, 'v')
        for i in range(0, 8):
            print(row)
            row = ""
            for j in range(0, 8):
                row += "00, " if b[i][j] is False else b[i][j].name + ", "


def makeboard():
    board = []  # (number, letter)
    rows, cols = 8, 8
    for i in range(cols):  # i iterates from 0 to value 'cols'
        col = [False for _ in range(rows)]
        board.append(col)  # List 'col' is added to List 'board'
    for i in range(8):  # pawns
        board[1][i] = Pawn("w", [1, i])
        board[6][i] = Pawn("b", [6, i])
    board[0][a] = Rook("w", [0, a])  # Rooks
    board[7][a] = Rook("b", [7, a])
    board[0][h] = Rook("w", [0, h])
    board[7][h] = Rook("b", [7, h])
    board[0][b] = Knight("w", [0, b])  # knights
    board[0][g] = Knight("w", [0, g])
    board[7][b] = Knight("b", [7, b])
    board[7][g] = Knight("b", [7, g])
    board[0][c] = Bishop("w", [0, c])  # Bishop
    board[7][c] = Bishop("b", [7, c])
    board[0][f] = Bishop("w", [0, f])
    board[7][f] = Bishop("b", [7, f])
    board[0][d] = Queen("w", [0, d])  # queen
    board[7][d] = Queen("b", [7, d])
    board[7][e] = King("b", [7, e])  # king
    board[0][e] = King("w", [0, e])
    return board


def matrixflip(m, d):
    tempm = m.copy()
    if d == 'h':
        for i in range(len(tempm)):
            tempm[i].reverse()
    elif d == 'v':
        tempm.reverse()
    return (tempm)


app = Flask(__name__)


def get_game(game_id):  # get the current game object
    try:
        return True, Game.allGames[int(game_id)]
    except KeyError:
        return False, "No such game"


@app.route("/newgame")
def register_Game():
    g = Game()
    return str(g.id)


@app.route("/register")
def register_player():
    game = request.args['game']
    valid, g = get_game(game)
    name = request.args['name']
    if not valid:
        return g
    g.register(name)
    if len(g.player_name) == 1:
        return json.dumps({"id": str(g.pname[name]), "is starting player": "true"})
    return json.dumps({"id": str(g.pname[name]), "is starting player": "false"})


@app.route("/doesExist")
def doesExist():
    game = request.args['game']
    valid, g = get_game(game)
    if not valid:
        return "no"
    return "yes"


@app.route("/getBoard")
def getBoard():
    game = request.args['game']
    valid, g = get_game(game)
    if not valid:
        return g
    return "".join(
        ["00" if not piece or piece is None else piece.name for I in matrixflip(g.board, 'v') for piece in I])


@app.route("/getLastMove")
def getlastMove():
    game = request.args['game']
    getplayer = request.args['player']
    g = get_game(game)[1]
    if type(g) is str:
        return json.dumps({"error": 'No such game'})  # “you loose” \ “waiting” \ “done”
    if g.PlayerType[str(getplayer)] == g.turn:  # g.PlayerType[str(getplayer)] -> 1
        return json.dumps({"status": g.status, "from": g.last_move["from"], "to": g.last_move["to"]})
    return json.dumps({"status": "waiting", "from": "", "to": ""})


@app.route("/getPieceOptions")
def options():
    game = request.args['game']
    piece = request.args['piece']
    valid, g = get_game(game)
    if not valid:
        return json.dumps({"error": 'No such game'})
    CurrentPiece = []  # a1
    CurrentPiece.append(int(piece[1]) - 1)  # (number, letter)
    CurrentPiece.append(int(getNum(piece[0])))
    CP = g.board[CurrentPiece[0]][CurrentPiece[1]]
    if not g.board[CurrentPiece[0]][CurrentPiece[1]]:
        return "[]"  # loc
    options = CP.move(board=g.board) if CP.color == g.turn else []
    side = 0 if g.turn == 'w' else 7
    # if certain positions are empty and flag of w/b is false then move king and rook also not if there is check and that position
    if CP.name[0] in ['K', 'R']:
        if g.flag[g.turn][0] == False and g.board[side][1] == g.board[side][2] == g.board[side][3] == False and \
                g.board[side][0] != False and g.board[side][4].name[0] != False and g.board[side][0].name[0] == "R" and \
                g.board[side][4].name[0] == "K":
            g.casting[g.turn][0] = True
            options.append(("c" if CP.name[0] == "K" else "d") + str(side + 1))
        if g.flag[g.turn][1] == False and g.board[side][6] == g.board[side][5] == False and g.board[side][
            0] != False and g.board[side][4].name[0] != False and g.board[side][7].name[0] == "R" and \
                g.board[side][4].name[0] == "K":
            g.casting[g.turn][1] = True
            options.append(("c" if CP.name[0] == "K" else "d") + str(side + 1))
    return str(options)


@app.route("/movePiece")
def movePiece():
    game = request.args['game']
    player = request.args['player']
    startpos = request.args['startPos']
    destPos = request.args['destPos']
    valid, g = get_game(game)
    if not valid:
        return json.dumps({"error": 'No such game'})
    if g.PlayerType[str(player)] is not g.turn:
        return "3"
    AttackingPiece = g.board[int(startpos[1]) - 1][int(getNum(startpos[0]))]
    if str(destPos) in AttackingPiece.move(g.board):
        g.last_move["from"] = startpos
        g.last_move["to"] = destPos
        g.status = "done"
        g.turn = 'w' if g.turn == 'b' else 'b'
        g.board[int(destPos[1]) - 1][int(getNum(destPos[0]))] = AttackingPiece
        g.board[int(startpos[1]) - 1][int(getNum(startpos[0]))] = False
        AttackingPiece.pos = [int(destPos[1]) - 1, int(getNum(destPos[0]))]
        if AttackingPiece.name[0] == "P" and int(destPos[1]) in [1, 8]:
            AttackingPiece = Queen(AttackingPiece.color, AttackingPiece.pos)
            print("pawn is now a queen")
        return "0"
    g.status = "waiting"
    g.last_move["from"] = ""
    g.last_move["to"] = ""
    return "2"


def checkForKing(options, color):
    for i in options:
        if i and i.name[0] == "K" and i.color != color:  # checking for king
            return "check"
    return False


def getNum(PieceRow):
    if type(PieceRow) is int:
        return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'][PieceRow]
    return {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}[PieceRow]


def run_game():
    app.run(host='127.0.0.1', port='8083', debug=True)


def name(num, letter):
    l = getNum(int(letter))
    n = str(num + 1)
    return l + n


def name2(pos):
    l = getNum(int(pos[1]))
    n = str(pos[0] + 1)
    return l + n




