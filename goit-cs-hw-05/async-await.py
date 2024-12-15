import asyncio
import os
from pathlib import Path
import shutil
import argparse
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def read_folder(source_folder: Path, output_folder: Path):
    """
    Асинхронно читає всі файли у вихідній папці та її підпапках,
    сортує їх за розширенням і копіює до цільової папки.
    """
    try:
        # Рекурсивний пошук файлів
        tasks = []
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = Path(root) / file
                tasks.append(copy_file(file_path, output_folder))

        # Виконуємо всі копії асинхронно
        await asyncio.gather(*tasks)
        logging.info("Сортування файлів завершено.")
    except Exception as e:
        logging.error(f"Помилка під час читання папки: {e}")


async def copy_file(file_path: Path, output_folder: Path):
    """
    Асинхронно копіює файл до підпапки, що відповідає його розширенню.
    """
    try:
        # Отримуємо розширення файлу
        extension = file_path.suffix[1:] if file_path.suffix else "unknown"
        target_folder = output_folder / extension

        # Створюємо цільову папку, якщо її немає
        target_folder.mkdir(parents=True, exist_ok=True)

        # Копіюємо файл
        target_path = target_folder / file_path.name
        shutil.copy(file_path, target_path)
        logging.info(f"Копіювання файлу {file_path} до {target_path}")
    except Exception as e:
        logging.error(f"Помилка копіювання файлу {file_path}: {e}")


def main():
    # Обробка аргументів командного рядка
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки.")
    parser.add_argument("output", type=str, help="Шлях до цільової папки.")
    args = parser.parse_args()

    source_folder = Path(args.source)
    output_folder = Path(args.output)

    # Перевірка існування папок
    if not source_folder.is_dir():
        logging.error(f"Вихідна папка {source_folder} не існує.")
        return

    # Запуск асинхронного сортування
    asyncio.run(read_folder(source_folder, output_folder))


if __name__ == "__main__":
    main()