import sqlite3

class database:
    def __init__(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlCreateTableDeposit = "CREATE TABLE if not exists Deposit ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT, \
            position VARCHAR(20) NOT NULL, \
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
    
    def insertTableDeposit(self, position, lastUpdate, deposit):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlInsertTableDeposit = "INSERT INTO Deposit (position, lastUpdate, deposit) \
                                VALUES (?, ?, ?)"
        cursor.execute(sqlInsertTableDeposit, (position, lastUpdate, deposit))
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
        sqlSelectTableDeposit = "SELECT deposit FROM Deposit"
        result = cursor.execute(sqlSelectTableDeposit)

        total = 0
        for row in result:
            total += row[0]
        return total

    def getTypeBudgetAndSpending(self, mmyyyy, type):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlSelectTableBudget = "SELECT budget From Budget \
                                WHERE mmyyyy = ? \
                                AND type = ?"
        sqlSelectTableSpending = "SELECT cost FROM Spending \
                                WHERE strftime('%Y-%m', date) = ? \
                                AND type = ?"

        result = cursor.execute(sqlSelectTableBudget, (mmyyyy, type, ))
        for row in result:
            MonthlyBudget = row[0]

        result = cursor.execute(sqlSelectTableSpending, (mmyyyy, type, ))
        MonthlySpending = 0
        for row in result:
            MonthlySpending += row[0]

        cursor.close()
        conn.commit()
        conn.close()

        return MonthlyBudget, MonthlySpending

    def truncateTable(self, tableName):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
        sqlTruncateTable = "DELETE FROM {tableName}".format(tableName = tableName)
        cursor.execute(sqlTruncateTable)
        cursor.close()
        conn.commit()
        conn.close()