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

    for widget in edit_frame_content.winfo_children():
        widget.destroy()

    if edit_frame.winfo_ismapped():
        metadata_frame.place(x=20, y=20, width=450, height=460)
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
            label = Label(edit_frame_content, text="EXIF Format not found", fg="red").pack(anchor="w", padx=10)
            continue
        metadata_text[key] = value
        label = Label(edit_frame_content, text=f"{key}:", fg="green")
        label.pack(anchor="w", padx=10)

        box = Entry(edit_frame_content)
        box.insert(0, value)
        box.pack(fill="x", padx=10, pady=5)

        canvas_width = img_canvas.winfo_width()
        box.config(width=canvas_width)

        text_box[key] = box

    metadata_text_display = "\n".join([f"{key}: {value}" for key, value in metadata_text.items()])
    metadata_label.config(text=metadata_text_display)

    update_canvas_scroll()

def update_canvas_scroll():
    edit_frame_canvas.config(scrollregion=edit_frame_canvas.bbox("all"))


def save_data():
    if edit_frame.winfo_ismapped() != True:
        print("no changes have been made to the metadata")
        return
    
    for key, box in text_box.items():
        metadata_text[key] = box.get()
    print(f"Updated ", metadata_text)


def edit_metadata():
    global file_path, metadata, text_box

    if not file_path:
        print("No file selected")
        return
    metadata_frame.place_forget()
    edit_frame.place(x=20, y=20, width=450, height=460)
    
    v = Scrollbar(edit_frame, orient="vertical", command=edit_frame_canvas.yview)
    v.place(x=430, y=0, width=20, height=460)
    
    edit_frame_canvas.config(yscrollcommand=v.set)
    update_canvas_scroll()

def create_window():
    win = Tk()
    win.title("Scorpion")
    win.geometry("800x500")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    global metadata_frame, edit_frame, edit_frame_canvas, edit_frame_content
    metadata_frame = Frame(win)

    edit_frame = Frame(win)
    
    edit_frame_canvas = Canvas(edit_frame, width=430, height=460)
    edit_frame_canvas.pack(side="left", fill="both", expand=True)
    
    edit_frame_content = Frame(edit_frame_canvas)
    edit_frame_canvas.create_window((0, 0), window=edit_frame_content, anchor="nw")

    metadata_frame.place(x=20, y=20, width=450, height=460)

    global metadata_label
    metadata_label = Label(metadata_frame, text="Metadata info", justify="left", anchor="nw", bg="lightgreen")
    metadata_label.pack(fill="both", expand=True)

    global img_canvas
    img_canvas = Canvas(win, width=300, height=300, bg="lightgray")
    img_canvas.place(x=490, y=20)

    button_frame = Frame(win)
    button_frame.place(x=580, y=350)

    Button(button_frame, text="Select", command=select_file, width=15).pack(pady=5)
    Button(button_frame, text="Edit metadata", command=edit_metadata, width=15).pack(pady=5)
    Button(button_frame, text="Save", command=save_data, width=15).pack(pady=5)
    Button(button_frame, text="Exit", command=win.quit, width=15).pack(pady=5)

    win.mainloop()
