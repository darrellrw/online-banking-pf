class Account:
    def __init__(self, id, balance, created_at):
        self.id = id
        self.balance = balance
        self.created_at = created_at

    def get_account(self):
        return {
            "id": self.id,
            "balance": self.balance,
        }

class Debit(Account):
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if self.balance < amount:
            return "Insufficient balance"
        self.balance -= amount
    
    def transfer(self, amount, account):
        if self.balance < amount:
            return "Insufficient balance"
        self.balance -= amount
        account.balance += amount
    
    def payment(self, amount, account):
        if self.balance < amount:
            return "Insufficient balance"
        self.balance -= amount
        account.balance += amount

class User:
    def __init__(self, id, name, phone, email, created_at):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.created_at = created_at
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def get_user(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at,
        }

    def get_account(self):
        return {
            "name": self.name,
            "accounts": [account.get_account() for account in self.accounts]
        }