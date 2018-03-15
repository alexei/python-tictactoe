# -*- coding: utf-8 -*-

from operator import itemgetter

from PyQt4 import QtCore

from players import Player


class Board(QtCore.QObject):
    playerMoved = QtCore.pyqtSignal(int, Player)

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
        return len(filter(None, self.state)) != len(self.positions)

    def getAvailablePositions(self):
        return [
            position for position, value in enumerate(self.state) if not value
        ]

    def getWinner(self):
        for winningState in self.WINNING_STATES:
            # compare winning state to actual state
            actualState = filter(None, itemgetter(*winningState)(self.state))
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
