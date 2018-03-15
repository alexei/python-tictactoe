# -*- coding: utf-8 -*-

from itertools import cycle
import random

from PyQt4 import QtCore


class PlayersGroup(object):
    def __init__(self, player_1, player_2):
        self.players = [player_1, player_2]
        self.playersIterator = cycle(self.players)
        self.currentPlayer = None

    def current(self):
        return self.currentPlayer

    def switch(self):
        self.currentPlayer = self.playersIterator.next()


class Player(object):
    def __init__(self, role, board):
        self.role = role
        self.board = board

    def __str__(self):
        return str(self.role)

    def headsUp(self):
        pass


class HumanPlayer(Player):
    def acceptInput(self, position):
        self.board.move(position, self)


class MachinePlayer(Player):
    pass


class DumbMachinePlayer(MachinePlayer):
    def headsUp(self):
        def move():
            self.timer.stop()
            if self.board.hasAvailablePositions():
                self.board.move(
                    random.choice(self.board.getAvailablePositions()), self
                )
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(move)
        self.timer.start(500)
