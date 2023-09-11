from prettytable import PrettyTable
from colorama import Fore, Style  # Импортируем нужные стили из библиотеки colorama

# Замените ваши цветовые escape-последовательности ANSI на стили colorama
P = Fore.MAGENTA  # Purple
B = Style.BRIGHT  # Bold
G = Fore.LIGHTBLUE_EX  # Light Blue
T = Fore.RED
RES = Style.RESET_ALL  # Сброс форматирования


class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags or []

    def __str__(self):
        return self.text

    def add_tag(self, tag):
        self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def has_tag(self, tag):
        return tag in self.tags


class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags=None):
        note = Note(text, tags)
        self.notes.append(note)

    def search_notes_by_tag(self, tag):
        matching_notes = [note for note in self.notes if note.has_tag(tag)]
        return matching_notes

    def search_notes_by_text(self, query):
        matching_notes = [note for note in self.notes if query in note.text]
        return matching_notes

    def edit_note(self, index, new_text):
        if 0 <= index < len(self.notes):
            self.notes[index].text = new_text

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]

    def get_all_notes(self):
        return self.notes

    def sort_notes_by_tags(self, tag):
        sorted_notes = sorted(self.notes, key=lambda note: note.has_tag(tag))
        return sorted_notes


note_manager = NoteManager()


def add_note(*args):
    text = ' '.join(args)
    if not text:
        return f"{T}{B}Error: Nothing to add. Please provide text for the note.{RES}"

    tags = [word for word in text.split() if word.startswith("#")]
    text_without_tags = ' '.join(word for word in text.split() if not word.startswith("#"))
    note_manager.add_note(text_without_tags, tags)
    return f"{G}{B}Note added successfully{RES}"


def search_notes_by_tag(*args):
    tag = args[0]
    matching_notes = note_manager.search_notes_by_tag(tag)
    if matching_notes:
        result = []
        for i, note in enumerate(matching_notes, 1):
            result.append(f"{G}{B}Note {i}:\nText: {note.text}\nTags: {' '.join(note.tags)}\n{RES}")
        return "\n".join(result)
    return f"{T}{B}Tag not found{RES}"


def search_notes_by_text(*args):
    query = args[0]
    matching_notes = note_manager.search_notes_by_text(query)
    if matching_notes:
        result = []
        for i, note in enumerate(matching_notes, 1):
            result.append(f"{G}{B}Note {i}:\nText: {note.text}\nTags: {' '.join(note.tags).replace('|', ' ')}\n{RES}")
        return "\n".join(result)
    return f"{T}{B}Text not found{RES}"


def edit_note(*args):
    try:
        index = int(args[0]) - 1
        if 0 <= index < len(note_manager.get_all_notes()):
            new_text = ' '.join(args[1:])
            note_manager.edit_note(index, new_text)
            return f"{G}{B}Note {index + 1} updated successfully{RES}"
        else:
            return f"{T}{B}Note not found with index {index + 1}{RES}"
    except (IndexError, ValueError):
        return f"{T}{B}Invalid input. Please provide a valid index and new text.{RES}"


def delete_note(*args):
    try:
        index = int(args[0])
        if 0 <= index < len(note_manager.get_all_notes()):
            note_manager.delete_note(index)
            return f"{G}{B}Note {index} deleted successfully{RES}"
        else:
            return f"{T}{B}Note not found with index {index}{RES}"
    except (IndexError, ValueError):
        return f"{T}{B}Invalid input. Please provide a valid index.{RES}"


def get_all_notes(*args):
    notes = note_manager.get_all_notes()
    if notes:
        table = PrettyTable()
        table.field_names = [f"{P}{B}Note{RES}", f"{G}{B}Text{RES}", f"{T}{B}Tags{RES}"]
        for i, note in enumerate(notes, 1):
            tags = ' '.join(tag for tag in note.tags if tag.startswith("#"))
            table.add_row([f"{P}{B}{i}{RES}", f"{G}{B}{note.text}{RES}", f"{T}{B}{tags}{RES}"])
        return str(table)
    return "No notes found."


def no_command(*args):
    return f'{T}{B}Unknown command, try again{RES}' if isinstance(args, list) else ''


def exit(*args):
    return '''Good Bye'''


COMMANDS = {
    add_note: 'add_note',
    search_notes_by_tag: 'search_notes_by_tag',
    search_notes_by_text: 'search_notes_by_text',
    edit_note: 'edit_note',
    delete_note: 'delete_note',
    get_all_notes: 'get_all_notes',
    no_command: None,
    exit: ['exit', 'close', 'good bye'],

}


def command_handler(text):
    for command, kword in COMMANDS.items():
        if isinstance(kword, str):
            if text.lower().startswith(kword):
                return command, text.replace(kword, '').strip().split()
        elif isinstance(kword, list):
            if text.strip().lower() in kword:
                return command, []
    return no_command, []


def help(*args):
    return f'''
    {P}{B}Додавання нотатки:{RES} {G}{B}add_note ТЕКСТ #ТЕГ1 #ТЕГ2 ...{RES}
    {P}{B}Пошук нотаток за тегами:{RES}  {G}{B}search_notes_by_tag #ТЕГ{RES}
    {P}{B}Пошук нотаток за текстом:{RES}  {G}{B}search_notes_by_text ТЕКСТ{RES}
    {P}{B}Редагування нотатки:{RES}  {G}{B}edit_note ІНДЕКС НОВИЙ_ТЕКСТ{RES}
    {P}{B}Видалення нотатки:{RES}   {G}{B}delete_note ІНДЕКС{RES}
    {P}{B}Отримання списку всіх нотаток:{RES}  {G}{B}get_all_notes{RES}
    {P}{B}Приклади:{RES}

    {P}{B}Додати замітку:{RES} {G}{B}add_note Meeting with John Doe at 2 PM #meeting #important{RES} 
    {P}{B}Пошук за тегами:{RES} {G}{B}search_notes_by_tag #meeting{RES} 
    {P}{B}Пошук за текстом:{RES} {G}{B}search_notes_by_text Meeting with John Doe at 2 PM{RES} 
    {P}{B}Редагувати нотатку за номером:{RES} {G}{B}edit_note 1 Updated meeting with John Doe at 3 PM{RES} 
    {P}{B}Видалити нотатку за номером:{RES} {G}{B}delete_note 1{RES} 
    {P}{B}Отримати список усіх нотаток:{RES} {G}{B}get_all_notes{RES} 
    "{G}{B}good bye{RES}", "{G}{B}close{RES}", "{G}{B}exit{RES}" {P}{B}по будь-якій з цих команд бот завершує свою 
    роботу після того, як виведе у консоль{RES} 
    "{G}{B}Good bye!{RES}" '''



def main():
    print(help())
    while True:
        user_input = input('>>>')
        command, data = command_handler(user_input)

        if command == exit:
            print(command())
            break

        result = command(*data)
        if result:
            print(result)
        else:
            print("Command failed. Please try again.")
        if command == exit:
            break


if __name__ == '__main__':
    main()
