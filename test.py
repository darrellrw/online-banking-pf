from database.db import Database

db = Database()

transactions = db.execute("SELECT", "* FROM transaksi WHERE rekening_id IN (SELECT no_rekening FROM rekening WHERE nasabah_id = ?)", (f"{1}",))

print(transactions)