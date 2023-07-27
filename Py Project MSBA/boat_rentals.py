import db_base as db
import sqlite3
import csv
import random

'''
Administrator class contains the details of admin who has access to the entire application, This class also contains
CRUD operations to add, update, delete and fetch admin records for all the tables in this application.
'''

class AdministratorInfo(db.DBbase):
    def __init__(self, row=None):
        if row:
            self.admin_id = row[0]
            self.admin_name = row[1]
            self.admin_passkey = row[2]

        super(AdministratorInfo, self).__init__("Boat-Rentals.sqlite")

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS admin_info;
                CREATE TABLE admin_info(
                admin_id varchar(30) NOT NULL PRIMARY KEY,
                admin_name varchar(30),
                admin_passkey varchar(30)
                )
            """
            super().execute_script(sql)
            print("Admin Table created successfully!")
        except Exception as e:
            print("An error occurred", e)
        finally:
            super().close_db()


    def add_admin_data_from_csv(self, csv_file_path):
        try:
            with open(csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:

                    admin_id, admin_name, admin_passkey = row
                    self.admin_id = admin_id
                    self.admin_name = admin_name
                    self.admin_passkey = admin_passkey


                    super().get_cursor.execute(
                        """INSERT INTO admin_info (admin_id, admin_name, admin_passkey) VALUES (?, ?, ?)""",
                        (self.admin_id, self.admin_name, self.admin_passkey)
                    )


            super().get_connection.commit()
            print("Data from CSV file added to the Admin Table successfully!")
        except Exception as e:
            print("An error occurred", e)

#ADDING ADMIN
    def add_admin(self, admin_id= None, admin_name=None,admin_passkey=None):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT INTO admin_info (admin_id, admin_name,admin_passkey) values (?,?,?);
                """,
                (admin_id, admin_name,admin_passkey)
            )
            super().get_connection.commit()
            print(f"Added {admin_name} successfully")
        except Exception as e:
            print("An error has occurred",e)

#UPDATING ADMIN
    def update_admin(self,admin_id, admin_name=None,admin_passkey=None):
        try:
            super().connect()
            if admin_name is not None and admin_name != "":
                super().get_cursor.execute(
                    """UPDATE admin_info SET admin_name = ? WHERE admin_id = ?;
                    """,
                    (admin_name, admin_id,)
                )
            if admin_passkey is not None and admin_passkey != "":
                super().get_cursor.execute(
                    """UPDATE admin_info SET admin_passkey = ? WHERE admin_id = ?;
                    """,
                    (admin_passkey,admin_id,)
                )

            super().get_connection.commit()
            print(f"Updated admin with id {admin_id} successfully")
        except Exception as e:
            print("An error occurred while updating the admin information",e)
        finally:
            super().close_db()

#DELETING ADMIN

    def delete_admin(self,admin_id):
        try:
            super().connect()
            super().get_cursor.execute(
                """DELETE FROM admin_info WHERE admin_id=?;
                """,
                (admin_id,)
            )
            super().get_connection.commit()
            print(f"Admin with id {admin_id} deleted successfully!")
        except Exception as e:
            print("Error occured while deleting the customer",e)
        finally:
            super().close_db()

#FETCHING ADMIN

    def fetch_admin(self,admin_id=None):
        try:
            super().connect()
            if admin_id is not None:
                return super().get_cursor.execute(
                    """SELECT * FROM admin_info WHERE admin_id=?
                """,
                    (admin_id,)).fetchone()
            else:
                return super().get_cursor.execute(
                    """SELECT * FROM admin_info
                    """
                    ).fetchall()
        except Exception as e:
            print("An error has occurred",e)
        finally:
            super().close_db()



class CustomerInfo(db.DBbase):
    def __init__(self):
        super(CustomerInfo,self).__init__("Boat-Rentals.sqlite")

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS cust_info;
                CREATE TABLE cust_info(
                cust_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                cust_name varchar(30),
                cust_phone INTEGER NOT NULL,
                email varchar(30),
                password varchar(30) NOT NULL
                
                )
            """
            super().execute_script(sql)
            print("Customer Table created successfully!")
        except Exception as e:
            print("An error occured", e)
        finally:
            super().close_db()

    def add_customer_data_from_csv(self, csv_file_path):
        try:
            with open(csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    cust_id, cust_name, cust_phone, email, password = row[0].split(";")
                    super().get_cursor.execute(
                        """INSERT INTO cust_info (cust_id, cust_name, cust_phone, email, password) VALUES (?, ?, ?, ?, ?)""",
                        (cust_id, cust_name, cust_phone, email, password)
                    )
            super().get_connection.commit()
            print("Data from CSV file added to the Customer Table successfully!")
        except Exception as e:
            print("An error occurred", e)

#BOOKING A BOAT
    def book_a_boat(self, cust_id):
        try:
            super().connect()


            query = """
                SELECT b.boat_id, b.boat_capacity, b.manufacturer, b.year_manufactured, p.rental_price
                FROM boat_inventory b
                INNER JOIN rental_price p ON b.boat_id = p.boat_id
                WHERE b.is_available='Yes'
            """
            available_boats_with_price = super().get_cursor.execute(query).fetchall()

            if not available_boats_with_price:
                print("No boats are currently available for booking.")
                return

            print("\n---- Available Boats ----")
            print("{:<10} {:<15} {:<15} {:<18} {:<12}".format("Boat ID", "Boat Capacity", "Manufacturer",
                                                              "Year Manufactured", "Boat Price"))
            for boat in available_boats_with_price:
                print("{:<10} {:<15} {:<15} {:<18} {:<12}".format(boat[0], boat[1], boat[2], boat[3], boat[4]))

            boat_id = int(input("Enter the Boat ID you want to book: "))

            if boat_id not in [boat[0] for boat in available_boats_with_price]:
                print("Invalid Boat ID. Please select from the available boats.")
                return

            confirmation = input("Do you want to book this boat? (Y/N): ").upper()

            if confirmation == "Y":
                reservation_id = random.randint(1000, 9999)
                reservation.add_res_info(reservation_id, boat_id, cust_id, status="Booked")
                print(f"Boat with ID {boat_id} has been successfully booked.")
                print(f"Your Reservation ID is: {reservation_id}. Make of note of it for future use!")

                update_query = f"UPDATE boat_inventory SET is_available='No' WHERE boat_id={boat_id}"
                super().execute_script(update_query)
                super().get_connection.commit()
            else:
                print("Booking canceled.")
        except Exception as e:
            print("An error occurred while booking the boat.", e)
        finally:
            super().close_db()

#VIEWING RESERVATIONS OF CUSTOMER

    def view_customer_data_with_reservations(self, cust_id):
        try:
            super().connect()


            query = """
                SELECT c.cust_id, c.cust_name, c.cust_phone, c.email, r.reservation_id, r.boat_id, r.status, p.rental_price
                FROM cust_info c
                INNER JOIN reservations r ON c.cust_id = r.cust_id
                INNER JOIN rental_price p ON r.boat_id = p.boat_id
                WHERE c.cust_id=?
            """
            customer_data = super().get_cursor.execute(query, (cust_id,)).fetchall()

            if not customer_data:
                print("You have not reserved any boat!")
                return

            print("\n----Your Reservations ----")
            print("Customer ID\tCustomer Name\tCustomer Phone\tEmail\tReservation ID\tBoat ID\tStatus\tBoat Price")
            for data in customer_data:
                print(f"{data[0]}\t\t{data[1]}\t\t{data[2]}\t\t{data[3]}\t{data[4]}\t\t{data[5]}\t{data[6]}\t{data[7]}")

        except Exception as e:
            print("An error occurred while fetching customer data.", e)
        finally:
            super().close_db()

#ADDING CUSTOMER
    def add_cust(self, cust_name=None, cust_phone=None,email=None,password=None):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT INTO cust_info (cust_name,cust_phone,email,password) values (?,?,?,?);
                """,
                (cust_name,cust_phone,email,password)
            )
            super().get_connection.commit()
            cust_id = super().get_cursor.lastrowid

            print(f"Added {cust_name} successfully, your customer ID is {cust_id}")
        except Exception as e:
            print("An error has occurred",e)

