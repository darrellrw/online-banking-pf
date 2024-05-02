import sqlite3
import os

# Create Database class that implements Singleton
class Database:
  _instance = None

  def __new__(cls):
    if cls._instance is None and not os.path.exists('./database/bank.db'):
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
      jenis_rekening ENUM('debit', 'kredit') NOT NULL,
      nama_rekening VARCHAR(255) NOT NULL,
      no_rekening VARCHAR(255) NOT NULL,
      nasabah_id INTEGER NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (nasabah_id) REFERENCES nasabah(id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      rekening_id INTEGER NOT NULL,
      jenis ENUM('keluar', 'masuk') NOT NULL,
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
      FOREIGN KEY (nasabah_id) REFERENCES nasabah(id),
      FOREIGN KEY (rekening_id) REFERENCES rekening(id)
    );
    """)
  
    cursor.close()
  
  def __del__(self):
    self.connection.close()

