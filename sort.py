from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize
from prettytable import PrettyTable

def handle_media(filename: Path, target_folder: Path) -> None:

    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)  # робимо папку для архіва
    folder_for_file = target_folder / normalize(
        filename.name.replace(filename.suffix, "")
    )
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file)  # TODO: Check!
    except shutil.ReadError:
        print("It is not archive")
        folder_for_file.rmdir()
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can't delete folder: {folder}")


def main(folder: Path):
    
    parser.scan(folder)
    file_sorter_tbl = PrettyTable()
    
    file_sorter_tbl.align['Розширення'] = 'r'
    file_sorter_tbl.align['Кількість'] = 'c'
    file_sorter_tbl.field_names = ['Група', 'Розширення', 'Кількість']

    text_images = []
    count_images = []
    # зображення
    if len(parser.JPEG_IMAGES) > 0:
        text_images.append('jpeg:')
        count_images.append(f"{len(parser.JPEG_IMAGES)}")
        for file in parser.JPEG_IMAGES:        
            handle_media(file, folder / "images" / "JPEG")

    if len(parser.JPG_IMAGES) > 0:
        text_images.append('jpg:')
        count_images.append(f"{len(parser.JPG_IMAGES)}")
        for file in parser.JPG_IMAGES:
            handle_media(file, folder / "images" / "JPG")

    if len(parser.PNG_IMAGES) > 0:
        text_images.append('png:')
        count_images.append(f"{len(parser.PNG_IMAGES)}")
        for file in parser.PNG_IMAGES:
            handle_media(file, folder / "images" / "PNG")
    
    if len(parser.SVG_IMAGES) > 0:
        text_images.append('svg:')
        count_images.append(f"{len(parser.SVG_IMAGES)}")
        for file in parser.SVG_IMAGES:
            handle_media(file, folder / "images" / "SVG")
    
    if len(text_images) > 0: # відображення у таблиці
        file_sorter_tbl.add_row(['Зображення', '\n'.join(text_images),'\n'.join(count_images),], divider=True) 


    text_video = []
    count_video = []
    # відео файли
    if len(parser.AVI_VIDEO) > 0:
        text_video.append('avi:')
        count_video.append(f"{len(parser.AVI_VIDEO)}")
        for file in parser.AVI_VIDEO:
            handle_media(file, folder / "video" / "AVI")

    if len(parser.MP4_VIDEO) > 0:
        text_video.append('mp4:')
        count_video.append(f"{len(parser.MP4_VIDEO)}")
        for file in parser.MP4_VIDEO:
            handle_media(file, folder / "video" / "MP4")

    if len(parser.MOV_VIDEO) > 0:
        text_video.append('mov:')
        count_video.append(f"{len(parser.MOV_VIDEO)}")
        for file in parser.MOV_VIDEO:
            handle_media(file, folder / "video" / "MOV")

    if len(parser.MKV_VIDEO) > 0:
        text_video.append('mkv:')
        count_video.append(f"{len(parser.MKV_VIDEO)}")        
        for file in parser.MKV_VIDEO:
            handle_media(file, folder / "video" / "MKV")

    if len(text_video) > 0: # відображення у таблиці
        file_sorter_tbl.add_row(['Bідео файли', '\n'.join(text_video),'\n'.join(count_video),], divider=True)


    text_doc = []
    count_doc = []
    # документи
    if len(parser.DOC_DOCUMENTS) > 0:
        text_doc.append('doc:')
        count_doc.append(f"{len(parser.DOC_DOCUMENTS)}") 
        for file in parser.DOC_DOCUMENTS:
            handle_media(file, folder / "documents" / "DOC")

    if len(parser.DOCX_DOCUMENTS) > 0:
        text_doc.append('docx:')
        count_doc.append(f"{len(parser.DOCX_DOCUMENTS)}")   
        for file in parser.DOCX_DOCUMENTS:
            handle_media(file, folder / "documents" / "DOCX")

    if len(parser.TXT_DOCUMENTS) > 0:
        text_doc.append('txt:')
        count_doc.append(f"{len(parser.TXT_DOCUMENTS)}")
        for file in parser.TXT_DOCUMENTS:
            handle_media(file, folder / "documents" / "TXT")

    if len(parser.PDF_DOCUMENTS) > 0:
        text_doc.append('pdf:')
        count_doc.append(f"{len(parser.PDF_DOCUMENTS)}")
        for file in parser.PDF_DOCUMENTS:
            handle_media(file, folder / "documents" / "PDF")


    if len(parser.XLSX_DOCUMENTS) > 0:
        text_doc.append('xlsx:')
        count_doc.append(f"{len(parser.XLSX_DOCUMENTS)}")
        for file in parser.XLSX_DOCUMENTS:
            handle_media(file, folder / "documents" / "XLSX")

    if len(parser.XLS_DOCUMENTS) > 0:
        text_doc.append('xls:')
        count_doc.append(f"{len(parser.XLS_DOCUMENTS)}")
        for file in parser.XLS_DOCUMENTS:
            handle_media(file, folder / "documents" / "XLS")

    if len(parser.PPTX_DOCUMENTS) > 0:
        text_doc.append('pptx:')
        count_doc.append(f"{len(parser.PPTX_DOCUMENTS)}")
        for file in parser.PPTX_DOCUMENTS:
            handle_media(file, folder / "documents" / "PPTX")
           
    if len(parser.RTF_DOCUMENTS) > 0:
        text_doc.append('rtf:')
        count_doc.append(f"{len(parser.RTF_DOCUMENTS)}")
        for file in parser.RTF_DOCUMENTS:
            handle_media(file, folder / "documents" / "RTF")

    if len(text_doc) > 0: # відображення у таблиці
        file_sorter_tbl.add_row(['Документи', '\n'.join(text_doc),'\n'.join(count_doc),], divider=True)


    text_audio = []
    count_audio = []
    # музика
    if len(parser.MP3_AUDIO) > 0:
        text_audio.append('mp3:')
        count_audio.append(f"{len(parser.MP3_AUDIO)}")
        for file in parser.MP3_AUDIO:
            handle_media(file, folder / "audio" / "MP3")

    if len(parser.OGG_AUDIO) > 0:
        text_audio.append('ogg:')
        count_audio.append(f"{len(parser.OGG_AUDIO)}")
        for file in parser.OGG_AUDIO:
            handle_media(file, folder / "audio" / "OGG")


    if len(parser.WAV_AUDIO) > 0:
        text_audio.append('wav:')
        count_audio.append(f"{len(parser.WAV_AUDIO)}")
        for file in parser.WAV_AUDIO:
            handle_media(file, folder / "audio" / "WAV")

    if len(parser.AMR_AUDIO) > 0:
        text_audio.append('amr:')
        count_audio.append(f"{len(parser.AMR_AUDIO)}")
        for file in parser.AMR_AUDIO:
            handle_media(file, folder / "audio" / "AMR")

    if len(text_audio) > 0: # відображення у таблиці
        file_sorter_tbl.add_row(['Аудіо файли', '\n'.join(text_audio),'\n'.join(count_audio),], divider=True)
    
    
    text_archives = []
    count_archives = []
    # архіви

    if len(parser.ZIP_ARCHIVES) > 0:
        text_archives.append('zip:')
        count_archives.append(f"{len(parser.ZIP_ARCHIVES)}")
        for file in parser.ZIP_ARCHIVES:
            handle_media(file, folder / "archives" / "ZIP")

    if len(parser.GZ_ARCHIVES) > 0:
        text_archives.append('gz:')
        count_archives.append(f"{len(parser.GZ_ARCHIVES)}")
        for file in parser.GZ_ARCHIVES:
            handle_media(file, folder / "archives" / "GZ")
    
    if len(parser.TAR_ARCHIVES) > 0:
        text_archives.append('tar:')
        count_archives.append(f"{len(parser.TAR_ARCHIVES)}")
        for file in parser.TAR_ARCHIVES:
            handle_media(file, folder / "archives" / "TAR_ARCHIVES")
    
    if len(parser.RAR_ARCHIVES) > 0:
        text_archives.append('rar:')
        count_archives.append(f"{len(parser.RAR_ARCHIVES)}")
        for file in parser.RAR_ARCHIVES:
            handle_media(file, folder / "archives" / "RAR_ARCHIVES")

    if len(text_archives) > 0: # відображення у таблиці
        file_sorter_tbl.add_row(['Ахівні файли', '\n'.join(text_archives),'\n'.join(count_archives),], divider=True)


    for file in parser.MY_OTHER:
        handle_media(file, folder / "Other")

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

    print(file_sorter_tbl)
    result = f'Знайденно папок: {len(parser.FOLDERS)}'
    print(result)


if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        
        print(f"\n\nШлях у якому відсортовано файли: \n{folder_for_scan.resolve()} ")
        main(folder_for_scan.resolve())

        # # архіви
        # print(f"Archives zip: {len(parser.ZIP_ARCHIVES)}")
        # print(f"Archives gz: {len(parser.GZ_ARCHIVES)}")
        # print(f"Archives tar: {len(parser.TAR_ARCHIVES)}")

        # print(f"Types of files in folder: {(parser.EXTENSION)}")
        # print(f"Unknown files of types: {(parser.UNKNOWN)}")
        # print(f"MY_OTHER: {(parser.MY_OTHER)}")
        # # print(parser.REGISTER_EXTENSION)
        # print(len(parser.FOLDERS))
        # print(parser.FOLDERS[::-1])