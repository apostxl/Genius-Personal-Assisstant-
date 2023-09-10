import sys
from pathlib import Path

# зображення
JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []

# відео файли
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []

# документи
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
XLS_DOCUMENTS = []
PPTX_DOCUMENTS = []
RTF_DOCUMENTS = []

# музика
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []

# архіви
ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []
RAR_ARCHIVES = []

MY_OTHER = []


REGISTER_EXTENSION = {
    # зображення
    "JPEG": JPEG_IMAGES,
    "JPG": JPG_IMAGES,
    "PNG": PNG_IMAGES,
    "SVG": SVG_IMAGES,
    # відео файли
    "AVI": AVI_VIDEO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    # документи
    "DOC": DOC_DOCUMENTS,
    "DOCX": DOCX_DOCUMENTS,
    "TXT": TXT_DOCUMENTS,
    "PDF": PDF_DOCUMENTS,
    "XLSX": XLSX_DOCUMENTS,
    "XLS": XLS_DOCUMENTS,
    "PPTX": PPTX_DOCUMENTS,
    "RTF": RTF_DOCUMENTS,
    # музика
    "MP3": MP3_AUDIO,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    # архіви
    "ZIP": ZIP_ARCHIVES,
    "GZ": GZ_ARCHIVES,
    "TAR": TAR_ARCHIVES,
    "RAR": RAR_ARCHIVES
}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return (
        Path(filename).suffix[1:].upper()
    )  # перетворюємо розширення файлу на назву папки jpg -> JPG


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Якщо це папка то додаємо її до списку FOLDERS і переходимо до наступного елемента папки
        if item.is_dir():
            # перевіряємо, щоб папка не була тією в яку ми складаємо вже файли
            if item.name not in (
                "archives",
                "video",
                "audio",
                "documents",
                "images",
                "Other",
            ):
                FOLDERS.append(item)
                # скануємо вкладену папку
                scan(item)  # рекурсія
            continue  # переходимо до наступного елементу в сканованій папці

        #  Робота з файлом
        ext = get_extension(item.name)  # беремо розширення файлу
        fullname = folder / item.name  # беремо шлях до файлу
        if not ext:  # якщо файл немає розширення то додаєм до невідомих
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо ми не зареєстрували розширення у REGISTER_EXTENSION, то додаємо до невідомих
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)


if __name__ == "__main__":
    pass
    # folder_to_scan = sys.argv[1]
    # print(f"Start in folder {folder_to_scan}")
    # scan(Path(folder_to_scan))

    # # зображення
    # print(f"Images jpeg: {JPEG_IMAGES}")
    # print(f"Images jpg: {JPG_IMAGES}")
    # print(f"Images png: {PNG_IMAGES}")
    # print(f"Images svg: {SVG_IMAGES}")

    # # відео файли
    # print(f"Video avi: {AVI_VIDEO}")
    # print(f"Video mp4: {MP4_VIDEO}")
    # print(f"Video mov: {MOV_VIDEO}")
    # print(f"Video mkv: {MKV_VIDEO}")
    # # документи
    # print(f"Documents doc: {DOC_DOCUMENTS}")
    # print(f"Documents docx: {DOCX_DOCUMENTS}")
    # print(f"Documents txt: {TXT_DOCUMENTS}")
    # print(f"Documents pdf: {PDF_DOCUMENTS}")
    # print(f"Documents xlsx: {XLSX_DOCUMENTS}")
    # print(f"Documents xls: {XLS_DOCUMENTS}")
    # print(f"Documents pptx: {PPTX_DOCUMENTS}")
    # print(f"Documents rtf: {RTF_DOCUMENTS}")
    # # музика
    # print(f"Audio mp3: {MP3_AUDIO}")
    # print(f"Audio ogg: {OGG_AUDIO}")
    # print(f"Audio wav: {WAV_AUDIO}")
    # print(f"Audio amr: {AMR_AUDIO}")
    # # архіви
    # print(f"Archives zip: {ZIP_ARCHIVES}")
    # print(f"Archives gz: {GZ_ARCHIVES}")
    # print(f"Archives tar: {TAR_ARCHIVES}")

    # print(f"Types of files in folder: {EXTENSION}")
    # print(f"Unknown files of types: {UNKNOWN}")
    # print(f"MY_OTHER: {MY_OTHER}")

    # print(FOLDERS)
