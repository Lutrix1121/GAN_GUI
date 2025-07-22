import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import os
from tkinter import messagebox


FILENAME = ""
SAVEPATH = ""
INTEGER_COLUMNS = []

class ToolTip:
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        self.schedule_tooltip()

    def on_leave(self, event=None):
        self.cancel_tooltip()
        self.hide_tooltip()

    def on_motion(self, event=None):
        self.x, self.y = event.x, event.y

    def schedule_tooltip(self):
        self.cancel_tooltip()
        self.id = self.widget.after(500, self.show_tooltip)  # 500ms delay

    def cancel_tooltip(self):
        if self.id:
            self.widget.after_cancel(self.id)
        self.id = None

    def show_tooltip(self):
        if self.tipwindow or not self.text:
            return
        
        # Calculate position relative to widget
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        
        # Make tooltip non-interactive
        tw.wm_attributes("-topmost", True)
        if hasattr(tw.wm_attributes, "-disabled"):
            tw.wm_attributes("-disabled", True)
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("Arial", "9", "normal"), padx=4, pady=2)
        label.pack()

    def hide_tooltip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            try:
                tw.destroy()
            except:
                pass

def setupPaths():
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
    
    file_button = tk.Button(file_frame, text="Browse for Data File", command=lambda: selectFile(file_status_label), 
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
                           command=lambda: selectSavePath(path_status_label), 
                           font=("Arial", 12), width=20, height=2, bg='lightgreen')
    path_button.pack(pady=5)
    
    path_status_label = tk.Label(path_frame, text="No save path selected", 
                                font=("Arial", 10), bg='white', fg='red')
    path_status_label.pack(pady=5)
    
    # Control buttons
    button_frame = tk.Frame(setup_window, bg='white')
    button_frame.pack(pady=30)
    
    done_button = tk.Button(button_frame, text="Done", 
                           command=lambda: closeSetup(setup_window), 
                           font=("Arial", 12), width=15, height=2, bg='lightgray')
    done_button.pack(side='left', padx=10)
    
    cancel_button = tk.Button(button_frame, text="Cancel", 
                             command=setup_window.destroy, 
                             font=("Arial", 12), width=15, height=2, bg='lightcoral')
    cancel_button.pack(side='left', padx=10)
    
    def selectFile(status_label):
        global FILENAME
        filename = askopenfilename(
            title="Select Data File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            FILENAME = filename
            status_label.config(text=f"Selected: {os.path.basename(FILENAME)}", fg='green')
            # Update main window file label
            file_label.config(text=f"Selected: {os.path.basename(FILENAME)}")
    
    def selectSavePath(status_label):
        global SAVEPATH
        savepath = filedialog.askdirectory(title="Select Save Location")
        if savepath:
            SAVEPATH = savepath
            status_label.config(text=f"Save to: {SAVEPATH}", fg='green')
            path_label.config(text=f"Save to: {SAVEPATH}")
    
    def closeSetup(window):
        global INTEGER_COLUMNS
        
        # Process integer columns input
        integer_input = integer_entry.get().strip()
        if integer_input:
            INTEGER_COLUMNS = [col.strip() for col in integer_input.split(',') if col.strip()]
        else:
            INTEGER_COLUMNS = []
        
        if FILENAME and SAVEPATH:
            integer_info = f" (Integer columns: {len(INTEGER_COLUMNS)})" if INTEGER_COLUMNS else " (No integer columns specified)"
            messagebox.showinfo("Setup Complete", 
                               f"Configuration saved!\n\n"
                               f"Data file: {os.path.basename(FILENAME)}\n"
                               f"Save location: {SAVEPATH}\n"
                               f"Integer columns: {', '.join(INTEGER_COLUMNS) if INTEGER_COLUMNS else 'None'}")
            window.destroy()
        else:
            response = messagebox.askyesno("Incomplete Setup", 
                                         "You haven't selected both file and save path. Close anyway?")
            if response:
                window.destroy()

def generateSamples():
    new_window = tk.Toplevel(gui)
    new_window.title("Generate Samples")
    new_window.geometry("500x600")
    new_window.resizable(width=False, height=False)
    
    def startGeneration():
        try:
            if not FILENAME:
                tk.messagebox.showerror("Error", "Please select a data file first!")
                return
            if not SAVEPATH:
                tk.messagebox.showerror("Error", "Please select a save path first!")
                return
                
            classLabel = class_entry.get()
            if not classLabel:
                tk.messagebox.showerror("Error", "Please enter a class column name!")
                return
                
            sampleSize = int(sample_size_entry.get())
            if sampleSize <= 0:
                tk.messagebox.showerror("Error", "Sample size must be a positive integer!")
                return
                
            epochs = int(epochs_entry.get()) if epochs_entry.get() else 1000
            batchSize = int(batch_size_entry.get()) if batch_size_entry.get() else 96
            latentDim = int(latent_dim_entry.get()) if latent_dim_entry.get() else 20
            learningRate = float(learning_rate_entry.get()) if learning_rate_entry.get() else 0.0001
            beta1 = float(beta1_entry.get()) if beta1_entry.get() else 0.5
            
            # Show progress message
            progress_label = tk.Label(new_window, text="Training GAN and generating samples...", font=("Arial", 10), fg="blue")
            progress_label.pack(pady=10)
            new_window.update()
            
            from tabular_gan_modified import TabularGAN
            
            # Initialize and train GAN
            gan = TabularGAN(FILENAME, class_column=classLabel, integer_columns=INTEGER_COLUMNS, latent_dim=latentDim, 
                           learning_rate=learningRate, beta1=beta1)
            
            # Train the GAN
            history = gan.train(epochs=epochs, batch_size=batchSize, verbose=1)
            
            # Generate samples
            generated_samples = gan.generate_samples(sampleSize)
            
            # Save generated samples
            output_filename = f"Generated_Samples_{sampleSize}.csv"
            output_path = os.path.join(SAVEPATH, output_filename)
            os.makedirs(SAVEPATH, exist_ok=True)
            generated_samples.to_csv(output_path, sep=';', index=False)
            
            progress_label.config(text=f"Generation completed! Saved to: {output_filename}", fg="green")
            tk.messagebox.showinfo("Success", f"Generated {sampleSize} samples successfully!\nSaved to: {output_path}")
            
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Invalid input: {e}")
        except ImportError as e:
            tk.messagebox.showerror("Error", f"Module not found: {e}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
    
    # Class column input
    class_label = tk.Label(new_window, text="Name of class column", font=("Arial", 10))
    class_label.pack(pady=5)
    class_entry = tk.Entry(new_window, font=("Arial", 10), width=30)
    class_entry.pack(pady=5)
    
    # Sample size input (main new feature)
    sample_size_label = tk.Label(new_window, text="Number of samples to generate", font=("Arial", 10))
    sample_size_label.pack(pady=5)
    sample_size_entry = tk.Entry(new_window, font=("Arial", 10), width=30)
    sample_size_entry.insert(0, "1000")  # Default value
    sample_size_entry.pack(pady=5)
    
    # Optional parameters with default values
    tk.Label(new_window, text="Optional Parameters (leave empty for defaults)", font=("Arial", 9), fg="gray").pack(pady=(10, 5))
    
    epochs_label = tk.Label(new_window, text="Epochs", font=("Arial", 9))
    epochs_label.pack(pady=2)
    epochs_entry = tk.Entry(new_window, font=("Arial", 9), width=30)
    epochs_entry.pack(pady=2)
    ToolTip(epochs_entry, "Number of training epochs for the GAN. Default is 1000.")
    
    batch_size_label = tk.Label(new_window, text="Batch size", font=("Arial", 9))
    batch_size_label.pack(pady=2)
    batch_size_entry = tk.Entry(new_window, font=("Arial", 9), width=30)
    batch_size_entry.pack(pady=2)
    ToolTip(batch_size_entry, "Batch size for training the GAN. Default is 96.")
    
    latent_dim_label = tk.Label(new_window, text="Latent dimension", font=("Arial", 9))
    latent_dim_label.pack(pady=2)
    latent_dim_entry = tk.Entry(new_window, font=("Arial", 9), width=30)
    latent_dim_entry.pack(pady=2)
    ToolTip(latent_dim_entry, "Dimensionality of the latent space. Default is 20.")
    
    learning_rate_label = tk.Label(new_window, text="Learning rate", font=("Arial", 9))
    learning_rate_label.pack(pady=2)
    learning_rate_entry = tk.Entry(new_window, font=("Arial", 9), width=30)
    learning_rate_entry.pack(pady=2)
    ToolTip(learning_rate_entry, "Learning rate for the GAN optimizer. Default is 0.0001.")
    
    beta1_label = tk.Label(new_window, text="Beta1", font=("Arial", 9))
    beta1_label.pack(pady=2)
    beta1_entry = tk.Entry(new_window, font=("Arial", 9), width=30)
    beta1_entry.pack(pady=2)
    ToolTip(beta1_entry, "Beta1 parameter for the Adam optimizer. Default is 0.5.")
    
    button_frame = tk.Frame(new_window)
    button_frame.pack(pady=20)
    
    generate_button = tk.Button(button_frame, text="Generate Samples", command=startGeneration, 
                               font=("Arial", 12), width=20, height=2, bg='lightgreen')
    generate_button.pack(side='left', padx=10, pady=20)

    cancel_button = tk.Button(button_frame, text="Cancel", 
                             command=new_window.destroy, 
                             font=("Arial", 12), width=15, height=2, bg='lightcoral')
    cancel_button.pack(side='left', padx=10, pady=20)

def findParameters():
    new_window = tk.Toplevel(gui)
    new_window.title("Search Parameters")
    new_window.geometry("400x650")
    new_window.resizable(width=False, height=False)
    
    def searchParameters():
        try:
            if not FILENAME:
                tk.messagebox.showerror("Error", "Please select a data file first!")
                return
            if not SAVEPATH:
                tk.messagebox.showerror("Error", "Please select a save path first!")
                return
                
            classLabel = class_entry.get().strip()
            if not classLabel:
                tk.messagebox.showerror("Error", "Please enter a class column name!")
                return
            
            epoch_str = epoch_entry.get().strip()
            if not epoch_str:
                tk.messagebox.showerror("Error", "Please enter epoch count!")
                return
            epoch = int(epoch_str)
            
            # Parse and validate iterations (only for random search)
            search_type = search_var.get()
            numIterations = 0
            if search_type == "random":
                iterations_str = numIterations_entry.get().strip()
                if not iterations_str:
                    tk.messagebox.showerror("Error", "Please enter number of iterations for random search!")
                    return
                numIterations = int(iterations_str)
            
            # Parse parameter lists with better error handling
            def parse_int_list(input_str, param_name):
                if not input_str.strip():
                    raise ValueError(f"{param_name} cannot be empty!")
                values = []
                for item in input_str.split(','):
                    item = item.strip()
                    if item:  # Only process non-empty items
                        try:
                            values.append(int(item))
                        except ValueError:
                            raise ValueError(f"Invalid integer value '{item}' in {param_name}")
                if not values:
                    raise ValueError(f"No valid values found in {param_name}")
                return values
            
            def parse_float_list(input_str, param_name):
                if not input_str.strip():
                    raise ValueError(f"{param_name} cannot be empty!")
                values = []
                for item in input_str.split(','):
                    item = item.strip()
                    if item:  # Only process non-empty items
                        try:
                            values.append(float(item))
                        except ValueError:
                            raise ValueError(f"Invalid float value '{item}' in {param_name}")
                if not values:
                    raise ValueError(f"No valid values found in {param_name}")
                return values
            
            # Parse all parameter lists
            latentDim = parse_int_list(latentDim_entry.get(), "Latent dimension")
            batchSize = parse_int_list(batchSize_entry.get(), "Batch size")
            learningRate = parse_float_list(learningRate_entry.get(), "Learning rate")
            beta1 = parse_float_list(beta1_entry.get(), "Beta1")
           
            # Show progress message
            progress_label = tk.Label(new_window, text="Starting parameter search...", 
                                    font=("Arial", 10), fg="blue")
            progress_label.pack(pady=10)
            new_window.update()
           
            from gan_parameter_tuning import search
            search(classLabel, epoch, numIterations, latentDim, batchSize, learningRate, beta1, 
                  data_path=FILENAME, results_dir=SAVEPATH, search_type=search_type, integer_columns=INTEGER_COLUMNS)
            new_window.destroy()
            tk.messagebox.showinfo("Success", "Parameter search completed!")
        except ValueError as e:
            tk.messagebox.showerror("Error", f"Invalid input: {e}")
        except ImportError as e:
            tk.messagebox.showerror("Error", f"Module not found: {e}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def on_search_type_change():
        """Callback function to update UI when search type changes"""
        search_type = search_var.get()
        
        if search_type == "grid":
            # For grid search, disable iterations entry and update label
            numIterations_entry.config(state="disabled", bg='lightgray')
            numIterations_label.config(text="Number of iterations (disabled for grid search)", 
                                     fg='gray')
            # Update info label
            info_label.config(text="Grid search will try ALL parameter combinations", 
                            fg='blue', bg='lightgray')
        else:  # random search
            # For random search, enable iterations entry and update label
            numIterations_entry.config(state="normal", bg='white')
            numIterations_label.config(text="Number of iterations (required for random search)", 
                                     fg='black')
            # Update info label
            info_label.config(text="Random search will try RANDOM parameter combinations", 
                            fg='green', bg='lightgray')

    search_type_label = tk.Label(new_window, text="Search Type", font=("Arial", 10, "bold"))
    search_type_label.pack(pady=5)
    search_var = tk.StringVar(value="grid")
    grid_radio = tk.Radiobutton(new_window, text="Grid Search (tries all combinations)", 
                                variable=search_var, command=on_search_type_change, value="grid", font=("Arial", 9),
                              )
    grid_radio.pack(pady=2)
    random_radio = tk.Radiobutton(new_window, text="Random Search (tries random combinations)", 
                                 variable=search_var, command=on_search_type_change, value="random", font=("Arial", 9))
    random_radio.pack(pady=2)

    info_label = tk.Label(new_window, text="Grid search will try ALL parameter combinations", 
                         font=("Arial", 9), bg='white', fg='blue')
    info_label.pack(pady=5)

    class_label = tk.Label(new_window, text="Name of a class column", font=("Arial", 8))
    class_label.pack(pady=5)
    class_entry = tk.Entry(new_window, font=("Arial", 8))
    class_entry.pack(pady=5)

    epoch_label = tk.Label(new_window, text="Epoch count", font=("Arial", 8))
    epoch_label.pack(pady=5)
    epoch_entry = tk.Entry(new_window, font=("Arial", 8))
    epoch_entry.pack(pady=5)
    ToolTip(epoch_entry, "Number of training epochs for the GAN.")

    numIterations_label = tk.Label(new_window, text="Number of iterations", font=("Arial", 8))
    numIterations_label.pack(pady=5)
    numIterations_entry = tk.Entry(new_window, font=("Arial", 8))
    numIterations_entry.pack(pady=5)
    if search_var.get() == "grid":
        numIterations_entry.config(state="disabled")
    else:
        numIterations_entry.config(state="normal")
    

    latentDim_label = tk.Label(new_window, text="Latent dimension values (Comma separated)", font=("Arial", 8))
    latentDim_label.pack(pady=5)
    latentDim_entry = tk.Entry(new_window, font=("Arial", 8))
    latentDim_entry.pack(pady=5)
    ToolTip(latentDim_entry, "Dimensionality of the latent space. Provide multiple values separated by commas for grid search.")

    batchSize_label = tk.Label(new_window, text="Batch size values (Comma separated)", font=("Arial", 8))
    batchSize_label.pack(pady=5)
    batchSize_entry = tk.Entry(new_window, font=("Arial", 8))
    batchSize_entry.pack(pady=5)
    ToolTip(batchSize_entry, "Batch size for training the GAN. Provide multiple values separated by commas for grid search.")

    learningRate_label = tk.Label(new_window, text="Learning rate values (Comma separated)", font=("Arial", 8))
    learningRate_label.pack(pady=5)
    learningRate_entry = tk.Entry(new_window, font=("Arial", 8))
    learningRate_entry.pack(pady=5)
    ToolTip(learningRate_entry, "Learning rate for training the GAN. Provide multiple values separated by commas for grid search.")

    beta1_label = tk.Label(new_window, text="Beta1 values (Comma separated)", font=("Arial", 8))
    beta1_label.pack(pady=5)
    beta1_entry = tk.Entry(new_window, font=("Arial", 8))
    beta1_entry.pack(pady=5)
    ToolTip(beta1_entry, "Beta1 for Adam optimizer. Provide multiple values separated by commas for grid search.")

    button_frame = tk.Frame(new_window)
    button_frame.pack(pady=20)
    
    search_button = tk.Button(button_frame, text="Start the search", command=searchParameters, font=("Arial", 12), width=20, height=2, bg='lightgray')
    search_button.pack(side='left', padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", 
                             command=new_window.destroy, 
                             font=("Arial", 12), width=15, height=2, bg='lightcoral')
    cancel_button.pack(side='left', padx=10)

    on_search_type_change()


gui = tk.Tk()
gui.title("GAN synthetic data generator")
gui.configure(bg='white')
gui.geometry("800x600")
gui.resizable(width=False, height=False)
title_label = tk.Label(gui, text="GAN Synthetic Data Generator", font=("Arial", 24), bg='white')
title_label.pack(pady=30)

setup_frame = tk.Frame(gui, bg='white')
setup_frame.pack(pady=25)
# Create buttons for different functionalities
setup_button = tk.Button(setup_frame, text="Setup Paths", command=setupPaths, font=("Arial", 16), width=20, height=2, bg='lightblue')
setup_button.pack(pady=5)
ToolTip(setup_button, "Define data file path and save path")

path_label = tk.Label(setup_frame, text="No save path selected", font=("Arial", 10), bg='white')
path_label.pack(pady=5)

# Label to show selected file
file_label = tk.Label(setup_frame, text="No file selected", font=("Arial", 10), bg='white')
file_label.pack(pady=5)

setParameters_button = tk.Button(gui, text="Generate Samples", command=generateSamples, font=("Arial", 16), width=20, height=2, bg='lightgreen')
setParameters_button.pack(pady=10)
ToolTip(setParameters_button, "Run the GAN to generate synthetic samples based on the selected data file and parameters")

findParameters_button = tk.Button(gui, text="Find Parameters", command=findParameters, font=("Arial", 16), width=20, height=2, bg='lightgreen')
findParameters_button.pack(pady=10)
ToolTip(findParameters_button, "Do the grid or random search for GAN parameters to optimize the model performance based on the lowest " \
                                "discriminator or generator loss saved in the results directory")
terminate_button = tk.Button(gui, text="End Program", command=gui.destroy, font=("Arial", 16), width=20, height=2, bg='red')
terminate_button.pack(pady=10)

gui.mainloop()