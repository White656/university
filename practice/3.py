import tkinter as tk
from tkinter import messagebox
from faker import Faker
from collections import Counter
import random
import string


def generate_text(paragraphs, sentences_per_paragraph, num_numbers: int, include_digits=False):
    fake = Faker()
    text = ""

    for _ in range(paragraphs):
        paragraph = " ".join(fake.sentence() for _ in range(sentences_per_paragraph))
        if include_digits:
            for _ in range(random.randint(1, 100)):
                position = random.randint(0, num_numbers)
                digit = random.choice(string.digits)
                paragraph = paragraph[:position] + digit + paragraph[position:]
        text += paragraph + "\n\n"

    return text


def analyze_text(text):
    letter_counts = Counter()
    digit_counts = Counter()

    for item in text:
        if item.isalpha():
            letter_counts[item.lower()] += 1
        elif item.isdigit():
            digit_counts[item] += 1

    most_common_letter = letter_counts.most_common(1)
    most_common_digit = digit_counts.most_common(1)

    total_letters = sum(letter_counts.values())
    total_digits = sum(digit_counts.values())

    result = ""
    if most_common_letter:
        result += f"Наиболее часто встречающаяся буква: '{most_common_letter[0][0]}' с количеством {most_common_letter[0][1]}\n"
    else:
        result += "Буквы в тексте отсутствуют.\n"

    if most_common_digit:
        result += f"Наиболее часто встречающаяся цифра: '{most_common_digit[0][0]}' с количеством {most_common_digit[0][1]}\n"
    else:
        result += "Цифры в тексте отсутствуют.\n"

    if total_letters > total_digits:
        result += f"Букв больше: {total_letters} против {total_digits}\n"
    elif total_digits > total_letters:
        result += f"Цифр больше: {total_digits} против {total_letters}\n"
    else:
        result += f"Количество букв и цифр одинаково: {total_letters}\n"

    return result


def on_generate():
    try:
        paragraphs = int(paragraphs_entry.get())
        sentences = int(sentences_entry.get())
        numbers = int(number_entry.get())
        include_digits = digits_var.get()

        generated_text = generate_text(paragraphs, sentences, numbers, include_digits)

        with open('files/in.txt', 'w', encoding='utf-8') as file:
            file.write(generated_text)

        analysis_result = analyze_text(generated_text)
        with open('files/out.txt', 'w', encoding='utf-8') as file:
            file.write(analysis_result)
        messagebox.showinfo("Результаты анализа", analysis_result)
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числа.")


root = tk.Tk()
root.title("Генератор текста")

tk.Label(root, text="Количество абзацев:").grid(row=0, column=0)
paragraphs_entry = tk.Entry(root)
paragraphs_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Количество предложений:").grid(row=1, column=0)
sentences_entry = tk.Entry(root)
sentences_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Количество цифр:").grid(row=2, column=0)
number_entry = tk.Entry(root)
number_entry.grid(row=2, column=1)

digits_var = tk.BooleanVar()
tk.Checkbutton(root, text="Добавить цифры", variable=digits_var).grid(row=3, column=0, columnspan=2, pady=10)

tk.Button(root, text="Сгенерировать и проанализировать", command=on_generate).grid(row=4, column=0, columnspan=2,
                                                                                   pady=20)

root.mainloop()
