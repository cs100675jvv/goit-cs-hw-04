import multiprocessing
import time
import os

# Функція для пошуку ключових слів у файлах
def search_keywords_in_files(files, keywords):
    results = {keyword: [] for keyword in keywords}  # Ініціалізуємо словник з порожніми списками для кожного ключового слова
    for file in files:
        try:
            if not os.path.exists(file):
                print(f"Файл не знайдено: {file}")
                continue
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                for keyword in keywords:
                    if keyword.lower() in content:
                        results[keyword].append(file)  # Додаємо файл у список для відповідного ключового слова
        except FileNotFoundError:
            print(f"Помилка: Файл {file} не знайдено.")
        except IOError:
            print(f"Помилка: Неможливо відкрити файл {file}.")
        except Exception as e:
            print(f"Невідома помилка при роботі з файлом {file}: {str(e)}")
    return results

# Процесна функція для обробки частини файлів
def process_search(files, keywords, queue):
    try:
        result = search_keywords_in_files(files, keywords)
        queue.put(result)
    except Exception as e:
        print(f"Помилка в процесі: {str(e)}")
        queue.put({})  # В разі помилки повертаємо порожній результат

# Основна функція
def main_multiprocessing(file_list, keywords):
    num_processes = 4  # Кількість процесів
    queue = multiprocessing.Queue()
    processes = []
    chunk_size = len(file_list) // num_processes

    # Вимірюємо час початку виконання
    start_time = time.time()

    try:
        for i in range(num_processes):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i != num_processes - 1 else len(file_list)
            process = multiprocessing.Process(target=process_search, args=(file_list[start:end], keywords, queue))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        # Збирання результатів з черги
        final_result = {keyword: [] for keyword in keywords}
        while not queue.empty():
            result = queue.get()
            for keyword, files in result.items():
                final_result[keyword].extend(files)

    except Exception as e:
        print(f"Помилка в основній функції: {str(e)}")

    # Вимірюємо час завершення виконання
    end_time = time.time()

    # Обчислюємо загальний час виконання
    execution_time = end_time - start_time

    # Виведення результатів
    print(f"Результати пошуку мультипроцесинг: {final_result}")
    print(f"Час виконання скрипта: {execution_time:.20f} секунд")

if __name__ == "__main__":
    # Приклад файлів та ключових слів
    file_list = ["./file1.txt", "./file2.txt", "./file3.txt", "./file4.txt"]
    keywords = ["keyword1", "keyword2", "keyword3", "keyword4"]

    main_multiprocessing(file_list, keywords)

