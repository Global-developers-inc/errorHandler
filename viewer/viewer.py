import sys


from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget, 
    QHBoxLayout,
    QVBoxLayout,
    QLabel, 
    QLineEdit,
    QCheckBox,
)


MAX_PANEL_WIDTH = 400
MAX_PANEL_HEIGHT = 300
WIDTH = 800
HEIGHT = 600
COUNT_COLUMNS = 6


class Contacts(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nameEdit = QLineEdit()
        self.dateEdit = QLineEdit()
        self.timeEdit = QLineEdit()
        self.errorEdit = QLineEdit()
        self.is_adminCheck = QCheckBox()
        self.check_is_adminCheck = QCheckBox()
        self.wgt = QWidget(self)
        layout = QHBoxLayout()
        self.setWindowTitle("Errors")
        self.resize(WIDTH, HEIGHT)
        # Set up the view and load the data
        self.view = QTableWidget()
        self.view.setColumnCount(COUNT_COLUMNS)
        self.view.setHorizontalHeaderLabels(["id", "name", "is_admin", "date", "time", "error_text"])
        self.update_table()
        layout.addWidget(self.view)
        panel = QWidget()
        panel.setMaximumWidth(MAX_PANEL_WIDTH)
        panel_layout = QVBoxLayout()
        panel.setLayout(panel_layout)
        panel_layout.addWidget(self.search_wgt())
        panel_layout.addWidget(QLabel())
        layout.addWidget(panel)
        self.wgt.setLayout(layout)
        self.setCentralWidget(self.wgt)
    
    def search_wgt(self):
        wgt = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.get_line(QLabel("name"), self.nameEdit))
        layout.addWidget(self.get_line(QLabel("is_admin\t\t\t\t"), self.is_adminCheck))
        layout.addWidget(self.get_line(QLabel("date"), self.dateEdit))
        layout.addWidget(self.get_line(QLabel("time"), self.timeEdit))
        layout.addWidget(self.get_line(QLabel("error_text"), self.errorEdit))
        layout.addWidget(self.get_line(QLabel('check "is_admin on search"\t\t'), self.check_is_adminCheck))
        btn = QPushButton(text="search") 
        btn.clicked.connect(self.search)
        layout.addWidget(btn)
        wgt.setLayout(layout)
        wgt.setMaximumWidth(MAX_PANEL_WIDTH)
        wgt.setMaximumHeight(MAX_PANEL_HEIGHT)
        return wgt
    
    def get_line(self, *args):
        line = QWidget()
        lay = QHBoxLayout()
        line.setLayout(lay)
        for a in args:
            lay.addWidget(a)
        return line
    
    def update_table(self, request=""):
        self.view.clear()
        query = QSqlQuery("SELECT id, name, is_admin, date, time, error_text FROM errors " + request)
        print("SELECT id, name, is_admin, date, time, error_text FROM errors " + request)
        row = 0
        while query.next():
            print("HI")
            self.view.setRowCount(row + 1)
            self.view.setItem(row, 0, QTableWidgetItem(str(query.value(0))))
            self.view.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.view.setItem(row, 2, QTableWidgetItem(str(query.value(2) == 1)))
            self.view.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
            self.view.setItem(row, 4, QTableWidgetItem(str(query.value(4))))
            self.view.setItem(row, 5, QTableWidgetItem(str(query.value(5))))
            row += 1
        self.view.setRowCount(row)
        self.view.resizeColumnsToContents()
    
    def add_brakeys(self, word):
        return '\"' + word + '\"' 
    
    def search(self):
        request = {}
        name = self.nameEdit.text()
        date = self.dateEdit.text()
        time = self.timeEdit.text()
        error = self.errorEdit.text()
        is_admin = self.is_adminCheck.isChecked()
        if name:
            request["name"] = self.add_brakeys(name)
        if date: 
            request["date"] = self.add_brakeys(date)
        if time:
            request["time"] = self.add_brakeys(time)
        if error:
            request["error_text"] = self.add_brakeys(error)
        if self.check_is_adminCheck.isChecked():
            request["is_admin"] = 1 if is_admin else 0
        r = []
        for k, v in request.items():
            r.append(f"{k} = {v}")
        if len(r) == 0:
            self.update_table()
            return 
        search_request = f"where ({' AND '.join(r)})"
        self.update_table(search_request)


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("data.db")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True


app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
win = Contacts()
win.show()
sys.exit(app.exec_())