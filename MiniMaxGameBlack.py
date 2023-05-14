import sys
from copy import deepcopy

class MiniMaxGameBlack:
    def __init__(self, board, output, depth):
        self.board = board
        self.output = output
        self.depth = depth
        self.considered = 0

    def neighbors(self, location):
        if location == 0:
            return [1, 3, 19]
        elif location == 1:
            return [0, 2, 4]
        elif location == 2:
            return [1, 5, 12]
        elif location == 3:
            return [0, 4, 6, 8]
        elif location == 4:
            return [1, 3, 5]
        elif location == 5:
            return [2, 4, 7, 11]
        elif location == 6:
            return [3, 7, 9]
        elif location == 7:
            return [5, 6, 10]
        elif location == 8:
            return [3, 9, 16]
        elif location == 9:
            return [6, 8, 13]
        elif location == 10:
            return [7, 11, 15]
        elif location == 11:
            return [5, 10, 12, 18]
        elif location == 12:
            return [2, 11, 21]
        elif location == 13:
            return [9, 14, 16]
        elif location == 14:
            return [13, 15, 17]
        elif location == 15:
            return [10, 14, 18]
        elif location == 16:
            return [8, 13, 17, 19]
        elif location == 17:
            return [14, 16, 18, 20]
        elif location == 18:
            return [11, 15, 17, 21]
        elif location == 19:
            return [0, 16, 20]
        elif location == 20:
            return [17, 19, 21]
        elif location == 21:
            return [12, 18, 20]

    def GenerateHopping(self, board, isWhite):
        L = []
        color = 'W' if isWhite else 'B'
        for location in range(len(board)):
            if board[location] == color:
                for next in range(len(board)):
                    if board[next] == 'x':
                        b = deepcopy(board)
                        b[location] = 'x'
                        b[next] = color
                        if self.closeMill(next, b):
                            L = self.generateRemove(b, L, not isWhite)
                        else:
                            L.append(b)
        return L


    # returns a list of board status after possible moves for the white
    def generateMove(self, board, isWhite):
        L = []
        color = 'W' if isWhite else 'B'
        for location in range(len(board)):
            if board[location] == color:
                n = self.neighbors(location)
                for neighbor in n:
                    if board[neighbor] == 'x':
                        b = deepcopy(board)
                        b[location] = 'x'
                        b[neighbor] = color
                        if self.closeMill(neighbor, b):
                            L = self.generateRemove(b, L, not isWhite)
                        else:
                            L.append(b)
        return L


    def generateMovesMidgame(self, board):
        bestScore = float('inf')
        bestboard = board
        possibleBoards = self.generateMove(board, False)
        
        for b in possibleBoards:
            score = self.minimax(b, 1, True)
            if score < bestScore:
                bestScore = score
                bestboard = b
        
        return [bestboard, bestScore]


    # removes a piece from the board
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
            return (b[0] == c and b[2] == c) 
        elif j == 2:
            return (b[0] == c and b[1] == c) or (b[5] == c and b[7] == c) or (b[12] == c and b[21] == c)
        elif j == 3:
            return (b[0] == c and b[6] == c) or (b[4] == c and b[5] == c) or (b[8] == c and b[16] == c)
        elif j == 4:
            return (b[3] == c and b[5] == c)
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
    
    
    def countPieces(self, board, isWhite):
        numWhitePieces = 0
        numBlackPieces = 0
        for b in board:
            if b == 'W':
                numWhitePieces += 1
            elif b == 'B':
                numBlackPieces += 1
        return numWhitePieces if isWhite else numBlackPieces

    def minimax(self, board, d, maximizingPlayer):
        # if leaf node
        if d == self.depth:
            self.considered += 1
            return self.estimation(board)

        pieces = self.countPieces(board, maximizingPlayer)
        if pieces <= 3:
            possibleBoards = self.GenerateHopping(board, maximizingPlayer)
        else:
            possibleBoards = self.generateMove(board, maximizingPlayer)

        if maximizingPlayer:
            value = float('-inf')
            for b in possibleBoards:
                value = max(value, self.minimax(b, d + 1, False))
            return value
        else:
            value = float('inf')
            for b in possibleBoards:
                value = min(value, self.minimax(b, d + 1, True))
            return value

    # Estimate the game, each player has 9 pieces
   # @staticmethod
    def estimation(self, board):
        numWhitePieces = self.countPieces(board, True)
        numBlackPieces = self.countPieces(board, False)

        if (numBlackPieces <= 3):
            blackMoves = self.GenerateHopping(board, False)
        else:
            blackMoves = self.generateMove(board, False)

        numBlackMoves = len(blackMoves)

        if (numBlackPieces <= 2): return 10000
        elif (numWhitePieces <= 2): return -10000
        elif (numBlackPieces == 0): return 10000
        else: return (1000 * (numWhitePieces - numBlackPieces) - numBlackMoves)


if __name__ == '__main__':
    # get command line arguments: input, output, depth
    if len(sys.argv) < 4:
        print("Usage: python MiniMaxGameBlack.py <input> <output> <depth>")
        sys.exit(1)
    else:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        depth = int(sys.argv[3])

    # read input file
    with open(inputFile, 'r') as f:
        board = list(f.readline().strip())

    game = MiniMaxGameBlack(board, outputFile, depth)
    bList, bestScore = game.generateMovesMidgame(board)

    print("Board Position   : " + ''.join(bList))
    board_position = str(''.join(bList))
    print("Positions evaluated by static estimation: " + str(game.considered))
    print("MINIMAX estimate: " + str(bestScore))
  
    # write to output file
    with open(outputFile, 'w') as f:
        f.write(board_position)