from tkinter import Tk, Label, Button, filedialog, Canvas, Entry, Frame, Scrollbar
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

    gps_info = metadata.get('GPSInfo', {})
    if gps_info:
        latitude = gps_info.get(2)
        longitude = gps_info.get(4)

        if latitude and longitude:
            latitude_degrees = float(latitude[0])
            latitude_minutes = float(latitude[1])
            latitude_seconds = float(latitude[2])

            longitude_degrees = float(longitude[0])
            longitude_minutes = float(longitude[1])
            longitude_seconds = float(longitude[2])

            latitude_decimal = latitude_degrees + (latitude_minutes / 60) + (latitude_seconds / 3600)
            longitude_decimal = longitude_degrees + (longitude_minutes / 60) + (longitude_seconds / 3600)

            if gps_info[1] == 'S':
                latitude_decimal = -latitude_decimal
            if gps_info[3] == 'W':
                longitude_decimal = -longitude_decimal

            metadata["GPSInfo"] = f"{latitude_decimal:.6f}°, {longitude_decimal:.6f}°"

            print(f"Updated GPS Info: {metadata['GPSInfo']}")

    for key, value in metadata.items():
        if key == "Error":
            label = Label(edit_frame, text="EXIF Format not found", fg="red").pack(anchor="w", padx=10)
            continue
        metadata_text[key] = value
        label = Label(edit_frame, text=f"{key}:", fg="green")
        label.pack(anchor="w", padx=10)

        box = Entry(edit_frame)
        box.insert(0, value)
        box.pack(fill="x", padx=10, pady=5)

        canvas_width = img_canvas.winfo_width()
        box.config(width=canvas_width)

        text_box[key] = box

def save_data():
    if edit_frame.winfo_ismapped() != True:
        print("no changes have been made to the metadata")
        return
    
    for key, box in text_box.items():
        metadata_text[key] = box.get()
    print(f"Updated metadata: ", metadata_text)


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
    Button(button_frame, text="Save", command=save_data, width=15).pack(pady=5)
    Button(button_frame, text="Exit", command=win.quit, width=15).pack(pady=5)

    def on_frame_resize(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    edit_frame.bind("<Configure>", on_frame_resize)

    win.mainloop()
