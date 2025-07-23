import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import os
from tkinter import messagebox
import GUI_globals as globals

def setupPaths(gui, file_label, path_label):
    setup_window = tk.Toplevel(gui)
    setup_window.title("Setup File and Save Path")
    setup_window.geometry("1300x900")
    setup_window.configure(bg='white')
    
    setup_window.transient(gui)
    setup_window.grab_set()
    setup_window.focus_set()

    # Title
    title_label = tk.Label(setup_window, text="Configure Data File and Save Location", 
                          font=("Arial", 16, "bold"), bg='white')
    title_label.pack(pady=20)
    
    # File selection section
    file_frame = tk.Frame(setup_window, bg='white')
    file_frame.pack(pady=20, padx=20, fill='x')
    
    file_section_label = tk.Label(file_frame, text="1. Select Data File", 
                                 font=("Arial", 12, "bold"), bg='white')
    file_section_label.pack(anchor='w', pady=(0, 10))
    
    file_button = tk.Button(file_frame, text="Browse for Data File", command=lambda: selectFile(file_status_label, file_label), 
                           font=("Arial", 12), width=20, height=2, bg='lightblue')
    file_button.pack(pady=5)
    
    file_status_label = tk.Label(file_frame, text="No file selected", 
                                font=("Arial", 10), bg='white', fg='red')
    file_status_label.pack(pady=5)

    # Integer columns section
    integer_frame = tk.Frame(setup_window, bg='white')
    integer_frame.pack(pady=20, padx=20, fill='x')
    
    integer_section_label = tk.Label(integer_frame, text="2. Specify Integer Columns (Optional)", 
                                    font=("Arial", 12, "bold"), bg='white')
    integer_section_label.pack(anchor='w', pady=(0, 10))
    integer_info_label = tk.Label(integer_frame, text="Enter column names that should be treated as integers, separated by commas:", 
                                 font=("Arial", 10), bg='white')
    integer_info_label.pack(anchor='w', pady=(0, 5))
    
    integer_entry = tk.Entry(integer_frame, font=("Arial", 10), width=60)
    integer_entry.pack(pady=5, fill='x')
    
    # Save path section
    path_frame = tk.Frame(setup_window, bg='white')
    path_frame.pack(pady=20, padx=20, fill='x')
    
    path_section_label = tk.Label(path_frame, text="3. Select Save Location", 
                                 font=("Arial", 12, "bold"), bg='white')
    path_section_label.pack(anchor='w', pady=(0, 10))
    
    path_button = tk.Button(path_frame, text="Browse for Save Location", 
                           command=lambda: selectSavePath(path_status_label, path_label), 
                           font=("Arial", 12), width=20, height=2, bg='lightgreen')
    path_button.pack(pady=5)
    
    path_status_label = tk.Label(path_frame, text="No save path selected", 
                                font=("Arial", 10), bg='white', fg='red')
    path_status_label.pack(pady=5)
    
    # Control buttons
    button_frame = tk.Frame(setup_window, bg='white')
    button_frame.pack(pady=30)
    
    done_button = tk.Button(button_frame, text="Done", 
                           command=lambda: closeSetup(setup_window, integer_entry), 
                           font=("Arial", 12), width=15, height=2, bg='lightgray')
    done_button.pack(side='left', padx=10)
    
    cancel_button = tk.Button(button_frame, text="Cancel", 
                             command=setup_window.destroy, 
                             font=("Arial", 12), width=15, height=2, bg='lightcoral')
    cancel_button.pack(side='left', padx=10)

def selectFile(status_label, file_label):
    filename = askopenfilename(
        title="Select Data File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if filename:
        globals.FILENAME = filename
        status_label.config(text=f"Selected: {os.path.basename(globals.FILENAME)}", fg='green')
        # Update main window file label
        file_label.config(text=f"Selected: {os.path.basename(globals.FILENAME)}")

def selectSavePath(status_label, path_label):
    savepath = filedialog.askdirectory(title="Select Save Location")
    if savepath:
        globals.SAVEPATH = savepath
        status_label.config(text=f"Save to: {globals.SAVEPATH}", fg='green')
        path_label.config(text=f"Save to: {globals.SAVEPATH}")

def closeSetup(window, integer_entry):
    # Process integer columns input
    integer_input = integer_entry.get().strip()
    if integer_input:
        globals.INTEGER_COLUMNS = [col.strip() for col in integer_input.split(',') if col.strip()]
    else:
        globals.INTEGER_COLUMNS = []
    
    if globals.FILENAME and globals.SAVEPATH:
        integer_info = f" (Integer columns: {len(globals.INTEGER_COLUMNS)})" if globals.INTEGER_COLUMNS else " (No integer columns specified)"
        messagebox.showinfo("Setup Complete", 
                           f"Configuration saved!\n\n"
                           f"Data file: {os.path.basename(globals.FILENAME)}\n"
                           f"Save location: {globals.SAVEPATH}\n"
                           f"Integer columns: {', '.join(globals.INTEGER_COLUMNS) if globals.INTEGER_COLUMNS else 'None'}")
        window.destroy()
    else:
        response = messagebox.askyesno("Incomplete Setup", 
                                     "You haven't selected both file and save path. Close anyway?")
        if response:
            window.destroy()