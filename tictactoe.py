# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui

from board import Board
from engine import Engine
from players import DumbMachinePlayer, HumanPlayer


BUTTON_SIZE = 100
BUTTON_FONT_SIZE = 60
GRID_SPACING = 0


class GameWindow(QtGui.QMainWindow):
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
        if not self.engine.gameRunning:
            event.accept()

        confirm = QtGui.QMessageBox.question(
            self, self.APP_TITLE, self.CONFIRM_QUIT,
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No)
        if confirm == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class BoardWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        engine = kwargs.pop('engine')

        super(BoardWidget, self).__init__(*args, **kwargs)

        self.setupEngine(engine)

        self.setupUi()

    def setupEngine(self, engine):
        self.engine = engine
        self.engine.playerMoved.connect(self.handlePlayerMoved)

    def setupUi(self):
        self.buttons = []

        for position in self.engine.board.positions:
            self.buttons.append(GameButton(position))

        size = 4 * GRID_SPACING + 3 * BUTTON_SIZE
        self.setFixedSize(size, size)

        grid = QtGui.QGridLayout()
        grid.setSpacing(GRID_SPACING)
        self.setLayout(grid)

        for button in self.buttons:
            grid.addWidget(button, button.position / 3, button.position % 3)
            button.playerClicked.connect(self.engine.handleInput)

    def handlePlayerMoved(self, position, player):
        self.buttons[position].markPlayer(player)


class GameButton(QtGui.QPushButton):
    playerClicked = QtCore.pyqtSignal(int)

    def __init__(self, position, *args, **kwargs):
        super(GameButton, self).__init__(*args, **kwargs)

        self.position = position
        # keep track of whether the button was marked or not in order to ignore
        # futher interaction
        self.isMarked = False

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

        font = QtGui.QFont()
        font.setStyleHint(QtGui.QFont.Monospace)
        self.setFont(font)

        self.clicked.connect(self.handleClick)

    def handleClick(self):
        if not self.isMarked:
            self.playerClicked.emit(self.position)

    def markPlayer(self, player):
        self.isMarked = True
        self.setText(str(player))


def main(argv):
    app = QtGui.QApplication(argv)
    the_game = GameWindow()
    the_game.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
