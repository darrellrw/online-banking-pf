from datetime import datetime
from account import Account, Debit, User

class BankingFactory:
    def create_account(self, user: User):
        raise NotImplementedError

class DebitBankingFactory(BankingFactory):
    def create_account(self, user: User):
        return Debit(len(user.accounts) + 1, 0, datetime.now().strftime("%Y-%m-%d"))

class BankingSystem:
    def __init__(self, factory: DebitBankingFactory):
        self.factory = factory
    
    def create_account(self, user: User):
        account =  self.factory.create_account(user)
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