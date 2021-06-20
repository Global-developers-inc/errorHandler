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
        self.hostnameEdit = QLineEdit()
        self.timeEdit = QLineEdit()
        self.categoryEdit = QLineEdit()
        self.levelEdit = QLineEdit()
        self.messageEdit = QLineEdit()
        self.wgt = QWidget(self)
        layout = QHBoxLayout()
        self.setWindowTitle("Events")
        self.resize(WIDTH, HEIGHT)
        # Set up the view and load the data
        self.view = QTableWidget()
        self.view.setColumnCount(COUNT_COLUMNS)
        self.view.setHorizontalHeaderLabels(["id", "Time", "Hostname", "Category", "Level", "Message"])
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
        layout.addWidget(self.get_line(QLabel("Hostname"), self.hostnameEdit))
        layout.addWidget(self.get_line(QLabel("Time\t\t\t\t"), self.timeEdit))
        layout.addWidget(self.get_line(QLabel("Category"), self.categoryEdit))
        layout.addWidget(self.get_line(QLabel("Level"), self.levelEdit))
        layout.addWidget(self.get_line(QLabel("Message"), self.messageEdit))
        btn = QPushButton(text="Search") 
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
        query = QSqlQuery("SELECT id, REALTIME_TIMESTAMP, HOSTNAME, SYSLOG_FACILITY, PRIORITY, MESSAGE FROM events " + request)
        row = 0
        while query.next():
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
        hostname = self.hostnameEdit.text()
        time = self.timeEdit.text()
        category = self.categoryEdit.text()
        level = self.levelEdit.text()
        message = self.messageEdit.text()
        if hostname:
            request["HOSTNAME"] = self.add_brakeys(hostname)
        if time: 
            request["REALTIME_TIMESTAMP"] = self.add_brakeys(time)
        if category:
            request["SYSLOG_FACILITY"] = self.add_brakeys(category)
        if level:
            request["PRIORITY"] = self.add_brakeys(level)
        if message:
            request["MESSAGE"] = self.add_brakeys(message)
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