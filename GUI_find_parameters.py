import tkinter as tk
import GUI_globals as globals
from GUI_tooltip import ToolTip

def findParameters(gui):
    new_window = tk.Toplevel(gui)
    new_window.title("Search Parameters")
    new_window.geometry("400x650")
    new_window.resizable(width=False, height=False)
    
    def searchParameters():
        try:
            if not globals.FILENAME:
                tk.messagebox.showerror("Error", "Please select a data file first!")
                return
            if not globals.SAVEPATH:
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
                  data_path=globals.FILENAME, results_dir=globals.SAVEPATH, search_type=search_type, integer_columns=globals.INTEGER_COLUMNS)
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