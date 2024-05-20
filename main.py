from banking import BankingSystem, DebitBankingFactory
from account import User, UserBuilder, Debit
import prettytable as pt
from feature_actions import transfer_action, payment_action, deposit_action, withdraw_action, numberToIDR
from merge_sort import BalanceMergeSort
import os
import pwinput

# Menyimpan fungsi aksi yang akan dilakukan ke dalam variabel dictionary
actions = {
  "transfer": transfer_action,
  "payment": payment_action,
  "deposit": deposit_action,
  "withdraw": withdraw_action
}

def pause():
  input("\nPress the <ENTER> key to continue...")

class BankApp(BankingSystem):
  _user: User = None

  def auth(self):    
    print("Welcome to Bank App")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = int(input("Choose menu: "))
    print("\n")
    if choice == 1:
      self.register()
    elif choice == 2:
      self.login()
    elif choice == 3:
      exit()
    else:
      print("Invalid choice")
      self.auth()

  def register(self):
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    password = pwinput.pwinput("Password: ")
    self._db.execute("INSERT", "INTO nasabah (nama, no_hp, email, password) VALUES (?, ?, ?, ?)", (name, phone, email, password))
    print("Register success")
    self.auth()
    
  def login(self):
    attempt = 3
    user = None
    
    while attempt > 0:
      email = input("Email: ")
      password = pwinput.pwinput(prompt="Password: ")
      user = self._db.execute("SELECT", "* FROM nasabah WHERE email = ? AND password = ?", (email, password))[0]
      if user:
        self._user = UserBuilder().set_id(user[0]).set_email(user[3]).set_name(user[1]).set_phone(user[2]).build()
        break
      else:
        print("Login failed\n")
        attempt -= 1

    if not user:
      print("You have reached maximum attempt")
      exit()
  
  def create_new_account(self):
    self.create_account(self._user)
    
  def show_balance(self, accounts):
    accounts_sort = [(account[0], account[1]) for account in accounts]
    BalanceMergeSort().sort(list_data=accounts_sort)
    accounts_sort = [(account[0], numberToIDR(account[1])) for account in accounts_sort]
    table = pt.PrettyTable()
    table.field_names = ["No Rekening", "Saldo"]
    table.align["Saldo"] = "l"
    table.add_rows(accounts_sort)
    print(table)
  
  def select_account(self, accounts) -> Debit:
    self.show_balance(accounts)
    
    no_rekening = input("No Rekening: ")
    selected_account = None
    
    for index, account in enumerate(accounts):
      if account[0] == no_rekening:
        selected_account = self._user.accounts[index]
        break
    
    if not selected_account:
      print("No Rekening tidak ditemukan")
      self.select_account(accounts)
      
    return selected_account

  # Method yang digunakan untuk memilih rekening yang akan digunakan untuk melakukan transaksi
  # dan menerapakan Higher Order Function untuk memilih aksi yang akan dilakukan
  def choose_account_action(self, accounts, action_func):
    print("\nSilahkan pilih rekening yang akan digunakan untuk melakukan transaksi")
    selected_account = self.select_account(accounts)
    action_func(selected_account)
  
  def transfer(self, accounts: list[Debit]):    
    # menerapkan first class function untuk memilih aksi yang akan dilakukan
    action = actions["transfer"]
    self.choose_account_action(accounts, action)
    
  def payment(self, accounts: list[Debit]):
    # menerapkan first class function untuk memilih aksi yang akan dilakukan
    action = actions["payment"]
    self.choose_account_action(accounts, action)
    
  def deposit(self, accounts: list[Debit]):
    # menerapkan first class function untuk memilih aksi yang akan dilakukan
    action = actions["deposit"]
    self.choose_account_action(accounts, action)
    
  def withdraw(self, accounts: list[Debit]):
    # menerapkan first class function untuk memilih aksi yang akan dilakukan
    action = actions["withdraw"]
    self.choose_account_action(accounts, action)
    
  def transaction_history(self):
    transactions = self._user.get_transactions()
    table = pt.PrettyTable()
    table.field_names = ["No", "No Rekening", "Jenis", "Nominal", "Keterangan", "Tanggal"]
    table.align["Keterangan"] = "l"
    table.align["Nominal"] = "l"
    table.align["Tanggal"] = "l"
    table.add_rows([(transaction[0], transaction[1], transaction[2], numberToIDR(transaction[3]), transaction[4], transaction[5]) for transaction in transactions])
    print(table)
    
  def main(self):
    self.auth()
    
    if not self._user:
      exit()
    
    accounts = self._user.get_account()
    if len(accounts) == 0:
      print("Kamu tidak memiliki rekening sama sekali")
      print("\nRekening baru akan dibuat")
      pause()
      self.create_account(self._user)
      accounts = self._user.get_account()
        
    print("Welcome to Bank App")
    
    pil = None
    while pil != 9:
      print("\nMenu")
      print("1. Lihat Saldo Semua Rekening")
      print("2. Transfer")
      print("3. Pembayaran")
      print("4. Deposit")
      print("5. Penarikan")
      print("6. Lihat data user")
      print("7. Buat Rekening Baru")
      print("8. Lihat Riwayat Transaksi")
      print("9. Exit")
      pil = int(input("Pilih menu: "))
      
      if pil == 1:
        print("\nSaldo anda adalah: ")
        self.show_balance(accounts)
      elif pil == 2:
        self.transfer(accounts)
      elif pil == 3:
        self.payment(accounts)
      elif pil == 4: 
        self.deposit(accounts)
      elif pil == 5:
        self.withdraw(accounts)
      elif pil == 6:
        user = self._user.get_user()
        print("\n")
        for key, value in user.items():
          print(f"{key}: {value}")
      elif pil == 7:
        self.create_new_account()
        print("Rekening baru berhasil dibuat")
      elif pil == 8:
        self.transaction_history()
      elif pil == 9:
        print("Terima kasih telah menggunakan Bank App")
        exit()
      else:
        print("Invalid choice")
      pause()
      accounts = self._user.get_account()
      os.system("clear||cls")
    
    
if __name__ == "__main__":
  debit_banking_factory = DebitBankingFactory()
  app = BankApp(debit_banking_factory)
  app.main()
