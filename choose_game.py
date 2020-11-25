import sys
import sqlite3
import random
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog, QTableWidgetItem

from game_with_cards import GameWithCards

from game_with_cards2 import Game

class ChooseGame(QDialog):
    def __init__(self, par):
        self.par = par
        super(ChooseGame, self).__init__()
        uic.loadUi('choose_game.ui', self)
        self.setWindowTitle(f"Выбор игры с набором: {self.par.set_name}")
        self.rejected.connect(self.quit)  # если он нажмет cancle
        self.accepted.connect(self.quit)  # если он нажмет yes
        self.game1.clicked.connect(self.start_game_1)
        self.game2.clicked.connect(self.start_game_2)

        self.set_name = par.set_name
        self.login = par.login
        self.set_name = par.set_name

    def start_game_1(self):
        self.x = GameWithCards(parent=self)
        self.hide()
        self.x.show()

    def start_game_2(self):
        self.x = Game(parant=self)
        self.hide()
        self.x.show()


    def quit(self):
        self.hide()
        self.par.show()