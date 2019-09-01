#!/usr/bin/env python

from random import randint

class Tile(object):
    def __init__(self, safe, rollagain):
        self.safe = safe
        self.rollagain = rollagain
        self.piece = 0

class Player(object):
    def __init__(self, player, path):
        self.player = player
        self.path = path
        self.score = 0
        #number of piece each player has ready to move onto the board
        self.reserve = 7

def board_init():
    #assumes the most likely configuration of paths
    #to use alternatives, maybe a new function or
	#some if/else stuff
    #initializes all the tiles
    board = [[Tile(False, False) for y in range(3)] for x in range(8)]
    #designates the safe spaces
    board[3][1].safe = True
    #designates the spaes that let you roll agian
    for n in [[0, 0], [0, 2], [7, 0], [7, 2], [3, 1]]:
         board[n[0]][n[1]].rollagain = True
    #initializes the traditional paths
    path1 = [board[x][0] for x in range(3, -1, -1)]
    path2 = [board[x][2] for x in range(3, -1, -1)]
    for x in range(8):
        path1.append(board[x][1])
        path2.append(board[x][1])
    for x in range(7, 5, -1):
        path1.append(board[x][0])
        path2.append(board[x][2])
    players = [Player(1, path1), Player(2, path2)]
    return board, players

def roll():
    return sum(randint(0, 1) for _ in range(4))

def printboard(board):
    horedge = "\033[0;37;40m+---+---+---+---+       +---+---+"
    hormid = "\033[0;37;40m+---+---+---+---+---+---+---+---+"
    print(horedge)
    print(printline(board,0))
    print(hormid)
    print(printline(board,1))
    print(hormid)
    print(printline(board,2))
    print(horedge)
    return

def printline(board, y):
    output = "\033[0;37;40m|"
    for x in range(len(board)):
        if board[x][y].piece == 0:
            output += "   "
        elif board[x][y].piece == 1:
            output += "\033[0;37;41m   "
        elif board[x][y].piece == 2:
            output += "\033[0;37;44m   "
        if (((y == 0) or (y == 2)) and (x == 4)):
            output += " "
        else:
            output += "\033[0;37;40m|"
    return output

def turn(board, players, playerturn):
    diceroll = roll()
    #find legal moves
    #counts pieces from the start to the finish for designations
    legalmoves = []
    if players[playerturn].reserve > 0:
        if players[playerturn].path[diceroll] != (playerturn + 1):
            legalmoves.append(0)
    count = 0
    for pos in range(len(players[playerturn].path)):
        if players[playerturn].path[pos + diceroll].piece == (playerturn + 1):
            count += 1
            if (pos + diceroll) <= len(players[playerturn].path):
                if players[playerturn].path[pos + diceroll] != (playerturn + 1):
                    if players[playerturn].path[pos + diceroll].safe == False:
                        legalmoves.append(count)
    #gets player input
    if len(legalmoves) == 0:
        print('no legal moves or roll of zero: skipping turn')
        playerturn = (playerturn + 1) % 2
    else:
        print('legal moves are: {}'.format(legalmoves))
        print('pieces are numbered in order from start to finish')
        print('moving pieces onto the table is 0')
        while (choice in legalmoves) == false:
            print('select which piece to move')
            choice = input()
        #finds the choice
        count = 0
        for pos in range(len(players[playerturn].path)):
            if players[playerturn].path[pos + diceroll].piece == (playerturn + 1):
                count += 1
                if count == choice:
                    startspace = pos
                    endspace = pos + diceroll
        #resolve move
        players[playerturn].path[startspace].piece = 0
        if endspace == len(players[playerturn].path):
            players[playerturn].score += 1
        else:
            if players[playerturn].path[endspace].piece != 0:
                players[(playerturn + 1) % 2].reserve += 1
            players[playerturn].path[endspace].piece = playerturn + 1
        #figure out who rolls next
        if  players[playerturn].path[endspace].rollagain == False:
            playerturn = (playerturn + 1) % 2
    return board, players, playerturn

def wincon(players):
    if players[0].score == 7:
        print("Player 1 Wins!")
        return True
    elif players[1].score == 7:
        print("Player 2 Wins!")
        return True
    else:
        return False

def main():    
    #initializes the game
    board, players = board_init()
    #takes each player turn
    playerturn = randint(0, 1)
    while True:
        board, players, playerturn = turn(
                board, players, playerturn
                )
        printboard(board)
        #exits if anyone wins
        if wincon(players) == True:
            break
        
if __name__ == '__main__':
    main()
