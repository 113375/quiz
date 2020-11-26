import sys
import sqlite3
import os
import random
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog, QTableWidgetItem
from func_for_texts import read_and_del_articles
from game_with_text import GameWithText


class ChoiceEx(QDialog):
    def __init__(self, par=None):
        super(ChoiceEx, self).__init__()

        uic.loadUi("choose_ex.ui", self)
        self.prepositions.clicked.connect(self.start_prep)
        self.articles.clicked.connect(self.start_art)

        self.setWindowTitle("Темы для заданий")

    def start_prep(self):
        i, okPressed = QInputDialog.getInt(self, "Введите количество абзацев", "", 1, 1, 20, 1)
        if okPressed:
            self.g = GameWithText(count=i, par=self, items=['on', 'at', 'on', "in", "by", "for"])
            self.g.show()
            self.hide()

    def start_art(self):
        i, okPressed = QInputDialog.getInt(self, "Введите количество абзацев", "", 1, 1, 20, 1)
        if okPressed:
            self.g = GameWithText(count=i, par=self, items=['a', 'an', 'the'])
            self.g.show()
            self.hide()