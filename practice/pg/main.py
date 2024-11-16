import re
import random
import string
import psycopg2
from psycopg2 import sql
from tkinter import messagebox
import tkinter as tk

# Параметры подключения к PostgreSQL
conn_params = {
    'dbname': 'company_data',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}

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


# Функция для очистки некорректных данных
def clear_invalid_data():
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    # Выбор и удаление некорректных данных
    cursor.execute("""
        DELETE FROM employees
        WHERE NOT (name ~ %s AND phone ~ %s AND city ~ %s);
    """, (name_regex.pattern, phone_regex.pattern, city_regex.pattern))

    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Готово", "Некорректные данные удалены.")


# Функция для формирования почтовых адресов
def generate_emails():
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    # Обновление пустых значений Email
    cursor.execute("""
        UPDATE employees
        SET email = LOWER(REPLACE(name, ' ', '.')) || '@company.com'
        WHERE email IS NULL OR email = '';
    """)

    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Готово", "Почтовые адреса успешно добавлены.")


# Функция для генерации паролей
def generate_passwords():
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    # Обновление пустых значений Password
    cursor.execute("""
        SELECT id FROM employees WHERE password IS NULL OR password = '';
    """)
    ids = [row[0] for row in cursor.fetchall()]

    for emp_id in ids:
        cursor.execute("""
            UPDATE employees
            SET password = %s
            WHERE id = %s;
        """, (generate_password(), emp_id))

    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Готово", "Пароли успешно сгенерированы.")


# Создание интерфейса tkinter
root = tk.Tk()
root.title("Обработка данных в PostgreSQL")

# Создание кнопок
btn_clear = tk.Button(root, text="Очистить некорректные значения", command=clear_invalid_data)
btn_clear.pack(pady=5)

btn_generate_emails = tk.Button(root, text="Сформировать почтовые адреса", command=generate_emails)
btn_generate_emails.pack(pady=5)

btn_generate_passwords = tk.Button(root, text="Сгенерировать пароли пользователей", command=generate_passwords)
btn_generate_passwords.pack(pady=5)

root.mainloop()
