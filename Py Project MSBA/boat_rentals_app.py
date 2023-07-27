from db_base import DBbase
from boat_rentals import admin_info, cust_info, boat_inventory,rental_price,reservation
import random

def display_menu():
    boat = """
                        __/___            
                  _____/______|           
          _______/_____\_______\_____     
          \              < < <       |    
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            """
    print(boat)
    print("~~~ WELCOME TO KKS BOAT RENTALS ~~~")
    print("1. I'm an Admin")
    print("2. I'm a Customer")
    print("3. Exit Application")

def display_menu_admin():
    print("Menu for admin updates:")
    print("1. Update Admin Name")
    print("2. Update Admin Passkey")
    print("3. Exit")

def display_menu_cust():
    print("Menu for customer updates:")
    print("1. Update Customer Name")
    print("2. Update Customer Phone")
    print("3. Update Customer Email")
    print("4. Update Customer Password")
    print("5. Exit")

def display_menu_boatinv():
    print("Menu for boat updates:")
    print("1. Update Boat Capacity")
    print("2. Update Manufacturer")
    print("3. Update Year Manufactured")
    print("4. Update Availability")
    print("5. Exit")


def display_menu_reservations():
    print("Menu for reservation updates:")
    print("1. Update Boat ID")
    print("2. Update Status")
    print("3. Exit")

def admin_login():
    admin_id = input("Enter Admin ID: ")
    admin_passkey = input("Enter Password: ")

    admin_data = admin_info.fetch_admin(admin_id)
    if admin_data and admin_data[2] == admin_passkey:
        print("Admin Login Successful!")
        admin_options(admin_id)
    else:
        print("Invalid Admin ID or Password.")


def admin_options(admin_id):
    while True:
        print("\n---- Admin Options ----")
        print("1. Add Boat")
        print("2. Update Boat")
        print("3. Delete Boat")
        print("4. View Boat Inventory")
        print("5. Add Rental Price")
        print("6. Update Rental Price")
        print("7. Delete Rental Price")
        print("8. View Rental Price")
        print("9. Update Reservations")
        print("10. Delete Reservations")
        print("11. View Reservations")
        print("12. Add new admin")
        print("13. Update existing admin")
        print("14. View existing admin")
        print("15. Remove admin")
        print("16. Add Customer")
        print("17. View Customer")
        print("18. Update Existing Customer")
        print("19. Remove Customer")
        print("20. Logout")

        choice = input("Enter your choice (1-20): ")

        if choice == "1":
            boat_capacity=int(input("Enter Capacity: "))
            manufacturer=input("Enter name of Manufacturer: ")
            year_manufactured=input("Enter year of Manufacture: ")
            is_available=input("Enter availability: ")
            boat_inventory.add_boat(boat_capacity,manufacturer,year_manufactured,is_available)

        elif choice == "2":
            while True:
                display_menu_boatinv()
                choice = input("Enter your choice (1-5): ")

                if choice == "1":
                    boat_id=int(input("Enter Boat ID: "))
                    boat_capacity= int(input("Enter Boat Capacity: "))
                    boat_inventory.update_boat(boat_id, boat_capacity=boat_capacity)

                elif choice == "2":
                    boat_id = int(input("Enter Boat ID: "))
                    manufacturer = input("Enter manufacturer: ")
                    boat_inventory.update_boat(boat_id, manufacturer=manufacturer)

                elif choice == "3":
                    boat_id = int(input("Enter Boat ID: "))
                    year_manufactured = int(input("Enter Year Manufactured: "))
                    boat_inventory.update_boat(boat_id, year_manufactured= year_manufactured)

                elif choice == "4":
                    boat_id = int(input("Enter Boat ID: "))
                    avail=input("Enter Availability: ")
                    boat_inventory.update_boat(boat_id, is_available=avail)
                elif choice == "5":
                    print("Exiting the application.")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "3":

            boat_id=int(input("Enter Boat ID: "))
            boat_inventory.delete_boat(boat_id)

        elif choice == "4":
            boat_id=input("Enter a Boat ID to view specific information or press enter to view all inventory")
            if boat_id is not None:
                boat_inventory.fetch_boat()
            else:
                boat_inventory.fetch_boat(boat_id)

        elif choice == "5":
            boat_id=int(input("Enter Boat ID: "))
            price= int(input("Enter Price of the Boat: "))
            rental_price.add_boat_rental(boat_id,price)

        elif choice == "6":
            boat_id = int(input("Enter Boat ID: "))
            price = int(input("Enter Price of the Boat: "))
            rental_price.update_boat_rental(boat_id, rental_price= price)

        elif choice == "7":
            boat_id = int(input("Enter Boat ID: "))
            rental_price.delete_boat_rental(boat_id)

        elif choice == "8":
            boat_id = input("Enter a Boat ID to view specific information or press enter to view all rental prices")
            if boat_id is not None:
                rental_price.fetch_boat_rental()
            else:
                rental_price.fetch_boat_rental(boat_id)

        elif choice == "9":
            while True:
                display_menu()
                choice = input("Enter your choice (1-3): ")

                if choice == "1":
                    reservation_id = int(input("Enter Reservation ID: "))
                    boat_id = int(input("Enter new Boat ID: "))
                    reservation.update_reservation(boat_id,reservation_id=reservation_id)

                elif choice == "2":
                    reservation_id = int(input("Enter Reservation ID: "))
                    status = input("Enter new Status: ")
                    reservation.update_reservation(reservation_id,status=status)

                elif choice == "3":
                    print("Exiting the application.")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "10":
            reservation_id=int(input("Enter Reservation ID: "))
            reservation.delete_reservation(reservation_id)

        elif choice == "11":
            reservation_id=input("Enter Reservation ID: ")
            if reservation_id is not None:
                print(reservation.fetch_boat_reserve())
            else:
                print(reservation.fetch_boat_reserve(reservation_id))

        elif choice == "12":
            admin_id=input("Enter Admin ID: ")
            admin_name=input("Enter Admin Name: ")
            admin_passkey=input("Enter Admin Passkey: ")
            admin_info.add_admin(admin_id,admin_name,admin_passkey)


        elif choice == "13":
            while True:
                display_menu_admin()
                choice = input("Enter your choice (1-3): ")

                if choice == "1":
                    admin_id=input("Enter Admin ID: ")
                    admin_name= input("Enter Admin Name to Update: ")
                    admin_info.update_admin(admin_id,admin_name=admin_name)

                elif choice == "2":
                    admin_id = input("Enter Admin ID: ")
                    admin_passkey = input("Enter Admin Passkey to Update: ")
                    admin_info.update_admin(admin_id, admin_passkey=admin_passkey)

                elif choice == "3":
                    print("Exiting the application.")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "14":
            admin_id=input("Enter Admin ID: ")
            print(admin_info.fetch_admin(admin_id))

        elif choice == "15":
            admin_id = input("Enter Admin ID: ")
            print(admin_info.delete_admin(admin_id))

        elif choice == "16":
            cust_name=input("Enter Name of the Customer: ")
            cust_phone=int(input("Enter Phone Number: "))
            cust_email=input("Enter Email Address: ")
            cust_pass= input("Enter Password:")
            cust_info.add_cust(cust_name,cust_phone,cust_email,cust_pass)

        elif choice == "17":
            cust_id=input("Enter Customer ID or hit enter to view all customer records: ")
            if cust_id is not None:
                cust_info.fetch_cust_adm()
            else:
                cust_info.fetch_cust_adm(cust_id)


        elif choice == "18":
            while True:
                display_menu_cust()
                choice = input("Enter your choice (1-4): ")

                if choice == "1":
                    cust_id=input("Enter Customer ID: ")
                    cust_name=input("Enter Customer Name")
                    cust_info.update_cust(cust_id,cust_name=cust_name)

                elif choice == "2":
                    cust_id = input("Enter Customer ID: ")
                    cust_phone = int(input("Enter Customer Phone"))
                    cust_info.update_cust(cust_id, cust_phone=cust_phone)

                elif choice == "3":
                    cust_id = input("Enter Customer ID: ")
                    cust_email = input("Enter Customer Email")
                    cust_info.update_cust(cust_id, email=cust_email)

                elif choice == "4":
                    cust_id= input("Enter Customer ID:")
                    cust_pass=input("Enter Customer Password to Update:")
                    cust_info.update_cust(cust_id,password=cust_pass)

                elif choice == "5":
                    print("Exiting the application.")
                    break
                else:
                    print("Invalid choice. Please try again.")


        elif choice == "19":
            cust_id=input("Enter Customer ID: ")
            cust_info.delete_cust(cust_id)

        elif choice == "20":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")



