import tkinter as tk
from tkinter import ttk, filedialog, Canvas, messagebox
from PIL import Image, ImageTk
import shutil
import json
import time
import threading
import sys
import os
from datetime import datetime
import re

def main():
    global map_file
    # Centering function
    def center_window(window, width, height):
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    # Initialize main application window
    app = tk.Tk()
    app.resizable(False, False)
    app.title("DSR SaveDaSit 1.0.1")
    center_window(app, 450, 610)
    # Determine the correct path to the images and icon
    if getattr(sys, 'frozen', False):
        # Executed from the exe
        base_dir = sys._MEIPASS
    else:
        # Executed from script
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Load images and set application icon
    image_path = os.path.join(base_dir, "src/bg.png")
    image2_path = os.path.join(base_dir, "src/zkrvf.png")
    icon_path = os.path.join(base_dir, "src/icon.ico")
    app.iconbitmap(icon_path)
    
    # Define a style
    style = ttk.Style()
    style.configure("TButton", font=('Arial', 12), padding=10)
    style.configure("TLabel", font=('Arial', 12), padding=1)
    style.configure("TEntry", font=('Arial', 12), padding=10)

    # Load image with Pillow
    image_original = Image.open(image_path)
    image = ImageTk.PhotoImage(image_original)

    # Load image2 with Pillow
    image2_original = Image.open(image2_path)
    image2 = ImageTk.PhotoImage(image2_original)

    # Creating the tab control
    tab_control = ttk.Notebook(app)

    # Creating the tabs
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)

    # Adding tabs to the tab control
    tab_control.add(tab1, text='Backup')
    tab_control.add(tab2, text='Restore')
    tab_control.add(tab3, text='Author')

    # Adding unique content to each tab
    ttk.Label(tab1, text='Backup and configuration').pack(pady=0)
    ttk.Label(tab2, text='Backup List and Restore').pack(pady=0)
    ttk.Label(tab3, text='zkrvf').pack(pady=0)

    # Create and package the label with the image
    label_image1 = tk.Label(tab1, image=image)
    label_image1.pack(pady=0)

    label_image2 = tk.Label(tab2, image=image)
    label_image2.pack(pady=0)

    label_image3 = tk.Label(tab3, image=image2)
    label_image3.pack(pady=0)

    # Package the tab control
    tab_control.pack(expand=1, fill='both')

    # Variables
    display_filepath_var = tk.StringVar()
    display_destpath_var = tk.StringVar()

    # Definición de variables
    filepath_var = tk.StringVar()
    destpath_var = tk.StringVar()
    interval_var = tk.IntVar(value=1)
    countdown_var = tk.StringVar(value="Waiting for start...")
    backup_running_var = tk.BooleanVar(value=False)

    # Agregando contenido a tab1
    frame1 = ttk.Frame(tab1)
    frame1.pack(pady=5, padx=20, fill=tk.X)

    def choose_file():
        filepath = filedialog.askopenfilename()
        if filepath:
            display_filepath_var.set(os.path.basename(filepath))
            filepath_var.set(filepath)

    def choose_destination():
        destpath = filedialog.askdirectory()
        if destpath:
            display_destpath_var.set(os.path.basename(destpath))
            destpath_var.set(destpath)

    ttk.Label(frame1, text="Source:").pack(side=tk.LEFT, padx=20)
    ttk.Entry(frame1, textvariable=display_filepath_var, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame1, text="Browse", command=choose_file, width=20).pack(side=tk.LEFT, padx=5)

    frame2 = ttk.Frame(tab1)
    frame2.pack(pady=5, padx=20, fill=tk.X)

    ttk.Label(frame2, text="Destination:").pack(side=tk.LEFT, padx=5)
    ttk.Entry(frame2, textvariable=display_destpath_var, width=20).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame2, text="Browse", command=choose_destination, width=20).pack(side=tk.LEFT, padx=5)

    frame3 = ttk.Frame(tab1)
    frame3.pack(pady=20, padx=20, fill=tk.X)
    ttk.Label(frame3, text="Backup interval (minutes):").pack(side=tk.LEFT, padx=5)

    def save_config():
        with open('config.json', 'w') as f:
            json.dump({
                'source': filepath_var.get(),
                'destination': destpath_var.get(),
                'interval': interval_var.get()
            }, f)

    def load_config():
        try:
            with open('config.json', 'r') as f:
                data = json.load(f)
                
                filepath_var.set(data['source'])
                destpath_var.set(data['destination'])
                interval_var.set(data['interval'])

                display_filepath_var.set(os.path.basename(data['source']))
                display_destpath_var.set(os.path.basename(data['destination']))
        except:
            pass

    def make_backup():
        def copy_file_with_timestamp():
            timestamp = time.strftime('%Y%m%d-%H%M%S')
            filename = f"{timestamp}_{os.path.basename(filepath_var.get())}"
            dest_path = os.path.join(destpath_var.get(), filename)
            try:
                shutil.copy(filepath_var.get(), dest_path)
                countdown_var.set(f"Backup made in: {dest_path}")
                print(f"Successful backup on: {dest_path}")  # Debug print
            except Exception as e:
                countdown_var.set(f"Error when making backup: {str(e)}")
                print(f"Error when making backup: {str(e)}")  # Debug print

        save_config()
        copy_file_with_timestamp()
        countdown_var.set("Immediate backup done!")
        time.sleep(2)  # Small pause so that the user notices the change in the interface

        while backup_running_var.get():
            time_remaining = int(interval_var.get()) * 60
            while time_remaining > 0 and backup_running_var.get():
                mins, secs = divmod(time_remaining, 60)
                countdown_var.set(f"Next backup in {mins}m {secs}s")
                time.sleep(1)
                time_remaining -= 1

            if backup_running_var.get():
                copy_file_with_timestamp()

    def configure_buttons(is_backup_running):
        start_button.config(state=tk.DISABLED if is_backup_running else tk.NORMAL)
        stop_button.config(state=tk.NORMAL if is_backup_running else tk.DISABLED)

    def start_backup():
        configure_buttons(True)
        backup_running_var.set(True)
        threading.Thread(target=make_backup).start()

    def stop_backup():
        configure_buttons(False)
        backup_running_var.set(False)
        countdown_var.set("Backup stopped")


    def validate_input(*args):
        value = interval_var.get()

        # Filtrar solo dígitos y cortar a 3 caracteres si es necesario
        cleaned_value = "".join(filter(str.isdigit, value))[:3]

        # Si el valor es más grande que 999, establecerlo en 999
        if cleaned_value and int(cleaned_value) > 999:
            cleaned_value = "999"

        interval_var.set(cleaned_value)

    # Configuración inicial
    interval_var = tk.StringVar()
    interval_var.trace("w", validate_input)

    # Elementos de la GUI
    ttk.Entry(frame3, textvariable=interval_var, width=3).pack(side=tk.LEFT, padx=5)
    ttk.Label(tab1, textvariable=countdown_var).pack(pady=0)

    frame_botones = ttk.Frame(tab1)
    frame_botones.pack(pady=5)

    start_button = ttk.Button(frame_botones, text="Start Backup", command=start_backup)
    start_button.pack(side=tk.LEFT, padx=10)

    stop_button = ttk.Button(frame_botones, text="Stop Backup", command=stop_backup)
    stop_button.pack(side=tk.LEFT, padx=10)
    stop_button.config(state=tk.DISABLED)

    load_config()

    # Main frame that will contain the list and information
    main_frame = ttk.Frame(tab2)
    main_frame.pack(pady=0, fill=tk.BOTH, expand=True, padx=85)  # Make sure it expands horizontally

    # Frame that will contain the listbox and the scrollbar
    frame_listbox = ttk.Frame(main_frame)
    frame_listbox.grid(row=0, column=0, padx=0, pady=0, sticky=tk.W+tk.N)

    # Info frame to the right of the listbox
    info_frame = ttk.Frame(main_frame)
    info_frame.grid(row=1, column=0, padx=0, pady=0, sticky=tk.W)

    # Variables to display information
    weight_var = tk.StringVar()
    var_quantity = tk.StringVar()

    # Information labels
    labels_text = [("Total weight:", weight_var), ("Total files:", var_quantity)]
    for idx, (text, var) in enumerate(labels_text):
        ttk.Label(info_frame, text=text, font=("Arial", 9)).grid(row=idx, column=0, sticky=tk.W)
        ttk.Label(info_frame, textvariable=var, font=("Arial", 9)).grid(row=idx, column=1, sticky=tk.W)

    # Create and configure scrollbar
    scrollbar = tk.Scrollbar(frame_listbox)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create and configure listbox
    listbox = tk.Listbox(frame_listbox, width=40, height=10, yscrollcommand=scrollbar.set)
    listbox.pack(pady=5, side=tk.LEFT)

    scrollbar.config(command=listbox.yview)

    def get_total_weight(directory):
        return sum(
            os.path.getsize(os.path.join(dirpath, f))
            for dirpath, _, filenames in os.walk(directory)
            for f in filenames
        )

    def get_number_files(directory):
        return sum(1 for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.sl2'))

    map_file = {}  # global dictionary to map formatted names to original file names

    def format_timestamp(archivo):
        timestamp_str = archivo.split("_")[0]
        year, month, day, hour, minute, second = timestamp_str[:4], timestamp_str[4:6], timestamp_str[6:8], timestamp_str[9:11], timestamp_str[11:13], timestamp_str[13:15]
        formatted_timestamp = f"{year}/{month}/{day} | {hour}:{minute}:{second}"
        
        match = re.search(r'\(([^)]+)\)', archivo)
        if match:
            narrative = match.group(1)  # Extract content inside the parentheses
            formatted_timestamp += f" ({narrative.replace('_', ' ')})"
        
        return formatted_timestamp

    def list_backups():
        global map_file
        map_file.clear()
        destination = destpath_var.get()
        
        if os.path.exists(destination):
            listbox.delete(0, tk.END)
            files = (f for f in os.listdir(destination) if os.path.isfile(os.path.join(destination, f)) and f.endswith('.sl2'))

            for index, archivo in enumerate(sorted(files, reverse=True)):
                formatted_timestamp = format_timestamp(archivo)
                map_file[formatted_timestamp] = archivo  # Update the dictionary
                listbox.insert(tk.END, formatted_timestamp)
                listbox.itemconfig(tk.END, bg='lightblue' if index % 2 == 0 else 'white')
            
            # Update weight and quantity information
            total_weight = get_total_weight(destination)
            number_files = get_number_files(destination)
            
            # Format weight to MB
            weight_var.set(f"{total_weight / (1024*1024):.2f} MB")
            var_quantity.set(str(number_files))

    list_backups()  # Call the function on startup to list available backups

    def restore_backup():
        selected_file_format = listbox.get(tk.ACTIVE)  # Get the formatted name from the listbox
        selected_file = map_file.get(selected_file_format)  # Get the original name from the dictionary

        if not selected_file:
            return

        if not messagebox.askyesno("Confirmation", f"Are you sure to restore the file: {selected_file_format}?"):
            return

        backup_path = os.path.join(destpath_var.get(), selected_file)
        original_file_path = filepath_var.get()
        backup_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Create a backup of the current original file
        backup_filename = f"{backup_timestamp}_{os.path.basename(original_file_path)}"
        shutil.copy2(original_file_path, os.path.join(os.path.dirname(original_file_path), backup_filename))
        
        # Restore the backup file over the original file
        shutil.copy2(backup_path, original_file_path)
        messagebox.showinfo("Success", f"File {selected_file} successfully restored!")

    def update_list():
        list_backups()
        print("Updated list!")

    def modify_name():
        selected_file_format = listbox.get(tk.ACTIVE)
        original_file = map_file.get(selected_file_format)

        if not original_file:
            return

        def accept():
            new_text = tackle.get().replace(" ", "_")
            if new_text:
                parts = original_file.split("_")
                # Assuming the last part is the original filename
                new_name = f"{parts[0]}_({new_text})_{parts[-1]}"
                os.rename(os.path.join(destpath_var.get(), original_file),
                          os.path.join(destpath_var.get(), new_name))
                windowed.destroy()
                update_list()  # Update the listbox

        windowed = tk.Toplevel(app)
        windowed.title("Add description")
        center_window(windowed, 300, 200)

        ttk.Label(windowed, text="Enter a short description:").pack(padx=10, pady=5)

        # Dividiendo en dos líneas
        tackle = ttk.Entry(windowed)
        tackle.pack(padx=10, pady=5)

        ttk.Button(windowed, text="Accept", command=accept).pack(pady=10)


    # Frame for main tab2 buttons
    frame_buttons_tab2 = ttk.Frame(tab2)
    frame_buttons_tab2.pack(pady=10)

    # Define main tab2 buttons
    buttons = [
        ("Update list", update_list),
        ("Restore Backup", restore_backup),
        ("Modify", modify_name)
    ]

    # Add the buttons to the frame
    for idx, (text, cmd) in enumerate(buttons):
        ttk.Button(frame_buttons_tab2, text=text, command=cmd).grid(row=0, column=idx, padx=10, pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()