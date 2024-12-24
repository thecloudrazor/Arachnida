from tkinter import Tk, Label, Button, filedialog, Canvas, Entry, Frame
from PIL import Image, ImageTk

def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=(
            ("PNG Files", "*.png"),
            ("JPG Files", "*.jpg"),
            ("JPEG Files", "*.jpeg"),
            ("GIF Files", "*.gif"),
            ("BMP Files", "*.bmp"),
        )
    )
    if not file_path:
        print("No file selected")
        return
    display_image(file_path)

def display_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((300, 300))  # Görüntüyü küçültmek için
    img_tk = ImageTk.PhotoImage(img)

    # Resmi Canvas üzerine yerleştirme
    canvas_width = img_canvas.winfo_width()
    canvas_height = img_canvas.winfo_height()

    img_canvas.create_image(canvas_width // 2, canvas_height // 2, image=img_tk, anchor="center")
    img_canvas.image = img_tk  # Referansı saklamamız gerekiyor

    # Metadata örneği (Gerçek metadata eklemek için bir kütüphane kullanılabilir)
    metadata_label.config(text=f"Filename: {file_path.split('/')[-1]}\nSize: {img.size}")

def create_window():
    win = Tk()
    win.title("Scorpion")
    win.geometry("800x500")
    win.resizable(False, False)

    # Metadata ve düzenleme alanı
    metadata_frame = Frame(win)
    metadata_frame.place(x=20, y=20, width=300, height=200)
    global metadata_label
    metadata_label = Label(metadata_frame, text="Metadata info", justify="left", anchor="nw")
    metadata_label.pack(fill="both", expand=True)

    # Edit Box
    edit_box = Entry(metadata_frame, width=30)
    edit_box.pack(pady=10)

    # Resim Placeholder
    global img_canvas
    img_canvas = Canvas(win, width=300, height=300, bg="lightgray")
    img_canvas.place(x=350, y=20)

    # Butonlar için Frame
    button_frame = Frame(win)
    button_frame.place(x=350, y=350)

    Button(button_frame, text="Select", command=select_file, width=15).pack(pady=5)
    Button(button_frame, text="Edit", command=lambda: print(f"Edit: {edit_box.get()}"), width=15).pack(pady=5)
    Button(button_frame, text="Exit", command=win.quit, width=15).pack(pady=5)

    win.mainloop()

if __name__ == "__main__":
    create_window()
