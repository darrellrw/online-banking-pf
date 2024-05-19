from database.db import Database

class Account:
    _db = None
    
    def __init__(self, account_number, balance):
        self.account_number = account_number 
        self.balance = balance
        self._db = Database()

    def get_account(self):
        account = self._db.execute("SELECT", "* FROM rekening WHERE no_rekening = ?", (self.account_number,))[0]
        return (account[1], account[3])

class Debit(Account):
    def deposit(self, amount):
        self.balance += amount
        self._db.execute("INSERT", "INTO transaksi (rekening_id, jenis, nominal) VALUES (?, ?, ?)", (self.account_number, "Deposit", amount))
        self._db.execute("UPDATE", "rekening SET balance = balance + ? WHERE no_rekening = ?", (amount, self.account_number))
    
    def withdraw(self, amount):
        if self.balance < amount:
            raise AssertionError("Insufficient balance")
        self._db.execute("INSERT", "INTO transaksi (rekening_id, jenis, nominal) VALUES (?, ?, ?)", (self.account_number, "Withdraw", amount))
        self._db.execute("UPDATE", "rekening SET balance = balance - ? WHERE no_rekening = ?", (amount, self.account_number))
        self.balance -= amount
    
    def transfer(self, amount, account):
        if self.balance < amount:
            raise AssertionError("Insufficient balance")
        self._db.execute("INSERT", "INTO transaksi (rekening_id, jenis, nominal) VALUES (?, ?, ?)", (self.account_number, "Transfer - Kirim", amount))
        self._db.execute("INSERT", "INTO transaksi (rekening_id, jenis, nominal) VALUES (?, ?, ?)", (account, "Transfer - Terima", amount))
        self._db.execute("UPDATE", "rekening SET balance = balance - ? WHERE no_rekening = ?", (amount, self.account_number))
        self._db.execute("UPDATE", "rekening SET balance = balance + ? WHERE no_rekening = ?", (amount, account))
        self.balance -= amount
    
    def payment(self, amount, account):
        if self.balance < amount:
            raise AssertionError("Insufficient balance")
        self._db.execute("INSERT", "INTO transaksi (rekening_id, jenis, nominal) VALUES (?, ?, ?)", (self.account_number, "Payment - Bayar", amount))
        self._db.execute("UPDATE", "rekening SET balance = balance - ? WHERE no_rekening = ?", (amount, self.account_number))
        self.balance -= amount

class UserBuilder:
    def __init__(self):
        self.id = None
        self.name = None
        self.phone = None
        self.email = None
        self.password = None

    def set_name(self, name):
        self.name = name
        return self

    def set_phone(self, phone):
        self.phone = phone
        return self

    def set_email(self, email):
        self.email = email
        return self
    
    def set_password(self, password):
        self.password = password
        return self
    
    def set_id(self, id):
        self.id = id
        return self

    def build(self):
        return User(self)


class User:
    _db = Database()
    
    def __init__(self, builder: UserBuilder):
        self.id = builder.id
        self.name = builder.name
        self.phone = builder.phone
        self.email = builder.email
        self.password = builder.password
        
        acc = self._db.execute("SELECT", "* FROM rekening WHERE nasabah_id = ?", (f"{self.id}",))
        self.accounts = [Debit(account[1], account[3]) for account in acc]

    def add_account(self, account):
        self.accounts.append(account)

    def get_user(self):
        created_at = self._db.execute("SELECT", "created_at FROM nasabah WHERE id = ?", (f"{self.id}",))[0]
        return {
            "ID": self.id,
            "Nama": self.name,
            "No Telepon": self.phone,
            "Email": self.email,
            "Terdaftar pada": created_at[0],
        }
    
    def get_account(self):
        return [account.get_account() for account in self.accounts]
    
    def get_transactions(self):
        transactions = self._db.execute("SELECT", "* FROM transaksi WHERE rekening_id IN (SELECT no_rekening FROM rekening WHERE nasabah_id = ?)", (f"{self.id}",))
        return transactions