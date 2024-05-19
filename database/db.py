import sqlite3
import os

# Create Database class that implements Singleton
class Database:
  _instance = None

  def __new__(cls):
    if cls._instance is None or not os.path.exists('./database/bank.db'):
      cls._instance = super().__new__(cls)
      cls._instance.connection = sqlite3.connect('./database/bank.db')
      cls._instance._create_table()
    return cls._instance
  

  def _create_table(self):
    cursor = self.connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nasabah (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nama VARCHAR(255) NOT NULL,
      no_hp VARCHAR(255) NOT NULL,
      email VARCHAR(255) NOT NULL,
      password VARCHAR(255) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cursor.execute("""  
    CREATE TABLE IF NOT EXISTS rekening (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      no_rekening VARCHAR(255) NOT NULL,
      jenis_rekening VARCHAR(50) NOT NULL,
      balance INTEGER DEFAULT 0, 
      nasabah_id INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (nasabah_id) REFERENCES nasabah(id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      rekening_id INTEGER NOT NULL,
      jenis VARCHAR(50) NOT NULL,
      nominal INTEGER NOT NULL,
      keterangan TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (rekening_id) REFERENCES rekening(id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nasabah_id INTEGER NOT NULL,
      jenis VARCHAR(255) NOT NULL,
      nominal INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (nasabah_id) REFERENCES nasabah(id)
    );
    """)
  
    cursor.close()
    
  def execute(self, method, query, data=None):
    if method.lower() == "insert":
      return self._insert(f"{method} {query}", data)
    elif method.lower() == "select":
      return self._fetch(f"{method} {query}", data)
    elif method.lower() == "update":
      return self._update(f"{method} {query}", data)
    elif method.lower() == "delete":
      return self._delete(f"{method} {query}", data)
    else:
      return None
  
  def _insert(self, query, data):
    cursor = self.connection.cursor()
    cursor.execute(query, data)
    self.connection.commit()
    cursor.close()
    return cursor.lastrowid

  def _fetch(self, query, data):
    cursor = self.connection.cursor()
    cursor.execute(query, data)
    result = cursor.fetchall()
    cursor.close()
    return result

  def _update(self, query, data):
    cursor = self.connection.cursor()
    cursor.execute(query, data)
    cursor.close()
    self.connection.commit()
  
  def _delete(self, query, data):
    cursor = self.connection.cursor()
    cursor.execute(query, data)
    cursor.close()
    self.connection.commit()
  
  def __del__(self):
    self.connection.close()