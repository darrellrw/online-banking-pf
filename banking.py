from datetime import datetime
from database.db import Database
from account import Account, Debit, User
import random

class BankingFactory:
    def create_account(self, user: User):
        raise NotImplementedError

class DebitBankingFactory(BankingFactory):
    _db = None
    
    def __init__(self):
        self._db = Database()
    
    def create_account(self, user: User):
        randomAccountNumber = random.randint(1000000000, 9999999999)
        lastrowid = self._db.execute("INSERT", "INTO rekening (no_rekening, jenis_rekening, balance, nasabah_id) VALUES (?, ?, ?, ?)", (randomAccountNumber, "debit", 50000, user.id))
        account = self._db.execute("SELECT", "* FROM rekening WHERE id = ?", (f"{lastrowid}",))[0]
        return Debit(account[1], account[3])

class BankingSystem:    
    def __init__(self, factory: DebitBankingFactory):
        self.factory = factory
        self._db = Database()
    
    def create_account(self, user: User):
        account = self.factory.create_account(user)
        user.add_account(account)
        return account

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