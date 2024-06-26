import asyncio
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import whisper
import threading


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
    try:
        model_type = "medium"
        language= "ru"
        model = whisper.load_model(model_type)

        audio = whisper.load_audio(filepath)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        _, probs = model.detect_language(mel)
        result = model.transcribe(filepath, language=language, fp16=False, verbose=True)

        segments = result["segments"]
        text_with_timestamps = "\n".join([f"[{segment['start']:.2f} - {segment['end']:.2f}] {segment['text']}" for segment in segments])

        text_editor.delete("1.0", END)
        text_editor.insert("1.0", text_with_timestamps)


    except Exception as e:
        # messagebox.showerror("Error", f"An error occurred: {e}")
         print(e)
    finally:
        window.destroy()

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filepath:
        text = text_editor.get("1.0", END)
        with open(filepath, "w") as file:
            file.write(text)


root = Tk()
root.title("SoundScript")
root.geometry("1000x500")

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
