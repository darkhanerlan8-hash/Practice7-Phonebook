
import csv
from connect import connect

conn = connect()

def create_table():
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(30) UNIQUE NOT NULL
                )
            """)

def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")

    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (name, phone)
            )
    print("Contact added!")

def import_csv():
    with open("contacts.csv", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        with conn:
            with conn.cursor() as cur:
                for row in reader:
                    cur.execute("""
                        INSERT INTO phonebook (name, phone)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                    """, (row["name"], row["phone"]))
    print("CSV imported!")

def show_contacts():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM phonebook ORDER BY id")
        for row in cur.fetchall():
            print(row)

def search_contact():
    print("1. Search by name")
    print("2. Search by phone prefix")
    choice = input("Choose: ")
    value = input("Search: ")

    with conn.cursor() as cur:
        if choice == "1":
            cur.execute(
                "SELECT * FROM phonebook WHERE name ILIKE %s",
                ("%" + value + "%",)
            )
        elif choice == "2":
            cur.execute(
                "SELECT * FROM phonebook WHERE phone LIKE %s",
                (value + "%",)
            )
        else:
            print("Invalid choice")
            return

        for row in cur.fetchall():
            print(row)

def update_contact():
    name = input("Current name: ")
    print("1. Change name")
    print("2. Change phone")
    choice = input("Choose: ")
    value = input("New value: ")

    if choice == "1":
        field = "name"
    elif choice == "2":
        field = "phone"
    else:
        print("Invalid choice")
        return

    with conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE phonebook SET {field} = %s WHERE name = %s",
                (value, name)
            )
            print("Updated rows:", cur.rowcount)

def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")
    choice = input("Choose: ")
    value = input("Value: ")

    if choice == "1":
        field = "name"
    elif choice == "2":
        field = "phone"
    else:
        print("Invalid choice")
        return

    with conn:
        with conn.cursor() as cur:
            cur.execute(
                f"DELETE FROM phonebook WHERE {field} = %s",
                (value,)
            )
            print("Deleted rows:", cur.rowcount)

try:
    create_table()

    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Add contact")
        print("2. Import CSV")
        print("3. Show contacts")
        print("4. Search contact")
        print("5. Update contact")
        print("6. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        try:
            if choice == "1":
                add_contact()
            elif choice == "2":
                import_csv()
            elif choice == "3":
                show_contacts()
            elif choice == "4":
                search_contact()
            elif choice == "5":
                update_contact()
            elif choice == "6":
                delete_contact()
            elif choice == "0":
                break
            else:
                print("Invalid choice")
        except Exception as e:
            conn.rollback()
            print("Error:", e)
finally:
    conn.close()
