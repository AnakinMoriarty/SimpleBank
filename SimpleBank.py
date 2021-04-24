# SQLite3 and luhn algorithm

import random as rn
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

# cur.execute("""CREATE TABLE card (
            # id integer PRIMARY KEY AUTOINCREMENT,
            # number text,
            # pin text,
            # balance  INTEGER DEFAULT 0 
            # )""")

print("1. Create an account")
print("2. Log in to account")
print("0. Quit")

what_to_do = input()
cards_in_system = {}
checking = []


def creating_accout():
    start_number = 400000
    additional_number = rn.randint(999999999, 9999999999)
    PIN = rn.randint(999, 9999)
    if PIN in cards_in_system:
        PIN = rn.randint(999, 9999)
    card_number = str(start_number) + str(additional_number)
    if card_number in cards_in_system:
        additional_number = rn.randint(999999999, 9999999999)
        card_number = str(start_number) + str(additional_number)
    while True: ##Luhn Algorithm applied to creating card number
        card_number_list = list(str(card_number))
        first_list = card_number_list[0::2]
        second_list = card_number_list[1::2]
        first_list = [int(i) for i in first_list]
        second_list = [int(i) for i in second_list]
        first_list = list(map(lambda x: x * 2, first_list))
        new_list = []
        for element in first_list:
            if element > 9:
                operation_one = element - 10
                last_ope = operation_one + 1
                new_list.append(last_ope)
            elif element < 9:
                new_list.append(element)
        second_list = list(map(lambda x: x * 1, second_list))
        sum_of_lists = sum(new_list) + sum(second_list)
        if sum_of_lists % 10 == 0:
            break
        elif sum_of_lists % 10 != 0:
            start_number = 400000
            additional_number = rn.randint(999999999, 9999999999)
            card_number = str(start_number) + str(additional_number)
            if card_number in cards_in_system:
                additional_number = rn.randint(999999999, 9999999999)
                card_number = str(start_number) + str(additional_number)

    print("Your card has been created")
    print(f"Your card number:\n{int(card_number)}")
    print(f"Your card PIN:\n{PIN}")
    cards_in_system[card_number] = str(PIN)
    cur.execute("INSERT INTO card(number, pin, balance) VALUES(?,?,?)", (card_number, PIN, 0))
    conn.commit()



def loggin():
    print("Enter your card number:")
    login = str(input())
    print("Enter your PIN:")
    password = str(input())
    if login in cards_in_system:
        if cards_in_system[login] == password:
            print("You have successfully logged in!")
        else:
            print("Wrong card number or PIN!")
    else:
        print("Wrong card number or PIN!")


def posibilities():
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")
    choose = input()
    while True:
        if choose == "1":
            print("Balance: 0")
            choose = input()
        elif choose == "2":
            print("You have successfully logged out!")
            print("1. Create an account")
            print("2. Log in to account")
            print("0. Quit")
            what_to_do = input()
        elif choose == "0":
            break


while True:
    if what_to_do == "1":
        creating_accout()
        what_to_do = input()
    elif what_to_do == "2":
        loggin()
        what_to_do = input()
    elif what_to_do == "0":
        conn.close()
        print("Bye!")
        break
