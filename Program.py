import os
import re
from person import Person, PersonDatabase
from person import _parse_date

def is_valid_date_format(date_str):
    pattern = r'\d{2}[./ -]\d{2}[./ -]\d{4}' # Паттерн для проверки формата даты
    return re.fullmatch(pattern, date_str) is not None

def load_database(database):
    while True:
        choice = input("Menu:\n1. Load database from file\n2. Create new database file\n3. Exit\nEnter your choice: ").lower()
        if choice == "1":
            filename = input("Enter filename to load: ")
            full_path = os.path.join("D:\\", filename + ".xlsx")
            if os.path.exists(full_path):
                database.load_from_excel(full_path)
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
                database.save_to_excel(full_path)
                print("New database created successfully.")
                break
        elif choice == "3":
            print("Exiting program.")
            exit()
        else:
            print("Invalid choice. Please enter '1', '2' or '3'.")

def main():
    database = PersonDatabase()
    load_database(database)  # Загрузка или создание базы данных при старте программы

    while True:
        print("\nMenu:")
        print("1. Add person")
        print("2. Search person")
        print("3. Save database to Excel")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                # Переменная для отслеживания введенных данных
                data_entered = False

                first_name = input("Enter first name: ").title()
                last_name = input("Enter last name: ").title()
                middle_name = input("Enter middle name (optional): ").title()

                # Loop until a valid birth date is entered
                while True:
                    birth_date = input("Enter birth date (dd.mm.yyyy): ")
                    if not birth_date.strip():
                        print("Birth date is required.")
                        break  # Exit loop if birth date is not provided
                    if is_valid_date_format(birth_date):
                        # Если введена хотя бы одна дата, устанавливаем флаг data_entered в True
                        data_entered = True
                        break
                    print("Invalid date format for birth date. Please use dd.mm.yyyy format.")

                # Если данные не были введены, возвращаемся к предыдущему меню
                if not data_entered:
                    print("No information entered. Returning to previous menu.")
                    break

                # Check for presence and input format of death date (if provided)
                death_date = input("Enter death date (optional, dd.mm.yyyy): ")
                if death_date:
                    while True:
                        if is_valid_date_format(death_date):
                            break
                        print("Invalid date format for death date. Please use dd.mm.yyyy format or leave blank.")
                        death_date = input("Enter death date (optional, dd.mm.yyyy): ")

                gender = input("Enter gender (male/female): ")

                # Проверяем, заполнены ли все обязательные поля
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

                # Adding person information to the database
                database.add_person(Person(first_name, last_name, birth_date, gender, middle_name, death_date))
                break


        elif choice == "2":
            while True:
                query = input("Enter search query: ")
                results = database.search_person(query)
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
                        print("Age:", int(person.age()))  # display age as integer

                    choice = input(
                        "Choose action:\n1. Edit\n2. Delete\n3. Return to previous menu\nEnter your choice: ")

                    while choice not in ['1', '2', '3']:
                        print("Invalid input. Please enter '1', '2', or '3'.")
                        choice = input(
                            "Choose action:\n1. Edit\n2. Delete\n3. Return to previous menu\nEnter your choice: ")

                    if choice == "1":
                        for person in results:
                            print("Editing data for", person.first_name, person.last_name)
                            edit_choice = input("What data do you want to edit? "
                                                "\n1-first name\n2-last name\n3-middle name\n4-birth date\n5-death date\nEnter your choice: ")
                            if edit_choice.lower() == "1":
                                new_first_name = input("Enter new first name: ")
                                person.first_name = new_first_name
                            elif edit_choice.lower() == "2":
                                new_last_name = input("Enter new last name: ")
                                person.last_name = new_last_name
                            elif edit_choice.lower() == "3":
                                new_middle_name = input("Enter new middle name: ")
                                person.middle_name = new_middle_name

                            elif edit_choice.lower() == "4":
                                while True:
                                    try:
                                        new_birth_date = input("Enter new birth date (dd.mm.yyyy): ")
                                        if is_valid_date_format(new_birth_date):
                                            person.birth_date = _parse_date(new_birth_date)
                                            print("Data has been updated successfully.")
                                            break
                                        else:
                                            print("Invalid date format for birth date. Please use dd.mm.yyyy format.")
                                    except Exception as e:
                                        print("An error occurred:", str(e))
                                        continue  # Возвращение к вводу даты

                            elif edit_choice.lower() == "5":
                                while True:
                                    try:
                                        new_death_date = input(
                                            "Enter new death date (dd.mm.yyyy) or leave blank to remove death date: ")
                                        if not new_death_date.strip():
                                            person.death_date = None
                                            print("Death date has been removed successfully.")
                                            break
                                        elif is_valid_date_format(new_death_date):
                                            person.death_date = _parse_date(new_death_date)
                                            print("Data has been updated successfully.")
                                            break
                                        else:
                                            print("Invalid date format for death date. Please use dd.mm.yyyy format.")
                                    except Exception as e:
                                        print("An error occurred:", str(e))
                                        continue  # Возвращение к вводу даты

                        break  # Returning to main menu
                    elif choice == "2":
                        confirm_delete = input("Would you like to delete your data? (y/n): ").lower()
                        while confirm_delete not in ['y', 'n']:
                            print("Invalid input. Please enter 'y' or 'n'.")
                            confirm_delete = input("Would you like to delete your data? (y/n): ").lower()

                        if confirm_delete == "y":
                            for person in results:
                                database.delete_person(person)
                            print("Data has been deleted.")
                            break  # Возврат к основному меню
                        elif confirm_delete == "n":
                            print("Returning to previous menu.")
                            break  # Возврат к основному меню
                    elif choice == "3":
                        print("Returning to previous menu.")
                        break  # Возврат к основному меню
                    else:
                        print("No matching records found.")
                        break

        elif choice == "3":
            while True:
                filename = input("Enter filename to save: ")
                full_path = os.path.join("D:\\", filename + ".xlsx")
                if os.path.exists(full_path):
                    choice = input("File already exists. Save changes? (y/n): ").lower()
                    if choice == 'y':
                        database.save_to_excel(full_path)
                        print("Database saved successfully.")
                        break
                    elif choice == 'n':
                        while True:
                            choice = input("Save as? (y/n): ").lower()
                            if choice == 'y':
                                new_filename = input("Enter new filename: ")
                                new_full_path = os.path.join("D:\\", new_filename + ".xlsx")
                                if os.path.exists(new_full_path):
                                    print("Filename already exists. Please choose another filename.")
                                    continue
                                else:
                                    database.save_to_excel(new_full_path)
                                    print("Database saved successfully.")
                                    break
                            elif choice == 'n':
                                print("Returning to previous menu.")
                                break
                            else:
                                print("Invalid choice. Please enter 'y' or 'n'.")
                        break
                    else:
                        print("Invalid choice. Please enter 'y' or 'n'.")
                else:
                    database.save_to_excel(full_path)
                    print("Database saved successfully.")
                    break

        elif choice == "4":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 4.")

if __name__ == "__main__":
    main()
