import tkinter as tk
from tkinter import messagebox
from faker import Faker

mapper = {
    '01': 'январь',
    '02': 'февраль',
    '03': 'март',
    '04': 'апрель',
    '05': 'май',
    '06': 'июнь',
    '07': 'июль',
    '08': 'август',
    '09': 'сентябрь',
    '10': 'октябрь',
    '11': 'ноябрь',
    '12': 'декабрь'
}

fake = Faker()


def generate_data():
    try:
        number = int(entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please, input correct numeric value.")
        return

    r_month = fake.month()
    month_name = mapper.get(r_month)

    data = {
        'count': number,
        'data': [generate_random_personal_data() for _ in range(number)]
    }

    result_names = []
    for value in data['data']:
        name, day, month = value.split()
        if month == r_month:
            result_names.append(name)

    result_text = f"Random month: {month_name}\nName: {' '.join(result_names)}"
    messagebox.showinfo("Result", result_text)


def generate_random_personal_data():
    name = fake.name().split()[0]
    date = fake.date(pattern="%d %m")
    return f"{name} {date}"


root = tk.Tk()
root.title("Generator")

label = tk.Label(root, text="Input number value:")
label.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="Generate", command=generate_data)
button.pack(pady=20)

root.mainloop()
