import sqlite3
import sys
import random as rd
from PyQt5.QtGui import QPainter, QColor, QPixmap
import PIL as pl
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget, QDialog
import sqlite3
from func import isalphadidgit, check_letter, empty_or_not, verify_password
from newUserUi import Ui_Dialog


class CreateNewUser(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.par = parent  # родительское окно регистрацииф
        self.setWindowTitle("Создание нового пользователя")
        self.rejected.connect(self.open_choice)  # если он нажмет cancle
        self.accepted.connect(self.end_creating)  # если он нажмет yes
        """Подключаем базу данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()

    def open_choice(self):
        """открывается, если пользователь захочет выйти из регистрации"""
        reply = QMessageBox.question(self, 'Выбор...',
                                     "Вы точно хотите вернуться ко входу?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.hide()
            self.par.show()
        else:
            self.show()

    def checks(self):
        """Проверки того, что все введено корректно"""
        self.password = str(self.password_edit.text()).strip()  # Вытаскиваем пароль
        self.repeat_password = str(self.password_repeat.text()).strip()  # вытаскиваем повторенный пороль
        self.login = str(self.login_edit.text()).strip()  # Вытаскиваем имя
        self.name = str(self.name_label.text()).strip()  # Вытаскиваем логин
        """Проверка, не являются ли стоки пустыми"""
        res = empty_or_not(self.login, self.password, self.name)
        if res != '1':
            self.error_label.setText(f"Пустое значение: {res}")
            return False
        """Состоит ли логин только из букв латинского алфавита итд"""
        if not check_letter(self.login):
            self.error_label.setText("Логин должен включать только буквы латинского алфавита и '-")
            return False

        """Проверка на то, нет ли такого логина в базе данных(они все должны быть уникальными)"""
        logins = self.cur.execute("SELECT Name FROM User WHERE Login = ?", (self.login,)).fetchall()
        if logins:
            self.error_label.setText("Такой логин уже имеется, введите другой")
            return False

        """Проверки пароля, более 8-ми символов и состоящая из букв и цифр, и только из латиницы"""
        res = verify_password(self.password)
        if res != "1":
            self.error_label.setText(res)
            return False
        if self.password != self.repeat_password:
            self.error_label.setText("Пароли не совпадают, проверьте пожалуйста")
            return False

        return True

    def create_user(self):
        """При создании сразу создается общий альбом, запоминаем его id в User"""
        self.cur.execute("""INSERT INTO Sets(title, login) VALUES('Все карточки', ?)""", (self.login,))
        idk = self.cur.execute("""SELECT id FROM SETS WHERE login = ? and title = 'Все карточки'""", (self.login, )).fetchone()
        self.cur.execute("""INSERT INTO User(Name, Login, Password, main_set) VALUES (?, ?, ?, ?)""",
                         (self.name, self.login, self.password, idk[0]))
        self.con.commit()



    def open_succes_bar(self):
        """При успешном создании пользователя"""
        reply = QMessageBox.question(self, 'Успех!',
                                     f"Пользователь {self.name} успешно создан!", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.hide()

    def end_creating(self):
        if self.checks():
            self.create_user()
            self.open_succes_bar()
            self.hide()
            self.par.show()
        else:
            self.show()
