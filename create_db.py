import os.path
import sqlite3


def create_db():
    print('Creating database...')
    if not os.path.isdir('database'):
        os.mkdir('database')
    print('Create new folder "database"')
    conn = sqlite3.connect('database\\word_db.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE words
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, English text, Ukrainian text)
                   """)
    cursor.execute("""CREATE TABLE last_id (last_id INTEGER)""")
    cursor.execute("INSERT INTO last_id VALUES ('487');")   # Початкове значення встановлюється вручну
    conn.commit()
    conn.close()
    print("New database successfully created.")


def main():
    if not os.path.isfile('database/word_db.db'):
        print("The database does not exist.")
        create_db()
    else:
        print("The database already exists.")


if __name__ == '__main__':
    main()  # Виклик головної функції
