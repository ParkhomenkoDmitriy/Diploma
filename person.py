import openpyxl
import datetime
import calendar

class Person:
    def __init__(self, first_name, last_name, birth_date, gender, middle_name=None, death_date=None):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.birth_date = self._parse_date(birth_date)
        self.death_date = self._parse_date(death_date) if death_date else None
        self.gender = gender

    def _parse_date(self, date_str):
        separators = ['.', ' ', '/', '-']
        for sep in separators:
            if sep in date_str:
                date_list = date_str.split(sep)
                break
        else:
            raise ValueError(
                "Invalid date format. Use one of the following formats: dd.mm.yyyy, dd mm yyyy, dd/mm/yyyy, dd-mm-yyyy")

        if len(date_list) != 3:
            raise ValueError(
                "Invalid date format. Use one of the following formats: dd.mm.yyyy, dd mm yyyy, dd/mm/yyyy, dd-mm-yyyy")

        try:
            day, month, year = map(int, date_list)
            return datetime.date(year, month, day)
        except ValueError:
            raise ValueError("Invalid date")

    def age(self):
        if self.death_date:
            delta = self.death_date - self.birth_date
        else:
            today = datetime.date.today()
            delta = today - self.birth_date

        years = delta.days / 365
        leap_years = sum(1 for year in range(self.birth_date.year, self.birth_date.year + int(years)) if calendar.isleap(year))

        return (delta.days + leap_years) / 365  # учитываем високосные годы

    def to_excel_row(self):
        return [self.first_name, self.last_name, self.middle_name, self.birth_date.strftime('%d.%m.%Y'),
                self.death_date.strftime('%d.%m.%Y') if self.death_date else '', self.gender]

# Остальной код остается без изменений


class PersonDatabase:
    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def search_person(self, query):
        results = []
        for person in self.people:
            if query.lower() in person.first_name.lower() or \
                    query.lower() in person.last_name.lower() or \
                    (person.middle_name and query.lower() in person.middle_name.lower()) or \
                    query.lower() == person.gender.lower():  # Поиск по полу
                results.append(person)
        return results

    def save_to_excel(self, filename):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["First Name", "Last Name", "Middle Name", "Birth Date", "Death Date", "Gender"])
        for person in self.people:
            sheet.append(person.to_excel_row())
        workbook.save(filename)

    def load_from_excel(self, filename):
        while True:
            try:
                workbook = openpyxl.load_workbook(filename)
                sheet = workbook.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    first_name, last_name, middle_name, birth_date, death_date, gender = row
                    self.add_person(Person(first_name, last_name, birth_date, gender, middle_name, death_date))
                break
            except FileNotFoundError:
                print("File not found.")
                filename = input("Enter filename to load: ")
                full_path = os.path.join("D:\\", filename + ".xlsx")
                continue
            except Exception as e:
                print("An error occurred while loading the database:", e)
                break

if __name__ == "__main__":
    main()
