from account import Debit
from utils import numberToIDR, generate_random_price

def confirm_action(message: str):
  print(message)
  print("1. Ya")
  print("2. Tidak")
  choice = int(input("Pilih: "))
  return choice == 1

def transfer_action(selected_account: Debit):
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

def payment_action(selected_account: Debit):
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


def deposit_action(selected_account: Debit):
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


def withdraw_action(selected_account: Debit):
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