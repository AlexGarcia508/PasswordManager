from cryptography.fernet import Fernet
from pathlib import Path
def main():
    pm = PasswordManager()

    print("""
Welcome to Password Manager.
1. Access a password.
2. Add a new password.
3. Change a password.
4. Delete a password.
0. Exit
    """)

    running = True

    while running:
        choice = input("Enter choice: ")

        if choice == "1":
            site = input("What site's password do you want?: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "2":
            site = input("Enter new site: ")
            password = input("Enter password: ")
            pm.add_password(site, password)
        elif choice == "3":
            site = input("Enter site's password to change: ")
            password = input("Enter new password: ")
            pm.change_password(site, password)
        elif choice == "4":
            site = input("Enter site's password to delete: ")
            pm.delete_password(site)
        elif choice == "0":
            running = False
            print("Closing...")
        else:
            print("Invalid choice.")

class PasswordManager:
    def __init__(self):
        password = {"discord", "something"}
        self.password_dict = {}
        self.key_file = "masterkey.txt"
        self.key = self.load_or_create_key_file(self.key_file)
        self.password_file = "passwordlog.txt"
        self.load_or_create_password_file(self.password_file, password)

    def load_or_create_key_file(self, key_file):
        key_path = Path(key_file) # Convert string to Path object

        # If the key file exists, read the key from the file
        if key_path.is_file():
            with key_path.open('rb') as f:
                key = f.read()
        else:
            # If the key file does not exist, create a new key and save it to the file
            key = Fernet.generate_key()
            with key_path.open('wb') as f:
                f.write(key)

        return key

    def load_or_create_password_file(self, password_file, initial_values):
        password_path = Path(password_file)  # Convert string to Path object

        # If the password file exists then load it
        if password_path.is_file():
            with password_path.open('r') as f:
                for line in f:
                    site, encrypted = line.split(":")
                    self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
                    print(self.password_dict)
        else:
            # If the password file does not exist, create new password file
            if initial_values is not None:
                for key, value in initial_values.items():
                    self.add_password(key, value)

    def get_password(self, site):
        print(self.password_dict)
        return self.password_dict[site]

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def change_password(self, site, new_password):
        self.password_dict[site] = new_password

        # rewrite all passwords with new encryptions including new password to file
        with open(self.password_file, 'w') as f:
            for site, password in self.password_dict.items():
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def delete_password(self, site):
        if site in self.password_dict:
            del self.password_dict[site]
            self.save_password_file()

    def save_password_file(self):
        with open(self.password_file, 'w') as f:
            for site, password in self.password_dict.items():
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

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