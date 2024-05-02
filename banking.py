from datetime import datetime
from database.db import Database

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

class BankingFactory:
    def create_account(self, user):
        raise NotImplementedError

class DebitBankingFactory(BankingFactory):
    def create_account(self, user):
        return Debit(len(user.accounts) + 1, 0, datetime.now().strftime("%Y-%m-%d"))

class BankingSystem:
    def __init__(self, factory):
        self.factory = factory
    
    def create_account(self, user):
        account =  self.factory.create_account(user)
        user.add_account(account)
        return account
class User:
    def __init__(self, name, phone, email, password):
        self.id = Database().execute("INSERT", "INTO nasabah (nama, no_hp, email, password) VALUES (?, ?, ?, ?)", (name, phone, email, password))
        self.name = name
        self.phone = phone
        self.email = email
        self.created_at = None
        self.accounts = []

    def add_account(self, jenis_rekening, nama_rekening, no_rekening, nasabah_id):
        self.accounts.append({
            "jenis_rekening": jenis_rekening,
            "nama_rekening": nama_rekening,
            "no_rekening": no_rekening,
            "nasabah_id": nasabah_id
        })
        Database().execute("INSERT", "INTO rekening (jenis_rekening, nama_rekening, no_rekening, nasabah_id) VALUES (?, ?, ?, ?)", (f"{jenis_rekening}", f"{self.name} - {len(self.accounts)}", f"{self.id}{len(self.accounts)}", f"{self.id}"))

    def get_user(self):
        user = Database().execute("SELECT", "* FROM nasabah WHERE id = ?", (f"{self.id}"))[0]
        return {
            "id": self.id,
            "name": user[1],
            "phone": user[2],
            "email": user[3],
            "created_at": user[5],
        }
        
    def get_account(self):
        return {
            "name": self.name,
            "accounts": [account for account in self.accounts]
        }

class UserBuilder:
    def __init__(self):
        self._name = ""
        self._phone = ""
        self._email = ""
        self._password = ""

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

    def build(self):
        return User(self._name, self._phone, self._email, self._password)


# Test case
def main():
    darrell = User(1, "Darrell", "1234567890", "admin@mail.com", "2024-01-01")
    dimas = User(2, "Dimas", "0987654321", "dimas@mail.com", "2024-01-02")

    saving_factory_debit = DebitBankingFactory()
    saving_system = BankingSystem(saving_factory_debit)

    darrell_saving_account_1 = saving_system.create_account(darrell)
    darrell_saving_account_2 = saving_system.create_account(darrell)

    dimas_saving_account_1 = saving_system.create_account(dimas)

    print("Case 1:")
    print("\tDarrell:")
    print("\t\t" + str(darrell.get_account()))
    print("\t\t" + str(darrell.get_user()))

    print("\tDimas:")
    print("\t\t" + str(dimas.get_account()))
    print("\t\t" + str(dimas.get_user()))

    print("\nCase 2:")
    darrell_saving_account_1.deposit(100000)

    print("\tDarrell:")
    print("\t\t" + str(darrell.get_account()))
    print("\t\t" + str(darrell.get_user()))

    print("\nCase 3:")
    darrell_saving_account_1.withdraw(1000)

    print("\tDarrell:")
    print("\t\t" + str(darrell.get_account()))
    print("\t\t" + str(darrell.get_user()))

    print("Case 4:")
    darrell_saving_account_1.transfer(1000, dimas_saving_account_1)

    print("\tDarrell:")
    print("\t\t" + str(darrell.get_account()))
    print("\t\t" + str(darrell.get_user()))

    print("\tDimas:")
    print("\t\t" + str(dimas.get_account()))
    print("\t\t" + str(dimas.get_user()))

if __name__ == "__main__":
    main()