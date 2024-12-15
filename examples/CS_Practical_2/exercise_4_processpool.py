import concurrent.futures
from collections import defaultdict
from pathlib import Path
import timeit


def search_in_file(file_path, keywords):
    result = []
    # TODO Додати обробку можливих помилок 
    with open(file_path, 'r') as file:
        content = file.read()
        for keyword in keywords:
            if keyword in content:
                result.append((keyword, file_path))

    return result


def main_concurrent_process(file_paths, keywords):
    # TODO Додати вимір часу виконання
    results = defaultdict(list)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        #TODO Описати логіку ефективного розділення файлів між процесами
        for future in concurrent.futures.as_completed():
            result = future.result()
            for keyword, file_path in result:
                results[keyword].append(file_path)

    return results


if __name__ == '__main__':
    file_paths = list(Path("input").glob("*.py"))
    print(f"File paths: {file_paths}\n")
    keywords = []
    results = main_concurrent_process(file_paths, keywords)
    print(results)
