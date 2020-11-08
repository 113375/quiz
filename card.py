import sqlite3
import sys
import random as rd
from PyQt5.QtGui import QPainter, QColor, QPixmap
import PIL as pl
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget
from cardUi import Ui_Form


class Card(QWidget, Ui_Form):
    """Это класс карточки, в которой будет картинка и слово, при нажатии на кнопку будет перевод показываться"""

    def __init__(self, word, translate, image, id, flag):
        super().__init__()
        self.id = id
        self.flag = flag
        self.word = str(word).title() # слово на другом языке, которое будет изображено на карточке
        self.mean = str(translate).title() # Его перевод на русский язык
        self.path_to_img = image  # картинка, привязанная к карточке
        self.setupUi(self)
        self.create_card()




    def create_card(self):
        """Создает уже карточку окончательно"""
        self.image.setPixmap(QPixmap(f"images/{self.path_to_img}").scaled(230, 230, QtCore.Qt.KeepAspectRatio))
        self.word_label.setText(str(self.word))
        if self.flag:
            self.trans.setText(str(self.mean))

