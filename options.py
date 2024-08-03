from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
import secrets

class PasswordManager:
    def __init__(self, master_password):
        password = {"discord": "purple", "google": "blue"}
        self.password_dict = {}
        self.salt_file = "salt.txt"
        self.password_file = "passwordlog.txt"

        self.salt = self.handle_salt(self.salt_file)

        self.key = self.derive_key(master_password, self.salt)

        self.handle_password_file(self.password_file, password)

    def handle_salt(self, salt_file):
        salt_path = Path(salt_file)

        # If the salt file exists then load salt from it
        if salt_path.is_file():
            with salt_path.open('rb') as f:
                salt = f.read()
        else:
            # If the salt file does not exist, create new salt and save to file
            salt = secrets.token_bytes(16)
            with salt_path.open('wb') as f:
                f.write(salt)
        return salt

    def derive_key(self, password, salt):
        # Derive key from password and salt using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def handle_password_file(self, password_file, initial_values):
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