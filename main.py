from banking import BankingSystem, DebitBankingFactory
from account import User, UserBuilder, Debit
import prettytable as pt
from utils import numberToIDR, generate_random_price
from merge_sort import BalanceMergeSort
import os
import pwinput

def pause():
  input("\nPress the <ENTER> key to continue...")

def confirm_action(message: str):
  print(message)
  print("1. Ya")
  print("2. Tidak")
  choice = int(input("Pilih: "))
  return choice == 1

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

  def choose_account_action(self, accounts, action_func):
    print("\nSilahkan pilih rekening yang akan digunakan untuk melakukan transaksi")
    selected_account = self.select_account(accounts)
    action_func(selected_account)
  
  def transfer(self, selected_account: Debit):
    print("=" * 10, "Transfer", "=" * 10, "\n")
    print("\nSilahkan masukkan nomor rekening tujuan")
    no_rekening_tujuan = input("No Rekening: ")
    nominal = int(input("Nominal: "))
    try:
      if confirm_action(f"\nApakah anda yakin ingin mentransfer sejumlah {numberToIDR(nominal)} ke rekening {no_rekening_tujuan}?"):
        selected_account.transfer(nominal, no_rekening_tujuan)
        print("Transfer berhasil")
      else:
        print("Transfer dibatalkan")
    except AssertionError as e:
      print(str(e))
      
  def payment(self, selected_account: Debit):
    print("\nSilahkan masukkan kode pembayaran")
    kode_pembayaran = input("Kode Pembayaran: ")
    price = generate_random_price()
    
    try:      
      if confirm_action(f"\nAnda akan membayar sejumlah {numberToIDR(price)} dengan kode pembayaran {kode_pembayaran}"):
        selected_account.payment(price, kode_pembayaran)
        print("Pembayaran berhasil")
      else:
        print("Pembayaran dibatalkan")
    except AssertionError as e:
      print(str(e))
  
  def deposit(self, selected_account: Debit):
    print("=" * 10, "Deposit", "=" * 10, "\n")
    nominal = int(input("Nominal: "))
    
    try:
      if confirm_action(f"\nAnda akan melakukan deposit sejumlah {numberToIDR(nominal)}"):
        selected_account.deposit(nominal)
        print("Deposit berhasil")
      else:
        print("Deposit dibatalkan")
    except AssertionError as e:
      print(str(e))
  
  def withdraw(self, selected_account: Debit):
    print("=" * 10, "Penarikan", "=" * 10, "\n")
    nominal = int(input("Nominal: "))
    
    try:
      if confirm_action(f"\nAnda akan melakukan penarikan sejumlah {numberToIDR(nominal)}"):
        selected_account.withdraw(nominal)
        print("Penarikan berhasil")
      else:
        print("Penarikan dibatalkan")
    except AssertionError as e:
      print(str(e))
  
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
        self.choose_account_action(accounts, self.transfer)
      elif pil == 3:
        self.choose_account_action(accounts, self.payment)
      elif pil == 4: 
        self.choose_account_action(accounts, self.deposit)
      elif pil == 5:
        self.choose_account_action(accounts, self.withdraw)
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
