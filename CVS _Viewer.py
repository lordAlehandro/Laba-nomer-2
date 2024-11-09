import pandas as pd # Импортируем библиотеку pandas
import tkinter as tk # Импортируем библиотеку tkiner
from tkinter import ttk, filedialog, messagebox
import chardet  # Импортируем библиотеку chardet

class CSVDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer")
        
        self.data = None
        
        # Настройка адаптивности
        self.root.grid_rowconfigure(1, weight=1)  # Делаем строку с Treeview адаптивной
        self.root.grid_columnconfigure(0, weight=1)  # Делаем столбец адаптивным

        # Кнопка для загрузки CSV файла
        self.load_button = tk.Button(root, text="Загрузить CSV", command=self.load_csv, width=20)
        self.load_button.grid(row=0, column=0, pady=10, sticky="ew", padx=(10, 10))
        
        # Treeview для отображения данных
        self.tree = ttk.Treeview(root)
        self.tree.grid(row=1, column=0, pady=10, sticky="nsew")
        
        # Выпадающий список для выбора столбца
        self.column_selector = ttk.Combobox(root)
        self.column_selector.grid(row=2, column=0, pady=5, sticky="ew", padx=(10, 10))
        
        # Кнопка для нахождения среднего значения
        self.mean_button = tk.Button(root, text="Среднее значение", command=self.calculate_mean, width=20)
        self.mean_button.grid(row=3, column=0, pady=5, sticky="ew", padx=(10, 10))
        
        # Кнопка для нахождения минимального и максимального значений
        self.min_max_button = tk.Button(root, text="Мин/Макс значения", command=self.find_min_max, width=20)
        self.min_max_button.grid(row=4, column=0, pady=5, sticky="ew", padx=(10, 10))
        
        # Поле для фильтрации
        self.filter_entry = tk.Entry(root)
        self.filter_entry.grid(row=5, column=0, pady=5, sticky="ew", padx=(10, 10))
        
        self.filter_button = tk.Button(root, text="Фильтровать", command=self.filter_data, width=20)
        self.filter_button.grid(row=6, column=0, pady=5, sticky="ew", padx=(10, 10))

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            # Определение кодировки файла
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
            
            try:
                self.data = pd.read_csv(file_path, encoding=encoding)
                self.display_data()
                self.update_column_selector()  # Обновление выпадающего списка
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def display_data(self):
        # Очистка Treeview
        self.tree.delete(*self.tree.get_children())
        
        # Установка заголовков
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"
        
        # Настройка заголовков и их вырвнивание
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        
        # Заполнение Treeview данными
        for index, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def update_column_selector(self):
        # Обновление выпадающего списка с названиями столбцов
        self.column_selector['values'] = list(self.data.columns)
        if self.data.columns:
            self.column_selector.current(0)  # Устанавливаем первый столбец по умолчанию

    def calculate_mean(self):
        selected_column = self.column_selector.get()
        if selected_column in self.data.columns:
            mean_value = self.data[selected_column].mean()
            messagebox.showinfo("Среднее значение", f"Среднее значение для '{selected_column}': {mean_value}")
        else:
            messagebox.showerror("Ошибка", "Выберите корректный столбец.")

    def find_min_max(self):
        selected_column = self.column_selector.get()
        if selected_column in self.data.columns:
            min_value = self.data[selected_column].min()
            max_value = self.data[selected_column].max()
            messagebox.showinfo("Мин/Макс значения", f"Минимум: {min_value}, Максимум: {max_value}")
        else:
            messagebox.showerror("Ошибка", "Выберите корректный столбец.")

    def filter_data(self):
        filter_value = self.filter_entry.get()  
        if filter_value: 
        # Фильтруем данные, проверяя, содержится ли filter_value в любом из столбцов
            filtered_data = self.data[self.data.apply(lambda row: row.astype(str).str.contains(filter_value, na=False).any(), axis=1)]
    
            if filtered_data.empty:
                messagebox.showinfo("Результат фильтрации", "Совпадений не найдено.")
            else:
                self.data = filtered_data  # Обновление данных
                self.display_data()  # Отображаем отфильтрованные данные
        else:
            messagebox.showinfo("Ошибка", "Введите значение для фильтрации.")

# Цикл, который поддерживает работу Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVDataApp(root)
    root.mainloop()
