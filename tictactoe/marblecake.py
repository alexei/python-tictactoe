# -*- coding: utf-8 -*-

import random

from PyQt4 import QtGui


BUTTON_SIZE = 100
BUTTON_FONT_SIZE = 60
BUTTON_BORDER_SIZE = 2
GRID_SPACING = 0
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

        size = 3 * (BUTTON_SIZE + GRID_SPACING) + 6 * BUTTON_BORDER_SIZE
        self.setFixedSize(size, size)

        grid = GameGrid()
        self.setLayout(grid)


class GameGrid(QtGui.QGridLayout):
    def __init__(self, *args, **kwargs):
        super(GameGrid, self).__init__(*args, **kwargs)

        self.setSpacing(GRID_SPACING)

        for i in range(0, 9):
            row = i / 3
            col = i % 3
            button = GameButton(row, col)
            self.addWidget(button, row, col)


class GameButton(QtGui.QPushButton):
    def __init__(self, row, col, *args, **kwargs):
        super(GameButton, self).__init__(*args, **kwargs)

        self.row = row
        self.col = col
        self.value = row * 3 + col

        self.setText(random.choice([CHARACTER_X, CHARACTER_0]))

        self.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.setFlat(True)
        style = ("font-size: {font_size}px;"
                 "line-height: {font_size}px;"
                 "border: {border_size}px dotted transparent;")
        if row % 3:
            style += "border-top-color: black;"
        if col % 3:
            style += "border-left-color: black;"
        style = style.format(
            font_size=BUTTON_FONT_SIZE,
            border_size=BUTTON_BORDER_SIZE,
        )
        self.setStyleSheet(style)

        font = QtGui.QFont()
        font.setStyleHint(QtGui.QFont.Monospace)
        self.setFont(font)
