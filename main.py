from database.db import Database
from banking import User, UserBuilder

dimas = UserBuilder().set_name("Dimas").set_phone("08123456789").set_email("dimas@gmail.com").set_password("dimpram").build()
print(dimas.get_user())

dimas.add_account("Tabungan", "Tabungan BCA", "1234567890", dimas.id)
print(dimas.get_account())

