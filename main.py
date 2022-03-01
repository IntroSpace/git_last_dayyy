import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connect = sqlite3.connect('coffee.sqlite')
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec())