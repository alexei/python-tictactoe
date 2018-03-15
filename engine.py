# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from players import Player, PlayersGroup


class Engine(QtCore.QObject):
    gameStarted = QtCore.pyqtSignal()
    roundStarted = QtCore.pyqtSignal()
    roundEnded = QtCore.pyqtSignal()
    gameEnded = QtCore.pyqtSignal()
    playerMoved = QtCore.pyqtSignal(int, Player)

    ROLE_X = 'X'
    ROLE_0 = '0'

    def __init__(self, board, player_1, player_2, *args, **kwargs):
        super(Engine, self).__init__(*args, **kwargs)

        self.board = board
        self.board.playerMoved.connect(self.handlePlayerMove)

        self.players = PlayersGroup(player_1, player_2)

    def startGame(self):
        self.gameStarted.emit()

        self.gameRunning = True

        if self.gameRunning and self.board.hasAvailablePositions():
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
        self.gameEnded.emit()

        self.gameRunning = False

    def handlePlayerMove(self, position, player):
        self.awaitingMove = False

        self.playerMoved.emit(position, player)

        self.endRound()

    def handleInput(self, position):
        if self.awaitingMove and getattr(self.players.current(), 'acceptInput', None):
            self.players.current().acceptInput(position)
