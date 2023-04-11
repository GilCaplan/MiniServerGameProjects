from flask import Flask, request
from random import randint
import random, json
import math


class Game:
    allGames = dict()  # contains all game id's

    def __init__(self):
        self.numCurrentplaying = 0  # checks how many current players there are in the game
        self.numPlayers = 0  # how many players should be in the game
        self.rounds = 3  # how many rounds are in each game defaults at 3
        self.currentRound = 1  # the current round of the game is being played
        self.hand = dict()  # each player has a value which is an array in the hand dict which contains the cards that each player has
        self.bluffs = dict()  # what each players bluff is (name:bluff)
        self.cards = []  # all the cards in play in the round(bluffs which are submitted)
        self.guess = dict()  # what each persons guess is including REAL
        self.story = ""  # story line
        self.card = 0  # chosen card for that round
        self.scores = dict()  # score for that round
        self.turn = 0  #
        self.usedCards = []

        self.playerid = []  # contains all the players id's we use this when looping through each turn cause can't do that with dict...
        self.playerNames = dict()  # all the players name key=id number value=name-string
        self.names = []
        self.totalscores = dict()  # total overall score
        self.status = 'registering'
        self.storyTeller = ''
        self.id = randint(1, 10)  # makes a random id
        while self.id in self.allGames:  # makes sure that id isn’t already used
            self.id = randint(1, 25)
        self.allGames[self.id] = self  # adds id to dictionary

    def registerplayer(self, name):
        if int(self.numCurrentplaying) == int(self.numPlayers):
            print("current cards out are: ", self.hand)
            return json.dumps({"error": "max players in current game"})
        if name in self.playerNames.values():
            return json.dumps({"error": "Name already taken"})
        id = randint(10000, 99999)
        while id in self.playerNames.keys():
            id = randint(10000, 99999)
        self.playerid.append(id)
        self.playerNames[id] = name
        self.hand[name] = []
        self.names.append(name)
        self.numCurrentplaying += 1
        self.scores[name] = 0
        self.totalscores[name] = 0
        if int(self.numCurrentplaying) == int(self.numPlayers):
            self.status = 'ready'
            self.storyTeller = self.getnextstoryteller()
            self.giveoutHand()
            print("current cards out are: ", self.hand)
            self.scores[name] = 0
            self.totalscores[name] = 0
        return json.dumps(int(id))

    def getStory(self):
        print(self.status)
        if self.currentRound > self.rounds:  # > 3
            return json.dumps({'status': 'DONE'})
        if self.status == 'registering':  # int(self.numCurrentplaying) < int(self.numPlayers) or
            return json.dumps({'status': 'registering'})
        if self.status == 'ready':
            print(self.turn, " line 63")
            self.story = ""
            return json.dumps({'status': 'ready', "storyTeller": self.storyTeller})
        if self.status == 'story_told':
            return json.dumps({'status': 'story_told', "storyTeller": self.storyTeller, "story": self.story})
        return json.dumps({'status': 'ready', 'storyTeller': self.storyTeller})

    def giveoutHand(self):
        for key in self.playerNames.keys():
            arr = []
            for _ in range(0, 6):
                x = randint(1, 80)
                while x in self.usedCards:
                    x = randint(1, 80)
                arr.append(str(x))
                self.usedCards.append(x)
            if self.playerNames[key] in self.hand:
                self.hand[self.playerNames[key]] = arr

    def insertToHand(self, player):
        print(self.hand[self.playerNames[int(player)]], "   ", len(self.hand[self.playerNames[int(player)]]),
              " line 89")
        while len(self.hand[self.playerNames[int(player)]]) < 6:
            x = randint(1, 80)
            while x in self.usedCards:
                x = randint(1, 80)
            self.usedCards.append(x)
            if self.playerNames[int(player)] in self.hand:
                self.hand[self.playerNames[int(player)]].append(str(x))

    def playerlist(self):
        print(self.playerNames)
        lst = []
        for value in self.playerNames.values():
            lst.append(value)
        return lst

    def mixCards(self):
        if len(self.cards) < int(self.numPlayers):
            guess = []
            for _ in self.playerNames.values():
                guess.append("hidden")
            return guess
        mix = []
        used = []
        num = int(self.numPlayers)
        for _ in range(0,
                       num):  # self.cards is the bluffs which get submitted, an array, if all have been submitted then the length should be numPlayers
            x = randint(0, num - 1)
            while x in used:
                x = randint(0, num - 1)
            if len(self.cards) > x:
                used.append(x)
                mix.append(str(self.cards[x]))
        return mix

    def getGuesses(self):
        if len(self.cards) < int(self.numPlayers):
            hiddenGuess = dict()
            for value in self.playerNames.values():
                hiddenGuess[value] = "hidden"
            return json.dumps(hiddenGuess)
        return json.dumps(self.guess)

    def getnextstoryteller(self):
        if self.turn < len(self.names):
            return self.names[self.turn]
        return self.names[0]

    def newTurn(self):
        self.turn += 1
        self.storyTeller = self.getnextstoryteller()
        self.story = ""  # story line
        self.guess = dict()
        self.bluffs = dict()
        self.cards = []
        self.status = 'ready'
        for key in self.scores.keys():
            self.scores[key] = 0

    def newRound(self):
        self.currentRound += 1  # the current round of the game is being played
        self.bluffs = dict()  # what each players bluff is (name:bluff)
        self.cards = []  # all the cards in play in the round(bluffs which are submitted)
        self.guess = dict()  # what each persons guess is including REAL
        self.story = ""  # story line
        self.card = 0  # chosen card for that round

        for key in self.scores.keys():
            self.scores[key] = 0
        self.turn = 0  #
        self.status = 'ready'
        self.storyTeller = self.getnextstoryteller()
        self.usedCards = []
        print("hand is changing", " line 176")
        self.giveoutHand()

    def updateScore(self):
        cntCorrect = 0
        for key in self.guess.keys():
            if key != "*REAL*" and key != self.storyTeller and key in self.guess:
                cntCorrect += 1
        if int(cntCorrect) == 0 or int(cntCorrect) == int(self.numPlayers) - 1:
            for value in self.playerNames.values():
                if value in self.totalscores.keys() and value in self.scores.keys() and str(
                        self.guess.get(value)) == str(self.card):
                    self.totalscores[value] += 2
                    self.scores[value] += 2
        else:
            if self.storyTeller in self.scores and self.storyTeller in self.scores:
                self.totalscores[self.storyTeller] += 3
                self.scores[self.storyTeller] += 3
            for value in self.playerNames.values():  # value is the players names
                if value in self.guess.keys() and value in self.scores.keys() and value in self.totalscores.keys() and \
                        self.guess[value] == str(self.card) and str(value) != str(self.storyTeller) and self.guess[
                    value] == str(self.card):
                    self.totalscores[value] += 3
                    self.scores[value] += 3
                elif value in self.totalscores and value in self.scores:
                    self.totalscores[value] += 1
                    self.scores[value] += 1

    def get_key(self, val):
        for key in self.guess.items():
            if val == key:
                return key
        return "key doesn't exist"


