import os
from tkinter import Tk, filedialog, Button, Label
from PIL import Image
import imagehash

# Global variable to store selected folder path
selected_folder = ""

# Function to select folder
def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_label.config(text=selected_folder)

# Function to get image hash
def get_image_hash(image_path):
    with Image.open(image_path) as img:
        return imagehash.average_hash(img)

# Function to remove duplicate images
def remove_duplicates(image_directory):
    image_hashes = {}
    for file in os.listdir(image_directory):
        file_path = os.path.join(image_directory, file)
        if os.path.isfile(file_path) and file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            try:
                img_hash = get_image_hash(file_path)
                file_size = os.path.getsize(file_path)

                # If hash already exists, compare sizes and keep the smaller one
                if img_hash in image_hashes:
                    existing_file, existing_size = image_hashes[img_hash]
                    if file_size < existing_size:
                        os.remove(existing_file)  # Remove larger existing file
                        image_hashes[img_hash] = (file_path, file_size)
                    else:
                        os.remove(file_path)  # Remove current larger file
                else:
                    image_hashes[img_hash] = (file_path, file_size)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
    print("Duplicate images with larger sizes have been removed.")

# Function to run duplicate removal
def run_removal():
    if selected_folder:
        remove_duplicates(selected_folder)
    else:
        print("No folder selected. Please select a folder first.")

# Create GUI app
root = Tk()
root.title("Duplicate Image Remover")
root.geometry("400x200")

folder_label = Label(root, text="Select a folder to scan for duplicates", wraplength=300)
folder_label.pack(pady=10)

select_button = Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=10)

run_button = Button(root, text="Run", command=run_removal)
run_button.pack(pady=20)

root.mainloop()
