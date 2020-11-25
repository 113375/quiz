import sys
import sqlite3
import random
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFileDialog, QButtonGroup
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets


class Picrure:
    def __init__(self, word, path, number, par):
        self.right = False
        self.word = word
        self.path = path
        self.number = number
        roll, coll = (number) // 2, number % 2

        self.button = QPushButton()
        self.button.setStyleSheet("background: transparent;")
        self.button.setIcon(QIcon(path))
        self.button.setIconSize(QSize(270, 270))
        self.button.setObjectName(str(number))

        par.pic_button_group.addButton(self.button)

        par.grid.addWidget(self.button, roll, coll)

    def check(self, word):
        return word == self.word


list_img = []

pictures = ['im.png', 'im2.jpeg', 'im3.jpeg', 'im4.jpeg', 'im5.jpeg', 'im6.jpeg']

dict = {}
words = ["Слово1", "Слово2", "Слово3", "Слово4", "Слово5", "Слово6"]
for i in range(6):
    dict[pictures[i]] = words[i]


class Game(QWidget):
    def __init__(self):
        super(Game, self).__init__()
        uic.loadUi('game_with_cards2.ui', self)
        self.all_words = words

        self.word = ''


        self.pic_button_group = QButtonGroup()

        self.coords = QLabel(self)

        self.button_g = QButtonGroup()
        self.button_g.buttonClicked.connect(self.choose_word)
        self.fill_in_pic()
        self.pic_button_group.buttonClicked.connect(self.check)
        random.shuffle(self.all_words)
        self.fill_in_words()

    def fill_in_pic(self):
        for i in range(6):
            pic = pictures[i]
            word = dict[pic]
            list_img.append(Picrure(word, pic, i, par=self))

    def choose_word(self, button):
        print(button.text())
        if len(self.all_words) > 1:
            self.word = button.text()
            self.now_button, self.last_button = button, self.now_button
            self.now_button.setStyleSheet("font: 18pt 'Helvetica'; background: transparent; color: rgb(255, 0, 0);")
            self.last_button.setStyleSheet("font: 18pt 'Helvetica'; background: transparent; color: rgb(0, 0, 0);")
        else:
            self.now_button = button
            self.now_button.setStyleSheet("font: 18pt 'Helvetica'; background: transparent; color: rgb(255, 0, 0);")
            self.word = button.text()

    def fill_in_words(self):

        self.widget = QWidget()
        self.scrollArea.setWidget(self.widget)
        self.hor_lay = QHBoxLayout(self.widget)
        for i in self.all_words:
            self.but = QPushButton(i)
            self.but.setStyleSheet("font: 18pt 'Helvetica'; background: transparent;")
            self.but.setMinimumSize(100, 20)
            self.now_button = self.but
            self.button_g.addButton(self.but)
            self.hor_lay.addWidget(self.but)

        self.hor_lay.addStretch(0)

    def check_all_right(self):
        self.flag = True
        for i in range(6):
            pic = list_img[i]
            if pic.right == False:
                return True
        return False



    def check(self, button):
        """Функция для проверки того, """
        self.number_pic = int(button.objectName()) # номер объекта, к которому принадлежит картинка
        self.pic = list_img[self.number_pic]
        if self.pic.check(self.word):
            self.pic.right = True
            self.del_word_from_list()
            self.to_green()
        else:
            self.to_red()

        if self.check_all_right:
            pass

    def to_green(self):
        self.pic.button.setStyleSheet("")
        self.pic.button.setStyleSheet("background-color: rgb(0, 255, 0);")

    def return_ind(self):
        for i in range(len(self.all_words)):
            if self.all_words[i] == self.word:
                return i

    def del_word_from_list(self):
        self.all_words.pop(self.return_ind())
        self.fill_in_words()


    def to_red(self):
        self.pic.button.setStyleSheet("")
        self.pic.button.setStyleSheet("background-color: rgb(255, 0, 0);")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Game()
    form.show()
    sys.exit(app.exec())
