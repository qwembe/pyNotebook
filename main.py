# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4
# https://stackoverflow.com/a/
# https://stackoverflow.com/a/18430351


import sys
from PyQt4 import QtGui
from index import Ui_MainWindow
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


# from mariadb import init, SqlTableDatabase


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.con = init()
        self.msUi = Ui_MainWindow()
        self.msUi.setupUi(self)
        self.initUI()

    def initUI(self):
        EnterBtn = self.msUi.EnterBtn
        ChanheUsrBtn = self.msUi.ChangeUserBtn
        RegBtn = self.msUi.RegBtn
        ForgotPassBtn = self.msUi.ForgotPassBtn
        ChnPassBtn = self.msUi.ChnPassBtn
        CancelBtn_2 = self.msUi.CancelBtn_2
        AccBtn = self.msUi.AccBtn
        CancelBtn = self.msUi.CancelBtn
        db_bulb_label = self.msUi.db_bulb_label
        self.table = self.msUi.tableView

        # Radio buttons
        rbname = ["rb" + str(i) for i in range(1, 14)]
        rb = [getattr(self.msUi, u) for u in rbname]

        # Database

        # Page 1
        EnterBtn.clicked.connect(self.auth)
        ChanheUsrBtn.clicked.connect(self.deAuth)
        RegBtn.clicked.connect(self.regWidget)
        ForgotPassBtn.clicked.connect(self.forgotPassword)
        # Restore pass page
        ChnPassBtn.clicked.connect(self.restorePass)
        CancelBtn_2.clicked.connect(self.backToMain)
        # New user page
        AccBtn.clicked.connect(self.newUser)
        CancelBtn.clicked.connect(self.backToMain)

    def moveTo(self, index):
        stackedWidget = self.msUi.stackedWidget
        stackedWidget.setCurrentIndex(index)

    def auth(self):
        self.initTable()
        self.moveTo(3)

    def deAuth(self):
        self.moveTo(0)

    def regWidget(self):
        self.moveTo(1)

    def forgotPassword(self):
        self.moveTo(2)

    def backToMain(self):
        self.moveTo(0)

    def restorePass(self):
        self.backToMain()

    def newUser(self):
        self.moveTo(0)

    def initTable(self):
        if self.con is None:
            assert "No database found"
        self.model = QSqlTableModel(None, self.con)
        self.model.setTable("notebook")
        self.model.select()

        self.table.setModel(self.model)
        self.show()


def init(config=None):
    if config is None:
        con = QSqlDatabase.addDatabase("QMYSQL")
        con.setHostName("192.168.0.5")
        con.setDatabaseName("dbnote")
        con.setUserName("pynotebook")
        con.setPassword("12345")
        con.setPort(3306)

    if con.open():
        return con
    else:
        return None


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    qb = App()
    qb.show()
    sys.exit(app.exec_())
