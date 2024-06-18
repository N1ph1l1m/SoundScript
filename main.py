from tkinter import *
from tkinter import ttk, filedialog, messagebox
import whisper

root = Tk()
root.title("SoundScript")
root.geometry("1000x500")


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


text_editor = Text(root, wrap=WORD)
text_editor.grid(column=0, columnspan=2, row=0, sticky=NSEW)

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3 *.flac *.aac *.ogg *.wma")])
    if filepath:
        try:
            model = whisper.load_model("base")
            result = model.transcribe(filepath, fp16=False)
            text = result["text"]
            print(text)

            text_editor.delete("1.0", END)
            text_editor.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)


def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filepath:
        text = text_editor.get("1.0", END)
        with open(filepath, "w") as file:
            file.write(text)


open_button = ttk.Button(root, text="Открыть файл", command=open_file)
open_button.grid(column=0, row=1, sticky=NSEW, padx=10, pady=10)

save_button = ttk.Button(root, text="Сохранить файл", command=save_file)
save_button.grid(column=1, row=1, sticky=NSEW, padx=10, pady=10)

root.mainloop()
