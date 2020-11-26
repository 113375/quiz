import sys
import sqlite3
import os
import random
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog
from func_for_texts import read_and_del_articles
from game_with_text import GameWithText


class ChoiceEx(QDialog):
    def __init__(self, par=None):
        super(ChoiceEx, self).__init__()

        uic.loadUi("choose_ex.ui", self)
        self.prepositions.clicked.connect(self.start_prep)
        self.articles.clicked.connect(self.start_art)

        self.setWindowTitle("Темы для заданий")
        self.topic = ""



    def start_prep(self):
        if self.thema():
            i, okPressed = QInputDialog.getInt(self, "Введите количество абзацев", "", 1, 1, 6, 1)
            if okPressed:
                self.g = GameWithText(count=i, par=self, items=['on', 'at', 'on', "in", "by", "for"], topic=self.topic)
                self.g.show()
                self.hide()

    def thema(self):
        topic, okPressed = QInputDialog.getItem(self, "Выберете тему для текста", "Укажите тему",
                                                ("Еда", "Наука", "Путешествия"), 1, False)
        if okPressed:
            if topic == "Еда":
                self.topic = "food"
                return True
            elif topic == "Путешествия":
                self.topic = "trav"
                return True
            else:
                self.topic = "science"
                return True
        else:
            return False


    def start_art(self):
        if self.thema():
            i, okPressed = QInputDialog.getInt(self, "Введите количество абзацев", "", 1, 1, 6, 1)
            if okPressed:
                self.g = GameWithText(count=i, par=self, items=['a', 'an', 'the'], topic=self.topic)
                self.g.show()
                self.hide()
