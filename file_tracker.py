import re
import os
import time
import shutil


DAY_LIMIT = 3
SOURCE = 'Z:/to_print'
DESTINATION = 'O:/Book'
TIMER = 300


def get_order_dict():
    """
    :return: Словарь. Ключ - имя папки "день". Значения - список заказов. Количество ключей (дней) ограничено DAY_LIMIT.
    """
    day_dict = {}
    for day in reversed(os.listdir(SOURCE)):
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', day):
            day_dict[day] = [order for order in os.listdir(f'{SOURCE}/{day}') if re.fullmatch(r'\d{6}', order)]
        if len(day_dict) == DAY_LIMIT:
            break
    return {key: day_dict[key] for key in reversed(day_dict)}


def get_order_scan(path, pattern):
    total_size = 0
    folder_list = [os.path.relpath(path, pattern)]
    file_list = []
    for root, dirs, files in os.walk(path):
        for folder in dirs:
            folder_abs_path = os.path.join(root, folder)
            folder_rel_path = os.path.relpath(folder_abs_path, pattern)
            folder_list.append(folder_rel_path)
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, pattern)
            file_list.append(rel_path)
    return total_size, folder_list, file_list


def main():
    while True:
        print('Сканирую на наличие новых заказов', '                                           ', end='\r')
        order_dict = get_order_dict()
        folder_list, file_list = [], []
        for day in order_dict:
            for order in order_dict[day]:
                s_path = f'{SOURCE}/{day}/{order}'
                d_path = f'{DESTINATION}/{day}/{order}'
                z_order = get_order_scan(s_path, SOURCE)
                o_order = get_order_scan(d_path, DESTINATION)
                if o_order[0] < z_order[0]:
                    folder_list.extend(z_order[1])
                    file_list.extend(z_order[2])
        print('Создаю каталоги', '                                                                ', end='\r')
        for name in folder_list:
            os.makedirs(f'{DESTINATION}/{name}', exist_ok=True)
        file_list_len = len(file_list)
        for name in file_list:
            p_name = name.rsplit("\\")
            print(f'Осталось скопировать: {file_list_len} файлов ({p_name[1]} - {p_name[-1]})     ', end='\r')
            shutil.copy2(f'{SOURCE}/{name}', f'{DESTINATION}/{name}')
            file_list_len -= 1
        c = TIMER
        while c != 0:
            print(f'Копирование завершено. Жду {c} секунд', '                          ', end='\r')
            time.sleep(1)
            c -= 1


if __name__ == '__main__':
    main()
