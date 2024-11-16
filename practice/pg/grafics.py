import psycopg2
import matplotlib.pyplot as plt

# Параметры подключения к PostgreSQL
conn_params = {
    'dbname': 'company_data',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}


# Подключение к базе данных и получение данных
def fetch_data(query):
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


# SQL-запрос для группировки сотрудников по городам
query = """
SELECT city, COUNT(*) as employee_count
FROM employees
GROUP BY city
ORDER BY employee_count DESC;
"""

# Получаем данные
data = fetch_data(query)

# Преобразуем данные в списки для построения графика
cities = [row[0] for row in data]
employee_counts = [row[1] for row in data]

# Построение графика
plt.figure(figsize=(10, 6))
plt.bar(cities, employee_counts, color='skyblue')
plt.xlabel('Город')
plt.ylabel('Количество сотрудников')
plt.title('Количество сотрудников по городам')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Отображение графика
plt.show()
