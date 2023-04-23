import json
import openai
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("OpenAI Whisper 轉錄工具")
        self.master.resizable(False, False)
        self.master.eval('tk::PlaceWindow . center')
        self.language_mapping = {
            "English": "en",
            "繁體中文": "zh",
            "日本語": "ja",
            "한국어": "ko"
        }
        self.create_widgets()

    def create_widgets(self):
        # API Key 輸入欄位
        self.api_key_label = tk.Label(self.master, text="API Key:")
        self.api_key_label.grid(row=0, column=0)

        self.api_key_var = tk.StringVar(value=openai.api_key)
        self.api_key_entry = tk.Entry(self.master, textvariable=self.api_key_var)
        self.api_key_entry.grid(row=0, column=1)

        # 選擇音訊檔案
        self.file_label = tk.Label(self.master, text="Select audio file:")
        self.file_label.grid(row=1, column=0)

        self.file_button = tk.Button(self.master, text="Browse", command=self.select_file)
        self.file_button.grid(row=1, column=1)

        # 選擇語言
        self.lang_label = tk.Label(self.master, text="Select language:")
        self.lang_label.grid(row=2, column=0)

        self.lang_var = tk.StringVar(value="繁體中文")
        self.lang_options = list(self.language_mapping.keys())

        self.lang_menu = tk.OptionMenu(self.master, self.lang_var, *self.lang_options)
        self.lang_menu.grid(row=2, column=1)

        # 轉錄按鈕
        self.transcribe_button = tk.Button(self.master, text="Transcribe", command=self.transcribe)
        self.transcribe_button.grid(row=3, column=1, pady=10)

        # 轉錄進度條
        self.progressbar = tk.ttk.Progressbar(self.master, orient="horizontal", length=300, mode="determinate")
        self.progressbar.grid(row=4, column=0, columnspan=2, pady=10)

        # 轉錄結果
        self.result_label = tk.Label(self.master, text="Transcription result:")
        self.result_label.grid(row=5, column=0, pady=10)

        self.result_text = tk.Text(self.master, width=50, height=10, state=tk.DISABLED)
        self.result_text.grid(row=6, column=0, columnspan=2)

    def select_file(self):
        self.file_name = filedialog.askopenfilename()
        self.file_label.config(text="Selected file: " + os.path.basename(self.file_name))

    def transcribe(self):
        try:
            if not hasattr(self, "file_name"):
                tk.messagebox.showerror("Error", "Please select an audio file first!")
                return

            language = self.lang_var.get()

            # 設置API Key
            openai.api_key = self.api_key_var.get()

            # 開始轉錄
            self.progressbar["value"] = 0
            self.progressbar["maximum"] = 100
            self.progressbar.start()

            threading.Thread(target=self.do_transcribe, args=(self.file_name, language)).start()
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

            # 停止進度條
            self.progressbar.stop()
            self.progressbar["value"] = 0

            self.transcribe_button.config(state=tk.NORMAL)
            self.file_button.config(state=tk.NORMAL)
            self.lang_menu.config(state=tk.NORMAL)
    def do_transcribe(self, file_name, language):
        try:
            self.transcribe_button.config(state=tk.DISABLED)
            self.file_button.config(state=tk.DISABLED)
            self.lang_menu.config(state=tk.DISABLED)

            with open(file_name, "rb") as audio_file:
                transcription = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    response_format="srt",
                    language = self.language_mapping[language]
                )

            try:
                text = json.loads(transcription)
            except json.decoder.JSONDecodeError as e:
                text = transcription

            lines = text.split('\n')
            new_lines = [line.replace(')', '') for line in lines if not line.startswith('HTTP')]
            new_text = '\n'.join(new_lines).strip() + '\n'

            # 利用 os.path 模組操作檔案路徑
            out_file_name = os.path.splitext(file_name)[0] + ".srt"
            with open(out_file_name, "w") as f:
                f.write(new_text)

            # 顯示轉錄結果
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, new_text)
            self.result_text.config(state=tk.DISABLED)

            # 停止進度條
            self.progressbar.stop()
            self.progressbar["value"] = 100

            tk.messagebox.showinfo("Success", "Transcription completed successfully!")

            self.transcribe_button.config(state=tk.NORMAL)
            self.file_button.config(state=tk.NORMAL)
            self.lang_menu.config(state=tk.NORMAL)

        except openai.error.APIError as e:
            tk.messagebox.showerror("Error", "Transcription failed: " + str(e))
            self.transcribe_button.config(state=tk.NORMAL)
            self.file_button.config(state=tk.NORMAL)
            self.lang_menu.config(state=tk.NORMAL)
            # 停止進度條
            self.progressbar.stop()
            self.progressbar["value"] = 0

        except openai.error.InvalidRequestError as e:
            tk.messagebox.showerror("Error", str(e))
            self.transcribe_button.config(state=tk.NORMAL)
            self.file_button.config(state=tk.NORMAL)
            self.lang_menu.config(state=tk.NORMAL)
            # 停止進度條
            self.progressbar.stop()
            self.progressbar["value"] = 0
        except openai.error.AuthenticationError as e:
            tk.messagebox.showerror("Error", str(e))
            self.transcribe_button.config(state=tk.NORMAL)
            self.file_button.config(state=tk.NORMAL)
            self.lang_menu.config(state=tk.NORMAL)
            # 停止進度條
            self.progressbar.stop()
            self.progressbar["value"] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

