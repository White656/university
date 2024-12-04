import psycopg2
import re
import random
import string
import tkinter as tk
from tkinter import messagebox

# Параметры подключения к базе данных PostgreSQL
DB_HOST = 'localhost'
DB_NAME = 'mydatabase'
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'

# Регулярные выражения для проверки данных
name_regex = re.compile(r'^[A-Za-z\s]+$')
phone_regex = re.compile(r'^\+?\d{10,15}$')
city_regex = re.compile(r'^[A-Za-z\s]+$')


# Функция для генерации случайного пароля
def generate_password(length=10):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


# Функция для генерации почтового адреса
def generate_email(name):
    return name.lower().replace(" ", ".") + "@company.com"


# Функция для подключения к базе данных
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# Функция для очистки некорректных данных
def clear_invalid_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Чтение данных из таблицы employees
    cursor.execute("SELECT id, name, phone, city FROM employees")
    rows = cursor.fetchall()

    valid_data = []
    invalid_data = []

    for row in rows:
        id, name, phone, city = row
        if name and phone and city and name_regex.match(name) and phone_regex.match(phone) and city_regex.match(city):
            valid_data.append((id, name, phone, city))
        else:
            invalid_data.append((id, name, phone, city))

    # Перемещение корректных данных в таблицу cleaned_employees
    cursor.executemany("""
        INSERT INTO cleaned_employees (id, name, phone, city)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, valid_data)

    # Перемещение некорректных данных в таблицу invalid_data
    cursor.executemany("""
        INSERT INTO invalid_data (id, name, phone, city)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, invalid_data)

    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Готово", "Некорректные данные обработаны.")


# Функция для генерации почтовых адресов
def generate_emails():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email FROM cleaned_employees")
    rows = cursor.fetchall()

    for row in rows:
        id, name, email = row
        if not email:
            new_email = generate_email(name)
            cursor.execute("""
                UPDATE cleaned_employees
                SET email = %s
                WHERE id = %s
            """, (new_email, id))

    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Готово", "Почтовые адреса успешно добавлены.")


# Функция для генерации паролей
def generate_passwords():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, password FROM cleaned_employees")
    rows = cursor.fetchall()

    for row in rows:
        id, password = row
        if not password:
            new_password = generate_password()
            cursor.execute("""
                UPDATE cleaned_employees
                SET password = %s
                WHERE id = %s
            """, (new_password, id))

    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Готово", "Пароли успешно сгенерированы.")


# Создание интерфейса tkinter
root = tk.Tk()
root.title("Обработка данных сотрудников")

# Создание кнопок
btn_clear = tk.Button(root, text="Очистить некорректные значения", command=clear_invalid_data)
btn_clear.pack(pady=5)

btn_generate_emails = tk.Button(root, text="Сформировать почтовые адреса", command=generate_emails)
btn_generate_emails.pack(pady=5)

btn_generate_passwords = tk.Button(root, text="Сгенерировать пароли пользователей", command=generate_passwords)
btn_generate_passwords.pack(pady=5)

root.mainloop()
