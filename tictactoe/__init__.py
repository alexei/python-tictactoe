# -*- coding: utf-8 -*-

from __future__ import absolute_import

from PyQt4 import QtGui

from .marblecake import GameWindow


def main(argv):
    app = QtGui.QApplication(argv)
    the_game = GameWindow()
    the_game.show()
    app.exec_()
