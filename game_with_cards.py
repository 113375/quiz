import random as rd
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QButtonGroup, QWidget, QDialog
import sqlite3
from card import Card
from GameWithCardsUi import Ui_Dialog


class GameWithCards(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Заучивание набора карточек")
        """Подключение базы данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()

        """Остальное"""
        self.par = parent  # родитель этого класса
        self.rejected.connect(self.open_choice)  # если он нажмет cancle
        self.accepted.connect(self.open_choice)  # если он нажмет yes
        self.widget = QWidget()
        self.set_label.setText(f"Заучиваем набор: {self.par.set_name}")
        self.game = True
        self.not_right_style = "color: rgb(125, 0, 0);font: 15pt 'Helvetica';"
        self.right_style = "color: rgb(0, 125, 0);font: 15pt 'Helvetica';"

        self.right_cards = []

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.check_button)
        self.button_group.buttonClicked.connect(self.what_to_do)

        if self.game:
            self.start_game()

    def what_to_do(self, button):
        """Смотрит по названию кнопки, что она должна выполнить"""
        self.button_name = button.text()
        if self.button_name == "Проверить":
            self.check_button.setText('Продолжить')
            self.word.setDisabled(True)
            self.check_answer()
        elif self.button_name == "Продолжить":
            if not self.cards:
                self.end_of_game()
            else:

                self.check_button.setText('Проверить')
                self.next_card()

    def next_card(self):
        """Заменяет карточку на следующую"""
        self.right_or_not.setText(" ")
        self.num += 1
        self.word.setDisabled(False)
        try:
            self.hor.itemAt(0).widget().setParent(None)
            self.hor.addWidget(self.cards[self.num])
        except IndexError:
            self.num = 0
            rd.shuffle(self.cards)
            self.hor.addWidget(self.cards[self.num])

    def check_answer(self):
        """Проверяет правильность значения, меняет тескст в нижнем лэйбле"""
        self.right_answer = self.cards[self.num].mean
        copy_right = self.right_answer.lower()
        self.right_word = self.cards[self.num].word
        self.answer = self.word.text()
        copy_answer = self.answer.lower()
        self.answer = self.answer.strip()
        if copy_right == copy_answer:
            self.right_or_not.setText(f"Вы ответили верно, {self.right_word} - {self.right_answer}")
            self.right_or_not.setStyleSheet(self.right_style)
            self.cards.pop(self.num)
        else:
            self.right_or_not.setText(f"Вы ответили неверно, правильный ответ - {self.right_answer}")
            self.right_or_not.setStyleSheet(self.not_right_style)

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
        rd.shuffle(list_of_cards)
        return list_of_cards

    def start_game(self):
        """Тут начинается вся игра"""
        self.num = 0
        self.cards = self.get_all_cards()  # Создается массив
        self.lenght = len(self.cards)
        self.hor.addWidget(self.cards[self.num])
        self.before_the_game()

    def open_choice(self):
        """Если он захочет закончить игру"""
        """открывает выбор, хочет ли пользователь войти без регистрации"""
        reply = QMessageBox.question(self, 'Муки выбора',
                                     "Вы точно хотите прервать игру?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.hide()
            self.game = False
            self.par.show()
        else:
            self.show()

    def before_the_game(self):
        """До начала игры тут показываются правила"""
        reply = QMessageBox.question(self, 'Правила',
                                     f"Перед началом игры хотелось бы рассказать немного о том, что тут вообще "
                                     f"надо делать. Тут все сделано в игровой форме и не на время, так что можете не торопиться, "
                                     f"в специальном поле будет появляться карточка с текстом без перевода, его вам и надо "
                                     f"будет ввести в поле, далее нажимайте единственную кнопку, и все, приятной игры) ",
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            pass

    def end_of_game(self):
        """Когда ты выучил все слова"""
        reply = QMessageBox.question(self, 'Конец, вы молодец!',
                                     f"Вы уже заучили этот набор, вы выучили сейчас карточек: {self.lenght}",
                                     QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.par.show()
            self.hide()
