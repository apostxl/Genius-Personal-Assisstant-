import art
from prettytable import PrettyTable



def header_text():

    attention = '*******attention********'.upper()
    text_GPA = art.text2art(" GPA", font='lean', chr_ignore=True, space=1)
    text_full = '***** Your Genius Personal Assistant ******'.upper()

    print(f'{attention:^110}\n', text_GPA, f'{text_full:^105}')


def inf_table():
    app_table = PrettyTable()

    app_table.field_names = ['№', 'Назва', 'Інформація']
    app_table.add_row(['1', 'AddressBook', 'Книга контактів для зберігання телефонів, емейлів днів народження та іншої корисної інформації'], divider = True)
    app_table.add_row(['2', 'NoteBook',
                       'Ззаписник в який можна додавати необхідні повсякденні записи'], divider=True)
    app_table.add_row(['3', 'FileSorter',
                       'Дозволяє відсортувати будь-яку теку з файлами'],
                      divider=True)
    app_table.add_row(['4', 'GPT навігатор',
                       'Допомагає витягти будь яку інформацію збережену в AddressBook чи NoteBook'])
    print(app_table)


header_text()
inf_table()




