from faker import Faker
from faker.providers import person
from normalize import normalize
from functools import wraps
from ab_classes import (
    AdressBook,
    Phone,
    Name,
    Record,
    Birthday,
    IncorrectData,
    Iteraror,
)
import pickle
from itertools import islice


adress_book = AdressBook()


def decor_input_error(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

        except IndexError:
            print("Something wrong ")
            return main()
        except TypeError:
            print("Something wrong")
            return main()
        except KeyError:
            print("Something wrong")
            return main()
        except ValueError:
            print("Something wrong")
            return main()
        except IncorrectData as e:
            print(e)
            return main()

        return result

    return inner_func


def log_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("phone_book.bin", "wb") as file:
            pickle.dump(adress_book, file)
        return result

    return inner


def show_help(user_input):
    return f'"hello"ex=hello (show welcome)\n\n"search" examle: search lost(lost =name,phone or birthday)\n\n"chunk" example: chunk n(show the adress_book in pieces of "n" rows)\n\n"show_bd" example:show_bd name(Shows how many days are left until the birthday and how many years will be fulfilled)\n\n"fill" example: fill n(n =кількість рандомних контактів які будуть додані до телефонної книги)\n\n"load"(load phone_book into the file)\n\n"clear"(clear all contacts into the phone book)\n\n"add"  example: add name phone_number(add name and phone number)\n\n"change" example: change name new_numder(change phone number)\n\n"phone" example:phone name (show phone number)\n\n"show_all" example: show_all(show all phone book)\n\n"del"  example: del phone(del phone number into contact)\n\n"del_contact name", "remove_contact name"(remove contact into the phone_book)\n\n"good bye", "quit", "exit", "bye", "close"(close app)\n\n"help" example: help (show commands list)'


def left_day_to_bd(user_input: str) -> str:
    name = Name(user_input[1])
    rec: Record = adress_book.get(name.value)
    if rec:
        return rec.days_to_birthday()
    return f"No contact {name} in address book"


def search(user_input: str) -> str:
    return adress_book.search_contacts(user_input[1])


def load_phone_book(user_input: str) -> str:
    return adress_book.load_phone_book()


def clear_phone_book(user_input: str) -> str:
    return adress_book.clear_phone_book()


def exit(user_input: str) -> None:
    return None


def hello_func(user_input: str) -> str:
    return "How can I help you?"


def phone(user_input: str) -> str:
    return adress_book[user_input[1]]


def show_all(user_input: str) -> dict:
    return adress_book


def show_string_contact(user_input: str) -> Iteraror:
    return adress_book.iterator(int(user_input[1]))


@log_decorator
def del_contact(user_input: str) -> str:
    name = Name(user_input[1])
    rec: Record = adress_book.get(name.value)
    if rec:
        return adress_book.del_record(rec)
    return f"No contact {name} in address book"


@log_decorator
def fill_book(user_input: str) -> str:
    fake = Faker("uk-UA")
    fake.add_provider(person)
    n = user_input[1]
    for i in range(int(n)):
        name: str = normalize(fake.name()).lower().split(" ")
        name = Name(("_").join(name))

        map = {ord(" "): "", ord("-"): "", ord("("): "", ord(")"): ""}
        phone = Phone(fake.phone_number().translate(map))

        birthday = fake.profile()["birthdate"]
        birthday = Birthday(birthday.strftime("%d-%m-%Y"))

        rec = Record(name, phone, birthday)
        adress_book.add_record(rec)
    return f"Adress book been filled with {n} random contacts"


@decor_input_error
@log_decorator
def add_name_and_phone_number(user_input: str) -> dict:
    name = Name(user_input[1])
    phone = Phone(user_input[2])
    rec: Record = adress_book.get(str(name))
    if rec:
        return rec.add_phone(phone)

    if len(user_input) == 4:
        birthday = Birthday(user_input[3])

        rec = Record(name, phone, birthday)
        return adress_book.add_record(rec)

    rec = Record(name, phone)

    return adress_book.add_record(rec)


@log_decorator
def change(user_input: str) -> dict:
    name = Name(user_input[1])
    old_phone = Phone(user_input[2])
    new_phone = Phone(user_input[3])
    rec: Record = adress_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@log_decorator
def del_phone(user_input: str) -> str:
    name = Name(user_input[1])
    phone = Phone(user_input[2])
    rec: Record = adress_book.get(str(name))
    if rec:
        return rec.del_phone(phone)
    return f"No contact {name} in address book"


@decor_input_error
def get_handler(command: str) -> object:
    for comm, func in COMMANDS.items():
        if command in comm:
            return func


@decor_input_error
def main() -> str:
    print(
        '"help" show list of commands"\n"Для наповнення адресної книги користуйтесь командами"fill" або "load"'
    )
    while True:
        user_input = input(">>>").lower()
        user_input = user_input.strip().split()
        return_func = get_handler(user_input[0])
        if return_func == exit:
            print("Good bye! Have a nice day!")
            break

        result = return_func(user_input)
        if isinstance(result, Iteraror):
            input_str = ""
            for gen in result.list:
                input_str += "\n"
                for contacts in gen:
                    input_str += "\n" + str(contacts)
                    result = input_str
        print(result)


COMMANDS = {
    ("good bye", "quit", "exit", "bye", "close"): exit,
    ("hello", "hey"): hello_func,
    ("додай", "add"): add_name_and_phone_number,
    ("change",): change,
    ("phone", "show_phone"): phone,
    ("show_all", "show_book"): show_all,
    ("del_contact", "remove_contact"): del_contact,
    ("del"): del_phone,
    ("help"): show_help,
    ("load"): load_phone_book,
    ("clear"): clear_phone_book,
    ("fill"): fill_book,
    ("show_bd"): left_day_to_bd,
    ("chunk"): show_string_contact,
    ("search"): search,
}


if __name__ == "__main__":
    main()
