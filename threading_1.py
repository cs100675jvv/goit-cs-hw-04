import threading
import time

# Функція для пошуку ключових слів у файлах
def search_keywords_in_files(files, keywords):
    results = {keyword: [] for keyword in keywords}  # Ініціалізуємо словник з порожніми списками для кожного ключового слова
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for keyword in keywords:
                if keyword.lower() in content:
                    results[keyword].append(file)  # Додаємо файл у список для відповідного ключового слова
    return results

# Потокова функція для обробки частини файлів
def threaded_search(files, keywords, result, thread_id):
    partial_result = search_keywords_in_files(files, keywords)
    result[thread_id] = partial_result

# Основна функція
def main_threading(file_list, keywords):
    num_threads = 4  # Кількість потоків
    result = {}
    threads = []
    chunk_size = len(file_list) // num_threads

    # Вимірюємо час початку виконання
    start_time = time.time()

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_threads - 1 else len(file_list)
        thread = threading.Thread(target=threaded_search, args=(file_list[start:end], keywords, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Об'єднання результатів від кожного потоку
    final_result = {keyword: [] for keyword in keywords}
    for thread_id, partial_result in result.items():
        for keyword, files in partial_result.items():
            final_result[keyword].extend(files)

    # Вимірюємо час завершення виконання
    end_time = time.time()

    # Обчислюємо загальний час виконання
    execution_time = end_time - start_time

    # Виведення результатів
    print(f"Результати пошуку мультипоточність: {final_result}")
    print(f"Час виконання скрипта: {execution_time:.20f} секунд")

if __name__ == "__main__":
    # Приклад файлів та ключових слів
    file_list = ["./file1.txt", "./file2.txt", "./file3.txt", "./file4.txt"]  # Замініть на реальні шляхи до файлів
    keywords = ["keyword1", "keyword2", "keyword3", "keyword4"]  # Замініть на реальні ключові слова

    main_threading(file_list, keywords)

