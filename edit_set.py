import sqlite3
import sys

from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5 import uic, QtCore, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QCheckBox, QHBoxLayout, QVBoxLayout, QDialog, QWidget
from PyQt5.QtWidgets import QButtonGroup, QMessageBox, QLabel, QInputDialog, QPushButton
from card import Card
from editSetUi import Ui_Dialog


class EditSet(QDialog, Ui_Dialog):
    """Этот класс изменяет сет"""

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        """подключаем базу данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()
        self.setWindowTitle("Редактирование сета")
        self.par = parent  # родитель
        self.head_label.setText(f"Редактирование сета: {self.par.name}")
        self.rejected.connect(self.open_parent)  # если он нажмет cancle
        self.accepted.connect(self.open_parent)  # если он нажмет yes
        self.make_list_of_cards()
        self.choose_all_button.clicked.connect(self.choose_all)  # подключаем кнопку выбора всех карточек
        self.delete_set_button.clicked.connect(self.before_the_deliion)  # подключаем кнопку удаления сета
        self.save_editions_button.clicked.connect(self.count)

    def count(self):
        """Считает количество активированных"""

        count = 0
        for i in self.check_boxs:
            if i.isChecked():
                count += 1
        if count > 0:
            self.change()
        elif count == 0:
            self.before_the_deliion()

    def choose_all(self):
        """Делает все чекбоксы нажатыми"""
        for i in self.check_boxs:
            i.setChecked(True)

    def delete_set(self):
        """Удаляет данный сет целиком"""
        self.cur.execute("""DELETE FROM Sets WHERE id = ?""", (self.par.id_of_set,))
        self.con.commit()
        self.par.fill_in()
        self.open_succes_bar()

    def change(self):
        """Эта функция уже меняет сам сет"""
        num = 0
        for i in self.check_boxs:
            id_of_card = self.all_card[num].id
            self.sets = self.cur.execute("""SELECT sets FROM Card WHERE id = ?""", (id_of_card,)).fetchone()[0]
            if i.isChecked():
                """Если чекбокс активен"""
                """Дальше есть два варианта, был ли он изначально там, либо нет"""
                if not f"{self.par.id_of_set};" in self.sets:
                    self.sets += f"{self.par.id_of_set};"

            else:
                """Если она не была выбрана"""
                if f"{self.par.id_of_set};" in self.sets:
                    self.sets = self.sets.split(";")
                    self.sets = [i for i in self.sets if i != str(self.par.id_of_set)]
                    self.sets = ";".join(self.sets)

            num += 1
            """Вносим изменения и созраняем их"""
            self.cur.execute("""UPDATE Card
                                               SET sets = ?
                                               WHERE id = ?""", (self.sets, id_of_card))

            self.con.commit()
        self.open_succes_bar_after_changing()

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
            j = 0
            self.check_boxs = []
            for i in self.all_card:
                self.wid = QWidget()
                self.check = QCheckBox("Выбрать")
                self.check.setObjectName(f"checkbox{j}")
                self.check.setStyleSheet("""color: rgb(96, 47, 151)""")
                self.check_boxs.append(self.check)
                self.sets_of_this_card = self.cur.execute("""SELECT sets FROM Card WHERE id = ?""", (i.id,)).fetchone()
                self.sets_of_this_card = self.sets_of_this_card[0]  # все сеты, к которым принадлежит карточкаданная
                if f"{self.par.id_of_set}" in self.sets_of_this_card:
                    """Если она изначально была в этом сете, то надо будет сделать чекбокс сразу активным"""
                    self.check.setChecked(True)

                """изменяем размер шрифта чекбокса"""
                f = self.check.font()
                f.setPointSize(25)
                self.check.setFont(f)

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
            self.layout_SArea.addWidget(QLabel("Упс, тут пока что пусто, но вы можете это исправить"))

    def before_the_deliion(self):
        reply = QMessageBox.question(self, 'Выбор',
                                     "Вы точно хотите удалить этот набор?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.delete_set()

    def open_succes_bar(self):
        """При успешномудалении сета"""
        reply = QMessageBox.question(self, 'Успех',
                                     f"Сет успешно удален", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.par.show()
            self.hide()

    def open_succes_bar_after_changing(self):
        """после успешного обновления сета"""
        reply = QMessageBox.question(self, 'Успех',
                                     f"Сет успешно обновлен", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            pass


    def open_parent(self):
        self.hide()
        self.par.show()
