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
            lastUpdate DATE NOT NULL, \
            mmyyyy DATE NOT NULL, \
            type VARCHAR(20) NOT NULL, \
            budget INTEGER NOT NULL)"
        sqlCreateTableSpending = "CREATE TABLE if not exists Spending ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            lastUpdate DATE NOT NULL, \
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

    def insertTableBudget(self, lastUpdate, mmyyyy, type, budget):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlInsertTableBudget = "INSERT INTO Budget (lastUpdate, mmyyyy, type, budget) \
                                VALUES (?, ?, ?, ?)"
        cursor.execute(sqlInsertTableBudget, (lastUpdate, mmyyyy, type, budget))
        cursor.close()
        conn.commit()
        conn.close()

    def insertTableSpending(self, lastUpdate, date, type, item, cost):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlInsertTableSpending = "INSERT INTO Spending (lastUpdate, date, type, item, cost) \
                                VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sqlInsertTableSpending, (lastUpdate, date, type, item, cost))
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

    def deleteLatestDeposit(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlDeleteTableDeposit = "DELETE FROM Deposit WHERE lastUpdate IN (SELECT lastUpdate FROM Deposit ORDER BY lastUpdate DESC limit 1)"
        sqlUpdateTableDeposit = "UPDATE sqlite_sequence SET seq = seq-1 WHERE name = 'Deposit'"
        cursor.execute(sqlDeleteTableDeposit)
        cursor.execute(sqlUpdateTableDeposit)
        cursor.close()
        conn.commit()
        conn.close()

    def deleteLatestBudget(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlDeleteTableBudget = "DELETE FROM Budget WHERE lastUpdate IN (SELECT lastUpdate FROM Budget ORDER BY lastUpdate DESC limit 1)"
        sqlUpdateTableBudget = "UPDATE sqlite_sequence SET seq = (SELECT id FROM Budget ORDER BY id DESC limit 1) WHERE name = 'Budget'"
        cursor.execute(sqlDeleteTableBudget)
        cursor.execute(sqlUpdateTableBudget)
        cursor.close()
        conn.commit()
        conn.close()

    def deleteLatestSpending(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlDeleteTableSpending = "DELETE FROM Spending WHERE lastUpdate IN (SELECT lastUpdate FROM Spending ORDER BY lastUpdate DESC limit 1)"
        sqlUpdateTableSpending = "UPDATE sqlite_sequence SET seq = seq-1 WHERE name = 'Spending'"
        cursor.execute(sqlDeleteTableSpending)
        cursor.execute(sqlUpdateTableSpending)
        cursor.close()
        conn.commit()
        conn.close()
        
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