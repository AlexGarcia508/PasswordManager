import hashlib
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from argon2.low_level import hash_secret_raw, Type
import base64
import secrets

class PasswordManager:
    def __init__(self):
        password = {"discord": "purple", "google": "blue"}
        self.password_dict = {}
        self.username_file = "username.txt"
        self.password_file = "passwordlog.txt"
        self.salt_file = "salt.txt"

        self.salt = self.handle_salt(self.salt_file)
        # Handle username storage and verification
        if self.handle_username():
            pass
        if self.authenticate_user(password):
            pass
    def handle_username(self):
        username_path = Path(self.username_file)

        while True:
            # Hash the username
            username = input("Username: ")
            username_hash = hashlib.sha256(username.encode()).hexdigest()

            # If the username file exists then load username from it
            if username_path.is_file():
                with username_path.open('r') as f:
                    stored_username_hash = f.read().strip()

                # Verify the hashed username
                if stored_username_hash != username_hash:
                    print("Username does not match. Try again.")
                else:
                    return True
            else:
                # If the username file does not exist, accept username and save to file
                with username_path.open('w') as f:
                    f.write(username_hash)
                    return True

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

    def authenticate_user(self, password):
        while True:
            master_password = input("Password: ")
            self.key = self.derive_key(master_password, self.salt)
            try:
                self.handle_password_file(self.password_file, password)
                print("Login successful!")
                return  # Exit the loop on successful login
            except InvalidToken:
                print("Incorrect password. Please try again.")

    def derive_key(self, password, salt):
        # Derive a key using Argon2 with customizable parameters
        hashed = hash_secret_raw(
            password.encode(),  # The password to hash
            salt,  # The salt to use
            time_cost=2,  # The time cost parameter (default 2)
            memory_cost=65536,  # The memory cost parameter (default 65536 bytes)
            parallelism=2,  # The parallelism parameter (default 2)
            hash_len=32,  # The length of the derived key (default 32 bytes)
            type=Type.ID  # The Argon2 type (ID variant)
        )
        key = base64.urlsafe_b64encode(hashed)  # Encode the key in a URL-safe base64 format
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
            self.save_password_file()

    def change_password(self, site, new_password):
        # new password added to dictionary
        self.password_dict[site] = new_password

        # rewrite all passwords with new encryptions including new password to file
        self.save_password_file()

    def delete_password(self, site):
        if site in self.password_dict:
            del self.password_dict[site]
            self.save_password_file()

    def validate_site(self):
        site = None
        invalid = True

        while invalid:
            site = input("Enter site: ")
            # Check for ":" in the site
            if ":" in site:
                print("Site cannot contain the ':' character. Please try again.")
            else:
                invalid = False

        return site

    def save_password_file(self):
        with open(self.password_file, 'w') as f:
            for site, password in self.password_dict.items():
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")