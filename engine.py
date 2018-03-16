# -*- coding: utf-8 -*-

from builtins import next
from itertools import cycle
from operator import itemgetter
import random

try:
    from PyQt4.QtCore import pyqtSignal, QObject, QTimer
except ImportError:
    from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class Player(object):
    ''' Represent a player of any kind
    '''

    def __init__(self, role, board):
        self.role = role
        self.board = board

    def __str__(self):
        return str(self.role)

    def headsUp(self):
        ''' A way to notify a player that it's their turn. A machine would
        need such behavior so it knows it's time to make their move.
        '''

        pass


class HumanPlayer(Player):
    ''' Represents a human player
    '''

    def acceptInput(self, position):
        ''' A human player might require UI, CLI or other means to submit their
        move.
        '''

        self.board.move(position, self)


class MachinePlayer(Player):
    ''' Represents a machine player

    Might be powered by AI or a simple random number generator
    '''

    pass


class DumbMachinePlayer(MachinePlayer):
    ''' The Dumb Machine Player is pretty much random
    '''

    def headsUp(self):
        def move():
            self.timer.stop()
            if self.board.hasAvailablePositions():
                self.board.move(
                    random.choice(self.board.getAvailablePositions()), self
                )
        self.timer = QTimer()
        self.timer.timeout.connect(move)
        self.timer.start(500)


class PlayersGroup(object):
    ''' Groups players together and manages turns
    '''

    def __init__(self, player_1, player_2):
        self.players = [player_1, player_2]
        self.playersIterator = cycle(self.players)
        self.currentPlayer = None

    def current(self):
        return self.currentPlayer

    def switch(self):
        self.currentPlayer = next(self.playersIterator)


class Board(QObject):
    ''' The board keeps track of available positions and moves
    '''

    playerMoved = pyqtSignal(int, Player)

    WINNING_STATES = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)

        self.positions = range(9)
        self.state = [''] * len(self.positions)

    def hasAvailablePositions(self):
        return len([p for p in self.state if p]) != len(self.positions)

    def getAvailablePositions(self):
        return [
            position for position, value in enumerate(self.state) if not value
        ]

    def getWinner(self):
        for winningState in self.WINNING_STATES:
            # compare winning state to actual state
            actualState = [p for p in itemgetter(*winningState)(self.state) if p]
            # check if these positions are marked and they belong to the
            # same player
            if len(actualState) == 3 and len(set(actualState)) == 1:
                return actualState[0]

    def move(self, position, player):
        # prevent accidents
        if self.state[position]:
            return

        self.state[position] = player

        self.playerMoved.emit(position, player)


class Engine(QObject):
    '''The actual game engine

    The game engine is basically a finite state machine that acts as an arbiter
    given a board and two players
    '''

    gameStarted = pyqtSignal()
    roundStarted = pyqtSignal()
    roundEnded = pyqtSignal()
    gameEnded = pyqtSignal()
    playerMoved = pyqtSignal(int, Player)

    ROLE_X = 'X'
    ROLE_0 = '0'

    def __init__(self, board, player_1, player_2, *args, **kwargs):
        super(Engine, self).__init__(*args, **kwargs)

        self.board = board
        self.board.playerMoved.connect(self.handlePlayerMove)

        self.players = PlayersGroup(player_1, player_2)

        self.gameRunning = False
        self.awaitingMove = False

    def startGame(self):
        self.gameStarted.emit()

        self.gameRunning = True

        if self.board.hasAvailablePositions():
            self.players.switch()
            self.startRound()
        else:
            self.endGame()

    def startRound(self):
        self.roundStarted.emit()

        self.awaitingMove = True
        self.players.current().headsUp()

    def endRound(self):
        self.roundEnded.emit()

        if self.board.getWinner():
            self.endGame()
        elif self.gameRunning and self.board.hasAvailablePositions():
            self.players.switch()
            self.startRound()
        else:
            self.endGame()

    def endGame(self):
        self.gameRunning = False

        self.gameEnded.emit()

    def handlePlayerMove(self, position, player):
        self.awaitingMove = False

        self.playerMoved.emit(position, player)

        self.endRound()

    def handleInput(self, position):
        # pass input to current player only if they are able to accept it
        if self.awaitingMove and getattr(self.players.current(), 'acceptInput', None):
            self.players.current().acceptInput(position)
