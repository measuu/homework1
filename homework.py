import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles
import pandas as pd

#Завдання 1

a = 5
b = 4

area = a * b

print(f"Площа прямокутника зі сторонами {a} та {b} дорівнює {area}.")

#Завдання 3

year = int(input("Введіть рік: "))

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"Рік {year} є високосним.")
else:
    print(f"Рік {year} не є високосним.")

# #Завдання 4

number = int(input("Введіть число для таблиці: "))

for i in range(1, 11):
    print(f"{number} * {i} = {number * i}")

#Завдання 5

number = 1
total = 0

while number <= 50:
    if number % 2 == 0:
        number += 1
        continue

    total += number
    number += 1

print(f"Сума непарних чисел від 1 до 50: {total}")

#Завдання 6

def create_full_name(first_name, last_name="Іванов"):
    return f"{last_name} {first_name}"


full_name1 = create_full_name(first_name="Петро", last_name="Петренко")
print(f"Повне ім'я: {full_name1}")

full_name2 = create_full_name(first_name="Олена")
print(f"Повне ім'я: {full_name2}")


assert full_name1 == "Петренко Петро"
assert full_name2 == "Іванов Олена"