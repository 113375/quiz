import sqlite3
import sys
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget
from PyQt5.QtGui import QPainter, QColor, QPixmap
import shutil
import webbrowser



class CreateNewCard(QWidget):
    """Этот класс будет собирать данные для карточки, которые будут записывать в базу данных"""

    def __init__(self, parent=None):
        super().__init__()
        self.hide()
        """Подключение БД"""
        self.con = sqlite3.connect("quiz.db")
        self.cur = self.con.cursor()
        self.par = parent
        self.ask_word()

    def load_image(self):
        """Загрузка изображения для карточки"""
        #TODO: Сделать запрос в яндексе по названию этой картинки с предложением его сказать и уже дальше выбрать
        self.path_to_img, ok = QFileDialog.getOpenFileName(self, 'Выбрать картинку для карточки',
                                                           '')
        if ok:
            self.load_in_db()
        else:
            self.ask_translate()

    def load_in_db(self):
        """Добавляем карточку в общий альбом"""
        """Достаем id главного сета, основного"""
        id_of_main_set = self.cur.execute("""SELECT main_set FROM User WHERE Login = ?""", (self.par.login,)).fetchone()
        """Запихиваем картинку в папку с картинками"""
        self.lenght = len(self.cur.execute("""SELECT id FROM Card""").fetchall()) #Чтобы знать, какой номер дать карточке

        self.image_name = self.path_to_img.split('/')[-1]
        self.file = open(f"images/image{self.lenght}", mode="wb")
        shutil.copyfile(self.path_to_img, f'images/image{self.lenght}')
        self.file.close()

        """Создаем новую карточку"""

        self.cur.execute("""INSERT INTO Card(image, translate, word, sets) VALUES (?, ?, ?, ?)""",
                         (f'image{self.lenght}', self.translate, self.word, f"{id_of_main_set[0]};"))

        self.con.commit()

        self.open_succes_bar()

    def open_succes_bar(self):
        """При успешном создании карточки"""
        reply = QMessageBox.question(self, 'Успех',
                                     f"Карточка {self.word} - {self.translate} созданна успешно", QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.hide()

    def ask_word(self):
        """запрашиваем слово на иностранном языке"""
        self.word, ok_pressed = QInputDialog.getText(self, "Новая карточка", "Введите слово(на иностранном языке)")
        if ok_pressed and self.word:
            self.word = self.word.strip()
            self.ask_translate()
        else:
            reply = QMessageBox.question(self, 'муки выбора',
                                         "Вы точно хотите вернуться на главную?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.hide()
            else:
                self.ask_word()

    def ask_translate(self):
        """Запрашиваем перевод этого слова"""

        #TODO сделать авто перевод текста с помощью API яндекса
        self.translate, ok_pressed = QInputDialog.getText(self, "Новая карточка", "Введите его перевод")
        if ok_pressed and self.translate:
            webbrowser.register('Safari', None, webbrowser.BackgroundBrowser(
                '/User/Desctop/Safari'))
            webbrowser.open_new_tab(
                f'https://www.google.com/search?q={self.word}&newwindow=1&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjp8sza_5jtAhXjwosKHbZ8BYQQ_AUoAnoECB4QBA&cshid=1606145893253510&biw=1280&bih=881')
            self.load_image()
            self.translate = self.translate.strip()
        else:
            reply = QMessageBox.question(self, 'Снова выбор',
                                         "Вы точно хотите вернуться шаг назад?", QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.ask_word()
            else:
                self.ask_translate()

