import sys
import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5 import uic

from UI.addEditCoffeeForm import Ui_AddWindow
from UI.main import Ui_MainWindow


class AddForm(QMainWindow, Ui_AddWindow):
    def __init__(self, connect, main):
        super().__init__()
        self.setupUi(self)
        self.connect = connect
        self.main = main
        self.pushButton.clicked.connect(self.check)
        cursor = self.connect.cursor()
        res = cursor.execute(f'select title '
                             f'from degree '
                             f'order by id').fetchall()
        for coff in res:
            self.degree_box.addItem(coff[0])
        res = cursor.execute(f'select title '
                             f'from kind '
                             f'order by id').fetchall()
        for coff in res:
            self.kind_box.addItem(coff[0])

    def check(self):
        try:
            name = self.name_edit.text()
            degree = self.degree_box.currentIndex() + 1
            kind = self.kind_box.currentIndex() + 1
            desc = self.desc_edit.text()
            price = int(self.price_edit.text())
            volume = float(self.volume_edit.text())
        except ValueError:
            QMessageBox.critical(self, 'Ошибка', 'Некорректные данные', QMessageBox.Ok)
            return
        cursor = self.connect.cursor()
        cursor.execute(f'insert into coffee(name, degree, kind, desc, price, volume) '
                       f'values(\'{name}\', {degree}, {kind}, \'{desc}\', {price}, {volume})')
        self.connect.commit()
        self.main.initUi()
        self.close()


class EditForm(QMainWindow, Ui_AddWindow):
    def __init__(self, connect, main, item):
        super().__init__()
        self.setupUi(self)
        self.connect = connect
        self.main = main
        self.item = item
        self.pushButton.clicked.connect(self.check)
        cursor = self.connect.cursor()
        res = cursor.execute(f'select title '
                             f'from degree '
                             f'order by id').fetchall()
        for coff in res:
            self.degree_box.addItem(coff[0])
        res = cursor.execute(f'select title '
                             f'from kind '
                             f'order by id').fetchall()
        for coff in res:
            self.kind_box.addItem(coff[0])
        res = cursor.execute(f'select name, desc, price, volume '
                             f'from coffee '
                             f'where id = {self.item}').fetchone()
        self.name_edit.setText(res[0])
        self.desc_edit.setText(res[1])
        self.price_edit.setText(str(res[2]))
        self.volume_edit.setText(str(res[3]))

    def check(self):
        try:
            name = self.name_edit.text()
            degree = self.degree_box.currentIndex() + 1
            kind = self.kind_box.currentIndex() + 1
            desc = self.desc_edit.text()
            price = int(self.price_edit.text())
            volume = float(self.volume_edit.text())
        except ValueError:
            QMessageBox.critical(self, 'Ошибка', 'Некорректные данные', QMessageBox.Ok)
            return
        cursor = self.connect.cursor()
        cursor.execute(f'update coffee '
                       f'set name = \'{name}\', '
                       f'degree =  {degree}, '
                       f'kind = {kind}, '
                       f'desc = \'{desc}\', '
                       f'price = {price}, '
                       f'volume = {volume} '
                       f'where id = {self.item}')
        self.connect.commit()
        self.main.initUi()
        self.close()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect = sqlite3.connect('data/coffee.sqlite')
        self.add_btn.clicked.connect(self.add_coffee)
        self.edit_btn.clicked.connect(self.edit_coffee)
        self.initUi()

    def initUi(self):
        cur = self.connect.cursor()
        coffee = cur.execute(f'select c.id, c.name, degree.title, '
                             f'kind.title, c.desc, c.price, c.volume '
                             f'from coffee c '
                             f'left join degree on c.degree = degree.id '
                             f'left join kind on c.kind = kind.id;').fetchall()
        title = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса',
                 'Цена', 'Объем порции']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(coffee))
        for i, row in enumerate(coffee):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def add_coffee(self):
        self.add_form = AddForm(self.connect, self)
        self.add_form.setWindowModality(Qt.ApplicationModal)
        self.add_form.show()

    def edit_coffee(self):
        if self.tableWidget.currentRow() != -1:
            cur_item = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        else:
            QMessageBox.critical(self, 'Ошибка', 'Выберите нужную строку', QMessageBox.Ok)
            return

        self.edit_form = EditForm(self.connect, self, cur_item)
        self.edit_form.setWindowModality(Qt.ApplicationModal)
        self.edit_form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec())