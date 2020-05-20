import requests
import json
from board import board_id

long_board_id = 0

base_url = "https://api.trello.com/1/{}"
config_path = "../trello.cfg"

auth_params = None

width_ = 77
jobs_list = []

def getJSONdata(filename):
	"""получаем конфигурационные данные из файла
    в файле данные хранятся в виде"""
	fileJSON = open(filename)
	dataRaws = fileJSON.readlines()
	return json.loads(dataRaws[0])

def read():
    """Получаем список всех столбцов и заданий в столбцах,
    чтобы изначально избежать проблем с дубликатами названий как заданий
    так и столбцов, формируем список словарей, в которые сохраняем уникальные
    id и столбцов, и уникальные id всех заданий, при этом создаем сквозную
    нумерацию от 1++ для отображения всех элементов на экране, в таком варианте
    у нас будет однозначная связь: 'номер на экране' - id"""
    global jobs_list
    if jobs_list:
        jobs_list = []
    column_data = requests.get(f"{base_url.format('boards')}/{board_id}/lists",params=auth_params).json()
    index_ = 1
    column_idx = 1
    for column in column_data:
        tasks_ = []
        task_data = requests.get(f"{base_url.format('lists')}/{column['id']}/cards",params=auth_params).json()
        if not task_data:
            tasks_ = []
        else:
            for task in task_data:
                tasks_.append({"list_id":index_, "id":task['id'],"name":task['name']})
                index_ += 1
        jobs_list.append({"list_column_idx":column_idx, "id":column['id'], 'name':column['name'],"tasks":tasks_})
        column_idx +=1

def get_long_board_id():
    response = requests.get(base_url.format('boards/' + board_id), params=auth_params).json()
    return response['id']

def create_column(column_name):
    requests.post(base_url.format('lists'), data = {'name':column_name, 'idBoard': long_board_id, **auth_params})

def create(name, column_id):
    requests.post(base_url.format('cards'), data={'name':name, 'idList':column_id, **auth_params})

def move(task_id, column_id):
    requests.put(f"{base_url.format('cards')}/{task_id}/idList",data={'value': column_id, **auth_params})

def get_column_id_by_list_id(list_id):
    """получаем реальный id столбца по номеру в списке, если столбец не найден возвращаем False"""
    for jobs in jobs_list:
        if jobs['list_column_idx']==list_id:
            return jobs['id']
    return False

def get_task_id_by_list_id(list_id):
    """получаем реальный id задания по номеру в списке, если не найден возвращаем False"""
    for jobs in jobs_list:
        for job in jobs['tasks']:
            if job['list_id']==list_id:
                return job['id']
    return False

def main_menu(printJobsList):
    # --- выводим заголовок
    print('\n'*15) # сдвинем вывод в окне, чтобы не прилипать к предыдущему выводу
    print(f'+{"="*25}{"+"}{"="*25}{"+"}{"="*25}+')
    print(f'| L - Показать все задачи |   A - Добавить задачу   |   M - Изменить задачу   |')
    print(f'|{"-"*25}{"+"}{"-"*25}{"+"}{"-"*25}|')
    print(f'| C - Добавить столбец    |   R - Обновить список   |   Q - Выход             |')
    print(f'+{"="*25}{"+"}{"="*25}{"+"}{"="*25}+')
    # --- конец заголовка, дальше выводим список столбцов и задач в столбцах, полученных read()
    lines_count = 0
    if not printJobsList:
        print('\n'*16) # если список пуст просто выводим меню, это такая очистка экрана
    else:
        #вывод списка столбцов и задач в столбцах, добавим немножк форматирования, для красоты
        for jobs in printJobsList:
            str_column = f"| {jobs['list_column_idx']} - {jobs['name']}, задач: {len(jobs['tasks'])}"
            print(f"{str_column}{' '*(width_ - len(str_column)+1)}|")
            if len(jobs['tasks'])==0:
                print(f"|{' '*77}|")
            for task in jobs['tasks']:
                print(f"|     {task['list_id']} - {task['name']}{' '*(width_ - len(str(task['list_id'])) - len(task['name']) - 8)}|")
                lines_count +=1
            print(f"|{' '*77}|")
            lines_count += 2
        if lines_count <15:
            print("\n"*(15-lines_count-1))
    # под телом вывода, выведем футер с подсказкой команды для выхода
    print(f'\n+{"="*77}+')
    print(f"| Для завершения работы введите: q{' '*44}|")
    print(f'+{"="*77}+')

if __name__ == "__main__":
    try:
        auth_params = getJSONdata(config_path)
    except:
        print('Ошибка доступа к файлу конфигурации!\nСоздайте правильный конфигурационный файл!')
        exit()
    command_ = None
    long_board_id = get_long_board_id()
    main_menu([])
    read()
    while True:
        command_ = input("Введите команду:")
        if command_ == "L":
            main_menu(jobs_list)
        elif command_ =="A":
            # Добавляем новое задание
            print('Добавим новое задание!')
            column_id_ = input('Выберите столбец (номер слева от названия столбца): ')
            task_name_ = input('Введите задание (текст задания): ')
            try:
                column_id_ = int(column_id_)
            except:
                print('Ошибка! Такого столбца нет!')
                input()
            else:
                print('Добавляю...')
                column_id_ = get_column_id_by_list_id(column_id_)
                if column_id_:
                    create(task_name_, column_id_)
                    print('Обновляю...')
                    read()
                else:
                    print('Ошибка! такого столбца нет!')
                    input()                
                main_menu(jobs_list)
        elif command_ == "M":
            # Переместить задиние (какбэ изменяем)
            print('Перемещаем задание!')
            task_id_ = input('Выберите задание (номер слева от названия задания): ')
            column_id_ = input('Выберите целевой столбец (номер слева от названия столбца), куда переместить столбец: ')
            try:
                column_id_ = int(column_id_)
            except:
                print('Ошибка! Неверный столбец!')
            else:
                try:
                    task_id_ = int(task_id_)
                except:
                    print('Ошибка! Неверное задание')
                else:
                    print('Перемещаем...')
                    column_id_ = column_id_ = get_column_id_by_list_id(column_id_)
                    if not column_id_:
                        print('Отмена! Такого столбца нет!')
                        input()
                    else:
                        task_id_ = get_task_id_by_list_id(task_id_)
                        if task_id_:
                            move(task_id_, column_id_)
                            read()
                        else:
                            print('Отмена! Такой задачи нет!')
                            input()
                    main_menu(jobs_list)
        elif command_ == "C":
            column_name_ = input("Введите название новой колонки: ")
            print("Добавляю столбец...")
            create_column(column_name_)
            read()
            main_menu(jobs_list)
        elif command_ == "R":
            read()
            main_menu(jobs_list)
        elif command_ in ["q", "Q"]:
            break
        else:
            main_menu([])
