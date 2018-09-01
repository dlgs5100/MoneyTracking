import sqlite3

class database:
    def __init__(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlCreateTableDeposit = "CREATE TABLE if not exists Deposit ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            lastUpdate DATE NOT NULL, \
            deposit INTEGER NOT NULL)"
        sqlCreateTableBudget = "CREATE TABLE if not exists Budget ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            mmyyyy DATE NOT NULL, \
            type VARCHAR(20) NOT NULL, \
            budget INTEGER NOT NULL)"
        sqlCreateTableSpending = "CREATE TABLE if not exists Spending ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            date DATE NOT NULL, \
            type VARCHAR(20) NOT NULL, \
            item VARCHAR(20) NOT NULL, \
            cost INTEGER NOT NULL)"
        cursor.execute(sqlCreateTableDeposit)
        cursor.execute(sqlCreateTableBudget)
        cursor.execute(sqlCreateTableSpending)
        cursor.close()
        conn.commit()
        conn.close()
    
    def insertTableDeposit(self, lastUpdate, deposit):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlInsertTableDeposit = "INSERT INTO Deposit (lastUpdate, deposit) \
                                VALUES (?, ?)"
        cursor.execute(sqlInsertTableDeposit, (lastUpdate, deposit))
        cursor.close()
        conn.commit()
        conn.close()

    def insertTableBudget(self, mmyyyy, type, budget):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlInsertTableBudget = "INSERT INTO Budget (mmyyyy, type, budget) \
                                VALUES (?, ?, ?)"
        cursor.execute(sqlInsertTableBudget, (mmyyyy, type, budget))
        cursor.close()
        conn.commit()
        conn.close()

    def insertTableSpending(self, date, type, item, cost):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlInsertTableSpending = "INSERT INTO Spending (date, type, item, cost) \
                                VALUES (?, ?, ?, ?)"
        cursor.execute(sqlInsertTableSpending, (date, type, item, cost))
        cursor.close()
        conn.commit()
        conn.close()

    def getTotalDeposit(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableDeposit = "SELECT deposit, lastUpdate FROM Deposit ORDER BY lastUpdate DESC limit 1"
        cursor.execute(sqlSelectTableDeposit)

        result = cursor.fetchone()
        if result is None:
            return 0, '1991-01-01 00-00-00'
        else:
            return result[0], result[1]

    def getTypeBudget(self, mmyyyy, type):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableBudget = "SELECT budget From Budget \
                                WHERE mmyyyy = ? \
                                AND type = ?"
        cursor.execute(sqlSelectTableBudget, (mmyyyy, type, ))

        result = cursor.fetchone()
        if result is None:
            return 0
        else:
            return result[0]

    def getTypeSpending(self, mmyyyy, type):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT cost FROM Spending \
                                WHERE strftime('%Y-%m', date) = ? \
                                AND type = ?"

        result = cursor.execute(sqlSelectTableSpending, (mmyyyy, type, ))
        total = 0
        for row in result:
            total += row[0]

        return total

    def getTotalSpending(self, mmyyyy):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT cost FROM Spending \
                                WHERE strftime('%Y-%m', date) = ?"
        result = cursor.execute(sqlSelectTableSpending, (mmyyyy, ))

        total = 0
        for row in result:
            total += row[0]

        return total

    def getAllType(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT DISTINCT type FROM Spending"
        cursor.execute(sqlSelectTableSpending)

        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            list = []
            for row in result:
                list.append(row[0])
            return list
    
    def getAllItemFromType(self, type):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT DISTINCT item FROM Spending \
                                WHERE type = ?"
        cursor.execute(sqlSelectTableSpending, (type, ))
        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            list = []
            for row in result:
                list.append(row[0])
            return list

        
    def truncateTable(self, tableName):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlTruncateTable = "DELETE FROM {tableName}".format(tableName = tableName)
        sqlUpdateTable = "UPDATE sqlite_sequence SET seq = 0 WHERE name = ?"
        cursor.execute(sqlTruncateTable)
        cursor.execute(sqlUpdateTable, (tableName, ))
        cursor.close()
        conn.commit()
        conn.close()