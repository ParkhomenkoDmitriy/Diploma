import unittest
import datetime
from Program import Person, PersonDatabase


class TestPersonAndPersonDatabase(unittest.TestCase):
    class TestPerson(unittest.TestCase):

        def test_age_calculation(self):
            # Проверяем правильность подсчета полных лет для разных дат рождения
            person1 = Person("John", "Doe", datetime.date(1980, 1, 1), "male")
            person2 = Person("Jane", "Doe", datetime.date(1990, 1, 1), "female")
            person3 = Person("Alice", "Smith", datetime.date(2000, 5, 15), "female")

            # Имитируем текущую дату для тестирования
            today = datetime.date(2024, 5, 15)

            self.assertEqual(person1.age(today), 44)
            self.assertEqual(person2.age(today), 34)
            self.assertEqual(person3.age(today), 24)
    class TestPerson(unittest.TestCase):

        def test_parse_date_valid(self):
            # Проверяем, что метод _parse_date правильно парсит корректные даты
            person = Person("John", "Doe", "01.01.1980", "male")
            self.assertEqual(person.birth_date, datetime.date(1980, 1, 1))

        def test_parse_date_invalid(self):
            # Проверяем, что метод _parse_date правильно обрабатывает некорректные даты
            invalid_dates = [
                "1980-01-01",  # Неправильный формат
                "01.01",  # Неправильный формат
                "01.01.1980.01",  # Неправильный формат
                "",  # Пустая строка
                "01/01/1980",  # Дата в неподдерживаемом формате
                "01,01,1980",  # Дата в неподдерживаемом формате
                "01 01 1980"  # Дата в неподдерживаемом формате
            ]
            for date_str in invalid_dates:
                with self.assertRaises(ValueError):
                    Person("John", "Doe", date_str, "male")
    def test_person_search(self):
        # Тестирование метода search_person() класса PersonDatabase
        database = PersonDatabase()
        database.add_person(Person("John", "Doe", "01.01.1980", "male"))
        database.add_person(Person("Jane", "Doe", "01.01.1985", "female"))
        self.assertEqual(len(database.search_person("Doe")), 2)
        self.assertEqual(len(database.search_person("John")), 1)
        self.assertEqual(len(database.search_person("Jane")), 1)

    def test_person_search_partial_input(self):
        # Тестирование метода search_person() класса PersonDatabase с частичным вводом имени или фамилии
        database = PersonDatabase()
        database.add_person(Person("Дензел", "Вашингтон", "01.01.1954", "мужской"))
        database.add_person(Person("Джон", "Доу", "01.01.1980", "мужской"))
        database.add_person(Person("Джейн", "Доу", "01.01.1985", "женский"))

        self.assertEqual(len(database.search_person("Денз")), 1)
        self.assertEqual(len(database.search_person("Ваш")), 1)
        self.assertEqual(len(database.search_person("ел Вашингтон")), 1)
        self.assertEqual(len(database.search_person("нгтон")), 1)
        self.assertEqual(len(database.search_person("Джон")), 1)
        self.assertEqual(len(database.search_person("Доу")), 2)

if __name__ == '__main__':
    unittest.main()
