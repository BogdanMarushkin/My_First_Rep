import tkinter as tk
from tkinter import ttk, messagebox

class ShoppingListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список покупок")
        self.root.geometry("400x500")
        
        self.shopping_list = []
        
        # Создание виджетов
        self.create_widgets()
        
    def create_widgets(self):
        # Метка заголовка
        title_label = ttk.Label(self.root, text="Мой список покупок", 
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Метка инструкции
        instruction_label = ttk.Label(self.root, 
                                     text="Введите товар и нажмите 'Добавить' или Enter",
                                     font=("Arial", 10))
        instruction_label.pack(pady=5)
        
        # Поле ввода
        self.entry_frame = ttk.Frame(self.root)
        self.entry_frame.pack(pady=10, padx=20, fill="x")
        
        self.product_entry = ttk.Entry(self.entry_frame, font=("Arial", 12))
        self.product_entry.pack(side="left", fill="x", expand=True)
        self.product_entry.bind("<Return>", lambda e: self.add_product())
        
        # Кнопка добавления
        self.add_button = ttk.Button(self.entry_frame, text="Добавить",
                                     command=self.add_product)
        self.add_button.pack(side="left", padx=5)
        
        # Список покупок
        self.list_frame = ttk.LabelFrame(self.root, text="Ваш список:", padding=10)
        self.list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Прокручиваемый список
        self.listbox_frame = ttk.Frame(self.list_frame)
        self.listbox_frame.pack(fill="both", expand=True)
        
        # Scrollbar для списка
        scrollbar = ttk.Scrollbar(self.listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox для отображения списка
        self.listbox = tk.Listbox(self.listbox_frame, 
                                 font=("Arial", 11),
                                 yscrollcommand=scrollbar.set,
                                 selectbackground="#a6a6a6")
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Фрейм для кнопок управления
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)
        
        # Кнопка удаления выбранного элемента
        self.remove_button = ttk.Button(self.button_frame, text="Удалить выбранное",
                                        command=self.remove_selected)
        self.remove_button.pack(side="left", padx=5)
        
        # Кнопка очистки всего списка
        self.clear_button = ttk.Button(self.button_frame, text="Очистить все",
                                       command=self.clear_list)
        self.clear_button.pack(side="left", padx=5)
        
        # Кнопка копирования списка
        self.copy_button = ttk.Button(self.button_frame, text="Копировать список",
                                      command=self.copy_list)
        self.copy_button.pack(side="left", padx=5)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готово. Введите первый товар.")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var,
                                   relief="sunken")
        self.status_bar.pack(side="bottom", fill="x")
        
        # Установка фокуса на поле ввода
        self.product_entry.focus()
    
    def add_product(self):
        """Добавляет товар в список"""
        product = self.product_entry.get().strip()
        
        if not product:
            messagebox.showwarning("Пустой ввод", "Пожалуйста, введите название товара")
            return
            
        if product in self.shopping_list:
            messagebox.showinfo("Товар уже есть", f"'{product}' уже есть в списке")
            self.product_entry.select_range(0, tk.END)
            return
        
        # Добавляем в список
        self.shopping_list.append(product)
        
        # Добавляем в listbox
        self.listbox.insert(tk.END, f"• {product}")
        
        # Обновляем статус
        self.status_var.set(f"Добавлено: {product}. Всего товаров: {len(self.shopping_list)}")
        
        # Очищаем поле ввода и устанавливаем фокус
        self.product_entry.delete(0, tk.END)
        self.product_entry.focus()
    
    def remove_selected(self):
        """Удаляет выбранный товар из списка"""
        try:
            # Получаем индекс выбранного элемента
            selection = self.listbox.curselection()[0]
            product = self.shopping_list[selection]
            
            # Удаляем из обоих списков
            del self.shopping_list[selection]
            self.listbox.delete(selection)
            
            # Обновляем статус
            self.status_var.set(f"Удалено: {product}. Всего товаров: {len(self.shopping_list)}")
            
        except IndexError:
            messagebox.showwarning("Не выбран товар", 
                                 "Пожалуйста, выберите товар для удаления")
    
    def clear_list(self):
        """Очищает весь список"""
        if not self.shopping_list:
            return
            
        if messagebox.askyesno("Очистить список", 
                              "Вы уверены, что хотите очистить весь список?"):
            self.shopping_list.clear()
            self.listbox.delete(0, tk.END)
            self.status_var.set("Список очищен. Всего товаров: 0")
    
    def copy_list(self):
        """Копирует список в буфер обмена"""
        if not self.shopping_list:
            messagebox.showinfo("Пустой список", "Список покупок пуст")
            return
            
        # Формируем текст для копирования
        list_text = "Мой список покупок:\n"
        list_text += "\n".join([f"{i+1}. {item}" for i, item in enumerate(self.shopping_list)])
        
        # Копируем в буфер обмена
        self.root.clipboard_clear()
        self.root.clipboard_append(list_text)
        self.root.update()
        
        self.status_var.set("Список скопирован в буфер обмена!")
        messagebox.showinfo("Скопировано", "Список покупок скопирован в буфер обмена")

def main():
    root = tk.Tk()
    app = ShoppingListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()