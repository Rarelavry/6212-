import operator
import json
import sys
import argparse
import os


def write_txt(file_path: str, data: str) -> None:
    """func for write data

    Args:
        file_path (str): path to file
        data (str): current string
    """
    try:
        with open(file_path, 'w', encoding="UTF-8") as file:
            file.write(data)
    except Exception as e:
        print("Error:", e)


def read_json(file_path: str) -> dict[str:str]:
    """func for read data from json

    Returns:
        dict[str:str]: dictionary [key - value]
    """
    try:
        with open(file_path, 'r', encoding="UTF-8") as file:
            return json.load(file)
    except Exception as e:
        print("Error:", e)


def write_json(file_path: str, key: dict) -> None:
    """func for write data to json

    Args:
        file_path (str): path to file
        key (dict): dictionary [key - value]
    """
    try:
        with open(file_path, 'w', encoding="UTF-8") as file:
            json.dump(key, file)
    except Exception as e:
        print("Error:", e)


def read_txt(file_path: str) -> str:
    """func for read data

    Args:
        file_path (str): path to file

    Returns:
        str: file contents
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            return file.read().replace("\n", " \n")
    except Exception as e:
        print("Error:", e)


def text_process(text: str, key: dict) -> str:
    """function, which can process the text by key

    Args:
        text (str): text, we need to process
        key (dict): key for the processing

    Returns:
        str: result text
    """
    result = ""
    for i in text:
        if (i in key) and (len(key[i])):
            result += key[i]
        else:
            result += i
    return result


def get_freq(text: str) -> dict:
    """function,for getting text frequency

    Args:
        text (str): text for process

    Returns:
        dict: dictionary [key - value]
    """
    return dict(sorted({i: text.count(i)/len(text) for i in set(text)}.items(), key=operator.itemgetter(1), reverse=True))


def key_update(dict_key: dict, key: str, val: str) -> None:
    """function, which can create/update key for current text

    Args:
        dict_key (dict): old key-dict
        key (str): new key
        val (str): new value
    """
    if key in dict_key:
        dict_key[key] = val


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='text process',
        description='process the text by the key')
    parser.add_argument('dirrectory', type=str, help="dirrectory with files")
    parser.add_argument('key', type=str, help=".json file with key")
    parser.add_argument('main_file', type=str,
                        help=".txt file with ciphered text")
    parser.add_argument('processed_file', type=str,
                        help=".txt file with unciphered text")
    args = parser.parse_args()

    write_to = os.path.join(args.dirrectory, args.processed_file)
    file_from = os.path.join(args.dirrectory, args.main_file)
    key = os.path.join(args.dirrectory, args.key)
    
    write_txt(write_to, text_process(read_txt(file_from), read_json(key)))


if __name__ == '__main__':
    main()
