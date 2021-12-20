import copy
import random

class Board:
	def __init__(self, side1='x', side2='o'):
		self.board = [[None, None, None], [None, None, None], [None, None, None]]

		self.side1 = side1
		self.side2 = side2

		self.currentTurn = side1

	def Winner(self):
		if self.board[0][0] == self.board[1][1] == self.board[2][2] != None: return self.board[0][0]
		if self.board[0][2] == self.board[1][1] == self.board[2][0] != None: return self.board[0][2]
		
		if self.board[0][0] == self.board[1][0] == self.board[2][0] != None: return self.board[0][0]
		if self.board[0][1] == self.board[1][1] == self.board[2][1] != None: return self.board[0][1]
		if self.board[0][2] == self.board[1][2] == self.board[2][2] != None: return self.board[0][2]

		if self.board[0][0] == self.board[0][1] == self.board[0][2] != None: return self.board[0][0]
		if self.board[1][0] == self.board[1][1] == self.board[1][2] != None: return self.board[1][0]
		if self.board[2][0] == self.board[2][1] == self.board[2][2] != None: return self.board[2][0]

		return None

	def PossibleMoves(self):
		moves = []
		for y in range(3):
			for x in range(3):
				if self.board[y][x] == None: moves += [(y, x)]

		return moves

	def Push(self, position):
		if self.board[position[0]][position[1]] == None:
			self.board[position[0]][position[1]] = self.currentTurn
		else:
			raise BaseException("Move already has been played")

		self.currentTurn = self.side1 if self.currentTurn == self.side2 else self.side2

	# __str__
	def string(self):
		res = ""
		for y in self.board:
			for x in y:
				res += x if x != None else '.'
				res += ' '
			res += '\n'

		return res

def BestMove(board, side='x'):
	if not board.PossibleMoves() and not board.Winner(): return (None, 0)
	elif board.Winner(): 
		return (None, 1) if board.Winner() == side else (None, -1)

	enemyMove = board.currentTurn != side

	moves = board.PossibleMoves()
	results = {}
	for move in moves:
		newBoard = copy.deepcopy(board)
		newBoard.Push(move)
		results[move] = BestMove(newBoard, side)[1] # WARNING: If not to make a move, recursion error will be in copy

	if enemyMove: results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1])}

	else: results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}

	result = []
	for res in results.items():
		if (res[1] >= max(results.values()) and not enemyMove) or (res[1] <= min(results.values()) and enemyMove): #WARNING: speed
			result += [res]
	return random.choice(result)

board = Board()
inp = input("Your side (x or o): ")

if inp.upper() == 'O':
	while board.Winner() == None and board.PossibleMoves():
		move = BestMove(board)
		board.Push(move[0])

		print(board.string())
		print("Moving to", move[0], "with prediction", move[1])
		print()

		if not (board.Winner() == None and board.PossibleMoves()): break
		while True:
			try:
				move = input("> ")
				board.Push((int(move[0])-1, int(move[1])-1)) #WARNING: +-1
				break
			except BaseException as e:
				print(e, "\n")
else:
	while board.Winner() == None and board.PossibleMoves():
		while True:
			try:
				move = input("> ")
				board.Push((int(move[0])-1, int(move[1])-1)) #WARNING: +-1
				break
			except BaseException as e:
				print(e, "\n")

		if not (board.Winner() == None and board.PossibleMoves()): break

		move = BestMove(board, side='o')
		board.Push(move[0])

		print(board.string())
		print("Moving to", move[0], "with prediction", move[1])

print("\nThe winner:", board.Winner())
