import asyncio
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import whisper
import threading
import time
import re
from num2words import num2words

class Windows(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Loading...")
        self.geometry("150x50")

        self.value_var = IntVar()

        self.progressbar = ttk.Progressbar(self, orient="horizontal", variable=self.value_var, mode="indeterminate")
        self.progressbar.pack(fill=X, padx=6, pady=6)

        self.progressbar.start()

    def button_clicked(self):
        self.destroy()


def replace_numbers_with_words(text):
    def replace(match):
        number = int(match.group(0))
        return num2words(number, lang='ru')
    return re.sub(r'\b\d+\b',replace,text)

def replace_words(text,replace):
    for old, new in replace.items():
        text = text.replace(old,new)
    return text

word_array  = {
    'блять':'блядь',
}

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3 *.flac *.aac *.ogg *.wma")])
    if filepath:
        window = Windows(root)
        threading.Thread(target=process_file, args=(filepath, window)).start()


def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes}:{seconds:05.2f}"


def process_file(filepath, window):
    start_time = time.time()
    try:
        model_type = selected_method.get()
        language = selected_language.get()
        model = whisper.load_model(model_type)

        try:
            result = model.transcribe(filepath, language=language, fp16=False, verbose=True)
        except RuntimeError as e:
            messagebox.showinfo("Error", f"{e}")
            return

        segments = result["segments"]
        ## Результат с  временем
        ##text_with_timestamps = "\n".join([f"[{format_time(segment['start'])} - {format_time(segment['end'])}] {segment['text']}" for segment in segments])

        text_result = "\n".join([f"{segment['text']}" for segment in segments])

        text_editor.delete("1.0", END)
        ## Таймер
        ##text_editor.insert("1.0", text_with_timestamps)

        text_update_rep = text_result.replace('Короче', 'блять')
        replace_num = replace_numbers_with_words(text_update_rep)
        replace_word = replace_words(replace_num,word_array)
        text_update = replace_word

        text_editor.insert("1.0", text_update.lower())



        ##text_editor.insert("1.0", segment)

        end_time = time.time()

        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60

        messagebox.showinfo("Время обработки", f"Обработка файла заняла {minutes} минут {seconds:.1f} секунд")


    except Exception as e:
        messagebox.showinfo("Ошибка", f"{e}")

    finally:
        window.destroy()

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filepath:
        text = text_editor.get("1.0", END)
        with open(filepath, "w") as file:
            file.write(text)

def copy_text():
    root.clipboard_clear()
    root.clipboard_append(text_editor.get("1.0", "end-1c"))
   #messagebox.showinfo("Информация", "Текст скопирован в буфер обмена")

def clear_windows():
    text_editor.delete("1.0",END)

root = Tk()
root.title("SoundScript")
root.geometry("1000x550")


frame = ttk.Frame(root, width=170)
frame.grid(column=2, row=0, sticky=NE)

frame2 = ttk.Frame(root,width=70,height=300)
frame2.grid(column=2, row=0, sticky=NE,pady=150)

frame3 = ttk.Frame(root,width=270,height=100)
frame3.grid(column=2,row=0,stic=S)

methods = [
    {"name": "small", "display": "Малый"},
    {"name": "base", "display": "Базовый"},
    {"name": "medium", "display": "Средний"},
    {"name": "large", "display": "Большой"},
    {"name": "large-v2", "display": "Большой-V2"},
    {"name": "large-v3", "display": "Большой-V3"},
]

languages = [
    {"code": "ru", "name": "Russian", "display": "Русский"},
    {"code": "en", "name": "English", "display": "Английский"},
    {"code": "uk", "name": "Ukrainian", "display": "Украинский"},
    {"code": "bg", "name": "Bulgarian", "display": "Болгарский"},
    {"code": "it", "name": "Italian", "display": "Итальянский"},
    {"code": "ro", "name": "Romanian", "display": "Румынский"},
    {"code": "tr", "name": "Turkish", "display": "Турецкий"},
    {"code": "pl", "name": "Polish", "display": "Польский"}
]

selected_method = StringVar(value=methods[2]["name"])


header = ttk.Label(frame, text="Выберите алгоритм")
header.pack(anchor=N)

for method in methods:
    mth_btn = ttk.Radiobutton(frame, text=method["display"], value=method["name"], variable=selected_method)
    mth_btn.pack(anchor=NW)

selected_language = StringVar(value=languages[0]["code"])

header_lang = ttk.Label(frame2, text="Выберите язык аудио")
header_lang.pack(anchor=S)



for lang in languages:
    lang_btn = ttk.Radiobutton(frame2, text=lang["display"], value=lang["code"], variable=selected_language)
    lang_btn.pack(anchor=NW)

clear_windows = ttk.Button(frame3,text="Очистить окно",command=clear_windows)
clear_windows.pack(anchor=CENTER)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

text_editor = Text(root, wrap=WORD)
text_editor.grid(column=0, columnspan=2, row=0, sticky=NSEW)

open_button = ttk.Button(root, text="Открыть файл", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10, pady=10)

save_button = ttk.Button(root, text="Сохранить файл", command=save_file)
save_button.grid(column=1, row=1, sticky=NSEW, padx=10, pady=10)

save_text = ttk.Button(root, text="Скопировать текст", command=copy_text)
save_text.grid(column=2, row=1, sticky=NSEW, padx=10, pady=10)


root.mainloop()
