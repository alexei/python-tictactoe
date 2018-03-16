# -*- coding: utf-8 -*-

try:
    from PyQt4.QtCore import QObject, pyqtSignal
except ImportError:
    from PyQt5.QtCore import QObject, pyqtSignal

from players import Player, PlayersGroup


class Engine(QObject):
    '''The game engine

    The game engine is basically a FSM that acts as an arbiter given a board
    and two players
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
