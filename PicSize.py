import os
from tkinter import Tk, Label, Entry, Button, filedialog
from PIL import Image
from tqdm import tqdm
import threading
from tkinter import ttk

def resize_images(input_folder, output_folder, width, height, progress_bar):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the list of image files
    image_files = [
        filename for filename in os.listdir(input_folder)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    ]

    # Calculate the total number of images
    total_images = len(image_files)

    # Iterate over the image files
    for i, filename in enumerate(image_files):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Open the image file
        with Image.open(input_path) as image:
            # Calculate the aspect ratio
            aspect_ratio = image.width / float(image.height)

            # Calculate the new height based on the width and aspect ratio
            new_height = int(width / aspect_ratio)

            # Resize the image while preserving the aspect ratio
            resized_image = image.resize((width, new_height), Image.LANCZOS)

            # Get the DPI information, or set a default value if it doesn't exist
            dpi = image.info.get("dpi", (300, 300))  # Default DPI: 300

            # Save the resized image with the DPI information
            resized_image.save(output_path, dpi=dpi)

        # Update the progress bar
        progress_bar["value"] = (i + 1) / total_images * 100
        progress_bar.update()

def browse_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_entry.delete(0, 'end')
    input_folder_entry.insert('end', folder_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_entry.delete(0, 'end')
    output_folder_entry.insert('end', folder_path)

def resize_images_gui():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    width = int(width_entry.get())
    height = int(height_entry.get())

    # Disable the resize button during execution
    resize_button.config(state='disabled')

    # Create the progress bar
    progress_bar = ttk.Progressbar(window, length=300, mode='determinate')
    progress_bar.grid(row=6, column=0, columnspan=3, pady=10)

    def resize_thread():
        resize_images(input_folder, output_folder, width, height, progress_bar)

        # Enable the resize button after execution
        resize_button.config(state='normal')
        status_label.config(text="Image resizing completed.")

    # Start a separate thread for image resizing
    thread = threading.Thread(target=resize_thread)
    thread.start()

# Create the main window
window = Tk()
window.title("PicSize")

# Input folder widgets
input_folder_label = Label(window, text="Input Folder:")
input_folder_label.grid(row=0, column=0, sticky='e')
input_folder_entry = Entry(window, width=40)
input_folder_entry.grid(row=0, column=1)
input_folder_button = Button(window, text="Browse", command=browse_input_folder)
input_folder_button.grid(row=0, column=2)

# Output folder widgets
output_folder_label = Label(window, text="Output Folder:")
output_folder_label.grid(row=1, column=0, sticky='e')
output_folder_entry = Entry(window, width=40)
output_folder_entry.grid(row=1, column=1)
output_folder_button = Button(window, text="Browse", command=browse_output_folder)
output_folder_button.grid(row=1, column=2)

# Width widgets
width_label = Label(window, text="Width:")
width_label.grid(row=2, column=0, sticky='e')
width_entry = Entry(window, width=10)
width_entry.grid(row=2, column=1)

# Height widgets
height_label = Label(window, text="Height:")
height_label.grid(row=3, column=0, sticky='e')
height_entry = Entry(window, width=10)
height_entry.grid(row=3, column=1)

# Resize button
resize_button = Button(window, text="Resize Images", command=resize_images_gui)
resize_button.grid(row=4, column=1)

# Status label
status_label = Label(window, text="")
status_label.grid(row=5, column=0, columnspan=3)

# Start the main loop
window.mainloop()
