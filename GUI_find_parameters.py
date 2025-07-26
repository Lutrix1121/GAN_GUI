import tkinter as tk
from tkinter import ttk
import GUI_globals as globals
from GUI_tooltip import ToolTip

def findParameters(gui):
    current_theme = globals.CURRENT_THEME
    new_window = tk.Toplevel(gui)
    new_window.title("Search Parameters")
    new_window.geometry("600x1000")
    new_window.configure(bg=globals.CURRENT_THEME['bg'])
    new_window.resizable(width=False, height=False)

    new_window.transient(gui)
    new_window.grab_set()
    new_window.focus_set()

    def update_progress(progress_var, progress_label, current, total):
        progress = (current / total) * 100
        progress_var.set(progress)
        progress_label.config(text=f"Progress: {current}/{total} trials completed ({progress:.1f}%)")
        new_window.update()
    
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
            
            def parse_layer_config(input_str):
                """Parse layer configuration string into list of integers"""
                try:
                    # Split configurations by semicolon
                    configs = input_str.split(';')
                    layer_configs = []
                    
                    for config in configs:
                        if config.strip():
                            # Parse each configuration into a list of integers
                            layers = [int(x.strip()) for x in config.split(',') if x.strip()]
                            if layers:  # Only add non-empty configurations
                                layer_configs.append(layers)
                    
                    return layer_configs if layer_configs else None
        
                except ValueError as e:
                    raise ValueError(f"Invalid layer configuration: {input_str}. Format should be: 256,512,1024;128,256,512")
            
            # Parse layer configurations
            gen_layers = parse_layer_config(gen_layers_entry.get())
            disc_layers = parse_layer_config(disc_layers_entry.get())

            # Parse all parameter lists
            latentDim = parse_int_list(latentDim_entry.get(), "Latent dimension")
            batchSize = parse_int_list(batchSize_entry.get(), "Batch size")
            learningRate = parse_float_list(learningRate_entry.get(), "Learning rate")
            beta1 = parse_float_list(beta1_entry.get(), "Beta1")
           
            # Show progress message
            searching_label = tk.Label(new_window, text="Starting parameter search...", 
                                    font=("Arial", 10), bg=current_theme['bg'], fg="blue")
            searching_label.pack(pady=10)
            new_window.update()

            progress_frame = tk.Frame(new_window, bg=current_theme['bg'])
            progress_frame.pack(pady=10, padx=20, fill='x')
            
            progress_var = tk.DoubleVar()
            progress_label = tk.Label(progress_frame, text="Progress: 0/0 trials completed (0%)", font=("Arial", 9), bg=current_theme['bg'], fg=current_theme['text'])
            progress_label.pack()
            
            progress_bar = ttk.Progressbar(
                progress_frame,
                variable=progress_var,
                maximum=100,
                length=300,
                mode='determinate'
            )
            progress_bar.pack(pady=5)

           
            from gan_parameter_tuning import search
            search(classLabel, epoch, numIterations, latentDim, batchSize, learningRate, beta1, 
                   data_path=globals.FILENAME, 
                   results_dir=globals.SAVEPATH, 
                   search_type=search_type, 
                   integer_columns=globals.INTEGER_COLUMNS,
                   gen_layers=gen_layers,
                   disc_layers=disc_layers,
                   progress_callback=lambda current, 
                   total: update_progress(progress_var, progress_label, current, total))
            
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
            numIterations_entry.config(state="disabled", disabledbackground='gray')
            numIterations_label.config(text="Number of iterations (disabled for grid search)", 
                                     fg=current_theme['text'])
            # Update info label
            info_label.config(text="Grid search will try ALL parameter combinations", 
                            font=("Arial", 9, 'bold'))
        else:  # random search
            # For random search, enable iterations entry and update label
            numIterations_entry.config(state="normal", bg='white')
            numIterations_label.config(text="Number of iterations (required for random search)", 
                                     fg=current_theme['text'])
            # Update info label
            info_label.config(text="Random search will try RANDOM parameter combinations", 
                            font=("Arial", 9, 'bold'))

    search_type_label = tk.Label(new_window, text="Search Type:", font=("Arial", 10, "bold"), bg=current_theme['bg'], fg=current_theme['text'])
    search_type_label.pack(pady=5)
    search_var = tk.StringVar(value="grid")
    radio_frame = tk.Frame(new_window, bg='lightgray')
    radio_frame.pack(pady=10)
    grid_radio = tk.Radiobutton(radio_frame, text="Grid Search (tries all combinations)", 
                                variable=search_var, command=on_search_type_change, value="grid", font=("Arial", 9), bg='lightgray'
                              )
    grid_radio.pack(pady=2)
    random_radio = tk.Radiobutton(radio_frame, text="Random Search (tries random combinations)", 
                                 variable=search_var, command=on_search_type_change, value="random", font=("Arial", 9), bg='lightgray')
    random_radio.pack(pady=2)

    info_label = tk.Label(radio_frame, text="Grid search will try ALL parameter combinations", 
                         font=("Arial", 9), fg='black', bg='lightgray')
    info_label.pack(pady=5)

    class_label = tk.Label(new_window, text="Name of a class column", font=("Arial", 8), bg=current_theme['bg'], fg=current_theme['text'])
    class_label.pack(pady=5)
    class_entry = tk.Entry(new_window, font=("Arial", 8))
    class_entry.pack(pady=5)

    epoch_label = tk.Label(new_window, text="Epoch count", font=("Arial", 8), bg=current_theme['bg'], fg=current_theme['text'])
    epoch_label.pack(pady=5)
    epoch_entry = tk.Entry(new_window, font=("Arial", 8))
    epoch_entry.pack(pady=5)
    ToolTip(epoch_entry, "Number of training epochs for the GAN.")

    # Generator layers configuration
    gen_layers_label = tk.Label(new_window, 
        text="Generator layers (format: layer1,layer2,...;nextconfig... e.g., 256,512,1024;128,256,512)", 
        font=("Arial", 8), bg=current_theme['bg'], fg=current_theme['text'])
    gen_layers_label.pack(pady=5)
    gen_layers_entry = tk.Entry(new_window, font=("Arial", 8))
    gen_layers_entry.pack(pady=5)
    gen_layers_tooltip = """Generator layer configuration:
    - Format: config1;config2;...
    - Each config is a comma-separated list of integers
    - Example: 256,512,1024;128,256,512
    - Each configuration will be tested separately
    - Leave empty for default configuration
    - Layers are applied from input to output"""
    ToolTip(gen_layers_entry, gen_layers_tooltip)

    # Discriminator layers configuration
    disc_layers_label = tk.Label(new_window, 
        text="Discriminator layers (format: layer1,layer2,...;nextconfig... e.g., 768,512,256;512,256,128)", 
        font=("Arial", 8),bg=current_theme['bg'], fg=current_theme['text'])
    disc_layers_label.pack(pady=5)
    disc_layers_entry = tk.Entry(new_window, font=("Arial", 8))
    disc_layers_entry.pack(pady=5)
    disc_layers_tooltip = """Discriminator layer configuration:
    - Format: config1;config2;...
    - Each config is a comma-separated list of integers
    - Example: 768,512,256;512,256,128
    - Each configuration will be tested separately
    - Leave empty for default configuration
    - Layers are applied from input to output"""
    ToolTip(disc_layers_entry, disc_layers_tooltip)  

    numIterations_label = tk.Label(new_window, text="Number of iterations", font=("Arial", 8), bg=current_theme['bg'], fg=current_theme['text'])
    numIterations_label.pack(pady=5)
    numIterations_entry = tk.Entry(new_window, font=("Arial", 8))
    numIterations_entry.pack(pady=5)
    if search_var.get() == "grid":
        numIterations_entry.config(state="disabled")
    else:
        numIterations_entry.config(state="normal")
    

    latentDim_label = tk.Label(new_window, text="Latent dimension values (Comma separated)", font=("Arial", 8), bg=current_theme['bg'], fg=current_theme['text'])
    latentDim_label.pack(pady=5)
    latentDim_entry = tk.Entry(new_window, font=("Arial", 8))
    latentDim_entry.pack(pady=5)
    ToolTip(latentDim_entry, "Dimensionality of the latent space. Provide multiple values separated by commas for grid search.")

    batchSize_label = tk.Label(new_window, text="Batch size values (Comma separated)", font=("Arial", 8),bg = current_theme['bg'], fg=current_theme['text'])
    batchSize_label.pack(pady=5)
    batchSize_entry = tk.Entry(new_window, font=("Arial", 8))
    batchSize_entry.pack(pady=5)
    ToolTip(batchSize_entry, "Batch size for training the GAN. Provide multiple values separated by commas for grid search.")

    learningRate_label = tk.Label(new_window, text="Learning rate values (Comma separated)", font=("Arial", 8), bg=current_theme['bg'], fg=current_theme['text'])
    learningRate_label.pack(pady=5)
    learningRate_entry = tk.Entry(new_window, font=("Arial", 8))
    learningRate_entry.pack(pady=5)
    ToolTip(learningRate_entry, "Learning rate for training the GAN. Provide multiple values separated by commas for grid search.")

    beta1_label = tk.Label(new_window, text="Beta1 values (Comma separated)", font=("Arial", 8), bg=current_theme['bg'], fg=current_theme['text'])
    beta1_label.pack(pady=5)
    beta1_entry = tk.Entry(new_window, font=("Arial", 8))
    beta1_entry.pack(pady=5)
    ToolTip(beta1_entry, "Beta1 for Adam optimizer. Provide multiple values separated by commas for grid search.")

    button_frame = tk.Frame(new_window, bg=current_theme['bg'])
    button_frame.pack(pady=20)
    
    search_button = tk.Button(button_frame, text="Start the search", command=searchParameters, font=("Arial", 12), width=20, height=2, bg=current_theme['generate_bg'])
    search_button.pack(side='left', padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", 
                             command=new_window.destroy, 
                             font=("Arial", 12), width=15, height=2, bg='red')
    cancel_button.pack(side='left', padx=10)

    on_search_type_change()