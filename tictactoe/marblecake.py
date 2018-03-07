# -*- coding: utf-8 -*-

from functools import partial
from itertools import cycle
import random

from PyQt4 import QtCore, QtGui


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


class GameBoard(QtGui.QWidget):
    playerMoves = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)

        self.positions = range(9)
        self.values = [None] * len(self.positions)

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
            button.userInput.connect(self.handleInput)

        for player in self.parent().players:
            if isinstance(player, BaseMachinePlayer):
                player.move.connect(self.handleInput)

    def handleInput(self, position):
        current_player = self.parent().getCurrentPlayer()
        self.move(position, current_player)

    def move(self, position, player):
        if self.values[position]:
            return

        self.values[position] = player
        self.buttons[position].setText(str(player))
        self.playerMoves.emit()

    def getAvailableMoves(self):
        return [position for position in self.positions if not self.values[position]]


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


class BasePlayer(QtCore.QObject):
    def __init__(self, role, *args, **kwargs):
        super(BasePlayer, self).__init__(*args, **kwargs)

        self.role = role

    def __str__(self):
        return str(self.role)

    def __unicode__(self):
        return unicode(self.role)

    def poke(self, *args, **kwargs):
        pass


class BaseMachinePlayer(BasePlayer):
    move = QtCore.pyqtSignal(int)


class DumbMachinePlayer(BaseMachinePlayer):
    def __init__(self, *args, **kwargs):
        super(DumbMachinePlayer, self).__init__(*args, **kwargs)

    def poke(self, available_moves=[]):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(partial(self._move, available_moves))
        self.timer.start(1000)

    def _move(self, available_moves=[]):
        self.timer.stop()
        if available_moves:
            self.move.emit(random.choice(available_moves))


class HumanPlayer(BasePlayer):
    pass
