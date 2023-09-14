from pathlib import Path
import shutil
import sys
import os

CATEGORIES = {'images': {'categories':['JPEG', 'PNG', 'JPG', 'SVG', 'GIF', 'WEBP'], 'result':[]}, 
              'video': {'categories':['AVI', 'MP4', 'MOV', 'MKV'], 'result':[]},
              'documents': {'categories':['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'], 'result':[]},
              'audio': {'categories':['MP3', 'OGG', 'WAV', 'AMR'], 'result':[]},
              'archives': {'categories':['ZIP', 'GZ', 'TAR'], 'result':[]},
              'other': {'categories':[], 'result':[]}
}

known_extensions = []
unknown_extensions = []


def unpacking(file:Path, extract_dir:Path) -> None:
    shutil.unpack_archive(file, extract_dir)
    

def move(file:Path, category:str, root_dir:Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    if category == 'archives':
        unpacking(file, target_dir.joinpath(file.stem))
        file.unlink()
    else:
        file.replace(target_dir.joinpath(file.name))
    

def get_categories(file:Path) -> str:
    ext = file.suffix.upper().replace('.', '')
    for cat, exts in CATEGORIES.items():
        if ext in exts['categories']:
            if ext not in known_extensions:
                known_extensions.append(ext)
            exts['result'].append(file.name)
            return cat
    if ext not in unknown_extensions:
        unknown_extensions.append(ext)
        CATEGORIES['other']['result'].append(file.name)
    return 'other'


def sort(root_dir:Path, current_dir:Path) -> None:
    global res, known_extensions, unknown_extensions
    
    for element in current_dir.iterdir():
        if element.is_file() and element.parent.name not in CATEGORIES.keys():
            category = get_categories(element)
            move(element, category, root_dir)
            if element.parent != root_dir and not any(element.parent.glob('*')):
                element.parent.rmdir()
        elif element.is_dir():
            sort(root_dir, element)


def res_choices(choice:int) -> None:
    result_list = []
    if choice == 1:
        for cat in CATEGORIES.keys():
            if CATEGORIES[cat]['result']:
                print(f'\n┌{"  " + cat + "  ":─^50}\n|')
                for file in CATEGORIES[cat]['result']:
                    print(f'|\t{file}')
                print(f'|\n└{"":─^50}')
    elif choice == 2:
        for ext in known_extensions:
            result_list.append(ext)
        print(f'\n┌{"":─^50}\n|')
        print('|\tKnown extensions: ', ', '.join(result_list), end='\n')
        print(f'|\n└{"":─^50}')
    elif choice == 3:
        for ext in unknown_extensions:
            result_list.append(ext)
        print(f'\n┌{"":─^50}\n|')
        print('|\tUnknown extensions: ', ', '.join(result_list), end='\n')
        print(f'|\n└{"":─^50}')
    else:
        print(f'\n┌{"":─^50}\n|')
        print('|\tUnknown option. Try again.', end='\n')
        print(f'|\n└{"":─^50}')


def main() -> None:
    try:
        root_dir = Path(sys.argv[1])
    except IndexError:
        return 'Required argument not found.\nExample: python3 main.py /Users/Mytsai/Desktop/Anything'
        

    if not root_dir.exists():
        return 'Folder does not exists. Try another path.'
    if not any(root_dir.iterdir()):
        return 'The specified folder is empty.'

    sort(root_dir, root_dir)         
    print('\nThe work is completed :)')
    while True:
        print('\nYou can get information:\n1. Display a list of files by category\n2. List of extensions that have been encountered\n3. List of unknown extensions\n0. Exit')
        choice = int(input('\nChoose from the options above: '))
        if choice != 0:
            res_choices(choice)
        else:
            break


if __name__ == '__main__':
    main()
    