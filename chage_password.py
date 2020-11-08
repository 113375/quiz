import sqlite3
import sys
from PyQt5.QtGui import QPainter, QColor, QPixmap
import PIL as pl
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget, QDialog
from func import isempty, verify_password
import sqlite3

class ChangePassword(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi("changePassword.ui", self)
        self.setWindowTitle("Смена пароля")
        self.par = parent
        """Подключаем БД"""

        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()

        self.rejected.connect(self.open_choice)  # если он нажмет cancle
        self.accepted.connect(self.end_changing_password)  # если он нажмет yes

    def open_choice(self):
        """открывает выбор, хочет ли пользователь вернуться к регистрации"""
        reply = QMessageBox.question(self, 'Message',
                                     "Вы точно хотите вернуться к регистрации?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.hide()
            self.par.show()
        else:
            self.show()

    def check(self):
        """Проверка на корректность введенных данных"""
        self.password = str(self.new_password_edit.text()).strip()
        self.login = str(self.login_edit.text()).strip()

        """Проверка на то, нет ли пустых строк"""
        self.emp = isempty(self.password, self.login)
        if self.emp != "1":
            self.error_label.setText(f"Пустое значение: {self.emp}")
            return False

        """Проверка на то, есть ли такой юзер"""

        pas = self.cur.execute("""SELECT Password FROM User WHERE Login = ?""", (self.login,)).fetchone()
        if not pas:
            self.error_label.setText("Пользователь не найден")
            return False

        """Проверка на то, правильный ли пароль"""
        res = verify_password(self.password)
        if res != "1":
            self.error_label.setText(res)
            return False

        return True


    def change_password(self):
        self.cur.execute("""UPDATE User 
                            SET Password = ?
                            WHERE Login = ?""", (self.password, self.login))
        self.con.commit()

    def open_succes_bar(self):
        """При успешном создании пользователя"""
        reply = QMessageBox.question(self, 'Message',
                                     f"Пароль успешно обновлен", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.hide()



    def end_changing_password(self):
        if self.check():
            self.change_password()
            self.open_succes_bar()
            self.hide()
            self.par.show()
        else:
            self.show()


