import random

def numberToIDR(number):
    return "Rp{:,}".format(number).replace(',', '.')


def generate_random_price():
    base_number = random.randint(25, 450)
    special_number = base_number * 1000
    return special_number