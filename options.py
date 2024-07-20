def menu():
    print("Welcome to Password Manager.")
    print("1. Access passwords.")
    print("2. Add new password.")
    print("3. Delete a password.")
    print("4. Change a password.")
    print("0. Exit.")

    selection = input("Select an option.")

    if selection == 0:
        pass
    elif selection == 1:
        password_log()
    elif selection == 2:
        add_password()
    elif selection == 3:
        delete_password()
    elif selection == 4:
        change_password()

def password_log():
    pass


def add_password():
    pass


def delete_password():
    pass


def change_password():
    pass