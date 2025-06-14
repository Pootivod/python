import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Моё первое приложение на Tkinter")
root.geometry("400x300") 

def on_button_click():
    messagebox.showinfo("Привет!", "Вы нажали на кнопку!")

# Надпись
label = tk.Label(root, text="Добро пожаловать в приложение!", font=("Arial", 14))
label.pack(pady=20)

# Кнопка
button = tk.Button(root, text="Нажми меня", command=on_button_click)
button.pack(pady=10)

# Запуск главного цикла приложения
root.mainloop()
