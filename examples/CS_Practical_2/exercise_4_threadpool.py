import concurrent.futures
import timeit
from collections import defaultdict
from pathlib import Path


def search_in_file(file_path, keywords, results):
    # TODO Додати обробку можливих помилок
    with open(file_path, 'r') as file:
        content = file.read()
        for keyword in keywords:
            if keyword in content:
                results[keyword].append(file_path)


def main_concurrent_thread(file_paths, keywords):
    results = defaultdict(list)
    # TODO Додати вимір часу виконання

    with concurrent.futures.ThreadPoolExecutor() as executor:
        #TODO Описати логіку ефективного розділення файлів між потоками
        for future in concurrent.futures.as_completed():
            future.result()

    return results


if __name__ == '__main__':
    file_paths = list(Path("input").glob("*.py"))
    print(f"File paths: {file_paths}\n")
    keywords = []
    results = main_concurrent_thread(file_paths, keywords)
    print(results)
