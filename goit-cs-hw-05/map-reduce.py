import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import requests
import matplotlib.pyplot as plt

# Функція для завантаження тексту з URL
def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Помилка завантаження тексту: {e}")
        return None

# Функція для видалення пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

# Map function
def map_function(word):
    return word.lower(), 1

# Shuffle function
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# Reduce function
def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# MapReduce implementation
def map_reduce(text, search_words=None):
    # Remove punctuation
    text = remove_punctuation(text)
    words = text.split()

    # Filter words if search_words is provided
    if search_words:
        words = [word for word in words if word in search_words]

    # Parallel Mapping
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Parallel Reduction
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# Visualization function
def visualize_top_words(word_counts, top_n=10):
    # Sort words by frequency
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    words, counts = zip(*sorted_words)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.title("Top Words by Frequency")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # URL для завантаження тексту
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)

    if text:
        print("Текст успішно завантажено. Виконуємо аналіз...")

        # Виконання MapReduce
        word_counts = map_reduce(text)

        # Візуалізація топ-10 слів
        visualize_top_words(word_counts, top_n=10)
    else:
        print("Помилка: Не вдалося завантажити текст.")