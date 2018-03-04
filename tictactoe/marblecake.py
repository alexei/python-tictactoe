# -*- coding: utf-8 -*-

import random

from PyQt4 import QtGui


BUTTON_SIZE = 100
BUTTON_FONT_SIZE = 60
BUTTON_BORDER_SIZE = 2
GRID_SPACING = 1
CHARACTER_X = 'X'
CHARACTER_0 = '0'


class GameWindow(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Tic-tac-toe")

        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().showMessage("Click any square to begin")

        board = GameBoard(self)
        self.setCentralWidget(board)

        width = self.centralWidget().frameGeometry().width()
        height = self.centralWidget().frameGeometry().height() + \
            self.statusBar().frameGeometry().height()
        self.setFixedSize(width, height)


class GameBoard(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(GameBoard, self).__init__(*args, **kwargs)

        self.buttons = []
        for i in range(0, 9):
            self.buttons.append(GameButton(i))

        size = 4 * GRID_SPACING + 3 * BUTTON_SIZE + 6 * BUTTON_BORDER_SIZE
        self.setFixedSize(size, size)

        grid = QtGui.QGridLayout()
        grid.setSpacing(GRID_SPACING)
        self.setLayout(grid)

        for button in self.buttons:
            grid.addWidget(button, button.row, button.col)


class GameButton(QtGui.QPushButton):
    def __init__(self, value, *args, **kwargs):
        super(GameButton, self).__init__(*args, **kwargs)

        self.value = value
        self.row = self.value / 3
        self.col = self.value % 3

        self.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.setFlat(True)
        style = ('font-size: {font_size}px;'
                 'line-height: {font_size}px;'
                 'border: {border_size}px solid transparent;')
        if self.row % 3:
            style += 'border-top-color: black;'
        if (self.row + 1) % 3:
            style += 'border-bottom-color: black;'
        if self.col % 3:
            style += 'border-left-color: black;'
        if (self.col + 1) % 3:
            style += 'border-right-color: black;'
        style = style.format(
            font_size=BUTTON_FONT_SIZE,
            border_size=BUTTON_BORDER_SIZE,
        )
        self.setStyleSheet(style)

        font = QtGui.QFont()
        font.setStyleHint(QtGui.QFont.Monospace)
        self.setFont(font)

        self.clicked.connect(self.handleClick)

    def handleClick(self):
        self.setText(random.choice([CHARACTER_X, CHARACTER_0]))
