from tkinter import Tk, Label, Button, filedialog, Canvas, Entry, Frame
from PIL import Image, ImageTk
from Scorpion import get_file_metadata, get_exif_data

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

    if edit_frame.winfo_ismapped():
        metadata_frame.place(x=20, y=20, width=300, height=200)
        edit_frame.place_forget()

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

    metadata = get_file_metadata(file_path)
    metadata.update(get_exif_data(file_path))

    for key, value in metadata.items():
        metadata_text[key] = value
        label = Label(edit_frame, text=f"{key}:")
        label.pack(anchor="w", padx=10)

        box = Entry(edit_frame)
        box.insert(0, value)
        box.pack(fill="x", padx=10, pady=5)

        text_box[key] = box

    metadata_text_display = "\n".join([f"{key}: {value}" for key, value in metadata_text.items()])
    metadata_label.config(text=metadata_text_display)

def save_data():
    for key, box in text_box.items():
        metadata_text[key] = box.get()
    print(f"Updated " , metadata_text)

def edit_metadata():
    global file_path, metadata, text_box

    if not file_path:
        print("No file selected")
        return
    metadata_frame.place_forget()
    edit_frame.place(x=20, y=20, width=300, height=500)
    Button(edit_frame, text="Save", command=save_data, width=15).pack(pady=5)

def create_window():
    win = Tk()
    win.title("Scorpion")
    win.geometry("800x500")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    global metadata_frame, edit_frame
    metadata_frame = Frame(win)
    edit_frame = Frame(win)
    metadata_frame.place(x=20, y=20, width=300, height=200)
    edit_frame.place(x=20, y=20, width=300, height=500)
    edit_frame.place_forget()
    global metadata_label
    metadata_label = Label(metadata_frame, text="Metadata info", justify="left", anchor="nw")
    metadata_label.pack(fill="both", expand=True)

    global img_canvas
    img_canvas = Canvas(win, width=300, height=300, bg="lightgray")
    img_canvas.place(x=350, y=20)

    button_frame = Frame(win)
    button_frame.place(x=350, y=350)

    Button(button_frame, text="Select", command=select_file, width=15).pack(pady=5)
    Button(button_frame, text="Edit metadata", command=edit_metadata, width=15).pack(pady=5)
    Button(button_frame, text="Exit", command=win.quit, width=15).pack(pady=5)

    win.mainloop()
