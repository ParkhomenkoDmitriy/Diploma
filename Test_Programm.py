import unittest
import datetime  # Добавлен импорт datetime
from Program import Person, PersonDatabase  # Замените "Program" на имя вашего файла программы


class TestPersonAndPersonDatabase(unittest.TestCase):

    # В тестах
    def test_person_age_calculation(self):
        # Тестирование метода age() класса Person
        # Создание объекта Person с заданными датами рождения и смерти
        person = Person("John", "Doe", "01.01.1980", "male", death_date="01.01.2020")
        # Проверка, что метод age() возвращает целое число и соответствует ожидаемому возрасту
        self.assertIsInstance(person.age(datetime.date(2020, 1, 1)),
                              int)  # Проверка, что возраст является числом типа int
        self.assertEqual(person.age(datetime.date(2020, 1, 1)), 40)  # Ожидаемый возраст

    def test_person_age_input_formats(self):
        # Тестирование различных форматов ввода даты рождения
        formats = ["12.10.1980", "11 10 2000", "01/02/1995", "3-9-2007"]
        expected_ages = [41, 21, 27, 17]  # Ожидаемые возрасты для каждого формата

        for birth_date, expected_age in zip(formats, expected_ages):
            person = Person("Test", "Person", birth_date, "male")
            # Проверка, что фактический возраст равен ожидаемому возрасту
            self.assertEqual(int(person.age()), expected_age)

    def test_person_search(self):
        # Тестирование метода search_person() класса PersonDatabase
        # Создание объекта PersonDatabase и добавление персон в базу данных
        database = PersonDatabase()
        database.add_person(Person("John", "Doe", "01.01.1980", "male"))
        database.add_person(Person("Jane", "Doe", "01.01.1985", "female"))
        # Проверка, что метод search_person() правильно находит персон по запросу
        self.assertEqual(len(database.search_person("Doe")), 2)
        self.assertEqual(len(database.search_person("John")), 1)
        self.assertEqual(len(database.search_person("Jane")), 1)

    def test_person_search_partial_input(self):
        # Тестирование метода search_person() класса PersonDatabase с частичным вводом имени или фамилии
        # Создание объекта PersonDatabase и добавление персон в базу данных
        database = PersonDatabase()
        database.add_person(Person("Дензел", "Вашингтон", "01.01.1954", "мужской"))
        database.add_person(Person("Джон", "Доу", "01.01.1980", "мужской"))
        database.add_person(Person("Джейн", "Доу", "01.01.1985", "женский"))

        # Проверка, что метод search_person() находит персон даже при частичном вводе имени или фамилии
        self.assertEqual(len(database.search_person("Денз")), 1)
        self.assertEqual(len(database.search_person("Ваш")), 1)
        self.assertEqual(len(database.search_person("ел Вашингтон")), 1)
        self.assertEqual(len(database.search_person("нгтон")), 1)
        self.assertEqual(len(database.search_person("Джон")), 1)
        self.assertEqual(len(database.search_person("Доу")), 2)


if __name__ == '__main__':
    unittest.main()
