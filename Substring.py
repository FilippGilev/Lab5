import time

text = input("Введите строку: ")
pattern = input("Введите подстроку: ")

# Алгоритм Кнута-Морриса-Пратта
def KMP(text, pattern):
    n = len(text)
    m = len(pattern)
    # Инициализация массива для префикс-функции
    lps = [0] * m
    i = 1
    length = 0

    while i < m:
        # Обновляем значение lps[i] в соответствии с правилом KMP
        if pattern[i] == pattern[length] or pattern[i] == " ":
            length += 1
            lps[i] = length
            i += 1
        # Если символы не совпадают и length не равен 0, обновляем length
        elif pattern[i] != pattern[length] and length != 0:
            length = lps[length - 1]
        # Если символы не совпадают и length равен 0, присваиваем lps[i] значение 0
        elif pattern[i] != pattern[length] and length == 0:
            lps[i] = 0
            i += 1

    i = 0
    j = 0
    # Поиск вхождений подстроки в строку
    while i < n:
        if text[i] == pattern[j] or pattern[j] == " ":
            # Если символы совпадают, увеличиваем индексы
            i += 1
            j += 1
            if j == m:
                # Если j достигает конца подстроки, нашли вхождение
                print("Найдено вхождение на позиции:", i - j)
                j = lps[j - 1]

        # Если символы не совпадают и j не равно 0, обновляем j
        elif text[i] != pattern[j] and j != 0:
            j = lps[j - 1]

        # Если символы не совпадают и j равно 0, увеличиваем i
        elif text[i] != pattern[j] and j == 0:
            i += 1

# Алгоритм Бойера-Мура
def Boyer_Mur(text, pattern):
    # правило хорошего суффикса
    good_suffix = [0] * len(pattern)
    for i in range(len(pattern) - 1, -1, -1): # Обходим подстроку справа налево
        border = len(pattern) - 1
        # Находим расстояние от текущего символа до ближайшего совпадения в подстроке
        while border >= 0:
            # Если текущий символ не равен символу в суффиксе
            if pattern[i] != pattern[border]:
                border -= 1 # Перемещаемся к предыдущему символу в суффиксе
            else:
                break
        # Записываем в массив расстояние от текущего символа до ближайшего совпадения в подстроке
        good_suffix[i] = len(pattern) - 1 - border

    # правило хорошего суффикса
    last_symbol = {}
    for i in range(len(pattern) -1, -1, -1): # Обходим подстроку справа налево
        symbol = pattern[i]
        # Сохраняем последний встреченный индекс каждого символа в подстроке
        if symbol not in last_symbol:
            last_symbol[symbol] = i

    # Поиск вхождений подстроки в строку
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        # Сравниваем символы с конца подстроки и строки
        while j >= 0 and (pattern[j] == text[i + j] or pattern[j] == " "):
            j -= 1 # Перемещаемся к предыдущему символу подстроки
            if j == -1: # Нашли совпадение
                print("Найдено вхождение на позиции:", i)

        if j >= 0:  # Если j не стал -1, значит не все символы подстроки совпали
            # Используем правило плохого символа
            bad_char_shift = j - last_symbol.get(text[i + j], -1)
            # Используем правило хорошего суффикса
            good_suffix_shift = good_suffix[j]
            # Выбираем максимальное смещение
            shift = max(bad_char_shift, good_suffix_shift)
            # Сдвигаем подстроку
            i += shift
        else:
            # Все символы подстроки совпали, сдвигаем i на один символ
            i += 1


print("\n1. Чувствительный к регистру\n2. Нечувствительный к регистру\n")
action = int(input("Опция чувствительности: "))
match action:
    case 1:
        print("\nВстроенная функция поиска: \n")
        start_time_find = time.perf_counter()
        start_index = 0
        while True:
            index = text.find(pattern, start_index)
            if index == -1:
                break
            print("Найдено вхождение на позиции:", index)
            start_index = index + 1
        finish_time_find = time.perf_counter() - start_time_find
        print("\nВремя выполнения")
        print("--- {0} mcs ---".format(round(finish_time_find * 1000000)))
        print("\nАлгоритм Кнута-Морриса_Пратта: \n")
        start_time_KMP = time.perf_counter()
        KMP(text, pattern)
        finish_time_KMP = time.perf_counter() - start_time_KMP
        print("\nВремя выполнения")
        print("--- {0} mcs ---".format(round(finish_time_KMP * 1000000)))
        print("\nАлгоритм Бойера-Мура: \n")
        start_time_Boyer = time.perf_counter()
        Boyer_Mur(text, pattern)
        finish_time_Boyer = time.perf_counter() - start_time_Boyer
        print("\nВремя выполнения")
        print("--- {0} mcs ---".format(round(finish_time_Boyer * 1000000)))
    case 2:
        text = text.lower()
        pattern = pattern.lower()
        print("\nВстроенная функция поиска: \n")
        start_time_find = time.perf_counter()
        start_index = 0
        while True:
            index = text.find(pattern, start_index)
            if index == -1:
                break
            print("Найдено вхождение на позиции:", index)
            start_index = index + 1
        finish_time_find = time.perf_counter() - start_time_find
        print("\nВремя выполнения")
        print("--- {0} mcs ---".format(round(finish_time_find * 1000000)))
        print("\nАлгоритм Кнута-Морриса_Пратта: \n")
        start_time_KMP = time.perf_counter()
        KMP(text, pattern)
        finish_time_KMP = time.perf_counter() - start_time_KMP
        print("\nВремя выполнения")
        print("--- {0} mcs ---".format(round(finish_time_KMP * 1000000)))
        print("\nАлгоритм Бойера-Мура: \n")
        start_time_Boyer = time.perf_counter()
        Boyer_Mur(text, pattern)
        finish_time_Boyer = time.perf_counter() - start_time_Boyer
        print("\nВремя выполнения")
        print("--- {0} mcs ---".format(round(finish_time_Boyer * 1000000)))
