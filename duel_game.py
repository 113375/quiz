import random as rd
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QLineEdit, QMainWindow
from PyQt5.QtWidgets import QMainWindow, QButtonGroup, QWidget, QDialog
import sqlite3
import sys
from card import Card


class DuelWithCards(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('duelWindow.ui', self)
        self.setWindowTitle("Заучивание набора карточек")
        """Подключение базы данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()

        self.all_cards = {}


app = QApplication(sys.argv)
ex = DuelWithCards()
ex.show()
sys.exit(app.exec())
