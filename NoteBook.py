from collections import UserDict
import pickle


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


def add_note(*args):
    title = NoteName(input('Введіть назву запису: '))
    note = input('Введіть текст запису: ')
    tag = Tag(input('Введіть тег: '))
    note_rec = Record(title)
    note_rec.add_note(Note(note))
    if tag.value:
        note_rec.add_tag(tag)

    NOTEBOOK.add_record(note_rec)
    print(NOTEBOOK)

def change_note(*args):
    title = NoteName(input('Введіть назву запису яку треба змінити: '))
    if title.value in NOTEBOOK:



add_note()
print(NOTEBOOK)