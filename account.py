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

class User:
    _db = Database()
    
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        
        acc = self._db.execute("SELECT", "* FROM rekening WHERE nasabah_id = ?", (f"{self.id}",))
        self.accounts = [Debit(account[1], account[3]) for account in acc]
    
    def __init__(self, id, name, phone, email, password):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        
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
        

class UserBuilder:
    def __init__(self):
        self._id = None
        self._name = None
        self._phone = None
        self._email = None
        self._password = None

    def set_name(self, name):
        self._name = name
        return self

    def set_phone(self, phone):
        self._phone = phone
        return self

    def set_email(self, email):
        self._email = email
        return self
    
    def set_password(self, password):
        self._password = password
        return self
    
    def set_id(self, id):
        self._id = id
        return self

    def build(self):
        return User(self._id, self._name, self._phone, self._email, self._password)