import sqlite3
import sys
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QCheckBox, QHBoxLayout, QVBoxLayout, QDialog, QWidget
from PyQt5.QtWidgets import QButtonGroup, QMessageBox, QLabel
from card import Card
from deletecardsUi import Ui_Dialog


class DeleteCards(QDialog, Ui_Dialog):
    """Этот класс будет удалять карточки из базы данных"""

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        """подключаем базу данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()
        self.setWindowTitle("Удаление карточек")
        self.par = parent  # родитель
        self.make_list_of_cards()

        self.rejected.connect(self.open_main)  # если он нажмет cancle
        self.accepted.connect(self.open_delete)  # если он нажмет yes
        self.delete_button.clicked.connect(self.delete_checked)

    def open_main(self):
        self.hide()
        self.par.show()

    def open_delete(self):
        self.delete_checked()

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
                self.check = QCheckBox("Удалить")
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

    def delete_checked(self):
        """Эта функция удаляет выбранные карточки вообще """
        if self.all_card:
            self.active = []
            if self.open_choice():
                """Цикл по перебору значения в группе, и нахождения индексов выбранных"""
                for i in range(len(self.check_boxs)):
                    if self.check_boxs[i].isChecked():
                        self.active.append(i)
                if self.active:
                    for index in self.active:
                        checkbox = self.all_card[index]
                        id_of_check = checkbox.id
                        self.cur.execute("""DELETE FROM Card WHERE id = ?""", (id_of_check,))

                    self.con.commit()

                    self.open_succes_bar()
                else:
                    self.open_empty_bar()


            else:
                self.hide()
                self.par.show()
        else:
            self.open_empty_bar()

    def open_empty_bar(self):
        reply = QMessageBox.question(self, 'Пусто',
                                     f"Упс, вы ничего не выбрали", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.show()

    def open_succes_bar(self):
        """При успешном создании пользователя"""
        reply = QMessageBox.question(self, '',
                                     f"Выбранные карточки успешно удалены", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.par.show()
            self.hide()

    def open_choice(self):
        reply = QMessageBox.question(self, '',
                                     "Вы точно хотите удалить эти карточки?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            return True
        else:
            return False
