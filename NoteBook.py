from collections import UserDict
import pickle
from prettytable import PrettyTable


class NoteName:

    def __init__(self, name: str):
        self.__value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name):
        self.__value = name

    def __str__(self):
        return self.__value

    def __repr__(self):
        return str(self)


class Tag:
    def __init__(self, tag=None):
        self.__value = tag

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name):
        self.__value = name

    def __str__(self):
        return self.__value

    def __repr__(self):
        return str(self)


class Note:
    def __init__(self, note):
        self.__value = note

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name: str):
        self.__value = name

    def __str__(self):
        return self.__value

    def __repr__(self):
        return str(self)


class Record:
    def __init__(self, name, tag=None, note=None):
        self.title = name
        self.tags = [] if tag is None else [tag]
        self.note = note

    def add_note(self, note):
        self.note = note

    def add_tag(self, tag):
        self.tags.append(tag.value)

    def __str__(self):
        return f'{str(self.title)}, {(str(self.tags))}, {str(self.note)}'

    def __repr__(self):
        return str(self)


class NoteBook(UserDict):

    def __init__(self, counter_index=0, *args, **kwargs):
        self.counter_index = counter_index
        super().__init__(*args, **kwargs)

    def add_record(self, record):
        self.data[record.title.value] = record


NOTEBOOK = NoteBook()


def wrapper(funk):
    def inner(*args):
        try:
            return funk(*args)
        except ValueError as e:
            print(e)

    return inner


def add_note(*args):
    title = NoteName(input('Введіть назву нотатку: '))
    if title.value in NOTEBOOK.data:
        print(f'Нотаток {title.value} вже існує. Виберыть іншу назву для нотатка!!')
    else:
        note = input('Введіть текст нотатку: ')
        tag = Tag(input('Введіть тег: '))

        note_rec = Record(title)
        note_rec.add_note(Note(note))

        if tag.value:
            note_rec.add_tag(tag)

        if note_rec.title.value not in NOTEBOOK.data:
            NOTEBOOK.add_record(note_rec)

        print(f'Нотаток {note_rec.title.value} додано до книги нотатків')


def change_note(*args):
    title = NoteName(input('Введіть назву запису яку треба змінити: '))
    if title.value in NOTEBOOK.data:
        note = input('Введіть текст запису: ')
        NOTEBOOK.data[title.value].add_note(Note(note))
    else:
        print(f'Запису "{title}" не знайдено')


def del_note(*args):
    title = NoteName(input('Введіть назву запису яку треба видалити '))
    if title.value in NOTEBOOK.data:
        note = NOTEBOOK.data.pop(title.value)
    else:
        print(f'Запису "{title}" не знайдено')


def find_note(*args):
    title = NoteName(input('Введіть назву запису яку треба видалити '))
    if title.value in NOTEBOOK.data:
        print(f'{NOTEBOOK.data[title.value]}')
    else:
        print(f'Запису "{title}" не знайдено')


def show_notes(*args):
    contact_table = PrettyTable()
    contact_table.field_names = ['Назва нотатку', 'Теги', 'Нотаток']
    if not NOTEBOOK.data:
        print('В записній книзі немає записів')
    else:
        for values in NOTEBOOK.data.values():
            contact_table.add_row([f'{values.title.value}',
                                   ', '.join(values.tags),
                                   f'{values.note.value}'], divider=True)
        print(contact_table)


def no_command(*args):
    print('''Невідома команда, спробуйте ща раз''')


def help_table(*args):
    helper = PrettyTable()
    helper.field_names = ['Команда', 'Що виконує команда']
    helper.add_row(['add', 'додає записи в книгу нотатків'], divider=True)
    helper.add_row(['delete', 'видаляє записи з книги нотатків'], divider=True)
    helper.add_row(['change', 'зиінює запис в книзі нотатків'], divider=True)
    helper.add_row(['show all', 'виводить зміст книги нотатків'], divider=True)
    helper.add_row(['find', 'шукає записи в книгу нотатків'], divider=True)
    helper.add_row(['help', 'вивід списку команд'])

    print(helper)


def exit(*args):
    print('''Good Bye''')


COMMANDS = {add_note: 'add',
            exit: ['exit', 'close', 'good bye'],
            del_note: 'delete',
            change_note: 'change',
            show_notes: 'show all',
            find_note: 'find',
            help_table: 'help'
            }


def command_handler(text):
    for command, kword in COMMANDS.items():
        if isinstance(kword, str):
            if text.lower().startswith(kword):
                return command, None
        elif isinstance(kword, list):
            if text.strip().lower() in kword:
                return command, None
    return no_command, None


def main():
    flag = True
    while flag:
        user_input = input('>>>')
        command, data = command_handler(user_input)

        command(data)

        if command == exit:
            print(exit())
            flag = False


if __name__ == '__main__':
    main()
