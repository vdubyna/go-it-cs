import threading
import time
from collections import defaultdict
from pathlib import Path

def search_in_file(file_path, keywords, results, lock, thread_id):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    with lock:  # Блокування для безпечного доступу до результатів
                        results[keyword].append(str(file_path))
        print(f"Thread {thread_id}: Finished processing {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path} in Thread {thread_id}: {e}")

def thread_task(files, keywords, results, lock):
    thread_id = threading.get_ident()  # Get the unique identifier of the thread
    print(f"Thread {thread_id}: Starting task with {len(files)} files")
    for file in files:
        search_in_file(file, keywords, results, lock, thread_id)
    print(f"Thread {thread_id}: Task completed")

def main_threading(file_paths, keywords):
    start_time = time.time()

    num_threads = 4  # Number of threads
    threads = []
    results = defaultdict(list)
    lock = threading.Lock()  # Lock for synchronizing access to results

    # Divide files among threads
    files_per_thread = len(file_paths) // num_threads
    remainder = len(file_paths) % num_threads  # Залишок файлів, якщо не ділиться рівномірно

    start_index = 0
    for i in range(num_threads):
        # Визначаємо кількість файлів для поточного потоку
        end_index = start_index + files_per_thread + (1 if i < remainder else 0)
        thread_files = file_paths[start_index:end_index]
        start_index = end_index  # Зсуваємо початковий індекс для наступного потоку

        # Створюємо потік
        thread = threading.Thread(target=thread_task, args=(thread_files, keywords, results, lock))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Execution time (threading): {end_time - start_time:.2f} seconds")
    return results

if __name__ == '__main__':
    # Example invocation
    input_directory = Path("input")
    input_directory.mkdir(exist_ok=True)  # Create the input folder if it doesn't exist
    file_paths = list(input_directory.glob("*.txt"))  # List all .txt files
    keywords = ["example", "test", "keyword", "Lorem"]  # Define keywords

    if not file_paths:
        print("No files found in the 'input' directory. Please add some .txt files.")
    else:
        results = main_threading(file_paths, keywords)
        print("Search results:")
        for keyword, files in results.items():
            print(f"{keyword}: {files}")