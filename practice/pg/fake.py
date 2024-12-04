import psycopg2
from faker import Faker
import random

# Параметры подключения к PostgreSQL
conn_params = {
    'dbname': 'company_data',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Инициализация Faker
fake = Faker()


# Функция для генерации некорректных данных
def generate_invalid_data():
    name = random.choice([
        fake.name(),  # корректное имя
        str(fake.random_int()),  # числовое значение
        fake.text(max_nb_chars=10),  # случайная строка
        '',  # пустая строка
        None  # значение NULL
    ])
    phone = random.choice([
        fake.phone_number()[:15],  # Обрезаем номер до 15 символов
        '12345',  # слишком короткий
        'abcdef',  # буквы вместо цифр
        '',  # пустая строка
        None  # значение NULL
    ])
    city = random.choice([
        fake.city(),  # корректный город
        '12345',  # числовое значение
        None,  # значение NULL
        ''  # пустая строка
    ])
    email = random.choice([
        fake.email(),  # корректный email
        'invalid-email',  # некорректный email
        '',  # пустая строка
        None  # значение NULL
    ])
    password = random.choice([
        fake.password(),  # корректный пароль
        None  # значение NULL
    ])

    # Убедимся, что `name` не NULL или пустое
    if not name or name.strip() == '':
        name = 'Unknown'

    return name, phone, city, email, password


# Функция для наполнения базы данных некорректными данными
def populate_invalid_data(records=50):
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    for _ in range(records):
        name, phone, city, email, password = generate_invalid_data()

        # Вставка данных в таблицу
        cursor.execute("""
            INSERT INTO employees (name, phone, city, email, password)
            VALUES (%s, %s, %s, %s, %s);
        """, (name, phone, city, email, password))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{records} записей с некорректными данными успешно добавлено.")


# Запуск программы
if __name__ == "__main__":
    records_to_insert = 150  # Количество записей для генерации
    populate_invalid_data(records_to_insert)
