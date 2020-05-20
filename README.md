# Консольный клиент для Trello
##### Описание
Простой клиент для доступа к доскам Trello, позволяет:
* отображать список столбцов и заданий в них
* Добавлять колонки
* добавлять задания в столбцы
* перемещать задания между столбцами
* поддерживает работу с одинаковыми названиями как столбцов так и колонок

##### Установка и запуск
* скачать архивом
* распаковать архив
* перейти полученную папку
* установить зависимости (requirements.txt)
* заполнить данные в файлах:
  * board.py - короткий board_id доски - из ссылки после входа в доску trello, long_board_id - получается из ссылки после входа в доску trello, путем дописывания .json в строку адреса, в json-ответе сервера, первым полем будет длинный id
  * trello.cfg - json-файл с авторизационными данными для trello, key и token, получить можно на сайте trello, инструкции на сайте.
* запустить скрипт в python версии 3:<br>
  python trello.py<br>
или<br>
  python3 trello.py<br>
  