from faker import Faker
from faker.providers import person
from normalize import normalize

from functools import wraps
from ab_classes import AdressBook, Phone, Name, Record, Birthday, Iterarors
import pickle
from datetime import datetime, timedelta

# # import csv


# # # class Field:
# # #     area = None

# # #     def __init__(self, value, name) -> None:
# # #         self.__value = value
# # #         self._name = name

# # #     def __str__(self) -> str:
# # #         return self.value

# # #     def __repr__(self) -> str:
# # #         return str(self)

# # #     def get_value(self):
# # #         return self.__value


# # # obj = Field("bobs", "village")
# # # print(obj._name, obj._Field__value)

# # # # get = obj.value
# # # # print(get)


# # # print(obj.get_value())
# # # # obj.value = "shugar"

# # # # print(obj.value, obj.name)
# # # # setattr(obj, "value", "sugar")
# # # # print(obj.__dict__)
# # # # delattr(obj, "value")
# # # # print(obj.__dict__)
# # # obj.__dict__["area"] = "1 ar"
# # # print(obj.area, obj.__dict__)


# # def days_to_birthday(self):
# #     current_data = datetime.now()
# #     input_data = datetime.strptime(self, "%d-%m-%Y")
# #     old = current_data.year - input_data.year
# #     change_year = input_data.replace(year=current_data.year)
# #     left_to_bd = change_year - current_data
# #     if left_to_bd.days < 0:
# #         left_to_bd += timedelta(days=365)
# #     return f"{left_to_bd.days} days remained until the birthday "


# # print(days_to_birthday("10-02-1985"))


# def fill_book(user_input: str) -> str:
#     fake = Faker("uk-UA")
#     fake.add_provider(person)
#     n = user_input[1]
#     for i in range(int(n)):
#         name: str = normalize(fake.name()).lower().split(" ")
#         name = ("_").join(name)
#         map = {ord(" "): "", ord("-"): "", ord("("): "", ord(")"): ""}
#         ph = fake.phone_number().translate(map)

#         print(ph)


# fill_book("03")


# class IncorrectData(Exception):
#     ...


# class Field:
#     def __init__(self, value) -> None:
#         self.__value = value

#     def __str__(self) -> str:
#         return self.value

#     def __repr__(self) -> str:
#         return str(self)


# class Phone(Field):
#     def __init__(self, phone):
#         self.__phone = phone

#     @property
#     def phone(self):
#         return self.__phone

#     @phone.setter
#     def phone(self, phone):
#         print(len(phone))
#         if 13 >= len(phone) >= 6:
#             self.__phone = phone
#         else:
#             raise IncorrectData("Number to shot or to long")


# class Birthday(Field):
#     def __init__(self, date: str):
#         self.__date = date

#     @property
#     def date(self):
#         return self.__date

#     @date.setter
#     def date(self, date: str):
#         if len(date) == 10 and date[2] == "-" and date[5] == "-":
#             test = date.split("-")
#             if (
#                 0 < int(test[0]) <= 31
#                 and 0 < int(test[1]) <= 12
#                 and (datetime.now() - timedelta(days=43800)).year
#                 < int(test[2])
#                 < datetime.now().year
#             ):
#                 self.__date = date
#             else:
#                 raise IncorrectData("Need:dd-mm-YYYY |example: 01-02-2000")
#         else:
#             raise IncorrectData("Need:dd-mm-YYYY |example: 01-02-2000")


# number = Phone("911")
# number.phone = "+380506878385"
# bd = Birthday("10-12-1998")
# bd.date = "20-08-1885"
# print(number.phone, bd.date)

# def iterator(self, numbers_display_lines: int) -> str:
#         gen = (value for value in self.values())
#         count = 0
#         result = ""
#         for contact in gen:
#             result += str(contact) + "\n"
#             count += 1
#             if count > (numbers_display_lines - 1):
#                 yield result
#                 count = 0
#                 result = ""
#         if result:
#             yield result


# gen_list = dict_phones.iterator(5)
# for gen in gen_list:
#     print("\n")
#     for contacts in gen:
#         print(contacts)
def search_contacts(self, find_string: str) -> list:
    # find_string = find_string
    # search_list = [values for values in self.values()]
    find_list = [
        str(val) for val in self.values() if find_string.lower().strip() in str(val)
    ]

    # for val in self.values():
    #     if find_string in str(val):
    #         find_list.append(val)
    return find_list


dict_phones = AdressBook()
dict_phones.load_phone_book()
res = search_contacts(dict_phones, "ev")
for contact in res:
    print(contact)
