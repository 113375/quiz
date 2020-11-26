import sys
import sqlite3
import os
import random
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QInputDialog, QTableWidgetItem
from PyQt5.QtWidgets import QWidget, QTextBrowser, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QMessageBox, QGridLayout, QMainWindow
from func_for_texts import read_and_del_articles


class GameWithText(QMainWindow):
    def __init__(self, par=None, count=1):
        super(GameWithText, self).__init__()
        list_of_files = os.listdir("texts")
        file = random.choice(list_of_files)
        self.text = read_and_del_articles(f"texts/{file}", count)
        self.dict = self.text[1]
        self.all_labels = []
        uic.loadUi("game3.ui", self)
        print(self.text)
        self.text_b.setText(self.text[0])
        self.all_lines = []
        self.fill_in_words()
        self.checkButton.clicked.connect(self.counting_gaps)

        self.GREEN = "rgb(0, 200, 0)"
        self.RED = "rgb(200, 0, 0)"

    def counting_gaps(self):
        count = 0
        for line in self.all_lines:
            line = line
            text = line.text()
            if "" == text:
                count += 1
        if not count:
            self.check_all()
        else:
            self.warning(count)

    def warning(self, gaps):
        reply = QMessageBox.question(self, '',
                                     f"Вы точно хотите проверить результат? У вас имеются пропуски ({gaps})",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.check_all()

    def check_all(self):
        self.count = 0
        for i in range(len(self.all_lines)):
            text = self.all_lines[i].text()
            line = self.all_lines[i]
            label = self.all_labels[i]
            if self.dict[int(line.objectName())] == text.lower().strip():
                color = self.GREEN
                self.count += 1
            else:
                color = self.RED
            line.setStyleSheet(f"color: {color}; font-size: 20px;")
            line.setDisabled(True)
            label.setStyleSheet(f"color: {color}; font-size: 20px;")

        QMessageBox.question(self, '',
                             f"Всего правильных ответов: {self.count}/ {len(self.dict)}",
                             QMessageBox.Yes)

    def fill_in_words(self):
        """Заполняет словами"""
        self.widget = QWidget()
        self.scrollArea.setWidget(self.widget)
        self.hor_lay = QHBoxLayout(self.widget)
        for i in self.text[1]:
            self.label = QLabel(str(i))
            self.label.setStyleSheet("font-size: 20px;")
            self.hor_lay.addWidget(self.label)
            self.line = QLineEdit()
            self.line.setMinimumWidth(50)
            self.line.setObjectName(str(i))
            self.line.setStyleSheet("font-size: 20px;")
            self.all_lines.append(self.line)
            self.all_labels.append(self.label)
            self.hor_lay.addWidget(self.line)

        self.hor_lay.addStretch(0)