app = Flask(__name__)


def get_game(game_id):  # get the current game object
    if game_id is None or not str(game_id).isnumeric():
        return "game parameter is required and must be a number."
    try:
        return Game.allGames[int(game_id)]
    except KeyError:
        return "No such game"


@app.route("/newgame")
def newgame():
    g = Game()
    players = request.args['numPlayers']
    # rounds= request.args['numRounds']
    # if str(rounds).isnumeric() and int(rounds)>0:
    #     g.rounds=rounds
    # else:
    g.rounds = 3
    if str(players).isnumeric() and int(players) > 0:
        g.numPlayers = players
    else:
        g.numPlayers = 1
    print(str(g.id), " line 238")
    return json.dumps({"gameID": g.id})


@app.route("/register")
def register():
    game = request.args['game']
    print(game, " -game id")
    player = request.args['newPlayer']
    g = get_game(game)
    if type(g) is str:
        return json.dumps({"error": 'No such game'})
    check = g.registerplayer(str(player))
    if str(check).isnumeric():
        return json.dumps({"playerID": check.strip()})
    return check


@app.route("/getPlayerNames")
def getPlayerNames():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    return json.dumps(g.playerlist())


@app.route("/getMyHand")
def getMyHand():
    game = request.args['game']
    player = request.args['player']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    if str(player).isnumeric() and g.playerNames[int(player)] in g.hand:
        print(g.hand[g.playerNames[int(player)]])
        return json.dumps(g.hand[g.playerNames[int(player)]])
    else:
        print("error on line 245")
    return "No such player"


