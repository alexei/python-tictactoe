# -*- coding: utf-8 -*-

from functools import partial
import random

from PyQt4 import QtCore


__all__ = [
    'MachinePlayer',
    'DumbMachinePlayer',
    'HumanPlayer',
    'Player',
]


class Player(QtCore.QObject):
    def __init__(self, role, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        self.role = role

    def __str__(self):
        return str(self.role)

    def __unicode__(self):
        return unicode(self.role)

    def poke(self, *args, **kwargs):
        pass


class MachinePlayer(Player):
    move = QtCore.pyqtSignal(int)


class DumbMachinePlayer(MachinePlayer):
    def __init__(self, *args, **kwargs):
        super(DumbMachinePlayer, self).__init__(*args, **kwargs)

    def poke(self, available_moves=[]):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(partial(self._move, available_moves))
        self.timer.start(500)

    def _move(self, available_moves=[]):
        self.timer.stop()
        if available_moves:
            self.move.emit(random.choice(available_moves))


class HumanPlayer(Player):
    pass