#UPDATING CUSTOMER
    def update_cust(self,cust_id, cust_name=None,cust_phone=None,email=None,password=None):
        try:
            super().connect()
            if cust_name is not None and cust_name != "":
                super().get_cursor.execute(
                    """UPDATE cust_info SET cust_name = ? WHERE cust_id = ?;
                    """,
                    (cust_name, cust_id,)
                )
            if cust_phone is not None and cust_phone != "":
                super().get_cursor.execute(
                    """UPDATE cust_info SET cust_phone = ? WHERE cust_id = ?;
                    """,
                    (cust_phone, cust_id,)
                )
            if email is not None and email != "":
                super().get_cursor.execute(
                    """UPDATE cust_info SET email = ? WHERE cust_id = ?;
                    """,
                    (email, cust_id,)
                )
            if password is not None and password != "":
                super().get_cursor.execute(
                    """UPDATE cust_info SET password = ? WHERE password = ?;
                    """,
                    (password, cust_id,)
                )
            super().get_connection.commit()
            print(f"Updated customer{cust_id} successfully")
        except Exception as e:
            print("An error occurred while updating the customer information",e)
        finally:
            super().close_db()

#DELETING CUSTOMER

    def delete_cust(self,cust_id):
        try:
            super().connect()
            super().get_cursor.execute(
                """DELETE FROM cust_info WHERE cust_id=?;
                """,
                (cust_id,)
            )
            super().get_connection.commit()
            print(f"Customer with id {cust_id} deleted successfully!")
        except Exception as e:
            print("Error occurred while deleting the customer",e)
        finally:
            super().close_db()

#FETCHING CUSTOMER

    def fetch_cust(self,cust_id=None):
        try:
            super().connect()
            if cust_id is not None:
                return super().get_cursor.execute(
                    """SELECT * FROM cust_info WHERE cust_id=?
                """,
                    (cust_id,)).fetchone()
            else:
                return super().get_cursor.execute(
                    """SELECT * FROM cust_info
                    """
                    ).fetchall()
        except Exception as e:
            print("An error has occurred",e)
        finally:
            super().close_db()

#FETCHING CUSTOMER FOR ADMIN
    def fetch_cust_adm(self, cust_id=None):
        try:
            super().connect()
            cursor = super().get_cursor

            if cust_id is not None:
                cursor.execute(
                    """SELECT * FROM cust_info WHERE cust_id=?
                    """,
                    (cust_id,)
                )
                data = cursor.fetchone()
                if not data:
                    print("No data found for the specified customer ID.")
                    return
                else:
                    print("\n---- Customer Details ----")
                    print("{:<10} {:<20} {:<15} {:<30}".format("Customer ID", "Name", "Phone", "Email","Password"))
                    print("{:<10} {:<20} {:<15} {:<30}".format(data[0], data[1], data[2], data[3], data[4]))
            else:
                cursor.execute(
                    """SELECT * FROM cust_info
                    """
                )
                data = cursor.fetchall()
                if not data:
                    print("No customer data found.")
                    return
                else:
                    print("\n---- All Customers ----")
                    print("{:<10} {:<20} {:<15} {:<30} {:<40}".format("Customer ID", "Name", "Phone", "Email","Password"))
                    for row in data:
                        print("{:<10} {:<20} {:<15} {:<30} {:<40} ".format(row[0], row[1], row[2], row[3], row[4]))

        except Exception as e:
            print("An error has occurred", e)
        finally:
            super().close_db()

#FETCHING CUSTOMER FOR CUSTOMER
    def fetch_cust_cust(self, cust_id=None):
        try:
            super().connect()
            cursor = super().get_cursor

            if cust_id is not None:
                cursor.execute(
                    """SELECT * FROM cust_info WHERE cust_id=?
                    """,
                    (cust_id,)
                )
                data = cursor.fetchone()
                if not data:
                    print("No data found for the specified customer ID.")
                    return
                else:
                    print("\n---- YOUR ACCOUNT DETAILS ----")
                    print("{:<10} {:<20} {:<15} {:<30} {:<40}".format("Customer ID", "Name", "Phone", "Email","Password"))
                    print("{:<10} {:<20} {:<15} {:<30} {:<40}".format(data[0], data[1], data[2], data[3], data[4]))
        except Exception as e:
            print("An error has occurred", e)
        finally:
            super().close_db()


