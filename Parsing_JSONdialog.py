import datetime  # Модуль для отримання часу (для створення унікальних backup файлів)
import inspect  #
import json
import os.path  # Модулі за допомогою яких я створюю паки і отримую шлях до файлу з кодом
import shutil  # Модуль для копіювання файлів (для створення backup файла списку слів)
import sqlite3

# ============Условно глобальні змінні
JSON_FILE_NAME = 'result.json'
DIALOG_NAME = 'Рожище'
DB_NAME = 'word_db'
path = '\\database\\Backup\\'


def backup():
    file = inspect.getframeinfo(inspect.currentframe()).filename  #
    source_file_path = os.path.dirname(os.path.abspath(file))  # Визначаємо шлях до файла з виконуваним кодом
    if not os.path.exists(source_file_path + path):  # Перевіряємо чи існує папка Backup
        os.makedirs(source_file_path + path)  # Якщо ні, то створюємо її в директорії з виконуваним файлом
    time = get_time()
    backup_file_path = '{}{}{}_{}.db'.format(source_file_path, path, DB_NAME, time)  # Зберігаємо назву backup-файла
    shutil.copy2('{}\\database\\{}.db'.format(source_file_path, DB_NAME), backup_file_path)  # Копіюємо файл


def get_time():
    now = datetime.datetime.now()  # Отримуємо поточну дату і час
    time = '{}.{}.{}_{}.{}'.format(now.year, now.month, now.day, now.hour, now.minute) # Підганяємо під потрібний формат
    return time


def transfer_to_pair_list(lines):
    for iterator in range(len(lines)):
        index = lines[iterator].find('-')
        key = lines[iterator][:index - 1]
        value = lines[iterator][index + 2:-1]  # Якщо правою гранню зріза встановити -1 то буде братися рядок без \n
        lines[iterator] = [key, value]


def parsing_json(db_last_id):
    new_id = ''  # Змінна для зберігання id останнього збереженого повідомлення
    word_list = []  # Змінна для зберігання JSON-колекції
    file = open('JSON\\' + JSON_FILE_NAME, 'r',encoding='utf-8')  # Відкриваємо JSON файл
    content = json.load(file)
    chats_list = content['chats']['list']  # Отримуємо список всіх чатів
    for dialog in chats_list:  # Перебираємо список всіх чатів
        # Якщо ключ 'name' = 'Назва потрібного чату', то продовжуємо працювати з потрібним діалогом
        if dialog['name'] == DIALOG_NAME:
            message_list = dialog['messages']
            for message in message_list:  # Цикл для перебору всіх повідомлень
                if message['id'] > db_last_id:
                    word_list.append(str(message['text']) + '\n')
                    new_id = message['id']
    transfer_to_pair_list(word_list)  # Перетворюю список строк в список типу [key:value]
    return word_list, new_id


def main():  # Головна функція
    backup()  # Роблю бекап файлу з попереднім списком слів
    # ---
    conn = sqlite3.connect('database\\word_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM last_id")
    db_last_id = cursor.fetchall()
    db_last_id = db_last_id[0][0]
    print('data = ', db_last_id)
    word_list, new_id = parsing_json(db_last_id)
    # ---
    for i in word_list:
        cursor.execute("SELECT * FROM words WHERE English LIKE ?", (i[0],))
        result = cursor.fetchall()
        if result:
            print('i = ', i[0])
            print('result =', result)
        cursor.execute("INSERT INTO words (English, Ukrainian) VALUES (?,?)", (i[0], i[1],))
    if new_id:
        cursor.execute("UPDATE last_id SET last_id=? WHERE last_id=?", (new_id, db_last_id))
    conn.commit()
    conn.close()


# ============
if __name__ == '__main__':
    main()  # Виклик головної функції
