import tkinter as tk
from threading import Thread
from google.cloud import translate_v2 as translate
import openai
import obswebsocket
import obswebsocket.requests
from fpdf import FPDF

# Google Cloud Translation API 金鑰
google_cloud_api_key = 'AIzaSyDbynwUQuvWPw-lt2h7EwFtHBLaoMWvR2Y'

# OpenAI API 金鑰
openai_api_key = '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'
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("即時翻譯和摘要生成器")

        # 開始按鈕
        self.start_button = tk.Button(root, text="開始", command=self.start_translation)
        self.start_button.pack()

        # 停止按鈕
        self.stop_button = tk.Button(root, text="停止", command=self.stop_translation, state=tk.DISABLED)
        self.stop_button.pack()

        # 摘要按鈕
        self.summary_button = tk.Button(root, text="生成摘要", command=self.generate_summary)
        self.summary_button.pack()

        # PDF 匯出按鈕
        self.export_button = tk.Button(root, text="匯出PDF", command=self.export_to_pdf, state=tk.DISABLED)
        self.export_button.pack()

        # 文本顯示框
        self.text_widget = tk.Text(root, wrap='word')
        self.text_widget.pack(expand=1, fill='both')

        # OBS WebSocket 連接
        self.client = obswebsocket.obsws("localhost", 4444, "your_password")
        self.client.connect()

        # 翻譯線程
        self.translation_thread = None

    def start_translation(self):
        # 啟動翻譯線程
        self.translation_thread = Thread(target=self.translation_loop)
        self.translation_thread.start()

        # 啟用停止按鈕
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_translation(self):
        # 停止翻譯線程
        if self.translation_thread:
            self.translation_thread.join()
            self.translation_thread = None

        # 啟用開始按鈕
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # 啟用 PDF 匯出按鈕
        self.export_button.config(state=tk.NORMAL)

    def translation_loop(self):
        # 模擬從 OBS 獲取音訊並進行翻譯
        while True:
            # 假設從 OBS 獲取音訊並進行翻譯
            audio_text = self.get_audio_text()  # 從 OBS 獲取音訊文本
            translated_text = self.translate_text(audio_text, "zh")  # 將音訊文本翻譯成中文
            self.display_translation(translated_text)  # 顯示翻譯文本

    def get_audio_text(self):
        # 使用 OBS WebSocket 獲取音訊文本
        return "Hello, world!"  # 模擬獲取音訊文本

    def translate_text(self, text, target_language):
        # 使用 Google Cloud Translation API 進行翻譯
        translate_client = translate.Client(api_key=google_cloud_api_key)
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']

    def display_translation(self, text):
        # 在文本顯示框中顯示翻譯文本
        self.text_widget.insert('end', text + '\n')
        self.root.update()

    def generate_summary(self):
        # 獲取文本並使用 OpenAI API 生成摘要
        text = self.text_widget.get('1.0', 'end')
        summary = self.generate_summary_api(text)
        self.text_widget.insert('end', "摘要:\n" + summary + '\n')

        # 啟用 PDF 匯出按鈕
        self.export_button.config(state=tk.NORMAL)

    def generate_summary_api(self, text):
        # 使用 OpenAI API 生成摘要
        openai.api_key = openai_api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"請總結以下內容：{text}",
            max_tokens=150
        )
        summary = response.choices[0].text.strip()
        return summary

    def export_to_pdf(self):
        # 將文本內容保存為 PDF 文件
        text = self.text_widget.get('1.0', 'end')

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="摘要", ln=True, align="C")
        pdf.multi_cell(0, 10, txt=text)
        pdf.output("summary.pdf")

        self.text_widget.insert('end', "PDF 匯出完成\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
