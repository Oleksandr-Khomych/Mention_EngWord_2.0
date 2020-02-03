import sqlite3
import random


def from_english(word):
    question = word[1]
    answer = word[2]
    return question, answer


def from_ukraine(word):
    question = word[2]
    answer = word[1]
    return question, answer

def main():
    conn = sqlite3.connect('database\\word_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words")
    lines = cursor.fetchall()
    length = len(lines)
    # ---
    mode = input('Ukrainian => English press 1\nEnglish => Ukrainian press 2\n')
    print("======================================\n")
    count = 0  # Лічильник повторених слів
    while count < length:
        print("=============== Amount of repeating word: {} of {}\n".format(count, length))
        count += 1
        word = random.choice(lines)
        lines.remove(word)
        if mode == '1':
            question, answer = from_ukraine(word)
        else:
            question, answer = from_english(word)
        print('Please enter a translation : {}'.format(question))
        input()
        print('Right answer : {}'.format(answer))
    # ---
    conn.close()


if __name__ == '__main__':
    main()  # Виклик головної функції


'''
def add_new():
    conn = sqlite3.connect('database\\word_db.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO words (English, Ukrainian) VALUES ('Tom', 'Том');")
    cursor.execute("INSERT INTO words (English, Ukrainian) VALUES ('Tom2','Том2');")
    cursor.execute("INSERT INTO words (English, Ukrainian) VALUES ('Tom3','Том3');")
    conn.commit()
    conn.close()
'''