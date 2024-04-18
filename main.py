import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

checkActive = False

def finish():
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Файл мониторинга изменен\nЗакрытие приложения")

def click_button():
    global checkActive

    if checkActive == False:
        btn["text"] = f"Остановка мониторинга" # изменяем текст на кнопке
        text.insert("1.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Запуск мониторинга дирректории:" + path.get() + "\n")
        
        observer.start()
        observer.schedule(handler, path=path.get(), recursive=True)

        with open("monitoring.txt", "a") as file:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Запуск мониторинга дирректории:" + path.get(), file=file)
        
        checkActive = True
    else:
        btn["text"] = f"Запуск мониторинга"
        text.insert("1.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Остановка мониторинга дирректории:" + path.get() + "\n")

        observer.stop()

        with open("monitoring.txt", "a") as file:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Остановка мониторинга дирректории:" + path.get(), file=file)

        checkActive = False

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        text.insert("1.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" В файл [{event.src_path.split('\\')[-1]}] внесли изменения по пути [{event.src_path}]\n", "blue")

        with open("monitoring.txt", "a") as file:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" В файл [{event.src_path.split('\\')[-1]}] внесли изменения по пути [{event.src_path}]", file=file)

    def on_deleted(self, event):
        text.insert("1.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" Удален файл [{event.src_path.split('\\')[-1]}] по пути [{event.src_path}]\n", "red")

        with open("monitoring.txt", "a") as file:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" Удален файл [{event.src_path.split('\\')[-1]}] по пути [{event.src_path}]", file=file) 

    def on_created(self, event):
        text.insert("1.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" Создан файл [{event.src_path.split('\\')[-1]}] по пути [{event.src_path}]\n", "green")

        with open("monitoring.txt", "a") as file:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" Создан файл [{event.src_path.split('\\')[-1]}] по пути [{event.src_path}]", file=file)
    
    def on_moved(self, event):
        text.insert("1.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" Изменено название файла [{event.src_path.split('\\')[-1]}] по пути [{event.src_path}]\n", "blue")

        with open("monitoring.txt", "a") as file:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" Изменено название файла [{event.src_path.split('\\')[-1]}] по пути [{event.src_path}]", file=file)

handler = MyHandler()
observer = Observer()

root = Tk() # создаем корневой объект - окно
root.title("Мониторинг обращений к файловой системе") # заголовок окна
root.geometry("560x300")    # размеры окна
root.resizable(False, False) # нельзя менять размер окна

root.protocol("WM_DELETE_WINDOW", finish) # вызов метода при закрытии приложения

path = StringVar()

label = ttk.Label(text="Укажите путь к нужной дирректории") # создаем текстовую метку
label.pack(anchor=NW, padx=6, pady=6)    # размещаем метку в окне

path_folder = ttk.Entry(textvariable=path, width="200")
path_folder.pack(anchor=NW, padx=6, pady=6)

btn = ttk.Button(text="Запуск мониторинга", command=click_button) # создаем кнопку из пакета tkinter
btn.pack(anchor=NW, padx=6, pady=6) # размещаем кнопку в окне
 
text = ScrolledText(root, width=50,  height=10) # создаем многострочное текстовое поле с вертикальной полосой прокрутки
text.pack(fill=BOTH, side=LEFT, expand=True)

# создаем теги red,gree,blue и прикрепляем его к символам 1.0
text.tag_add("red", "1.0")
text.tag_add("green", "1.0")
text.tag_add("blue", "1.0")
# устанавливаем стили тегов red,gree,yellow
text.tag_configure("red", background="#fff", foreground="red", font="TkFixedFont", relief="raised")
text.tag_configure("green", background="#fff", foreground="green", font="TkFixedFont", relief="raised")
text.tag_configure("blue", background="#fff", foreground="blue", font="TkFixedFont", relief="raised")

root.mainloop()