from cryptography.fernet import Fernet
def main():
    password = {
        "discord": "blue",
        "google": "red"
    }

    pm = PasswordManager()

    print("""Welcome to Password Manager.
    1. Create new key
    2. Load key
    3. Create new password file
    4. Load password file
    5. Add new password
    6. Get password
    7. Exit
    """)

    done = False

    while not done:
        choice = input("Enter choice: ")
        if choice == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, password)
        elif choice == "4":
            path = input("Enter path: ")
            pm.load_password_file(path)
        elif choice == "5":
            site = input("Enter site: ")
            password = input("Enter password: ")
            pm.add_password(site, password)
        elif choice == "6":
            site = input("What site do you want?: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "7":
            done = True
            print("Bye")
        else:
            print("Invalid choice.")

class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        print(self.key)
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]

    def delete_password(self):
        pass

    def change_password(self):
        pass

if __name__ == "__main__":
    main()

'''
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
'''