import tkinter as tk
from TkinterDnD2 import *
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image, ImageTk
import PyPDF2

class PdfManagementApplication(tk.Frame):
    def __init__(self, master=None):
        self.entry_sv = tk.StringVar()
        self.filepath = ""
        self.images_num = 0
        self.dir_list = ["a", "b", "a", "c"]

        super().__init__(master)
        master.title("pdf管理ツールforQUADERNO")
        master.geometry("300x200")
        self.pack()
        self.create_widgets(master, entry_sv=self.entry_sv)

    # 部品の作成と設定
    def create_widgets(self, master, entry_sv):
        label = tk.Label(text="分割したいpdfファイルをドラッグしてください")
        label.pack(side="top")
        self.entry = tk.Entry(master, textvar=entry_sv, width=50)
        self.entry.pack(fill=tk.X)
        button = tk.Button(text="決定", command=self.create_window)
        button.pack()

    def create_window(self):
        print("ウィンドウ生成")
        self.get_textval()
        window = tk.Toplevel()
        window.wm_title("pdf分割")
        window.geometry("1200x800")
        label = tk.Label(window, text=self.filepath)
        label.pack(side="top")
        back_button = tk.Button(window, text="戻る")
        back_button.pack(side="top")
        preview_label = tk.Label(window, text="pdfプレビュー")
        preview_label.pack(side="top")
        # pdfを画像に変換後プレビュー表示
        self.convert_pdf_to_image()
        self.preview(window)
        # pdfを分割し保存
        restore_label = tk.Label(window, text="分割したpdfの保存先フォルダ")
        restore_label.pack(side="top")
        restore_button = tk.Button(window, text="分割", command=self.split_pdf(split_filepath="./"))
        restore_button.pack(side="top")

    def get_textval(self):
        self.filepath = self.entry_sv.get()

    def convert_pdf_to_image(self):
        pdf_path = Path(self.filepath)
        print("ファイルパス取得")
        images = convert_from_path(str(pdf_path), dpi=150, grayscale=True)
        self.images_num = len(images)
        # 画像を1枚ずつjpegファイルとして保存
        images_dir = Path("./preview_images")
        for i, page in enumerate(images):
            file_name = "images{:02d}".format(i+1) + ".jpg"
            image_path = images_dir / file_name
            page.save(str(image_path), "JPEG")
        print("画像生成")
    
    def preview(self, window):
        imgs = []
        x = 100
        global img
        for i in range(1, self.images_num+1):
            # tk.Button(text=f"{i}枚目", value=i, command=change_image).pack()
            pv_image_path = Path("./preview_images/images{:02d}".format(i) + ".jpg")
            img = Image.open(str(pv_image_path))
            img = img.resize((210, 297), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            imgs.append(img)
            canvas = tk.Canvas(window, bg="black", width=210, height=297)
            canvas.place(x=100 + x, y=200)
            canvas.create_image(0, 0, image=img, anchor=tk.NW)
            # label = tk.Label(window, image=img, width=140, height=198 + y)
            # label.configure(image=img)
            # label.pack()
            x += 300
        print("画像表示")
        # 画像が表示されない
    
    def change_image(self):
        pass

    # pdfファイルを1ページ1ファイルに分割
    def split_pdf(self, split_filepath):
        pdf = PyPDF2.PdfFileReader(self.filepath)
        for i in range(pdf.numPages):
            pw = PyPDF2.PdfFileWriter()
            pw.addPage(pdf.getPage(i))
            with open("{}{}/{:02d}.pdf".format(split_filepath, self.dir_list[i], i), "wb") as f:
                pw.write(f)

def drop(event): 
        app.entry_sv.set(event.data)


root = TkinterDnD.Tk() 
app = PdfManagementApplication(master=root)
app.entry.drop_target_register(DND_FILES)
app.entry.dnd_bind("<<Drop>>", drop)
app.mainloop()