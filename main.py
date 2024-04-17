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
        observer.schedule(handler, path=str(path.get()), recursive=True)

        with open("monitoring.txt", "a") as file:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Запуск мониторинга дирректории:" + path.get(), file=file)
        
        checkActive = True
    else:
        btn["text"] = f"Запуск мониторинга"
        text.insert("1.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Остановка мониторинга дирректории:" + path.get() + "\n")
        observer.stop()
        observer.join()
        checkActive = False

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"Событие {event.event_type} по пути {event.src_path}")
        text.insert("1.0", datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" Событие {event.event_type} по пути {event.src_path}\n")

        with open("monitoring.txt", "a") as file:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f"Событие {event.event_type} по пути {event.src_path}", file=file)

    def on_deleted(self, event):
        print(f"Событие {event.event_type} по пути {event.src_path}") 

    def on_created(self, event):
        print(f"Событие {event.event_type} по пути {event.src_path}")
    
    def on_moved(self, event):
        print(f"Событие {event.event_type} по пути {event.src_path}")

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

root.mainloop()