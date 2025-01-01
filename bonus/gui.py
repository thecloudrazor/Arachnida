from tkinter import Tk, Label, Button, filedialog, Canvas, Entry, Frame, Scrollbar
from PIL import Image, ImageTk, ExifTags
import os

metadata_text = {}
text_box = {}
file_path = None

def clear():
    global text_box, metadata_text, img_canvas

    if metadata_text:
        metadata_text.clear()
    if text_box:
        text_box.clear()

    for widget in edit_frame.winfo_children():
        widget.destroy()

    if img_canvas.find_all():
        img_canvas.delete("all")

def select_file():
    global file_path
    clear()
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
    global metadata_text

    img = Image.open(file_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)

    canvas_width = img_canvas.winfo_width()
    canvas_height = img_canvas.winfo_height()

    img_canvas.create_image(canvas_width // 2, canvas_height // 2, image=img_tk, anchor="center")
    img_canvas.image = img_tk

    metadata = img.getexif()
    for key, value in metadata.items():
        tag = ExifTags.TAGS.get(key, key)
        metadata_text[tag] = value

    for key, value in metadata_text.items():
        label = Label(edit_frame, text=f"{key}:", fg="green")
        label.pack(anchor="w", padx=10)

        box = Entry(edit_frame)
        box.insert(0, value)
        box.pack(fill="x", padx=10, pady=5)
        text_box[key] = box

def save_metadata():
    if not file_path:
        print("No file selected")
        return
    
    img = Image.open(file_path)
    exif_data = img.getexif()

    for key, box in text_box.items():
        value = box.get()
        for exif_key, exif_value in exif_data.items():
            if ExifTags.TAGS.get(exif_key) == key:
                exif_data[exif_key] = value
    
    img.save("updated_image.jpg", exif=exif_data)
    print("Metadata updated and saved as 'updated_image.jpg'.")

def delete_metadata():
    if not file_path:
        print("No file selected")
        return
    
    img = Image.open(file_path)
    img.info.pop("exif", None)
    img.save("metadata_deleted.jpg")
    print("Metadata deleted and saved as 'metadata_deleted.jpg'.")

def create_window():
    win = Tk()
    win.title("Scorpion")
    win.geometry("800x500")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    global edit_frame, edit_frame_canvas
    canvas_frame = Frame(win)
    canvas_frame.place(x=20, y=20, width=450, height=460)

    global img_canvas
    img_canvas = Canvas(win, width=300, height=300, bg="lightgray")
    img_canvas.place(x=490, y=20)

    canvas = Canvas(canvas_frame)
    scrollbar = Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    edit_frame = Frame(canvas)
    canvas.create_window((0, 0), window=edit_frame, anchor="nw")

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    button_frame = Frame(win)
    button_frame.place(x=580, y=350)

    Button(button_frame, text="Select", command=select_file, width=15).pack(pady=5)
    Button(button_frame, text="Save Metadata", command=save_metadata, width=15).pack(pady=5)
    Button(button_frame, text="Delete Metadata", command=delete_metadata, width=15).pack(pady=5)
    Button(button_frame, text="Exit", command=win.quit, width=15).pack(pady=5)

    def on_frame_resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    edit_frame.bind("<Configure>", on_frame_resize)

    win.mainloop()
