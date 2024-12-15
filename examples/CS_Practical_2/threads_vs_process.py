import concurrent.futures
import time
import random


def cpu_bound_task(n):
    start_time = time.time()
    result = 1
    for i in range(n):
        result = (result * result * i + 2 * result * i * i + 3) % 10000000
    end_time = time.time()
    print(f"CPU-bound task with n={n} took {end_time - start_time:.5f} seconds")
    return result


def io_bound_task(file_path):
    start_time = time.time()
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            time.sleep(random.uniform(0.1, 0.5))  # Simulating I/O latency
            result = len(content)
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        result = -1
    end_time = time.time()
    print(f"I/O-bound task for file {file_path} took {end_time - start_time:.5f} seconds")
    return result


def main():
    print("=== CPU-bound task with ProcessPoolExecutor ===")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        numbers = [1000000, 2000000, 3000000, 4000000, 5000000, 6000000]
        start_time = time.time()
        results = executor.map(cpu_bound_task, numbers)
        for result in results:
            print("Result:", result)
        end_time = time.time()
        print(f"Total time with ProcessPoolExecutor: {end_time - start_time:.5f} seconds\n")

    print("=== CPU-bound task with ThreadPoolExecutor ===")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        numbers = [1000000, 2000000, 3000000, 4000000, 5000000, 6000000]
        start_time = time.time()
        results = executor.map(cpu_bound_task, numbers)
        for result in results:
            print("Result:", result)
        end_time = time.time()
        print(f"Total time with ThreadPoolExecutor: {end_time - start_time:.5f} seconds\n")

    print("=== I/O-bound task with ProcessPoolExecutor ===")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        file_paths = ["file1.txt", "file2.txt", "file3.txt"]  
        start_time = time.time()
        results = executor.map(io_bound_task, file_paths)
        for result in results:
            print("Result:", result)
        end_time = time.time()
        print(f"Total time with ProcessPoolExecutor: {end_time - start_time:.5f} seconds\n")

    # I/O-bound task with ThreadPoolExecutor
    print("=== I/O-bound task with ThreadPoolExecutor ===")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        file_paths = ["file1.txt", "file2.txt", "file3.txt"]
        start_time = time.time()
        results = executor.map(io_bound_task, file_paths)
        for result in results:
            print("Result:", result)
        end_time = time.time()
        print(f"Total time with ThreadPoolExecutor: {end_time - start_time:.5f} seconds\n")


if __name__ == "__main__":
    main()