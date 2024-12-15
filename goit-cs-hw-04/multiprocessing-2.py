import multiprocessing
import time
from collections import defaultdict
from pathlib import Path


def search_in_file(file_path, keywords, queue):
    try:
        results = defaultdict(list)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(str(file_path))
        queue.put(results)  # Передаємо результати в чергу
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")


def process_task(files, keywords, queue):
    process_id = multiprocessing.current_process().pid  # Отримання PID процесу
    print(f"Process {process_id}: Starting task with {len(files)} files")
    for file in files:
        search_in_file(file, keywords, queue)
    print(f"Process {process_id}: Task completed")


def main_multiprocessing(file_paths, keywords):
    start_time = time.time()

    num_processes = multiprocessing.cpu_count()  # Кількість процесів
    processes = []
    queue = multiprocessing.Queue()
    results = defaultdict(list)

    # Розділення файлів між процесами
    files_per_process = len(file_paths) // num_processes
    remainder = len(file_paths) % num_processes  # Залишок файлів

    start_index = 0
    for i in range(num_processes):
        # Додаємо 1 файл до кожного процесу, якщо залишок > 0
        end_index = start_index + files_per_process + (1 if i < remainder else 0)
        process_files = file_paths[start_index:end_index]
        start_index = end_index  # Оновлюємо стартовий індекс для наступного процесу

        # Створюємо процес
        process = multiprocessing.Process(target=process_task, args=(process_files, keywords, queue))
        processes.append(process)
        process.start()

    # Очікуємо завершення всіх процесів
    for process in processes:
        process.join()

    # Отримуємо результати з черги
    while not queue.empty():
        partial_results = queue.get()
        for keyword, files in partial_results.items():
            results[keyword].extend(files)

    end_time = time.time()
    print(f"Execution time (multiprocessing): {end_time - start_time:.2f} seconds")
    return results


if __name__ == '__main__':
    # Приклад виклику
    input_directory = Path("input")
    input_directory.mkdir(exist_ok=True)  # Створити вхідну папку, якщо її немає
    file_paths = list(input_directory.glob("*.txt"))  # Список файлів .txt
    keywords = ["example", "test", "keyword", "Lorem"]  # Задати ключові слова

    if not file_paths:
        print("No files found in the 'input' directory. Please add some .txt files.")
    else:
        results = main_multiprocessing(file_paths, keywords)
        print("Search results:")
        for keyword, files in results.items():
            print(f"{keyword}: {files}")