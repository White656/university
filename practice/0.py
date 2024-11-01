import csv
import re
import random
import string
import tkinter as tk
from tkinter import messagebox

# Путь к файлам
input_file = 'files/employees.csv'
output_file = 'files/cleaned_employees.csv'
invalid_data_file = 'files/invalid_data.txt'

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
    valid_data = []
    invalid_data = []

    with open(input_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name'].strip()
            phone = row['Phone'].strip()
            city = row['City'].strip()

            if (name_regex.match(name) and phone_regex.match(phone) and city_regex.match(city)):
                valid_data.append(row)
            else:
                invalid_data.append(row)

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Name', 'Phone', 'City', 'Email', 'Password']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid_data)

    with open(invalid_data_file, mode='w', encoding='utf-8') as file:
        for row in invalid_data:
            file.write(f"{row}\n")

    messagebox.showinfo("Готово", "Некорректные данные удалены и записаны в отдельный файл.")

# Функция для формирования почтовых адресов
def generate_emails():
    data = []

    with open(output_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'Email' not in row or not row['Email']:
                row['Email'] = generate_email(row['Name'])
            data.append(row)

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Name', 'Phone', 'City', 'Email', 'Password']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    messagebox.showinfo("Готово", "Почтовые адреса успешно добавлены.")

# Функция для генерации паролей
def generate_passwords():
    data = []

    with open(output_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'Password' not in row or not row['Password']:
                row['Password'] = generate_password()
            data.append(row)

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Name', 'Phone', 'City', 'Email', 'Password']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    messagebox.showinfo("Готово", "Пароли успешно сгенерированы.")

# Создание интерфейса tkinter
root = tk.Tk()
root.title("Обработка CSV-файлов")

# Создание кнопок
btn_clear = tk.Button(root, text="Очистить некорректные значения", command=clear_invalid_data)
btn_clear.pack(pady=5)

btn_generate_emails = tk.Button(root, text="Сформировать почтовые адреса", command=generate_emails)
btn_generate_emails.pack(pady=5)

btn_generate_passwords = tk.Button(root, text="Сгенерировать пароли пользователей", command=generate_passwords)
btn_generate_passwords.pack(pady=5)

root.mainloop()