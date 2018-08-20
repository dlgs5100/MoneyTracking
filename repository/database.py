import sqlite3

class database:
    def __init__(self):
        conn = sqlite3.connect('dbmoneytracking.db')
        cursor = conn.cursor()
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
        cursor.execute(sqlCreateTableBudget)
        cursor.execute(sqlCreateTableSpending)
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