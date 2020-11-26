import sys
import sqlite3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox, QButtonGroup
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from login import Login
from create_new_card import CreateNewCard
from show_all_cards import ShowAllCards
from delete_cards import DeleteCards
from create_new_set import CreateNewSet
from edit_sets import ChooseSet
from mainUi import Ui_MainWindow
from choose_game import ChooseGame
from choice_ex import ChoiceEx


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.all_sets = {}  # Словарь с сетами, где ключ - его название, а в нем находится спиок классов карточек
        self.setupUi(self)
        self.setWindowTitle("Главная")
        self.login = " "
        self.fil_in_sets()  # функция заполнения ListView
        self.login_button.clicked.connect(self.open_login)  # подключаем кнопку входа
        self.quet.clicked.connect(self.quete)  # подключаем кнопку выхода
        self.name = "Неизвестный"  # первоначальное имя, если войти без регистрации

        self.new_card.clicked.connect(self.add_new_card)  # подключает функцию добавления новой карточки
        self.show_all.clicked.connect(self.show_all_cards)  # Подключает кнопку показа вообще всех карточек у юзера
        self.delete_cards.clicked.connect(self.delete_card)  # подключает функцию удаления карточек
        self.create_new_set.clicked.connect(self.new_set)  # подключает функцию создания нового сета
        self.edit_set.clicked.connect(self.edit_sets)  # подключает редактирование сетов
        self.game_with_words.clicked.connect(self.exercises)

    def exercises(self):
        self.x = ChoiceEx(self)
        self.x.show()



    def delete_card(self):
        self.delete = DeleteCards(self)
        self.delete.show()
        self.hide()

    def open_login(self):
        """Вход"""
        self.log = Login(parent=self)
        self.hide()
        self.log.show()

    def change_name(self):
        self.name_label.setText(self.name)
        self.fill_in()

    def quete(self):
        """Выход из аккаунта"""
        reply = QMessageBox.question(self, 'Точно?',
                                     "Вы точно хотите выйти из аккаунта?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.name = "неизвестный"
            self.hide()
            self.open_login()

    def show_main(self):
        self.show()

    def new_set(self):
        """Создает новый сет в настройках из имеющихся"""
        self.sets = CreateNewSet(parent=self)
        self.sets.show()
        self.hide()

    def edit_sets(self):
        """Эта функция будет изменять сет, можно выбрать, что в нем оставить или что в нем удалить"""
        self.edit = ChooseSet(self)
        self.edit.show()
        self.hide()

    def show_all_cards(self):
        """Показать вообще все имеющиеся карточки"""
        self.hide()
        self.show_cards = ShowAllCards(self)
        self.show_cards.show()

    def add_new_card(self):
        CreateNewCard(self)
        """Создает новую карточку с словом"""

    def fil_in_sets(self):
        """Заполняем список сетов в виде кнопок, """
        self.button_group = QButtonGroup()
        self.button_group.buttonClicked.connect(self.are_you_sure)  # подключает игру с сетом
        self.fill_in()

    """Эти кнопки для того, чтобы начать игру, при нажатии она начинается с выбранным сетом"""

    def are_you_sure(self, button):
        self.set_name = button.text()
        """Показывает окно, точно ли они хотят играть именно с этим сетом"""
        reply = QMessageBox.question(self, '?',
                                     f"Хотите заучить сет: {self.set_name}", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.open_choice()
        else:
            pass

    def open_choice(self):
        self.game = ChooseGame(par=self)
        self.game.show()

    def return_all_sets(self):
        """Достает названия всех сетов пользователя"""

        """подключаем базу данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()

        all_sets = self.cur.execute("""SELECT title FROM Sets WHERE login = ?""", (str(self.login),)).fetchall()
        all_sets2 = []
        for i in all_sets:
            i = i[0]
            if i != 'Все карточки':
                all_sets2.append(i)
        return all_sets2

    def fill_in(self):
        """заполняет ячейки listwidget"""
        self.all_sets = self.return_all_sets()
        num = 1
        if self.all_sets:
            self.widget = QWidget()
            self.scrollArea.setWidget(self.widget)
            self.layout_SArea = QVBoxLayout(self.widget)
            """Заполняем ScrollArea кнопками с топовым дизайном"""
            for i in self.all_sets:
                self.button = QPushButton(str(i))
                self.button.setDisabled(False)
                self.button.setObjectName(f"button{num}")
                num += 1
                self.button.setStyleSheet("""background-color: rgb(0, 0, 0);\ncolor: rgb(255, 250, 255);
                                            \nborder-radius: 20px;\nheight: 40px;\n""")
                f = self.button.font()
                f.setPointSize(20)
                self.button.setFont(f)
                self.button_group.addButton(self.button)
                self.layout_SArea.addWidget(self.button)

            self.layout_SArea.addStretch(1)
        else:
            self.widget = QWidget()

            self.scrollArea.setWidget(self.widget)
            self.layout_SArea = QHBoxLayout(self.widget)
            self.label = QLabel("Упс, тут пока что пусто \nНо вы можете это исправить")
            self.label.setStyleSheet("font: 18pt 'Helvetica';")
            self.layout_SArea.addWidget(self.label)


app = QApplication(sys.argv)
ex = Main()
ex.show()
sys.exit(app.exec())