@app.route("/lead")
def lead():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    player = request.args['player']
    card = request.args['card']
    story = request.args['story']
    if g.storyTeller != g.playerNames[int(player)]:
        return "Not your turn"
    if str(card).isnumeric():
        g.card = str(card)
        g.guess['*REAL*'] = str(card)
        g.guess[g.names[g.turn]] = str(card)
        g.cards.append(str(card))
        g.hand[g.playerNames[int(player)]].remove(str(card))
        g.insertToHand(int(player))
    g.story = str(story)
    g.status = 'story_told'
    return "OK"


@app.route("/getStory")
def getStory():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    return g.getStory()


@app.route('/submitBluff')
def submitBluff():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    player = request.args['player']
    bluff = request.args['bluff']
    if str(player).isnumeric() and str(bluff).isnumeric() and int(player) in g.playerNames and str(bluff) in g.hand[
        g.playerNames[int(player)]]:
        g.bluffs[g.playerNames[int(player)]] = str(bluff)
        g.cards.append(str(bluff))
        g.hand[g.playerNames[int(player)]].remove(str(bluff))
        g.insertToHand(int(player))  # add new cards to hand
    return "OK"


@app.route('/getPlayedCards')
def getPlayedCards():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    return json.dumps(g.mixCards())


@app.route('/submitGuess')
def submitGuess():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    player = request.args['player']
    guess = request.args['guess']
    if str(player).isnumeric() and str(guess).isnumeric and int(player) in g.playerNames:
        print("player name is : ", str(g.playerNames[int(player)]), " line 334")
        g.guess[str(g.playerNames[int(player)])] = str(guess)
    else:
        print("player name is but guess is not submitted:( : ", str(g.playerNames[int(player)]), " line 334")
    return "OK"


@app.route('/getGuesses')
def getGuesses():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    guess = g.getGuesses()
    if "*REAL*" in guess and len(g.guess) == len(g.playerNames) + 1:
        g.updateScore()
        if int(g.turn) < int(g.numPlayers) - 1:
            g.newTurn()
        else:
            g.newRound()
    if g.currentRound == g.rounds + 1:
        g.status = "DONE"
    return guess


@app.route('/getScores')
def getScores():  # tab + x
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return 'No such game'
    return json.dumps({'current_scores': g.scores, 'total_scores': g.totalscores})  # figure out how points work:)


@app.route('/getRoundInfo')
def getRoundInfo():
    game = request.args['game']
    g = get_game(game)
    if type(g) is str:
        return json.dumps('No such game')
    if g.currentRound < g.rounds + 1:
        return json.dumps(
            ('Round ' + str(g.currentRound) + ' of ' + str(g.rounds) + ', ' + str(g.storyTeller) + 's turn'))
    if g.currentRound == g.rounds + 1:
        return json.dumps("Game Over")
    print(g.currentRound)
    return json.dumps({"error": str("Game " + str(g.id) + " has not started yet.")})


# if __name__ == "__main__":
# app.run(host='0.0.0.0', port='8888', debug=True)