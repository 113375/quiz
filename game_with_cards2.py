import sys
import sqlite3
import random
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFileDialog, QButtonGroup
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from card import Card


class Picrure:
    def __init__(self, word, path, number, par):
        self.right = False
        self.green = False
        self.count_trying = 0
        self.word = word
        self.path = path
        self.number = number
        roll, coll = (number) // 2, number % 2

        self.button = QPushButton()
        self.button.setStyleSheet("background: transparent;")
        self.button.setIcon(QIcon(f"images/{path}"))
        self.button.setIconSize(QSize(270, 270))
        self.button.setObjectName(str(number))

        par.pic_button_group.addButton(self.button)

        par.grid.addWidget(self.button, roll, coll)

    def check(self, word):
        return word == self.word


class Game(QWidget):
    def __init__(self, parant):
        self.par = parant
        self.list_img = []
        super(Game, self).__init__()
        uic.loadUi('game_with_cards2.ui', self)
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()

        self.all_cards = self.get_all_cards()
        self.words = [i.word for i in self.all_cards]
        self.pictures = [i.path_to_img for i in self.all_cards]  # список всех путей к картинкам
        self.dict = self.make_dict_for_game()

        self.list_first = []

        self.all_words = self.words

        self.word = ''

        self.pic_button_group = QButtonGroup()

        self.coords = QLabel(self)

        self.button_g = QButtonGroup()
        self.button_g.buttonClicked.connect(self.choose_word)
        self.fill_in_pic()
        self.pic_button_group.buttonClicked.connect(self.check)
        random.shuffle(self.all_words)
        self.lenght = len(self.all_words)
        self.fill_in_words()

    def fill_in_pic(self):
        for i in range(6):
            try:
                pic = self.pictures[i]
                word = self.dict[pic]
                self.list_img.append(Picrure(word, pic, i, par=self))
            except IndexError:
                pass

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
        try:
            for i in range(3):
                pic = self.list_img[i]
                if pic.right == False:
                    return True
            return False
        except IndexError:
            return False

    def to_green(self):
        self.pic.button.setStyleSheet("")
        self.pic.button.setStyleSheet("background-color: rgb(0, 255, 0);")

    def return_ind(self):
        for i in range(len(self.all_words)):
            if self.all_words[i] == self.word:
                return i
        return -1

    def del_word_from_list(self):
        if self.return_ind() != -1:
            self.all_words.pop(self.return_ind())
            self.fill_in_words()

    def to_red(self):
        self.pic.button.setStyleSheet("")
        self.pic.button.setStyleSheet("background-color: rgb(255, 0, 0);")

    def get_all_cards(self):
        """Возвращает массив, заполненный полность карточками из выбранного сета"""
        id_of_set = self.cur.execute("""SELECT id FROM Sets WHERE login = ? and title = ?""",
                                     (self.par.login, self.par.set_name)).fetchone()[0]
        cards = self.cur.execute("""SELECT * FROM Card WHERE sets LIKE ?""", (f'%{id_of_set};%',)).fetchall()
        if not cards:
            return "-1"
        list_of_cards = []
        for card in cards:
            id = card[0]
            image = card[1]
            trans = card[2]
            word = card[3]
            list_of_cards.append(Card(word, trans, image, id, False))
        random.shuffle(list_of_cards)
        return list_of_cards

    def make_dict_for_game(self):
        dict = {}
        for i in range(6):
            try:
                dict[self.pictures[i]] = self.words[i]
            except IndexError:
                pass
        return dict

    def check(self, button):
        """Функция для проверки"""
        self.number_pic = int(button.objectName())  # номер объекта, к которому принадлежит картинка
        self.pic = self.list_img[self.number_pic]
        if self.pic.check(self.word):
            self.pic.right = True
            self.del_word_from_list()
            self.to_green()

        else:
            self.to_red()
            self.pic.count_trying += 1
        if not self.words:
            self.delete_cards()

    def find_ind(self, pic):
        word = pic.word
        for i in range(len(self.list_img)):
            if self.list_img[i].word == word:
                return i
        return -1


    def delete_cards(self):
        for i in self.list_img:
            ind = self.find_ind(i)
            if ind != -1:
                self.list_img.pop(self.find_ind(i))

        self.list_first = []
        self.fill_in_pic()
        self.fill_in_words()
        for i in self.list_img:
            i.count_trying = 0
    def end_of_game(self):
        """Когда ты выучил все слова"""
        reply = QMessageBox.question(self, 'Конец, вы молодец!',
                                     f"Вы уже заучили этот сет, вы выучили сейчас карточек:",
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.par.show()
            self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Game()
    form.show()
    sys.exit(app.exec())
