import os
import shutil
import mimetypes
import zipfile
import unicodedata
from colorama import Fore, Style
from prettytable import PrettyTable

P = Fore.MAGENTA  # Purple
B = Style.BRIGHT  # Bold
G = Fore.LIGHTBLUE_EX  # Light Blue
T = Fore.RED
RES = Style.RESET_ALL  # Сброс форматирования


class FileSorter:
    def __init__(self, target_folder):
        self.target_folder = target_folder
        self.image_extensions = ('.jpeg', '.jpg', '.png', '.svg')
        self.video_extensions = ('.avi', '.mp4', '.mov', '.mkv')
        self.document_extensions = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
        self.audio_extensions = ('.mp3', '.ogg', '.wav', '.amr')
        self.archive_extensions = ('.zip', '.gz', '.tar')
        self.known_extensions = set()
        self.unknown_extensions = set()

    def normalize(self, name):
        normalized_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
        normalized_name = ''.join(c if c.isalnum() else '_' for c in normalized_name)
        return normalized_name

    def handle_file(self, file_path):
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1].lower()

        if extension in self.image_extensions:
            folder_name = 'images'
        elif extension in self.video_extensions:
            folder_name = 'video'
        elif extension in self.audio_extensions:
            folder_name = 'audio'
        elif extension in self.document_extensions:
            folder_name = 'documents'
        elif extension in self.archive_extensions:
            folder_name = 'archives'
            self.extract_archive(file_path)
            return  # Skip moving archive files
        else:
            folder_name = 'unknown'
            self.unknown_extensions.add(extension)

        new_name = self.normalize(file_name)
        new_path = os.path.join(self.target_folder, folder_name, new_name)

        if file_path != new_path:  # Check if file needs to be moved
            if not os.path.exists(os.path.dirname(new_path)):
                os.makedirs(os.path.dirname(new_path))

            shutil.move(file_path, new_path)

    def extract_archive(self, archive_path):
        folder_name = os.path.splitext(os.path.basename(archive_path))[0]
        extract_path = os.path.join(self.target_folder, 'archives', folder_name)

        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    def process_folder(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.handle_file(file_path)

    def sort_files(self):
        if not os.path.exists(self.target_folder):
            print(f"{T}{B}Error: The specified folder does not exist.{RES}")
            return

        for folder_name in ['images', 'video', 'audio', 'documents', 'archives', 'unknown']:
            folder_path = os.path.join(self.target_folder, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        self.process_folder(self.target_folder)

        self.process_folder(self.target_folder)

    def print_results(self):
        table = PrettyTable()
        table.field_names = ["Category", "Extension Count"]

        categories = {
            "Images": self.image_extensions,
            "Videos": self.video_extensions,
            "Documents": self.document_extensions,
            "Audio": self.audio_extensions,
            "Archives": self.archive_extensions,
            "Unknown": list(self.unknown_extensions),
        }

        for category, extensions in categories.items():
            category_folder = os.path.join(self.target_folder, category.lower())
            extension_count = sum(1 for root, _, files in os.walk(category_folder) for file in files if
                                  os.path.splitext(file)[1].lower() in extensions)
            table.add_row([category, extension_count])

        print(table)

    def run(self):
        print(f"{G}{B}Sorting files in {self.target_folder}...{RES}")
        self.sort_files()
        print(f"{G}{B}Sorting complete.{RES}")
        self.print_results()


if __name__ == "__main__":
    target_folder = input("Enter the folder path to sort: ")
    file_sorter = FileSorter(target_folder)
    file_sorter.run()
