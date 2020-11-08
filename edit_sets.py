import sqlite3
import sys

from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5 import uic, QtCore, Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QCheckBox, QHBoxLayout, QVBoxLayout, QDialog, QWidget
from PyQt5.QtWidgets import QButtonGroup, QMessageBox, QLabel, QInputDialog, QPushButton
from edit_set import EditSet
from chooseSetUi import Ui_Dialog


class ChooseSet(QDialog, Ui_Dialog):
    """Этот класс дает список всех сетов, чтобы можно было выбрать"""

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        """подключаем базу данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()
        self.setWindowTitle("Выбор сета")
        self.par = parent  # родитель
        self.login = self.par.login

        self.rejected.connect(self.open_main)  # если он нажмет cancle
        self.accepted.connect(self.open_main)  # если он нажмет yes
        self.fill_in()  # заполняем лист виджет


    def choose_set(self, button):
        """Далее находим id этого сета"""

        self.name = button.text()
        self.id_of_set = self.cur.execute("""SELECT id FROM Sets WHERE title = ? and login = ?""", (button.text(), self.par.login)).fetchone()
        self.id_of_set = self.id_of_set[0] # id сета, который выбрал пользователь
        self.edit = EditSet(self)
        self.edit.show()
        self.hide()




    def return_all_sets(self):
        """Достает названия всех сетов пользователя"""
        all_sets = self.cur.execute("""SELECT title FROM Sets WHERE login = ? and title is 
                                    not 'Вcе карточки'""", (self.par.login,)).fetchall()
        all_sets2 = []
        for i in all_sets:
            i = i[0]
            if i != 'Все карточки':
                all_sets2.append(i)
        return all_sets2

    def fill_in(self):
        """заполняет ячейки listwidget"""
        self.button_group = QButtonGroup()  # группа кнопок, чтобы понять, какая активна
        self.button_group.setExclusive(True)
        self.all_sets = self.return_all_sets()

        self.button_group.buttonClicked.connect(self.choose_set)
        num = 1
        if self.all_sets:
            self.widget = QWidget()
            self.scrollArea.setWidget(self.widget)
            self.layout_SArea = QVBoxLayout(self.widget)
            # self.layout_SArea.setAlignment(Qt.AlignCenter)
            # self.layout_SArea.setAlignment()
            """Заполняем ScrollArea кнопками с топовым дизайном"""
            for i in self.all_sets:
                self.button = QPushButton(str(i))
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

    def open_main(self):
        self.hide()
        self.par.show()
        self.par.fill_in()
