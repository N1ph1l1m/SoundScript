import asyncio
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import whisper
import threading
import time

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


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3 *.flac *.aac *.ogg *.wma")])
    if filepath:
        window = Windows(root)
        threading.Thread(target=process_file, args=(filepath, window)).start()


def process_file(filepath, window):
    start_time = time.time()  # Начинаем измерение времени
    try:
        model_type = selected_method.get()
        language = selected_language.get()
        print(f"model_type = {model_type}  \n language =  {language}")
        model = whisper.load_model(model_type)

        try:
            result = model.transcribe(filepath, language=language, fp16=True, verbose=True)
        except RuntimeError as e:
            print(f"RuntimeError during transcription: {e}")
            return

        segments = result["segments"]
        text_with_timestamps = "\n".join([f"[{segment['start']:.3f} - {segment['end']:.3f}] {segment['text']}" for segment in segments])

        text_editor.delete("1.0", END)
        text_editor.insert("1.0", text_with_timestamps)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        window.destroy()
        end_time = time.time()

        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60

        messagebox.showinfo("Время обработки", f"Обработка файла заняла {minutes} минут {seconds:.1f} секунд")


def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filepath:
        text = text_editor.get("1.0", END)
        with open(filepath, "w") as file:
            file.write(text)

root = Tk()
root.title("SoundScript")
root.geometry("1000x550")

frame = ttk.Frame(root, width=170)
frame.grid(column=2, row=0, sticky=NE)

frame2 = ttk.Frame(root, width=70)
frame2.grid(column=2, row=0, sticky=NE,pady=150)

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

selected_method = StringVar(value=methods[0]["name"])

header = ttk.Label(frame, text="Выберите алгоритм")
header.pack(anchor=N)

for method in methods:
    mth_btn = ttk.Radiobutton(frame, text=method["display"], value=method["name"], variable=selected_method)
    mth_btn.pack(anchor=NW)

selected_language = StringVar(value=languages[0]["code"])

header_lang = ttk.Label(frame2, text="Выберите язык аудио")
header_lang.pack(anchor=N)

for lang in languages:
    lang_btn = ttk.Radiobutton(frame2, text=lang["display"], value=lang["code"], variable=selected_language)
    lang_btn.pack(anchor=NW)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

text_editor = Text(root, wrap=WORD)
text_editor.grid(column=0, columnspan=2, row=0, sticky=NSEW)

open_button = ttk.Button(root, text="Открыть файл", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10, pady=10)

save_button = ttk.Button(root, text="Сохранить файл", command=save_file)
save_button.grid(column=1, row=1, sticky=NSEW, padx=10, pady=10)

root.mainloop()