class BoatInventory(db.DBbase):
    def __init__(self):
        super(BoatInventory, self).__init__("Boat-Rentals.sqlite")

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS boat_inventory;
                CREATE TABLE boat_inventory(
                    boat_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                    boat_capacity varchar(30),
                    manufacturer varchar(30),
                    year_manufactured INTEGER NOT NULL,
                    is_available varchar(10)
                )
            """
            super().execute_script(sql)
            print("BoatInventory Table created successfully!")
        except Exception as e:
            print("An error occurred", e)
        finally:
            super().close_db()

    def generate_boat_id(self):

        return random.randint(10000, 99999)

    def add_boat(self, boat_capacity, manufacturer, year_manufactured,is_available):
        try:
            boat_id = self.generate_boat_id()

            super().get_cursor.execute(
                """INSERT INTO boat_inventory (boat_id, boat_capacity, manufacturer, year_manufactured, is_available)
                   VALUES (?, ?, ?, ?,?)""",
                (boat_id, boat_capacity, manufacturer, year_manufactured)
            )
            super().get_connection.commit()
            print("Added boat successfully")
        except Exception as e:
            print("An error has occurred", e)


    def add_boatinv_data_from_csv(self, csv_file_path):
        try:
            with open(csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:
                    boat_id, boat_capacity,manufacturer, year_manufactured, is_available = row[0].split(";")
                    super().get_cursor.execute(
                        """INSERT INTO boat_inventory (boat_id, boat_capacity,manufacturer, year_manufactured, is_available) VALUES (?, ?, ?, ?,?)""",
                        (boat_id, boat_capacity,manufacturer, year_manufactured, is_available)
                    )
            super().get_connection.commit()
            print("Data from CSV file added to the boat inventory Table successfully!")
        except Exception as e:
            print("An error occurred", e)


#ADDING BOAT INFO
    def add_boat(self, boat_capacity, manufacturer, year_manufactured, is_available):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT INTO boat_inventory (boat_capacity, manufacturer, year_manufactured, is_available) values (?,?,?,?);
                """,
                (boat_capacity,manufacturer,year_manufactured, is_available)
            )
            super().get_connection.commit()
            print(f"Added boat successfully")
        except Exception as e:
            print("An error has occurred",e)

#UPDATING BOAT INFO
    def update_boat(self,boat_id, boat_capacity=None, manufacturer=None, year_manufactured=None, is_available=None ):
        try:
            super().connect()
            if boat_capacity is not None and boat_capacity != "":
                super().get_cursor.execute(
                    """UPDATE boat_inventory SET boat_capacity = ? WHERE boat_id = ?;
                    """,
                    (boat_capacity, boat_id,)
                )
            if manufacturer is not None and manufacturer != "":
                super().get_cursor.execute(
                    """UPDATE boat_inventory SET manufacturer = ? WHERE boat_id = ?;
                    """,
                    (manufacturer, boat_id,)
                )
            if year_manufactured is not None and year_manufactured != "":
                super().get_cursor.execute(
                    """UPDATE boat_inventory SET year_manufactured = ? WHERE boat_id = ?;
                    """,
                    (year_manufactured, boat_id,)
                )
            if is_available is not None and is_available!= "":
                super().get_cursor.execute(
                    """UPDATE boat_inventory SET is_available = ? WHERE boat_id = ?;
                    """,
                    (is_available, boat_id,)
                )
            super().get_connection.commit()
            print(f"Updated boat with ID {boat_id} successfully")
        except Exception as e:
            print("An error occurred while updating the boat information",e)
        finally:
            super().close_db()

#DELETING BOAT INFO

    def delete_boat(self,boat_id):
        try:
            super().connect()
            super().get_cursor.execute(
                """DELETE FROM boat_inventory WHERE boat_id=?;
                """,
                (boat_id,)
            )
            super().get_connection.commit()
            print(f"Boat with id {boat_id} deleted successfully!")
        except Exception as e:
            print("Error occured while deleting the boat information",e)
        finally:
            super().close_db()

