import unittest
from unittest.mock import patch
from Program import Person, is_valid_date_format, _parse_date


class TestEditDataInput(unittest.TestCase):
    @patch('builtins.input', side_effect=['y', '2', 'NewLastName', ''])
    def test_mock_edit_data_input(self, mock_input):
        person = Person("John", "Doe", "01.01.1980", "male")

        choice = input("Do you want to edit data? (y/n): ").lower()
        while choice not in ['y', 'n']:
            print("Invalid input. Please enter 'y' or 'n'.")
            choice = input("Do you want to edit data? (y/n): ").lower()

        if choice == "y":
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
                while True:
                    new_birth_date = input("Enter new birth date (dd.mm.yyyy): ")
                    if is_valid_date_format(new_birth_date):
                        person.birth_date = _parse_date(new_birth_date)
                        print("Data has been updated successfully.")
                        break
                    else:
                        print("Invalid date format for birth date. Please use dd.mm.yyyy format.")

            if edit_choice.lower() == "5":
                while True:
                    new_death_date = input("Enter new death date (dd.mm.yyyy) or leave blank to remove death date: ")
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

        self.assertEqual(person.last_name, "NewLastName")


if __name__ == '__main__':
    unittest.main()
