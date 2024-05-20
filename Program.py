import os
import re
import time
from person import Person, PersonDatabase, _parse_date


def is_valid_date_format(date_str):
    pattern = r'\d{2}[./ -]\d{2}[./ -]\d{4}'
    return re.fullmatch(pattern, date_str) is not None


class PersonManager:
    def __init__(self):  # создается новый экземпляр класса PersonDatabase
        self.database = PersonDatabase()  # и присваивается атрибуту self.database

    def load_database(self):
        while True:
            choice = input("Menu:\n1. Load database from file\n2. Create new database file"
                           "\n3. Exit\nEnter your choice: ").lower()
            if choice == "1":
                filename = input("Enter filename to load: ")
                full_path = os.path.join("D:\\", filename + ".xlsx")
                if os.path.exists(full_path):
                    self.database.load_from_excel(full_path)
                    print("Database loaded successfully.")
                    break
                else:
                    print("File not found.")
                    continue
            elif choice == "2":
                filename = input("Enter filename to create: ")
                full_path = os.path.join("D:\\", filename + ".xlsx")
                if os.path.exists(full_path):
                    print("File already exists.")
                    continue
                else:
                    self.database.save_to_excel(full_path)
                    print("New database created successfully.")
                    break
            elif choice == "3":
                print("Exiting program.")
                exit()
            else:
                print("Invalid choice. Please enter '1', '2' or '3'.")

    def add_person(self):
        while True:
            data_entered = False  # Переменная для отслеживания введенных данных

            first_name = input("Enter first name: ").title()
            last_name = input("Enter last name: ").title()
            middle_name = input("Enter middle name (optional): ").title()

            while True:
                birth_date = input("Enter birth date (dd.mm.yyyy): ")
                if not birth_date.strip():
                    print("Birth date is required.")
                    break
                if is_valid_date_format(birth_date):
                    data_entered = True
                    break
                print("Invalid date format for birth date. Please use dd.mm.yyyy format.")

            if not data_entered:
                print("No information entered. Returning to previous menu.")
                break

            death_date = input("Enter death date (optional, dd.mm.yyyy): ")
            if death_date:
                while True:
                    if is_valid_date_format(death_date):
                        break
                    print("Invalid date format for death date. "
                          "Please use dd.mm.yyyy format or leave blank.")
                    death_date = input("Enter death date (optional, dd.mm.yyyy): ")

            gender = input("Enter gender (male/female): ")

            if not all([first_name, last_name, birth_date, gender]):
                print("Error: Please fill in all required fields.")
                choice = input("Do you want to fill them again? (y/n): ").lower()
                if choice == 'n':
                    break  # Finish data input
                else:
                    continue  # Return to data input

            if gender.lower() not in ['male', 'female']:
                print("Invalid gender. Please enter 'male' or 'female'.")
                continue

            self.database.add_person(Person(first_name, last_name, birth_date, gender, middle_name, death_date))
            break

    def search_person(self):
        while True:
            query = input("Enter search query: ")
            results = self.database.search_person(query)
            if results:
                print("Search results:")
                for person in results:
                    print("First Name:", person.first_name)
                    print("Last Name:", person.last_name)
                    print("Middle Name:", person.middle_name)
                    print("Birth Date:", person.birth_date.strftime('%d.%m.%Y'))
                    if person.death_date:
                        print("Death Date:", person.death_date.strftime('%d.%m.%Y'))
                    print("Gender:", person.gender)
                    print("Age:", int(person.age()))
                    time.sleep(2)
                choice = input("Choose action:\n1. Edit\n2. Delete\n3. "
                               "Return to previous menu\nEnter your choice: ")

                while choice not in ['1', '2', '3']:
                    print("Invalid input. Please enter '1', '2', or '3'.")
                    choice = input("Choose action:\n1. Edit\n2. Delete\n3. "
                                   "Return to previous menu\nEnter your choice: ")

                if choice == "1":
                    for person in results:
                        print("Editing data for", person.first_name, person.last_name)
                        edit_choice = input("What data do you want to edit? "
                                            "\n1-first name\n2-last name\n3-middle name"
                                            "\n4-birth date\n5-death date\nEnter your choice: ")
                        if edit_choice == "1":
                            while True:
                                new_first_name = input("Enter new first name: ").strip().title()
                                if new_first_name:
                                    person.first_name = new_first_name
                                    break
                                else:
                                    print("First name cannot be empty. "
                                          "Please enter a valid first name.")
                        elif edit_choice == "2":
                            while True:
                                new_last_name = input("Enter new last name: ").strip().title()
                                if new_last_name:
                                    person.last_name = new_last_name
                                    break
                                else:
                                    print("Last name cannot be empty. "
                                          "Please enter a valid last name.")
                        elif edit_choice == "3":
                            new_middle_name = input("Enter new middle name: ").strip().title()
                            person.middle_name = new_middle_name
                        elif edit_choice == "4":
                            while True:
                                new_birth_date = input("Enter new birth date (dd.mm.yyyy): ").strip()
                                if is_valid_date_format(new_birth_date):
                                    person.birth_date = _parse_date(new_birth_date)
                                    break
                                print("Invalid date format. "
                                      "Please enter a valid date in dd.mm.yyyy format.")
                        elif edit_choice == "5":
                            while True:
                                new_death_date = input("Enter new death date (optional, dd.mm.yyyy): ").strip()
                                if not new_death_date or is_valid_date_format(new_death_date):
                                    person.death_date = _parse_date(new_death_date) if new_death_date else None
                                    break
                                print("Invalid date format. "
                                      "Please enter a valid date in dd.mm.yyyy format.")
                        else:
                            print("Invalid choice.")
                            continue
                        print("Data updated successfully.")
                        break
                    break

                elif choice == "2":
                    if len(results) == 1:
                        confirm_delete = input("Are you sure you want to delete this person? (y/n): ").lower()
                        while confirm_delete not in ['y', 'n']:
                            print("Invalid input. Please enter 'y' or 'n'.")
                            confirm_delete = input("Are you sure you want to delete this person? (y/n): ").lower()
                        if confirm_delete == 'y':
                            self.database.delete_person(results[0])
                            print("Person deleted successfully.")
                        else:
                            print("Deletion canceled.")
                    else:
                        print("Multiple persons found. Please refine your search query.")
                    break

                elif choice == "3":
                    break
            else:
                print("No matching persons found.")
                break

    def save_database(self):
        while True:
            filename = input("Enter filename to save: ")
            full_path = os.path.join("D:\\", filename + ".xlsx")
            if os.path.exists(full_path):
                choice = input("File already exists. Do you want to overwrite it? (y/n): ").lower()
                if choice == "n":
                    continue
                elif choice == "y":
                    self.database.save_to_excel(full_path)
                    print("Database saved successfully.")
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
            else:
                self.database.save_to_excel(full_path)
                print("Database saved successfully.")
                break

    def run(self):
        self.load_database()

        while True:
            print("Options:")
            print("1. Add person")
            print("2. Search person")
            print("3. Save database")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_person()
            elif choice == "2":
                self.search_person()
            elif choice == "3":
                self.save_database()
            elif choice == "4":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter '1', '2', '3' or '4'.")


if __name__ == "__main__":
    manager = PersonManager()
    manager.run()
