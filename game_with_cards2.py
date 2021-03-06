import sys
import sqlite3
import random
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFileDialog, QButtonGroup
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QMessageBox, QGridLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from card import Card


class Picture(QWidget):
    def __init__(self, word, path, number, par):
        super(Picture, self).__init__()
        self.right = False
        self.green = False
        self.count_trying = 0
        self.word = word
        self.path = path
        self.number = number
        row, coll = (number) // 2, number % 2
        self.setWindowTitle("Игра2")

        self.button = QPushButton()
        self.button.setStyleSheet("background: transparent;")
        self.button.setIcon(QIcon(f"images/{path}"))
        self.button.setIconSize(QSize(270, 270))
        self.button.setObjectName(str(number))

        par.pic_button_group.addButton(self.button)

        par.grid.addWidget(self.button, row, coll)

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
        '''Показывает все картинки в layout'''
        for i in range(len(self.pictures)):
            try:
                pic = self.pictures[i]
                word = self.dict[pic]
                self.list_img.append(Picture(word, pic, i, par=self))
            except IndexError:
                pass

    def choose_word(self, button):
        """Смотрит, какое слово выбрал пользователь"""
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
        """Заполняет словами"""
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
        """Проверяет, привильно ли ответил пользователь"""
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
        """Если верно сопоставил, то становится зеленым"""
        self.pic.button.setStyleSheet("")
        self.pic.button.setStyleSheet("background-color: rgb(0, 255, 0);")

    def return_ind(self):
        """Возвращает индекс элемента по значению"""
        for i in range(len(self.all_words)):
            if self.all_words[i] == self.word:
                return i
        return -1

    def del_word_from_list(self):
        """Удаляет слова из списка"""
        if self.return_ind() != -1:
            self.all_words.pop(self.return_ind())
            self.fill_in_words()

    def to_red(self):
        """Закрашивает выбранное слово в красный"""
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
        for i in range(len(self.pictures)):
            try:
                dict[self.pictures[i]] = self.words[i]
            except IndexError:
                pass
        return dict

    def check(self, button):
        """Функция для проверки"""
        self.number_pic = int(button.objectName())  # номер объекта, к которому принадлежит картинка
        print(self.list_img)
        self.pic = self.list_img[self.number_pic]
        if self.pic.check(self.word):
            if self.pic.count_trying == 0:
                self.list_first.append(self.pic.path)
            self.del_word_from_list()
            self.to_green()

        else:
            self.to_red()
            self.pic.count_trying += 1
        if not self.words:
            self.delete_from_grid()
            self.delete_cards()

    def find_ind(self, path):
        for i in range(len(self.pictures)):
            if self.pictures[i] == path:
                return i
        return -1

    def delete_from_grid(self):
        """Удаляет все из grid"""
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

    def end_of_game(self):
        """Когда ты выучил все слова"""
        reply = QMessageBox.question(self, 'Конец, вы молодец!',
                                     f"Вы уже заучили этот сет, вы выучили сейчас карточек:",
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.par.show()
            self.hide()

    def make_new_words(self):
        for i in self.list_img:
            self.all_words.append(i.word)

    def find_ind_2(self, path):
        for i in range(len(self.list_img)):
            if self.list_img[i].path == path:
                return i
        return -1

    def delete_cards(self):
        """Удаляет карточки те, на которые он отвелтил с первого раза"""
        for i in self.list_first:
            ind = self.find_ind(i)
            if ind != -1:
                path = self.pictures[ind]
                ind2 = self.find_ind_2(path)
                self.pictures.pop(ind)
                self.list_img.pop(ind2)


        self.list_first = []
        if self.pictures:
            #self.words = [i.word for i in self.all_cards]
            #self.pictures = [i.path_to_img for i in self.all_cards]  # список всех путей к картинкам
            print(self.pictures)
            print(self.words)
            self.list_img = []
            self.fill_in_pic()
            self.make_new_words()
            self.fill_in_words()

        else:
            self.end_of_game()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Game()
    form.show()
    sys.exit(app.exec())