#FETCHING BOAT INFO

    def fetch_boat(self, is_available=None, boat_id=None):
        try:
            super().connect()
            cursor = super().get_cursor

            if is_available is not None:
                cursor.execute(
                    """SELECT * FROM boat_inventory WHERE is_available=?""",
                    (is_available,)
                )
            elif boat_id is not None:
                cursor.execute(
                    """SELECT * FROM boat_inventory WHERE boat_id=?""",
                    (boat_id,)
                )
            else:
                cursor.execute(
                    """SELECT * FROM boat_inventory"""
                )

            data = cursor.fetchall()

            if not data:
                print("No data found.")
                return

            print("\n---- Boat Inventory ----")
            print(
                "{:<10} {:<15} {:<15} {:<20} {:<15}".format("Boat ID", "Capacity", "Manufacturer", "Year Manufactured",
                                                            "Availability"))
            for boat in data:
                print("{:<10} {:<15} {:<15} {:<20} {:<15}".format(boat[0], boat[1], boat[2], boat[3], boat[4]))

        except Exception as e:
            print("An error has occurred", e)
        finally:
            super().close_db()


class RentalPrice(db.DBbase):
    def __init__(self):
        super(RentalPrice, self).__init__("Boat-Rentals.sqlite")

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS rental_price;
                CREATE TABLE rental_price(
                boat_id INTEGER NOT NULL,
                rental_price INTEGER NOT NULL,
                FOREIGN KEY (boat_id) REFERENCES boat_inventory(boat_id)

                )
            """
            super().execute_script(sql)
            print("RentalPrice Table created successfully!")
        except Exception as e:
            print("An error occurred", e)
        finally:
            super().close_db()

    def add_boatren_data_from_csv(self, csv_file_path):
        try:
            with open(csv_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for row in csv_reader:

                    boat_id, rental_price = row[0].split(";")
                    super().get_cursor.execute(
                        """INSERT INTO rental_price (boat_id, rental_price) VALUES (?, ?)""",
                        (boat_id, rental_price)
                    )
            super().get_connection.commit()
            print("Data from CSV file added to the rental price Table successfully!")
        except Exception as e:
            print("An error occurred", e)


#ADDING RENTAL INFO
    def add_boat_rental(self, boat_id, rental_price):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT INTO rental_price (boat_id,rental_price) values (?,?);
                """,
                (boat_id, rental_price)
            )
            super().get_connection.commit()
            print(f"Added rental price successfully")
        except Exception as e:
            print("An error has occurred",e)

#UPDATING BOAT RENTAL INFO
    def update_boat_rental(self, boat_id, rental_price=None):
        try:
            super().connect()
            if rental_price is not None and rental_price != "":
                super().get_cursor.execute(
                    """UPDATE rental_price SET rental_price = ? WHERE boat_id = ?;
                    """,
                    (rental_price, boat_id,)
                )
            super().get_connection.commit()
            print(f"Updated rental price for boat {boat_id} successfully")
        except Exception as e:
            print("An error occurred while updating the boat rental information",e)
        finally:
            super().close_db()

#DELETING BOAT RENTAL INFO

    def delete_boat_rental(self,boat_id):
        try:
            super().connect()
            super().get_cursor.execute(
                """DELETE FROM rental_price WHERE boat_id=?;
                """,
                (boat_id,)
            )
            super().get_connection.commit()
            print(f"Boat with id {boat_id} deleted successfully!")
        except Exception as e:
            print("Error occured while deleting the boat information",e)
        finally:
            super().close_db()

#FETCHING BOAT RENTAL INFO

    def fetch_boat_rental(self, boat_id=None):
        try:
            super().connect()
            cursor = super().get_cursor

            if boat_id is not None:
                cursor.execute(
                    """SELECT boat_inventory.boat_id, boat_capacity, manufacturer, year_manufactured, rental_price
                    FROM boat_inventory
                    INNER JOIN rental_price ON boat_inventory.boat_id = rental_price.boat_id
                    WHERE boat_inventory.boat_id=?
                    """,
                    (boat_id,)
                )
                data = cursor.fetchone()
                if not data:
                    print("No data found for the specified boat ID.")
                    return
            else:
                cursor.execute(
                    """SELECT boat_inventory.boat_id, boat_capacity, manufacturer, year_manufactured, rental_price, is_available
                    FROM boat_inventory
                    INNER JOIN rental_price ON boat_inventory.boat_id = rental_price.boat_id
                    """
                )
                data = cursor.fetchall()
                if not data:
                    print("No rental price data found.")
                    return

            print("\n---- Boat Rental Prices ----")
            print(
                "{:<10} {:<15} {:<15} {:<20} {:<15} {:<20}".format("Boat ID", "Capacity", "Manufacturer", "Year Manufactured",
                                                            "Rental Price","Availability"))
            for row in data:
                print("{:<10} {:<15} {:<15} {:<20} {:<15} {:<20}".format(row[0], row[1], row[2], row[3], row[4],row[5]))

        except Exception as e:
            print("An error has occurred", e)
        finally:
            super().close_db()


