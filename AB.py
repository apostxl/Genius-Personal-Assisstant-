import re
import datetime
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

class InvalidPhoneError(Exception):
    pass

class MissingNumberError(Exception):
    pass

class MissingEmailError(Exception):
    pass

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except InvalidPhoneError:
            return Fore.RED + 'Phone is not valid'
        except MissingNumberError:
            return Fore.RED + "No number"
        except MissingEmailError:
            return Fore.RED + "No emails given" 
        except KeyError:
            return Fore.RED + '\nEnter user name please.\n'
        except ValueError:
            return Fore.RED + '\nSecond argument must be a number.\n'
        except IndexError:
            return Fore.RED + '\nGive me name, phone, email, address, and birthday please.\n'
    return inner


def from_txt_to_dict(file, mode):
    dct_contacts = {}
    with open(file, mode) as fh:
        for line in fh:
            text = line.strip().split(':')
            name = text[0]
            contact_info = text[1].split(';')
            number = int(contact_info[0])
            email = contact_info[1]
            address = contact_info[2]
            birthday = contact_info[-1]
            dct_contacts[name] = {
                "number": number,
                "email": email,
                "address": address,
                "birthday": birthday
            }
    return dct_contacts

@input_error
def hello(*args):
    with open('hello.txt') as fh:
        return fh.read()

@input_error
def add(*args):
    list_of_param = args[0].split()
    name = list_of_param[0].capitalize()
    number = list_of_param[1]
    email = list_of_param[2]
    address = ' '.join(list_of_param[3:-1])
    birthday = list_of_param[-1]

    if not re.match("\+380\(\d{2}\)\d{3}-\d{2}-\d{2}", number):
        raise InvalidPhoneError

    if not number:
        raise MissingNumberError
    
    if not email:
        raise MissingEmailError

    with open('contacts.txt', 'a') as fh:
        fh.write(f'{name}:{number};{email},;{address};{birthday}\n')
    return '\nThe contact was saved.\n'


@input_error
def change(*args):
    dct = from_txt_to_dict('contacts.txt', 'r')
    list_of_param = args[0].split()
    name = list_of_param[0].capitalize()
    number = int(list_of_param[1])
    email = list_of_param[2]
    address = list_of_param[3:-1]
    birthday = list_of_param[-1]
    dct[name] = {
        "number": number,
        "email": email,
        "address": address,
        "birthday": birthday
    }
    with open('contacts.txt', 'w') as fh:
        fh.write('')
        for key, value in dct.items():
            fh.write(f'{key}:{value["number"]};{value["email"]};{value["address"]};{value["birthday"]}\n')
    return '\nThe contact was updated.\n'

@input_error
def days_to_birthday(birthday):
    if not birthday:
        return "Please enter days before birthday";
    if birthday:
        today = datetime.date.today()
        next_birthday = datetime.date(today.year, birthday.value.month, birthday.value.day)
        if today > next_birthday:
            next_birthday = datetime.date(today.year + 1, birthday.value.month, birthday.value.day)
        days_until_birthday = (next_birthday-today).days
        
        return days_until_birthday
    else:
        return -1


@input_error
def phone(*args):
    dct = from_txt_to_dict('contacts.txt', 'r')
    list_of_param = args[0].split()
    name = list_of_param[0].capitalize()
    contact = dct.get(name)
    if contact:
        return f'\nName: {name}\nPhone: {contact["number"]}\nEmail: {contact["email"]}\nAddress: {contact["address"]}\nBirthday: {contact["birthday"]}\n'
    return f'\n{name} not found in contacts.\n'

def show_all(*args):
    with open('contacts.txt') as fh:
        text = '\n'
        for line in fh.readlines():
            text += line
        if len(text) < 2:
            return '\nThe phone book is empty.\n'
    return text

def days_to_birthday(birthday):
    if birthday:
        birthday.date()
        today = datetime.date.today()
        next_birthday = datetime.date(today.year, birthday.month, birthday.day)
        if today > next_birthday:
            next_birthday = datetime.date(today.year + 1, birthday.month, birthday.day)
        days_until_birthday = (next_birthday-today).days
        
        return days_until_birthday
    else:
        return -1

@input_error
def show_contacts_where_some_days_until_birthday(sbdays):
    if not sbdays:
        return Fore.YELLOW + '\nPlease enter days before birthday\n'
    sbdays = int(sbdays)
    cwsdb = 0
    dct = from_txt_to_dict('contacts.txt', 'r')
    for key, contact in dct.items():
        name = key
        number = contact["number"]
        email = contact["email"]
        address = contact["address"]
        birthday = contact["birthday"]
        birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
        days_before_birthday = days_to_birthday(birthday)
        if days_before_birthday == sbdays:
            print(f'\nName: {name} Phone: {number} Email: {email} Address: {address} Birthday: {birthday}\n')
            cwsdb += 1
    if cwsdb == 0:
        return  Fore.MAGENTA + f'\n Contacts with birthday after {sbdays} days not found\n'




def good_bye(*args):
    return '\nGoodbye!\n'

def clear(*args):
    confirmation = input(
        Fore.Purple + '\nAre you sure you want to clear your phone book? If yes, type "clear": ').lower()

    if confirmation == 'clear':
        with open('contacts.txt', 'w') as fh:
            fh.write('')
        return Fore.GREEN + '\nThe phone book has been cleared.\n'
    return Fore.GREEN + '\nThe phone book has not been cleared.\n'

def no_command(*args):
    return '\nUnknown command! Try again.\n'

COMMANDS = {
    hello: 'hello',
    good_bye: ['exit', 'close', 'good bye'],
    add: 'add',
    change: 'change',
    clear: 'clear',
    phone: 'phone',
    show_all: 'show all',
    show_contacts_where_some_days_until_birthday: 'birthday'
}


def command_handler(text):
    for command, kword in COMMANDS.items():
        if isinstance(kword, str):
            if text.lower().startswith(kword):
                data = ' '.join(text.replace(kword, '').strip().split())
                return command, data
        elif isinstance(kword, list):
            if text.strip().lower() in kword:
                return command, None
    return no_command, None

def main():
    print("Type 'hello' for help.\n")
    while True:
        user_input = input(Fore.BLUE + 'Enter your command: ').lower()
        command, data = command_handler(user_input)
        print(command(data))
        if command == good_bye:
            break

if __name__ == '__main__':
    main()
