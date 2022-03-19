from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt4.QtSql import *
from PyQt4 import QtSql
from PyQt4.QtGui import QTabWidget





# class SqlTableDatabase(QSqlTableModel):
#     def __init__(self, DB, table):
#         super(SqlTableDatabase, self).__init__()
#         self.db = DB
#         if not self.ping():
#             print "Warning: Connection not established"
#             return
#         else:
#             self.database(self.db)
#             self.setTable(table)
#
#     def ping(self):
#         return self.db.isOpen()

    # def getRawDataByLetter(self, schema):
    #     if self.ping():
    #         query = QSqlQuery(con)
    #         query.exec_("SELECT * FROM notebook")
    #         print


# db = init()
# Table = SqlTableDatabase(db)
# ok = con.connect()
# if ok:
#     query = QSqlQuery(con)
#     query.exec_("SELECT * FROM notebook")
#     while query.next():
#         print query.value(0).toString().toUtf8()
#
# con.close()
