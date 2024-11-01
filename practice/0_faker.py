import csv
import os
from faker import Faker

# Инициализация Faker
fake = Faker()

# Путь к директории и файлу
directory = 'files'
filename = 'employees.csv'
file_path = os.path.join(directory, filename)


# Функция для генерации фиктивных данных с помощью Faker
def generate_initial_file(filepath, num_entries=1000):
    # Проверка, существует ли директория, и создание её, если нет
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Директория '{directory}' создана.")

    # Создание CSV файла с данными
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Name', 'Phone', 'City']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for _ in range(num_entries):
            # Генерация фиктивных данных с использованием Faker
            name = fake.name()
            phone = fake.phone_number()
            city = fake.city()

            writer.writerow({
                'Name': name,
                'Phone': phone,
                'City': city
            })

    print(f"Изначальный файл с фиктивными данными создан: {filepath}")


# Генерация файла с фиктивными данными
generate_initial_file(file_path)
