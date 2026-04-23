import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json
import os

# Путь к файлу с избранными
FAV_FILE = "favorites.json"

# Загрузка избранных пользователей
def load_favorites():
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение избранных
def save_favorites(favorites):
    with open(FAV_FILE, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, ensure_ascii=False, indent=4)

# Вызов API для поиска пользователя
def search_user():
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите имя пользователя.")
        return
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 404:
        messagebox.showerror("Не найдено", "Пользователь не найден.")
        return
    if response.status_code != 200:
        messagebox.showerror("Ошибка API", "Ошибка при соединении с GitHub API.")
        return
    user_data = response.json()
    display_user(user_data)

# Отображение результатов
def display_user(user):
    listbox.delete(0, tk.END)
    info = f"Имя: {user.get('name', 'Нет')}\n" \
           f"Логин: {user['login']}\n" \
           f"Репозитории: {user['public_repos']}\n" \
           f"Ссылка: {user['html_url']}"
    listbox.insert(tk.END, info)
    # Сохраняем текущих для добавления в избранное
    global current_user
    current_user = user

# Добавление в избранное
def add_to_favorites():
    global current_user
    if 'current_user' in globals():
        favorites = load_favorites()
        if any(u['login'] == current_user['login'] for u in favorites):
            messagebox.showinfo("Информация", "Этот пользователь уже в избранных.")
            return
        favorites.append(current_user)
        save_favorites(favorites)
        messagebox.showinfo("Успех", "Пользователь добавлен в избранное.")
    else:
        messagebox.showwarning("Ошибка", "Нет выбранного пользователя.")

# Загрузка favorites при старте
favorites_list = load_favorites()

# Создание GUI
root = tk.Tk()
root.title("GitHub User Finder")

# Поле поиска
tk.Label(root, text="Введите имя пользователя GitHub:").pack(padx=10, pady=5)
entry_search = tk.Entry(root, width=40)
entry_search.pack(padx=10)

# Кнопка поиска
btn_search = tk.Button(root, text="Поиск", command=search_user)
btn_search.pack(padx=10, pady=5)

# Область отображения результата
listbox = tk.Listbox(root, width=80, height=8)
listbox.pack(padx=10, pady=5)

# Кнопки добавления в избранное
btn_add_fav = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_add_fav.pack(padx=10, pady=5)

# Запуск
root.mainloop()
