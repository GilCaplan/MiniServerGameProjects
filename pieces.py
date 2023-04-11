in_range = lambda x: 0 <= x < 8
class Rook:
    def __init__(self, color, pos):
        self.name = "R" + str(color)
        self.color = color
        self.pos = pos

    def move(self, board = None):
        in_range = lambda x: 0 <= x < 8
        posses = []
        row, col = self.pos# row is number, col is letter
        if not in_range(row+1) and not in_range(row-1) and not in_range(col+1) and not in_range(col-1):
            return []
        for movement in [[0,1],[1,0]]:
            for dir in [-1,1]:
                new_row = row + dir*movement[0] 
                new_col = col + dir*movement[1]
                while in_range(new_row) and in_range(new_col) and board[new_row][new_col] is False:
                    print("in range to attack: ", target([new_row, new_col]))
                    posses.append(target([new_row, new_col]))
                    new_row += dir*movement[0] 
                    new_col += dir*movement[1]
                if in_range(new_row) and in_range(new_col) and board[new_row][new_col].color is not self.color:
                    posses.append(target([new_row, new_col]))
        print(posses)
        return posses
    def coords(self):
        l = getNum(int(self.pos[1]))
        n=str(self.pos[0]+1)
        return l+n
        
class Knight:
    def __init__(self, color, pos):
        self.name ="N"+ str(color)
        self.color = color
        self.pos = pos

    def move(self, board = None):
        in_range = lambda x: 0 <= x < 8
        posses = []
        row, col = self.pos
        for dir in [[1,2],[2,1]]:
            for dirC in [-1,1]:
                new_col = col + dirC*dir[0]
                for dirR in [-1,1]:
                    new_row = row + dirR*dir[1]
                    if in_range(new_row) and in_range(new_col) and (board[new_row][new_col] is False or board[new_row][new_col].color != self.color):
                        posses.append(target([new_row, new_col]))
        return posses
    def coords(self):
        l = getNum(self.pos[1])
        n = str(self.pos[0])
        return l+n
class Pawn:
    def __init__(self, color, pos):
        self.name ="P"+ str(color)
        self.color = color
        self.pos = pos #[number, letter]
        
    def move(self, board = None):
        in_range = lambda x: 0 <= x < 8
        move_dir = 1 if self.color == "w" else -1
        posses = []
        row, col = self.pos
        new_row = row + move_dir
        if not in_range(new_row):
            return []
        if board[new_row][col] is False:#checks if that location is false
            posses.append([col, new_row])#add it
            is_at_starting_pos = row == {'w': 1, 'b': 6}[self.color]# boolean if pawn is at initial location of the game
            if is_at_starting_pos and board[row + move_dir * 2][col] is False: 
                posses.append([col, new_row + move_dir])
        for diagonal in [1, -1]:
            if in_range(col + diagonal) and board[new_row][col + diagonal] and board[new_row][col + diagonal].color != self.color:
                posses.append([col + diagonal, new_row])
        return [getNum(c) + str(r + 1) for c, r in posses]
    def coords(self):
        l = getNum(self.pos[1])
        n = str(self.pos[0])
        return l+n

class Bishop:
    def __init__(self, color, pos):
        self.name ="B"+ str(color)
        self.color = color
        self.pos = pos
    def move(self, board = None):
        in_range = lambda x: 0 <= x < 8
        posses = []
        row, col = self.pos
        for dirC in [1,-1]:
            new_col = col + dirC
            for dirR in [-1 , 1]:
                new_row = row + dirR
                while in_range(new_row) and in_range(new_col) and board[new_row][new_col] is False:
                    posses.append(target([new_row, new_col]))
                    new_row += dirR 
                    new_col += dirC
                if in_range(new_row) and in_range(new_col) and board[new_row][new_col].color != self.color:
                    posses.append(target([new_row, new_col]))#target formats row and col to a2 (example)
                new_col = col + dirC
                new_row = row + dirR
        return posses
    def coords(self):
        l = getNum(self.pos[1])
        n = str(self.pos[0])
        return l+n
class King:
    def __init__(self, color, pos):
        self.name = "K"+ str(color)
        self.color = color
        self.pos =pos
    def move(self, board = None):
        in_range = lambda x: 0 <= x < 8
        posses = []
        row, col = self.pos
        if not in_range(row+1) and not in_range(row-1) and not in_range(col+1) and not in_range(col-1):
            return []
        for dirC in [1,-1, 0]:
            new_col = col + dirC
            for dirR in [1,-1,0]:
                new_row = row+ dirR
                if in_range(new_row) and in_range(new_col) and (board[new_row][new_col] is False or board[new_row][new_col].color != self.color) and self.checkForKing([row+dirR,col+dirC], board):
                    posses.append(target([new_row, new_col]))
        print(posses)
        return posses
    def coords(self):
        l = getNum(self.pos[1])
        n = str(self.pos[0])
        return l+n
    def checkForKing(self, coord, board):#coord -> (row, col)
        row, col = coord
        for dirC in [1,-1, 0]:
            new_col = col + dirC
            for dirR in [1,-1,0]:
                new_row = row + dirR
                if in_range(new_col) and in_range(new_row) and board[new_row][new_col] is not False and board[new_row][new_col].name[0] == "K" and board[new_row][new_col].color != self.color:
                    print("no no no n o")
                    return False
        return True
class Queen:
    def __init__(self, color, pos):
        self.name = "Q"+ str(color)
        self.color = color
        self.pos = pos
    def move(self, board = None):
        return Rook.move(self, board) + Bishop.move(self, board)
    def coords(self):
        l = getNum(self.pos[1])
        n = str(self.pos[0])
        return l+n
def target(arr):
    l = getNum(int(arr[1]))
    n=str(arr[0]+1)
    return l+n
def getNum(PieceRow):
    if type(PieceRow) is int:
        return ['a','b','c','d','e','f','g','h'][PieceRow]
    return {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}[PieceRow]
