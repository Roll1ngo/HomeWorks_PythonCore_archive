from collections import UserDict, UserList
import pickle
from faker import Faker
from normalize import normalize
from datetime import datetime, timedelta
from itertools import islice


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...


class IncorrectData(Exception):
    ...


class Iteraror(UserList):
    def __init__(self, list):
        self.list = list


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if 7 <= len(value) <= 13:
            self.__value = value
        else:
            raise IncorrectData("Number to shot or to long")


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> str:
        test = value.split("-")
        if (
            0 < int(test[0]) <= 31
            and 0 < int(test[1]) <= 12
            and (datetime.now() - timedelta(days=54750)).year
            < int(test[2])
            < (datetime.now() + timedelta(days=54750)).year
        ):
            self.__value = value

        else:
            raise IncorrectData(
                "Wrong Date Format or date out of range > Need:dd-mm-YYYY |example: 01-01-2001"
            )


class Record:
    def __init__(
        self, name: Name, phone: Phone = None, birthday: Birthday = None
    ) -> None:
        self.birthday = birthday
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def days_to_birthday(self) -> str:
        input_data = self.birthday
        current_data = datetime.now()
        input_data = datetime.strptime(str(self.birthday), "%d-%m-%Y")
        old = current_data.year - input_data.year
        change_year = input_data.replace(year=current_data.year)
        left_to_bd = change_year - current_data
        if left_to_bd.days < 0:
            left_to_bd += timedelta(days=365)
        return f"{left_to_bd.days} days remained until the birthday.Will be {old} years old"

    def add_phone(self, phone: Phone) -> str:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def change_phone(self, old_phone, new_phone) -> str:
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone

            return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"

    def del_phone(self, phone: Phone) -> str:
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)

                return f"number {phone} has been deleted in contact {self.name}"

        return f"{phone} not present in phones of contact {self.name}"

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)} Bd |{self.birthday if self.birthday else f'Not record'}|"


class AdressBook(UserDict):
    def search_contacts(self, find_string: str) -> list:
        find_list = [
            str(val) for val in self.values() if find_string.lower().strip() in str(val)
        ]
        return find_list

    def iterator(self, n: int) -> Iteraror:
        value_list = [value for value in self.values()]
        start = 0
        finish = n
        gen_list = []
        while start < len(value_list):
            gen = islice(value_list, start, finish)
            start += n
            finish = start + n
            gen_list.append(gen)
        iterator = Iteraror(gen_list)
        return iterator

    def load_phone_book(self) -> str:
        with open("phone_book.bin", "rb") as file:
            self.data = pickle.load(file)
        return f"Phone book has been loaded"

    def clear_phone_book(self) -> str:
        self.clear()
        return "Phone book is clear now"

    def add_record(self, record: Record) -> str:
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def del_record(self, rec: Record) -> str:
        del_rec = self.pop(rec.name.value)
        return f"contact {del_rec} has been deleted"

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
