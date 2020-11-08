import sqlite3
import sys
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QLabel, QDialog, QWidget
from card import Card
from showAllCardsUi import Ui_Dialog


class ShowAllCards(QDialog, Ui_Dialog):
    """Этот класс будет собирать данные для карточки, которые будут записывать в базу данных"""

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        """подключаем базу данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()
        self.setWindowTitle("Все ваши карточки")
        self.par = parent  # родитель
        self.make_list_of_cards()

        self.rejected.connect(self.open_main)  # если он нажмет cancle
        self.accepted.connect(self.open_main)  # если он нажмет yes

    def open_main(self):
        self.hide()
        self.par.show()

    def make_list_of_cards(self):
        """сначала достаем список с характеристиками, и из них создаем класс с карточкой"""
        self.login = self.par.login
        """вытаскиваем id главного сета"""
        self.id = self.cur.execute("""SELECT main_set FROM User WHERE login = ? """, (self.login,)).fetchone()

        """Достаем все карточки, принадлежащие этому логину"""
        self.card = self.cur.execute("""SELECT * FROM Card WHERE sets LIKE ?""", (f'{self.id[0]};%',)).fetchall()
        self.all_card = []
        for i in self.card:
            id = i[0]
            image = i[1]
            trans = i[2]
            word = i[3]
            self.all_card.append(Card(word, trans, image, id, True))
        self.fill_in_scroll()

    def fill_in_scroll(self):
        """Эта функция заполняет scrollarea значениями"""
        if self.all_card:
            self.widget = QWidget()

            self.all_cards.setWidget(self.widget)
            self.layout_SArea = QHBoxLayout(self.widget)

            for i in self.all_card:
                self.layout_SArea.addWidget(i)
            self.layout_SArea.addStretch(0)
        else:
            self.widget = QWidget()

            self.all_cards.setWidget(self.widget)
            self.layout_SArea = QHBoxLayout(self.widget)
            self.label = QLabel("Упс, тут пока что пусто \nНо вы можете это исправить")
            self.label.setStyleSheet("font: 18pt 'Helvetica';")
            self.layout_SArea.addWidget(self.label)
