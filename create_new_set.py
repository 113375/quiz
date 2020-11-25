import sqlite3
import sys
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QCheckBox, QHBoxLayout, QVBoxLayout, QDialog, QWidget
from PyQt5.QtWidgets import QButtonGroup, QMessageBox, QLabel, QInputDialog
from card import Card
from createNewSetUi import Ui_Dialog


class CreateNewSet(QDialog, Ui_Dialog):
    """Этот класс будет создавать новый сет из карточек с уникальным названием"""

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        """подключаем базу данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()
        self.setWindowTitle("Создание нового набора карточек")
        self.par = parent  # родитель

        self.rejected.connect(self.open_main)  # если он нажмет cancle
        self.accepted.connect(self.open_main)  # если он нажмет yes
        self.create_button.clicked.connect(self.create_set)
        self.make_list_of_cards()

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
            self.check_box_group = QButtonGroup()
            self.widget = QWidget()

            self.all_cards.setWidget(self.widget)
            self.layout_SArea = QHBoxLayout(self.widget)
            j = 0
            self.check_boxs = []
            for i in self.all_card:
                self.wid = QWidget()
                self.check = QCheckBox("Выбрать")
                self.check.setObjectName(f"checkbox{j}")
                self.check_boxs.append(self.check)

                """изменяем размер шрифта чекбокса"""
                f = self.check.font()
                f.setPointSize(25)
                self.check.setFont(f)

                self.check.setStyleSheet("""color: rgb(96, 47, 151)""")

                self.vboxlay = QVBoxLayout(self.wid)
                self.vboxlay.addWidget(i)
                self.vboxlay.addWidget(self.check)
                self.layout_SArea.addWidget(self.wid, stretch=1)
                self.vboxlay.addStretch(0)
            self.layout_SArea.addStretch(0)
        else:
            self.widget = QWidget()

            self.all_cards.setWidget(self.widget)
            self.layout_SArea = QHBoxLayout(self.widget)
            self.label = QLabel("Упс, тут пока что пусто \nНо вы можете это исправить")
            self.label.setStyleSheet("font: 18pt 'Helvetica';")
            self.layout_SArea.addWidget(self.label)

    def take_activated_checkbox(self):
        """Эта функция добывает классы тех карточек, которые были выбраны"""
        if self.all_card:
            self.active = []
            if self.open_choice():
                """Цикл по перебору значения в группе, и нахождения индексов выбранных"""
                for i in range(len(self.check_boxs)):
                    if self.check_boxs[i].isChecked():
                        self.active.append(i)
                if self.active:
                    self.active_cards = []  # в нем будут хранится экземпляры выбранных классов
                    for i in self.active:
                        self.active_cards.append(self.all_card[i])
                    """Тут будет функция создания, куда будут помещены нужные карточки из списка, искать их будем по id"""
                else:
                    self.open_empty_bar()


            else:
                self.hide()
                self.par.show()
        else:
            self.open_empty_bar()

    def not_unique(self):
        """Вызывает окошко, что имя сета не является уникальным и нужно придумать другое имя"""
        reply = QMessageBox.question(self, 'Ошибочка',
                                     f"Сет с таким именем уже имеется, придумайте другое", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.title_of_sets()

    def title_of_sets(self):
        """Запрашиваект название сета, и если оно уникальное, продолжает"""
        self.name, ok_pressed = QInputDialog.getText(self, "Новая карточка", "Введите название набора")
        if ok_pressed and self.name:
            names = self.cur.execute("""SELECT id FROM Sets WHERE login = ? AND title = ?""",
                                     (self.par.login, self.name)).fetchall()
            if names:
                self.not_unique()
        else:
            reply = QMessageBox.question(self, 'Муки выбора',
                                         "Вы не ввели название, хотите вернуться к выбору карточек?",
                                         QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                pass
            else:
                self.title_of_sets()

    def add_set_in_db(self):
        """Добавляем новый сет в БД и возвращаем его новый id"""
        self.cur.execute("""INSERT INTO Sets(title, login) VALUES (?, ?)""", (self.name, self.par.login))
        return self.cur.execute("""SELECT id FROM Sets WHERE login = ? and title = ?""",
                                (self.par.login, self.name)).fetchone()[0]

    def create_set(self):
        """Тут все сливается и содается новый сет"""
        self.take_activated_checkbox()

        if self.all_card and self.active:
            self.title_of_sets()
            self.id_of_set = self.add_set_in_db()

            """Добавляем каждому выбранному элементу принадлежность к этому сету"""
            for i in self.active_cards:
                id_of_card = i.id
                self.sets_of_card = \
                self.cur.execute("""SELECT sets FROM Card WHERE id = ?""", (id_of_card,)).fetchone()[0]
                self.sets_of_card += f"{self.id_of_set};"
                self.cur.execute("""UPDATE Card
                                            SET sets = ?
                                            WHERE id = ?""", (self.sets_of_card, id_of_card))

                self.con.commit()
            self.open_succes_bar()

    def open_empty_bar(self):
        reply = QMessageBox.question(self, 'Пусто',
                                     f"Упс, вы ничего не выбрали", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.show()

    def open_succes_bar(self):
        """При успешном создании нового сета"""
        reply = QMessageBox.question(self, 'Успех',
                                     f"Сет {self.name} успешно создан", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.par.fill_in()
            self.par.show()
            self.hide()

    def open_choice(self):
        """Тут будет выбор картчек"""
        return True
