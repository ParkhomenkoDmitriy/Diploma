import pytest
import datetime
import calendar
from person import Person, PersonDatabase, _parse_date, count_leap_years


def test_parse_date():
    assert _parse_date("15.04.1990") == datetime.date(1990, 4, 15)
    assert _parse_date("15 04 1990") == datetime.date(1990, 4, 15)
    assert _parse_date("15/04/1990") == datetime.date(1990, 4, 15)
    assert _parse_date("15,04,1990") == datetime.date(1990, 4, 15)
    assert _parse_date("15-04-1990") == datetime.date(1990, 4, 15)
    with pytest.raises(ValueError):
        _parse_date("15.04.90")


def test_count_leap_years():
    assert count_leap_years(2000, 2000) == 1  # 2000 is a leap year
    assert count_leap_years(2000, 2004) == 2  # 2000 and 2004 are leap years
    assert count_leap_years(2001, 2004) == 1  # Only 2004 is a leap year
    assert count_leap_years(1900, 1900) == 0  # 1900 is not a leap year
    assert count_leap_years(1600, 1600) == 1  # 1600 is a leap year
    assert count_leap_years(1996, 2020) == 7  # 1996, 2000, 2004, 2008, 2012, 2016, 2020 are leap years


def test_person_creation():
    person = Person("John", "Doe", "15.04.1990", "male")
    assert person.first_name == "John"
    assert person.last_name == "Doe"
    assert person.birth_date == datetime.date(1990, 4, 15)
    assert person.gender == "male"
    assert person.middle_name is None
    assert person.death_date is None


def test_person_age():
    person = Person("John", "Doe", "15.04.1990", "male")
    assert person.age(datetime.date(2020, 4, 15)) == 30
    assert person.age(datetime.date(2020, 4, 14)) == 29
    assert person.age(datetime.date(2020, 4, 16)) == 30


def test_person_to_excel_row():
    person = Person("John", "Doe", "15.04.1990", "male")
    assert person.to_excel_row() == ["John", "Doe", None, "15.04.1990", "", "male"]


def test_person_database_add():
    db = PersonDatabase()
    person = Person("John", "Doe", "15.04.1990", "male")
    db.add_person(person)
    assert len(db.people) == 1
    assert db.people[0] == person


def test_person_database_delete():
    db = PersonDatabase()
    person = Person("John", "Doe", "15.04.1990", "male")
    db.add_person(person)
    db.delete_person(person)
    assert len(db.people) == 0


def test_person_database_search():
    db = PersonDatabase()
    person1 = Person("John", "Doe", "15.04.1990", "male")
    person2 = Person("Jane", "Doe", "20.05.1992", "female")
    db.add_person(person1)
    db.add_person(person2)
    results = db.search_person("John")
    assert len(results) == 1
    assert results[0] == person1
    results = db.search_person("Doe")
    assert len(results) == 2
    results = db.search_person("female")
    assert len(results) == 1
    assert results[0] == person2


def test_person_database_save_load(tmpdir):
    db = PersonDatabase()
    person = Person("John", "Doe", "15.04.1990", "male")
    db.add_person(person)
    filename = tmpdir.join("test_database.xlsx")
    db.save_to_excel(str(filename))
    new_db = PersonDatabase()
    new_db.load_from_excel(str(filename))
    assert len(new_db.people) == 1
    assert new_db.people[0].first_name == "John"
    assert new_db.people[0].last_name == "Doe"
    assert new_db.people[0].birth_date == datetime.date(1990, 4, 15)
    assert new_db.people[0].gender == "male"
