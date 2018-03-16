# -*- coding: utf-8 -*-

import sys

try:
    from PyQt4.QtCore import pyqtSignal
    from PyQt4.QtGui import (
        QApplication, QButtonGroup, QFont, QGridLayout, QMainWindow,
        QMessageBox, QPushButton, QWidget,
    )
except ImportError:
    from PyQt5.QtCore import pyqtSignal
    from PyQt5.QtGui import QFont
    from PyQt5.QtWidgets import (
        QApplication, QButtonGroup, QGridLayout, QMainWindow, QMessageBox,
        QPushButton, QWidget,
    )

from board import Board
from engine import Engine
from players import DumbMachinePlayer, HumanPlayer


BUTTON_SIZE = 100
BUTTON_FONT_SIZE = 60
GRID_SPACING = 0


class GameWindow(QMainWindow):
    APP_TITLE = "Tic-tac-toe"
    MESSAGE_WAIT = "{player} moves"
    MESSAGE_WIN = "{player} wins \:D/"
    MESSAGE_DRAW = "It's a draw :|"
    CONFIRM_QUIT = "The game is still running. Are you sure you want to quit?"

    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(*args, **kwargs)

        self.setupEngine()

        self.setupUi()

        self.startGame()

    def setupEngine(self):
        ''' Sets up game engine

        By default, we're creating a human vs machine game
        '''

        board = Board()

        player_1 = HumanPlayer(Engine.ROLE_X, board)
        player_2 = DumbMachinePlayer(Engine.ROLE_0, board)

        self.engine = Engine(board, player_1, player_2)
        self.engine.roundStarted.connect(self.handleRoundStarted)
        self.engine.gameEnded.connect(self.handleGameEnded)

    def setupUi(self):
        self.setWindowTitle(self.APP_TITLE)

        self.boardWidget = BoardWidget(self, engine=self.engine)
        self.setCentralWidget(self.boardWidget)

        # compute contents sizes and set a fixed size on the window
        width = self.centralWidget().frameGeometry().width()
        height = self.centralWidget().frameGeometry().height() + \
            self.statusBar().frameGeometry().height()
        self.setFixedSize(width, height)

        # prevent resizing
        self.statusBar().setSizeGripEnabled(False)

    def startGame(self):
        self.engine.startGame()

    def handleRoundStarted(self):
        # notify player when it's their turn
        player = self.engine.players.current()
        self.notify(self.MESSAGE_WAIT.format(player=player))

    def handleGameEnded(self):
        # when the game ends, notify user if we have a winner
        winner = self.engine.board.getWinner()
        if winner:
            self.notify(self.MESSAGE_WIN.format(player=winner))
        else:
            self.notify(self.MESSAGE_DRAW)

    def notify(self, message):
        self.statusBar().showMessage(message)

    def closeEvent(self, event):
        if self.engine.gameRunning:
            confirm = QMessageBox.question(
                self, self.APP_TITLE, self.CONFIRM_QUIT,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)
            if confirm == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


class BoardWidget(QWidget):
    def __init__(self, *args, **kwargs):
        engine = kwargs.pop('engine')

        super(BoardWidget, self).__init__(*args, **kwargs)

        self.setupEngine(engine)

        self.setupUi()

    def setupEngine(self, engine):
        self.engine = engine
        self.engine.playerMoved.connect(self.handlePlayerMoved)

    def setupUi(self):
        grid = QGridLayout()
        grid.setSpacing(GRID_SPACING)
        self.setLayout(grid)

        self.buttonGroup = QButtonGroup()
        for position in self.engine.board.positions:
            button = GameButton(position)
            self.buttonGroup.addButton(button, position)
            grid.addWidget(button, position / 3, position % 3)
        self.buttonGroup.buttonClicked['int'].connect(self.engine.handleInput)

        size = 4 * GRID_SPACING + 3 * BUTTON_SIZE
        self.setFixedSize(size, size)

    def handlePlayerMoved(self, position, player):
        self.buttonGroup.buttons()[position].markPlayer(player)


class GameButton(QPushButton):
    def __init__(self, position, *args, **kwargs):
        super(GameButton, self).__init__(*args, **kwargs)

        self.position = position

        self.setupUi()

    def setupUi(self):
        self.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)

        styles = [
            'font-size: {font_size}px;',
            'line-height: {font_size}px;',
        ]
        style = ' '.join(styles).format(
            font_size=BUTTON_FONT_SIZE,
        )
        self.setStyleSheet(style)

        font = QFont()
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

    def markPlayer(self, player):
        self.setText(str(player))


def main(argv):
    app = QApplication(argv)
    the_game = GameWindow()
    the_game.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
