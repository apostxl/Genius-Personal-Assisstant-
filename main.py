from prettytable import PrettyTable


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
    tags = [word for word in text.split() if word.startswith("#")]
    text_without_tags = ' '.join(word for word in text.split() if not word.startswith("#"))
    note_manager.add_note(text_without_tags, tags)
    return "Note added successfully"


def search_notes_by_tag(*args):
    tag = args[0]
    matching_notes = note_manager.search_notes_by_tag(tag)
    if matching_notes:
        result = []
        for i, note in enumerate(matching_notes, 1):
            result.append(f"Note {i}:\nText: {note.text}\nTags: {' '.join(note.tags)}\n")
        return "\n".join(result)
    return "No matching notes found"


def search_notes_by_text(*args):
    query = args[0]
    matching_notes = note_manager.search_notes_by_text(query)
    if matching_notes:
        result = []
        for i, note in enumerate(matching_notes, 1):
            result.append(f"Note {i}:\nText: {note.text}\nTags: {' '.join(note.tags).replace('|', ' ')}\n")
        return "\n".join(result)
    return "No matching notes found"


def edit_note(*args):
    try:
        index = int(args[0])
        new_text = args[1]
        note_manager.edit_note(index, new_text)
        return f"Note {index} updated successfully"
    except (IndexError, ValueError):
        return "Invalid input. Please provide a valid index and new text."


def delete_note(*args):
    try:
        index = int(args[0])
        note_manager.delete_note(index)
        return f"Note {index} deleted successfully"
    except (IndexError, ValueError):
        return "Invalid input. Please provide a valid index."


def sort_notes_by_tags(*args):
    tag = args[0]
    sorted_notes = note_manager.sort_notes_by_tags(tag)
    if sorted_notes:
        result = []
        for i, note in enumerate(sorted_notes, 1):
            result.append(f"Note {i}:\nText: {note.text}\nTags: {' '.join(note.tags).replace('|', ' ')}\n")
        return "\n".join(result)
    return "No notes found with the specified tag."


def get_all_notes(*args):
    notes = note_manager.get_all_notes()
    if notes:
        table = PrettyTable()
        table.field_names = ["Note", "Text", "Tags"]
        for i, note in enumerate(notes, 1):
            tags = ' '.join(tag for tag in note.tags if tag.startswith("#"))
            table.add_row([i, note.text, tags])
        table.align = "l"
        return str(table)
    return "No notes found."


def no_command(*args):
    return 'Unknown command, try again' if isinstance(args, list) else ''


COMMANDS = {
    add_note: 'add_note',
    search_notes_by_tag: 'search_notes_by_tag',
    search_notes_by_text: 'search_notes_by_text',
    edit_note: 'edit_note',
    delete_note: 'delete_note',
    sort_notes_by_tags: 'sort_notes_by_tags',
    get_all_notes: 'get_all_notes',
    no_command: None

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


def main():
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


if __name__ == '__main__':
    main()
