from cryptography.fernet import Fernet
from pathlib import Path

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