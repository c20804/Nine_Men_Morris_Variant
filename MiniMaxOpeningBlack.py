import sys
from copy import deepcopy

class MiniMaxOpeningBlack:
    def __init__(self, board, output, depth):
        self.board = board
        self.output = output
        self.depth = depth
        self.considered = 0

    # returns a list of board status after possible moves for the color
    def generateAdd(self, board, isWhite):
        L = []
        color = 'W' if isWhite else 'B'
        for location in range(0, len(board)):
            if board[location] == 'x':
                b = deepcopy(board)
                b[location] = color
                if self.closeMill(location, b):
                    L = self.generateRemove(b, L, not isWhite)
                else:
                    L.append(b)
        return L

    def generateMovesOpening(self, board):
        bestScore = 1000
        bestboard = board
        # generate a list of possible boards after adding a black piece
        possibleBoards = self.generateAdd(board, False)
        
        for b in possibleBoards:
            score = self.minimax(b, 1, True)
            if score < bestScore:
                bestScore = score
                bestboard = b
        
        return [bestboard, bestScore]

    def minimax(self, board, d, isWhite):
        if d == self.depth:
            self.considered += 1
            return self.estimation(board)
    
        possibleBoards = self.generateAdd(board, isWhite)
        if isWhite:
            value = -1000
            for b in possibleBoards:
                value = max(value, self.minimax(b, d + 1, False))
            return value
        else:
            value = 1000
            for b in possibleBoards:
                value = min(value, self.minimax(b, d + 1, True))
            return value


    # removes a black piece from the board
    def generateRemove(self, board, L, removeWhite):
        color = 'W' if removeWhite else 'B'
        added = False
        for location in range(0, len(board)):
            if board[location] == color:
                if not self.closeMill(location, board):
                    b = deepcopy(board)
                    b[location] = 'x'
                    L.append(b)
                    added = True
        if not added:
            L.append(board)
        return L

    # parameter j is the location of the piece that was just placed, b is the board
    def closeMill(self, j, b):
        c = b[j]
        if j == 0:
            return (b[1] == c and b[2] == c) or (b[3] == c and b[6] == c)
        elif j == 1:
            return b[0] == c and b[2] == c 
        elif j == 2:
            return (b[0] == c and b[1] == c) or (b[5] == c and b[7] == c) or (b[12] == c and b[21] == c)
        elif j == 3:
            return (b[0] == c and b[6] == c) or (b[4] == c and b[5] == c) or (b[8] == c and b[16] == c)
        elif j == 4:
            return b[3] == c and b[5] == c
        elif j == 5:
            return (b[3] == c and b[4] == c) or (b[2] == c and b[7] == c) or (b[11] == c and b[18] == c)
        elif j == 6:
            return (b[0] == c and b[3] == c) or (b[9] == c and b[13] == c)
        elif j == 7:
            return (b[2] == c and b[5] == c) or (b[10] == c and b[15] == c)
        elif j == 8:
            return (b[3] == c and b[16] == c)
        elif j == 9:
            return (b[6] == c and b[13] == c)
        elif j == 10:
            return (b[7] == c and b[15] == c) or (b[11] == c and b[12] == c)
        elif j == 11:
            return (b[10] == c and b[12] == c) or (b[5] == c and b[18] == c)
        elif j == 12:
            return (b[10] == c and b[11] == c) or (b[2] == c and b[21] == c)
        elif j == 13:
            return (b[6] == c and b[9] == c) or (b[14] == c and b[15] == c) or (b[16] == c and b[19] == c)
        elif j == 14:
            return (b[13] == c and b[15] == c) or (b[17] == c and b[20] == c)
        elif j == 15:
            return (b[7] == c and b[10] == c) or (b[13] == c and b[14] == c) or (b[18] == c and b[21] == c)
        elif j == 16:
            return (b[19] == c and b[13] == c) or (b[17] == c and b[18] == c) or (b[3] == c and b[8] == c)
        elif j == 17:
            return (b[16] == c and b[18] == c) or (b[14] == c and b[20] == c)
        elif j == 18:
            return (b[16] == c and b[17] == c) or (b[11] == c and b[5] == c) or (b[15] == c and b[21] == c)
        elif j == 19:
            return (b[16] == c and b[13] == c) or (b[20] == c and b[21] == c)
        elif j == 20:
            return (b[19] == c and b[21] == c) or (b[14] == c and b[17] == c)
        elif j == 21:
            return (b[19] == c and b[20] == c) or (b[15] == c and b[18] == c) or (b[2] == c and b[12] == c)

    # Estimate the game, each player has 9 pieces
    @staticmethod
    def estimation(board):
        numWhitePieces = 0
        numBlackPieces = 0
        for b in board:
            if b == 'W':
                numWhitePieces += 1
            elif b == 'B':
                numBlackPieces += 1
        return (numWhitePieces - numBlackPieces)

if __name__ == '__main__':
    # get command line arguments: input, output, depth
    if len(sys.argv) < 4:
        print("Usage: python MiniMaxOpeningBlack.py <input> <output> <depth>")
        sys.exit(1)
    else:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        depth = int(sys.argv[3])

    # read input file
    with open(inputFile, 'r') as f:
        board = list(f.readline().strip())

    game = MiniMaxOpeningBlack(board, outputFile, depth)
    bList, bestScore = game.generateMovesOpening(board)

    print("Board Position   : " + ''.join(bList))
    board_position = str(''.join(bList))
    print("Positions evaluated by static estimation: " + str(game.considered))
    print("MINIMAX estimate: " + str(bestScore))
  
    # write to output file
    with open(outputFile, 'w') as f:
        f.write(board_position)