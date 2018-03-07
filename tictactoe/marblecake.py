# -*- coding: utf-8 -*-

from __future__ import absolute_import

from itertools import cycle
from operator import itemgetter

from PyQt4 import QtCore, QtGui

from .players import (
    DumbMachinePlayer, HumanPlayer, MachinePlayer, Player
)


BUTTON_SIZE = 100
BUTTON_FONT_SIZE = 60
BUTTON_BORDER_SIZE = 2
GRID_SPACING = 1
CHARACTER_X = 'X'
CHARACTER_0 = '0'


class GameWindow(QtGui.QMainWindow):
    playerSwitch = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Tic-tac-toe")

        self.statusBar().setSizeGripEnabled(False)

        self.players = [
            HumanPlayer(CHARACTER_X),
            DumbMachinePlayer(CHARACTER_0),
        ]
        self.players_iterator = cycle(self.players)

        self.board = GameBoard(self)
        self.setCentralWidget(self.board)
        self.board.playerMoves.connect(self.switchPlayers)
        self.board.weHaveAWinner.connect(self.handleWinner)
        self.board.weHaveADraw.connect(self.handleDraw)

        width = self.centralWidget().frameGeometry().width()
        height = self.centralWidget().frameGeometry().height() + \
            self.statusBar().frameGeometry().height()
        self.setFixedSize(width, height)

        self.current_player = self.switchPlayers()

    def switchPlayers(self):
        self.current_player = self.players_iterator.next()
        self.current_player.poke(self.board.getAvailableMoves())
        self.statusBar().showMessage(
            "{player} moves".format(player=self.current_player)
        )
        return self.current_player

    def getCurrentPlayer(self):
        return self.current_player

    def handleWinner(self, player):
        self.statusBar().showMessage(
            "{player} wins \:D/".format(player=player)
        )

    def handleDraw(self):
        self.statusBar().showMessage("It's a draw :(")


class GameBoard(QtGui.QWidget):
    playerMoves = QtCore.pyqtSignal()
    weHaveAWinner = QtCore.pyqtSignal(Player)
    weHaveADraw = QtCore.pyqtSignal()

    WINNING_POSITIONS = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [1, 4, 8],
        [2, 4, 6],
    ]

    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)

        self.positions = range(9)
        self.state = [None] * len(self.positions)

        self.buttons = []
        for i in self.positions:
            self.buttons.append(GameButton(i))

        size = 4 * GRID_SPACING + 3 * BUTTON_SIZE + 6 * BUTTON_BORDER_SIZE
        self.setFixedSize(size, size)

        grid = QtGui.QGridLayout()
        grid.setSpacing(GRID_SPACING)
        self.setLayout(grid)

        for button in self.buttons:
            grid.addWidget(button, button.row, button.col)
            button.userInput.connect(self.handleHumanInput)

        for player in self.parent().players:
            if isinstance(player, MachinePlayer):
                player.move.connect(self.handleMachineInput)

    def handleHumanInput(self, position):
        current_player = self.parent().getCurrentPlayer()
        if not isinstance(current_player, HumanPlayer):
            return
        self.move(position, current_player)

    def handleMachineInput(self, position):
        current_player = self.parent().getCurrentPlayer()
        if not isinstance(current_player, MachinePlayer):
            return
        self.move(position, current_player)

    def move(self, position, player):
        if self.state[position]:
            return

        self.state[position] = player
        self.buttons[position].setText(str(player))
        self.playerMoves.emit()
        self.checkState()

    def getAvailableMoves(self):
        return [position for position in self.positions if not self.state[position]]

    def checkState(self):
        for positions in GameBoard.WINNING_POSITIONS:
            state = filter(None, itemgetter(*positions)(self.state))
            is_same_user = len(set(state)) == 1
            if len(state) == 3 and is_same_user:
                self.weHaveAWinner.emit(state[0])

        if len(self.getAvailableMoves()) == 0:
            self.weHaveADraw.emit()


class GameButton(QtGui.QPushButton):
    userInput = QtCore.pyqtSignal(int)

    def __init__(self, value, *args, **kwargs):
        super(GameButton, self).__init__(*args, **kwargs)

        self.value = value
        self.row = self.value / 3
        self.col = self.value % 3

        self.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.setFlat(True)
        styles = [
            'font-size: {font_size}px;',
            'line-height: {font_size}px;',
            'border: {border_size}px solid transparent;',
        ]
        if self.row % 3:
            styles.append('border-top-color: black;')
        if (self.row + 1) % 3:
            styles.append('border-bottom-color: black;')
        if self.col % 3:
            styles.append('border-left-color: black;')
        if (self.col + 1) % 3:
            styles.append('border-right-color: black;')
        style = ' '.join(styles).format(
            font_size=BUTTON_FONT_SIZE,
            border_size=BUTTON_BORDER_SIZE,
        )
        self.setStyleSheet(style)

        font = QtGui.QFont()
        font.setStyleHint(QtGui.QFont.Monospace)
        self.setFont(font)

        self.clicked.connect(self.handleClick)

    def handleClick(self):
        self.userInput.emit(self.value)
