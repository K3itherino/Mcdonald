import sqlite3 as sql
class accmanag:
    def __init__(self, database):
        
        self.database = database
        self.conn = sql.connect(self.database, check_same_thread=False)
        self.cursor = self.conn.cursor()
   
    def createDB(self):
        
        self.conn.commit()
   
    def createTable(self, value):
        
        self.cursor.execute(
        f"""CREATE TABLE {value} (
            id int, username text, product text, quantity int
        )"""
        )
        self.conn.commit()
    
    def insertRow(self, username, password, table):
        
        instrucc = f"INSERT INTO {table} VALUES ('{username}', '{password}', '0', '0')"
        self.cursor.execute(instrucc)
        self.conn.commit()
    
    def findusername(self, table: str , username):
        
        instrucc = f"SELECT username FROM {table} WHERE username = '{username}'"
        self.cursor.execute(instrucc)
        username_f = self.cursor.fetchone()
        self.conn.commit()
        return username_f
    
    def findpassword(self, table: str , username):
        
        instrucc = f"SELECT password FROM {table} WHERE username = '{username}'"
        self.cursor.execute(instrucc)
        username_f = self.cursor.fetchone()
        self.conn.commit()
        return username_f
    
    def updatemenu(self, table, username, n:int, burger):
        
        c=f"UPDATE {table} set {burger} = {burger} + {n} WHERE username = '{username}'"
        self.cursor.execute(c)
        self.conn.commit()
    def read(self, table, username):
        
        c = f"SELECT burger, cheeseburger FROM {table} WHERE username = '{username}'"
        self.cursor.execute(c)
        p = self.cursor.fetchone()
        self.conn.commit()
        return p
    def createid(self, table):
        instrucc = f"SELECT id FROM {table} ORDER BY id DESC LIMIT 1"
        self.cursor.execute(instrucc)
        maxid = self.cursor.fetchone()
        self.conn.commit()
        return maxid

    def insertProduct(self, table, username, product, quantity, id):
        
        instrucc = f"INSERT INTO {table} VALUES ( '{id}', '{username}', '{product}', '{quantity}')"
        self.cursor.execute(instrucc)
        self.conn.commit()
    
    def read_buy(self, table, username):
        instrucc = f"SELECT * FROM {table} WHERE username = '{username}'"
        self.cursor.execute(instrucc)
        maxid = self.cursor.fetchall()
        self.conn.commit()
        return maxid
    def delete(self, table, id):

        instrucc = f"DELETE FROM {table} WHERE id = {id}"
        self.cursor.execute(instrucc)
        self.conn.commit()
    
        

    def close(self):
        
        self.conn.close()










        
