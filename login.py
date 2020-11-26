import sqlite3
import sys
import random as rd

from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtCore, QtGui
from PyQt5.uic import pyuic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget, QDialog
import sqlite3
from new_user import CreateNewUser
from change_password import ChangePassword
from loginUi import Ui_Dialog


class Login(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Вход")
        """Подключение базы данных"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()

        """Остальное"""
        self.par = parent  # родитель этого класса
        self.new_password.clicked.connect(self.change_password) #подключает меню для смены пароля
        self.create_new_ak.clicked.connect(self.new_account) #подключает меню для создания нового аккаунта
        self.rejected.connect(self.open_choice)  # если он нажмет cancle
        self.accepted.connect(self.end_registration)  # если он нажмет yes

    def new_account(self):
        """Создает новый аккаунт"""
        self.new = CreateNewUser(parent=self)
        self.new.show()
        self.hide()


    def change_password(self):
        """Меняет пароль, если его забыли"""
        self.change_password = ChangePassword(parent=self)
        self.change_password.show()
        self.hide()

    def open_choice(self):
        """открывает выбор, хочет ли пользователь войти без регистрации"""
        reply = QMessageBox.question(self, '',
                                     "Вы точно хотите войти без регистрации?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.par.name = "Неизвестный"
            self.par.login = " "
            self.par.change_name()
            self.hide()
            self.par.show()
            self.par.fil_in_sets()
        else:
            self.show()

    def keyPressEvent(self, event):
        """Фиксирование нажатий клавиш"""
        if event.key() == Qt.Key_Enter:
            self.end_registration()
        elif event.key() == Qt.Key_Escape:
            self.open_choice()



    def verify_project(self):
        """Проверяет в базе данных, есть ли такой пользователь и т. д."""
        pas = self.cur.execute("""SELECT Password FROM User WHERE Login = ?""", (self.log, )).fetchone()
        if not pas:
            self.error_label.setText("Пользователь не найден")
            return False
        try:
            if self.pas != pas[0]:
                self.error_label.setText("Неверный пароль")
                return False
            self.name = self.cur.execute("""SELECT name FROM User WHERE Login = ?""", (self.log, )).fetchone()
            self.name = self.name[0] #Имя пользователя, чтобы потом оно отображалось
            return True
        except IndexError:
            self.error_label.setText("Вы что-то ввели не так, будьте аккуратнее")
            return False

    def end_registration(self):
        self.log = str(self.login.text()).strip()
        self.pas = str(self.password.text()).strip()
        if self.verify_project():
            self.hide()
            self.par.show()
            self.par.name = self.name
            self.par.login = self.log
            self.par.change_name()
            self.par.fil_in_sets()

        else:
            self.show()