class Reservations(db.DBbase):
    def __init__(self):
        super(Reservations, self).__init__("Boat-Rentals.sqlite")

    def reset_database(self):
        try:
            sql = """
                DROP TABLE IF EXISTS reservations;
                CREATE TABLE reservations(
                reservation_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                boat_id INTEGER NOT NULL ,
                cust_id INTEGER NOT NULL ,
                status varchar(10),
                FOREIGN KEY (boat_id) REFERENCES boat_inventory(boat_id),
                FOREIGN KEY (cust_id) REFERENCES cust_info(cust_id)
                )
            """
            super().execute_script(sql)
            print("Reservations Table created successfully!")
        except Exception as e:
            print("An error occurred", e)
        finally:
            super().close_db()


#ADDING RESERVATION INFO
    def add_res_info(self, reservation_id,boat_id, cust_id,status):
        try:
            super().connect()
            super().get_cursor.execute(
                """INSERT INTO reservations (reservation_id,boat_id,cust_id,status) values (?,?,?,?);
                """,
                (reservation_id,boat_id,cust_id,status)
            )
            super().get_connection.commit()
            print(f"Added reservation price successfully")
        except Exception as e:
            print("An error has occurred",e)

#UPDATING RESERVATION INFO
    def update_reservation(self, reservation_id=None,boat_id=None, cust_id=None,status=None):
        try:
            super().connect()
            if boat_id is not None and boat_id != "":
                super().get_cursor.execute(
                    """UPDATE reservations SET boat_id = ? WHERE reservation_id = ?;
                    """,
                    (boat_id, reservation_id,)
                )
            if status is not None and status != "":
                super().get_cursor.execute(
                    """UPDATE reservations SET status = ? WHERE reservation_id = ?;
                    """,
                    (status,reservation_id,)
                )

            super().get_connection.commit()
            print(f"Updated reservations for boat {reservation_id} successfully")
        except Exception as e:
            print("An error occurred while updating the reservation information",e)
        finally:
            super().close_db()

#DELETING RESERVATION INFO

    def delete_reservation(self,reservation_id):
        try:
            super().connect()
            super().get_cursor.execute(
                """DELETE FROM reservations WHERE reservation_id=?;
                """,
                (reservation_id,)
            )
            super().get_connection.commit()
            print(f"Reservation with id {reservation_id} deleted successfully!")
        except Exception as e:
            print("Error occured while deleting the reservation information",e)
        finally:
            super().close_db()

#FETCHING RESERVATIONS INFO

    def fetch_boat_reserve(self,reservation_id=None):
        try:
            super().connect()
            if reservation_id is not None:
                return super().get_cursor.execute(
                    """SELECT * FROM reservations WHERE reservation_id=?
                """,
                    (reservation_id,)).fetchone()
            else:
                return super().get_cursor.execute(
                    """SELECT * FROM reservations
                    """
                    ).fetchall()
        except Exception as e:
            print("An error has occurred",e)
        finally:
            super().close_db()




#First Uncomment reset database for all tables ; This will create empty tables
#Run
#Second Uncomment "csv" for all tables ; This will load csv data into the empty tables
#Run



#Create admin_info table
admin_info= AdministratorInfo()
# admin_info.add_admin_data_from_csv("admin_data.csv")
#admin_info.reset_database()

# Create cust_info table
cust_info=CustomerInfo()
#cust_info.add_customer_data_from_csv("customer_data.csv")
#cust_info.reset_database()

# Create boatinventory table
boat_inventory= BoatInventory()
# boat_inventory.add_boatinv_data_from_csv("boat_data.csv")
#boat_inventory.reset_database()


# Create rentalprice table
rental_price= RentalPrice()
# rental_price.add_boatren_data_from_csv("rental_data.csv")
#rental_price.reset_database()

# Create reservations table
reservation= Reservations()
#reservation.reset_database()



