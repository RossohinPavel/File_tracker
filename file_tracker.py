import re
import os
import time
import shutil


DAY_LIMIT = 3
SOURCE = 'D:/тест/Book'
DESTINATION = 'E:/copy here'
TIMER = 300


def get_order_dict():
    day_dict = {}
    for day in reversed(os.listdir(SOURCE)):
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', day):
            day_dict[day] = tuple(order for order in os.listdir(f'{SOURCE}/{day}') if re.fullmatch(r'\d{6}', order))
        if len(day_dict) == DAY_LIMIT:
            break
    return {key: day_dict[key] for key in reversed(day_dict)}


def get_file_list(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            root = root.replace(path, '')
            if root.startswith('\\'):
                root = root[1:]
            yield root, file


def main():
    flag = False
    print('Сканирую на наличие новых заказов'.ljust(100, ' '), end='\r')
    order_dict = get_order_dict()
    folder_list, file_list = set(), []
    for day in order_dict:
        for order in order_dict[day]:
            s_files = tuple(get_file_list(f'{SOURCE}/{day}/{order}'))
            d_files = tuple(get_file_list(f'{DESTINATION}/{day}/{order}'))
            for line in s_files:
                if line not in d_files:
                    folder_list.add(f'{day}/{order}/{line[0]}')
                    file_list.append(f'{day}/{order}/{line[0]}/{line[1]}')
    if file_list:
        flag = True
        print('Создаю каталоги'.ljust(100, ' '), end='\r')
        for name in folder_list:
            os.makedirs(f'{DESTINATION}/{name}', exist_ok=True)
        file_list_len = len(file_list)
        for file in file_list:
            splited_line = file.split('/')
            print(f'Осталось: {file_list_len} файлов ({splited_line[1]} - {splited_line[-1]})'.ljust(100, ' '), end='\r')
            shutil.copy2(f'{SOURCE}/{file}', f'{DESTINATION}/{file}')
            file_list_len -= 1
    return flag


if __name__ == '__main__':
    while True:
        start = int(time.time())
        func_work = main()
        end = int(time.time())
        if func_work:
            TIMER = 300
        if not func_work and TIMER < 4800:
            TIMER += TIMER
        count = TIMER - (end - start)
        while count > 0:
            print(f'Копирование завершено. Жду {count} секунд'.ljust(100, ' '), end='\r')
            time.sleep(1)
            count -= 1
