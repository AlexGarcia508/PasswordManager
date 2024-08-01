from options import *

def menu():
    print("""
Welcome to Password Manager.
1. Access a password.
2. Add a new password.
3. Change a password.
4. Delete a password.
0. Exit
        """)
def main():
    pm = PasswordManager()

    running = True

    while running:
        menu()
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

if __name__ == "__main__":
    main()