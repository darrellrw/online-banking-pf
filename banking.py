from datetime import datetime

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