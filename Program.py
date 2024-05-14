import os
from person import Person, PersonDatabase


def load_database(database):
    while True:
        filename = input("Enter filename to load: ")
        full_path = os.path.join("D:\\", filename + ".xlsx")
        if os.path.exists(full_path):
            database.load_from_excel(full_path)
            print("Database loaded successfully.")
            break
        else:
            choice = input("File not found. Repeat input? (y/n): ").lower()
            if choice == 'n':
                print("Exiting program.")
                exit()
            elif choice != 'y':
                print("Invalid choice. Please enter 'y' or 'n'.")


def main():
    database = PersonDatabase()
    load_database(database)  # Загрузка базы данных из файла при старте программы

    while True:
        print("\nMenu:")
        print("1. Add person")
        print("2. Search person")
        print("3. Save database to Excel")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                first_name = input("Enter first name: ")
                last_name = input("Enter last name: ")
                middle_name = input("Enter middle name (optional): ")
                birth_date = input("Enter birth date (dd.mm.yyyy): ")
                gender = input("Enter gender (male/female): ")

                if not all([first_name, last_name, birth_date, gender]):
                    print("Error: Please fill in all required fields.")
                    choice = input("Do you want to fill them again? (y/n): ").lower()
                    if choice == 'y':
                        continue
                    elif choice == 'n':
                        break
                    else:
                        print("Invalid choice. Please enter 'y' or 'n'.")
                        continue

                if birth_date.count(".") != 2 or len(birth_date.split(".")) != 3:
                    print("Invalid date format for birth date. Please use dd.mm.yyyy format.")
                    continue

                death_date = input("Enter death date (optional, dd.mm.yyyy): ")
                if death_date and (death_date.count(".") != 2 or len(death_date.split(".")) != 3):
                    print("Invalid date format for death date. Please use dd.mm.yyyy format.")
                    continue

                if gender.lower() not in ['male', 'female', 'мужской', 'женский']:
                    print("Invalid gender. Please enter 'male' or 'female' or 'мужской' or 'женский'.")
                    continue

                # Добавление персоны в базу данных
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
                        print("Age:", int(person.age()))  # выводим возраст как целое число

                    choice = input("Do you want to edit data? (y/n): ").lower()
                    while choice not in ['y', 'n']:
                        print("Invalid input. Please enter 'y' or 'n'.")
                        choice = input("Do you want to edit data? (y/n): ").lower()

                    if choice == "y":
                        for person in results:
                            print("Editing data for", person.first_name, person.last_name)
                            edit_choice = input("What data do you want to edit? "
                                                "(1-first name/2-last name/3-middle name/4-birth date/5-death date): ")
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
                                new_birth_date = input("Enter new birth date (dd.mm.yyyy): ")
                                person.birth_date = new_birth_date
                            elif edit_choice.lower() == "5":  #внесены изменения
                                new_death_date = input("Enter new death date (dd.mm.yyyy): ")
                                person.death_date = person._parse_date(new_death_date)
                            else:
                                print("Invalid choice.")
                        print("Data has been updated successfully.")
                        break  # Returning to main menu
                    elif choice == "n":
                        confirm_delete = input("Would you like to delete your data? (y/n): ").lower()
                        while confirm_delete not in ['y', 'n']:
                            print("Invalid input. Please enter 'y' or 'n'.")
                            confirm_delete = input("Would you like to delete your data? (y/n): ").lower()

                        if confirm_delete == "y":
                            for person in results:
                                database.delete_person(person)
                            print("Data has been deleted.")
                            break
                        elif confirm_delete == "n":
                            print("Returning to previous menu.")
                            break
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

