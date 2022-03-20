# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4
# https://stackoverflow.com/a/
# https://stackoverflow.com/a/18430351


import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from index import Ui_MainWindow
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt4.QtGui import QMessageBox, QLineEdit
from PyQt4.QtCore import QDate, QString
import marshal

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# from mariadb import init, SqlTableDatabase


class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.con = init()
        self.msUi = Ui_MainWindow()
        self.msUi.setupUi(self)
        self.initUI()

    def initUI(self):

        self.msUi.NewPassLine.setEchoMode(QLineEdit.Password)
        self.msUi.RepPassLine.setEchoMode(QLineEdit.Password)
        self.d = None
        EnterBtn = self.msUi.EnterBtn
        ChanheUsrBtn = self.msUi.ChangeUserBtn
        RegBtn = self.msUi.RegBtn
        ForgotPassBtn = self.msUi.ForgotPassBtn
        ChnPassBtn = self.msUi.ChnPassBtn
        CancelBtn_2 = self.msUi.CancelBtn_2
        AccBtn = self.msUi.AccBtn
        CancelBtn = self.msUi.CancelBtn
        db_bulb_label = self.msUi.db_bulb_label
        db_bulb_label.setVisible(False)
        self.table = self.msUi.tableView

        # Radio buttons
        rbname = ["rb" + str(i) for i in range(1, 14)]
        rbtns = [getattr(self.msUi, u) for u in rbname]
        # print rbtns
        # print [str(str(rb.text()).decode('utf-8')) for rb in rbtns]
        for b in rbtns:
            # lm = lambda: self.setFilter(b.text())
            # print b
            b.toggled.connect(lambda: self.setFilter(b))
        # [ for b in rbtns]
        # Database

        # Page 1
        EnterBtn.clicked.connect(self.auth)
        ChanheUsrBtn.clicked.connect(self.deAuth)
        RegBtn.clicked.connect(self.regWidget)
        ForgotPassBtn.clicked.connect(self.forgotPassword)
        flagPass = self.msUi.ShowPassFlag
        flagPass.toggled.connect(
            lambda flag: self.msUi.PasswordLine.setEchoMode(QLineEdit.Normal if flag else QLineEdit.Password))
        # Restore pass page
        ChnPassBtn.clicked.connect(self.restorePass)
        CancelBtn_2.clicked.connect(self.backToMain)
        # New user page
        AccBtn.clicked.connect(self.newUser)
        CancelBtn.clicked.connect(self.backToMain)

        f = None
        try:
            f = open("login.dmp", "rb")
        except IOError:
            pass
        if f is not None:
            login_pass = None
            try:
                login_pass = marshal.load(f)
            except MemoryError:
                f.close()
            if login_pass is not None:
                # print login_pass["user"].decode("UTF-8")
                self.auth(None, username=login_pass["user"].decode("UTF-8"),
                          passwd=login_pass["password"].decode("UTF-8"))

    def setFilter(self, rb):
        rbtn = self.sender()
        # print rbtn.text()
        if rbtn.isChecked() == True:
            # print rbtn.text()
            # print QString("Username  RLIKE '^[") + QString(rbtn.text()) + QString("]'")
            self.model.setFilter(QString("Username  RLIKE '^[") + QString(rbtn.text()) + QString("]'"))
            self.model.select()

            if self.model.rowCount() == 0:
                self.updateDialog()


    def moveTo(self, index):
        stackedWidget = self.msUi.stackedWidget
        stackedWidget.setCurrentIndex(index)

    def auth(self, arg, username=None, passwd=None):
        d = self.checkPass(username, passwd)
        if d is not None:
            self.msUi.ChangeUserBtn.setText(d)
            self.initTable()
            self.moveTo(3)
            self.birthdayReminder()

    def deAuth(self):
        self.msUi.NameLine.setText("")
        self.msUi.PasswordLine.setText("")
        import os
        try:
            os.remove("login.dmp")
        except WindowsError:
            pass
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
        name = self.msUi.NewNameLine.text()
        paswd = self.msUi.NewPassLine.text()
        rePass = self.msUi.RepPassLine.text()
        date = self.msUi.NewDateEdit.date()
        if paswd == rePass:
            model = QSqlTableModel(None, self.con)
            model.setTable("auth")
            record = model.record()
            record.setValue(0, name)
            record.setValue(1, paswd)
            record.setValue(2, date)
            if not model.insertRecord(-1, record):
                self.showMsg("Incorrect login or password", QMessageBox.Information)
            print model.lastError().text()
            self.moveTo(0)
        else:
            self.showMsg("Incorrect password", QMessageBox.Warning)

    def checkPass(self, user=None, password=None):
        if user is None:
            user = self.msUi.NameLine.text()
            password = self.msUi.PasswordLine.text()
        query = QSqlQuery()
        query.exec_("SELECT * FROM auth WHERE Username = '%s' AND Pass = '%s' " % (user, password))
        if query.size() == 0:
            self.showMsg("Access denied", QMessageBox.Information)
            return None
        else:
            savePass = self.msUi.RemindMeFlag.isChecked()
            if savePass:
                self.savePass(user, password)
            return user

    def savePass(self, user, password):
        login_pass_save = {}
        login_pass_save["user"] = user
        login_pass_save["password"] = password
        f = open('login.dmp', "wb")
        marshal.dump(login_pass_save, f)
        f.close()
        pass

    def birthdayReminder(self):
        if self.con.isOpen():
            query = QSqlQuery()
            query.exec_("SELECT * FROM notebook")
            today = QDate.currentDate()
            year = today.year()
            nextWeek = QDate.currentDate().addDays(7)
            wins = []
            while query.next():
                # print query.value(2).toDate()
                d = query.value(2).toDate()
                d = QDate(year,d.month(), d.day())
                if today <= d <= nextWeek:
                    wins.append(query.value(0).toString())

            if wins:
                msgBox = QtGui.QDialog()
                layout = QtGui.QVBoxLayout()
                label = QtGui.QLabel()
                label.setText("Birtdays!")
                listWidget = QtGui.QListWidget()
                for i, p in enumerate(wins):
                    listWidget.insertItem(i, p)
                msgBox.setLayout(layout)
                layout.addWidget(label)
                layout.addWidget(listWidget)
                msgBox.exec_()

    def initTable(self):
        if self.con is None:
            assert "No database found"
        self.model = QSqlTableModel(None, self.con)
        self.model.setTable("notebook")
        self.model.select()

        self.table.setModel(self.model)
        selectionModel = self.table.selectionModel()
        selectionModel.currentRowChanged.connect(self.changeDialog)
        selectionModel.currentChanged.connect(self.changeDialog)
        self.table.entered.connect(self.updateDialog)


        self.show()

    def changeDialog(self, current, previous):
        print [current.column(), current.row()]
        if current.column() == -1:
            return
        self.d = QtGui.QDialog()
        self.d.setWindowTitle("Dialog")

        # print self.model.record(current.row()).value(0)
        layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel(self.model.record(current.row()).value(0).toString())
        b1 = QtGui.QPushButton("Add new")
        b2 = QtGui.QPushButton("Update current")
        b3 = QtGui.QPushButton("Delete current")
        b4 = QtGui.QPushButton("Abort")
        b1.clicked.connect(lambda: self.updateDialog(None))
        b2.clicked.connect(lambda: self.updateDialog(current.row()))
        b3.clicked.connect(lambda: self.deleteElem(current.row()))

        layout.addWidget(label)
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addWidget(b4)
        # b1.move(50, 50)
        # d.setWindowModality(QtCore.Qt.ApplicationModal)
        self.d.setLayout(layout)
        # d.show()
        self.d.exec_()

    def deleteElem(self, cursor):
        self.d.accept()
        if self.showMsg("Are you sure?", QMessageBox.Warning) == 1024:
            print "Yes"
            self.model.removeRows(cursor, 1)

        else:
            print "No"
        # pass

    def updateDialog(self, cursor=None):
        if self.d is not None:
            self.d.reject()
        self.d = QtGui.QDialog()
        self.d.setWindowTitle("Update")
        layout = QtGui.QVBoxLayout()
        line1 = QtGui.QLineEdit(self.d)
        line2 = QtGui.QLineEdit(self.d)
        line3 = QtGui.QDateEdit(self.d)
        if cursor is not None:
            line1.setText(self.model.record(cursor).value(0).toString())
            line2.setText(self.model.record(cursor).value(1).toString())
            line3.setDate(self.model.record(cursor).value(2).toDate())

        layout2 = QtGui.QHBoxLayout()
        Ok = QtGui.QPushButton("Ok")
        Cancel = QtGui.QPushButton("Cancel")
        layout2.addWidget(Ok)
        layout2.addWidget(Cancel)

        # buttonBox.accepted.connect(self.d.accept)
        Ok.clicked.connect(lambda: self.acceptChanges(cursor, line1, line2, line3))
        Cancel.clicked.connect(self.d.reject)

        layout.addWidget(line1)
        layout.addWidget(line2)
        layout.addWidget(line3)
        layout.addLayout(layout2)

        self.d.setLayout(layout)
        self.d.exec_()

    def acceptChanges(self, cursor, line1, line2, line3):
        self.d.reject()
        self.d = None
        t1 = line1.text()
        t2 = line2.text()
        if len(t1) == 0 or len(t2) == 0:
            self.showMsg("Incorrect field input")
            return
        record = self.model.record()
        record.setValue(0, line1.text())
        record.setValue(1, line2.text())
        record.setValue(2, line3.date())
        if cursor is not None:
            self.model.setRecord(cursor, record)
            if not self.model.submitAll():
                self.model.revertAll()
                self.showMsg("Duplicat!", QMessageBox.Warning)
        else:
            if not self.model.insertRecord(-1, record):
                self.model.revertAll()
                self.showMsg("Duplicat!", QMessageBox.Warning)

    def showMsg(self, msg, type):
        msgBox = QMessageBox()
        msgBox.setIcon(type)
        msgBox.setText(msg)
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msgBox.exec_()


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
