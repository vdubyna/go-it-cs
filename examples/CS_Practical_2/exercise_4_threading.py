import threading
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


def thread_task(files, keywords, results):
    for file in files:
        search_in_file(file, keywords, results)


def main_threading(file_paths, keywords):
    # TODO Додати вимір часу виконання

    # Вибір кількості потоків тяжчий, так як процесори можуть мати різні можливості до Hyper-Threading 
    # для кожного ядра і пораховане Hyper-Threading * CPU Cores значення всеодно не буде гарантовано оптимальним
    num_threads = 4 
    threads = []
    results = defaultdict(list)
    #TODO Описати логіку ефективного розділення файлів між потоками
    for i in range(num_threads):
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results


if __name__ == '__main__':
    # Приклад виклику
    file_paths = list(Path("input").glob("*.py"))
    print(f"File paths: {file_paths}\n")
    keywords = []
    results = main_threading(file_paths, keywords)
    print(results)