def cust_options():
    while True:
        print("\n---- Customer Options ----")
        print("1. New Customer")
        print("2. Existing Customer")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            cust_name = input("Enter Your Name: ")
            cust_phone = input("Enter Your 10 Digit Phone Number: ")
            cust_email = input("Enter Your Email ID: ")
            cust_pass = input("Enter your password: ")
            cust_info.add_cust(cust_name, cust_phone, cust_email, cust_pass)

        elif choice == "2":
            cust_id = input("Enter Customer ID: ")
            cust_pass = input("Enter Password: ")

            cust_data = cust_info.fetch_cust(cust_id)
            if cust_data and cust_data[4] == cust_pass:
                print("Login Successful")
                ext_cust_options(cust_id)
            else:
                print("Invalid Customer ID or Password.")

        elif choice == "3":
            print("Exiting Customer Options...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-3).")



def ext_cust_options(cust_id):
    while True:
        print("\n---- Welcome!!! ----")
        print("1. View Boat Inventory")
        print("2. Book a Boat")
        print("3. View My Reservations")
        print("4. View My Account")
        print("5. Exit")

        choice = input("Enter your choice (1-4): ")

        try:
            choice = int(choice)
            if choice == 1:
                boat_id= input("Enter Boat ID to view specific boat details or press enter to view all: ")

                if boat_id is not None:
                    rental_price.fetch_boat_rental()
                else:
                    rental_price.fetch_boat_rental(boat_id)

            elif choice == 2:
                cust_info.book_a_boat(cust_id)
            elif choice == 3:
                cust_info.view_customer_data_with_reservations(cust_id)

            elif choice == 4:
                 cust_info.fetch_cust_cust(cust_id)
            elif choice == 5:
                print("Thank you, Visit Again!!")
                break
            else:
                print("Invalid choice. Please enter a valid option (1-4).")
        except ValueError:
            print("Invalid choice. Please enter a valid option (1-4).")



def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            admin_login()
        elif choice == "2":
            cust_options()
        elif choice == "3":
            print("Thanks for Using KKS BOAT RENTALS. We hope you visit again!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

