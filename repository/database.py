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
        sqlCreateTableIncome = "CREATE TABLE if not exists Income ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            lastUpdate DATE NOT NULL, \
            date DATE NOT NULL, \
            type VARCHAR(20) NOT NULL, \
            item VARCHAR(20) NOT NULL, \
            income INTEGER NOT NULL)"
        
        cursor.execute(sqlCreateTableDeposit)
        cursor.execute(sqlCreateTableBudget)
        cursor.execute(sqlCreateTableSpending)
        cursor.execute(sqlCreateTableIncome)
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

    def insertTableIncome(self, lastUpdate, date, type, item, income):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlInsertTableIncome = "INSERT INTO Income (lastUpdate, date, type, item, income) \
                                VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sqlInsertTableIncome, (lastUpdate, date, type, item, income))
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
                                WHERE mmyyyy = ? AND type = ? ORDER BY lastUpdate DESC limit 1"
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

    def getTotalIncome(self, mmyyyy):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableIncome = "SELECT income FROM Income \
                                WHERE strftime('%Y-%m', date) = ?"
        result = cursor.execute(sqlSelectTableIncome, (mmyyyy, ))

        total = 0
        for row in result:
            total += row[0]

        return total

    def getAllTypeFromSpending(self):
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
    
    def getAllTypeFromIncome(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableIncome = "SELECT DISTINCT type FROM Income"
        cursor.execute(sqlSelectTableIncome)

        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            list = []
            for row in result:
                list.append(row[0])
            return list
    
    def getAllTypeByMMYYYFromSpending(self, mmyyyy):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT DISTINCT type FROM Spending\
                                WHERE strftime('%Y-%m', date) = ?"
        cursor.execute(sqlSelectTableSpending, (mmyyyy, ))

        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            list = []
            for row in result:
                list.append(row[0])
            return list
    
    def getAllTypeByMMYYYFromIncome(self, mmyyyy):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableIncome = "SELECT DISTINCT type FROM Income\
                                WHERE strftime('%Y-%m', date) = ?"
        cursor.execute(sqlSelectTableIncome, (mmyyyy, ))

        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            list = []
            for row in result:
                list.append(row[0])
            return list
    
    def getAllItemByTypeFromSpending(self, type):
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

    def getAllItemByTypeFromIncome(self, type):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableIncome = "SELECT DISTINCT item FROM Income \
                                WHERE type = ?"
        cursor.execute(sqlSelectTableIncome, (type, ))
        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            list = []
            for row in result:
                list.append(row[0])
            return list
    
    def getAllCostByTypeFromSpending(self, type, mmyyyy):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT cost FROM Spending \
                                WHERE type = ? AND strftime('%Y-%m', date) = ?"
        cursor.execute(sqlSelectTableSpending, (type, mmyyyy, ))
        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            total = 0
            for row in result:
                total += row[0]
            return total

    def getAllCostByTypeFromIncome(self, type, mmyyyy):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableIncome = "SELECT income FROM Income \
                                WHERE type = ? AND strftime('%Y-%m', date) = ?"
        cursor.execute(sqlSelectTableIncome, (type, mmyyyy, ))
        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            total = 0
            for row in result:
                total += row[0]
            return total
    
    def getAllYearsAndMonthInSpending(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT DISTINCT strftime('%Y-%m', date) FROM Spending"
        cursor.execute(sqlSelectTableSpending)
        result = cursor.fetchall()
        if result is None:
            return 0
        else:
            list = []
            for row in result:
                list.append(row[0])
            return list
    
    def getLatestSpendingDate(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT date FROM Spending ORDER BY date DESC limit 1"
        cursor.execute(sqlSelectTableSpending)

        result = cursor.fetchone()
        if result is None:
            return '0'
        else:
            return result[0]

    def getLatestIncomeDate(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableIncome = "SELECT date FROM Income ORDER BY date DESC limit 1"
        cursor.execute(sqlSelectTableIncome)

        result = cursor.fetchone()
        if result is None:
            return '0'
        else:
            return result[0]

    def getDetailByTypeFromSpending(self, type, mmyyyy):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableSpending = "SELECT id, date, item, cost FROM Spending \
                                WHERE type = ? AND strftime('%Y-%m', date) = ? ORDER BY date ASC"
        cursor.execute(sqlSelectTableSpending, (type, mmyyyy, ))
        result = cursor.fetchall()
        if result is None:
            return '0'
        else:
            return result
    
    def getDetailByTypeFromIncome(self, type, mmyyyy):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableIncome = "SELECT id, date, item, income FROM Income \
                                WHERE type = ? AND strftime('%Y-%m', date) = ? ORDER BY date ASC"
        cursor.execute(sqlSelectTableIncome, (type, mmyyyy, ))
        result = cursor.fetchall()
        if result is None:
            return '0'
        else:
            return result

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

    def deleteLatestIncome(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlDeleteTableIncome = "DELETE FROM Income WHERE lastUpdate IN (SELECT lastUpdate FROM Income ORDER BY lastUpdate DESC limit 1)"
        sqlUpdateTableIncome = "UPDATE sqlite_sequence SET seq = seq-1 WHERE name = 'Income'"
        cursor.execute(sqlDeleteTableIncome)
        cursor.execute(sqlUpdateTableIncome)
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