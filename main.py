from database.db import Database
from banking import UserBuilder


class BankApp:
  _user = None
  _db = None
    
  def __init__(self):
    self._db = Database() 

  def register(self):
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    password = input("Password: ")
    user = UserBuilder().set_email(email).set_name(name).set_password(password).set_phone(phone).build()
    self._user = user
    print("Register success")
    self.auth()
    
  def login(self):
    attempt = 3
    user = None
    
    while attempt > 0:
      email = input("Email: ")
      password = input("Password: ")
      user = self._db.execute("SELECT", "* FROM nasabah WHERE email = ? AND password = ?", (email, password))
      if user:
        self._user = UserBuilder().set_email(user[0][3]).set_name(user[0][1]).set_password(user[0][4]).set_phone(user[0][2]).build()
      else:
        print("Login failed")
        attempt -= 1

    if not user:
      print("You have reached maximum attempt")
      exit()
  
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
    
  def main(self):
    self.auth()
    
    if not self._user:
      exit()
    
    print("Welcome to Bank App")
    
    
if __name__ == "__main__":
  app = BankApp()
  app.main()
