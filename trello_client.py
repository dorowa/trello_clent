import requests
import sys
import json

base_url = "https://api.trello.com/1/{}"
config_path = "../trello.cfg"
board_id = "pF5Bin10"

auth_params = None

def getJSONdata(filename):
	"""получаем данные из файла"""
	fileJSON = open(filename)
	dataRaws = fileJSON.readlines()
	return json.loads(dataRaws[0])

def read():
    column_data = requests.get(f"{base_url.format('boards')}/{board_id}/lists",params=auth_params).json()
    for column in column_data:
        print(column['name'])
        task_data = requests.get(f"{base_url.format('lists')}/{column['id']}/cards",params=auth_params).json()
        if not task_data:
            print(f'\t {"Нет задач"}')
            continue
        for task in task_data:
            print(f"\t {task['name']}")
def create(name, column_name):
    column_data = requests.get(f"{base_url.format('boards')}/{board_id}/lists",params=auth_params).json()
    for column in column_data:
        if column['name']==column_name:
            requests.post(base_url.format('cards'), data={'name':name, 'idList':column['id'], **auth_params})
            break

def move(name, column_name):
    column_data = requests.get(f"{base_url.format('boards')}/{board_id}/lists",params=auth_params).json()
    task_id = None
    for column in column_data:
        column_tasks = requests.get(f"{base_url.format('lists')}/{column['id']}/cards",params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break
    for column in column_data:
        if column['name'] == column_name:
            requests.put(f"{base_url.format('cards')}/{task_id}/idList",data={'value': column['id'], **auth_params})
            break

if __name__ == "__main__":
    auth_params = getJSONdata(config_path)
    if len(sys.argv)<=3:
        read()
    elif sys.argv[1]=='create':
        create(sys.argv[2],sys.argv[3])
    elif sys.argv[1]=='move':
        move(sys.argv[2], sys.argv[3])
    else:
        print('Неверный аргумент')
