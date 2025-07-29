import tkinter as tk
from tkinter import ttk, messagebox
import GUI_globals as globals
from GUI_tooltip import ToolTip


class FindParametersWindow:
    """Window for parameter search functionality"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_theme = globals.CURRENT_THEME
        self.entries = {}
        self.search_var = tk.StringVar(value="grid")
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Search Parameters")
        self.window.geometry("800x700")  # Made wider for 2 columns, shorter height
        self.window.configure(bg=self.current_theme['bg'])
        self.window.resizable(width=False, height=False)
        
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.create_search_type_section()
        self.create_parameter_fields()
        self.create_control_buttons()
        self.on_search_type_change()  # Initialize UI state
    
    def create_search_type_section(self):
        """Create search type selection section"""
        search_type_label = tk.Label(
            self.window, 
            text="Search Type:",
            font=("Arial", 10, "bold"), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        search_type_label.pack(pady=5)
        
        radio_frame = tk.Frame(self.window, bg='lightgray')
        radio_frame.pack(pady=10)
        
        grid_radio = tk.Radiobutton(
            radio_frame, 
            text="Grid Search (tries all combinations)",
            variable=self.search_var,
            command=self.on_search_type_change,
            value="grid",
            font=("Arial", 9), 
            bg='lightgray'
        )
        grid_radio.pack(pady=2)
        
        random_radio = tk.Radiobutton(
            radio_frame, 
            text="Random Search (tries random combinations)",
            variable=self.search_var,
            command=self.on_search_type_change,
            value="random",
            font=("Arial", 9), 
            bg='lightgray'
        )
        random_radio.pack(pady=2)
        
        self.info_label = tk.Label(
            radio_frame, 
            text="Grid search will try ALL parameter combinations",
            font=("Arial", 9), 
            fg='black', 
            bg='lightgray'
        )
        self.info_label.pack(pady=5)
    
    def create_parameter_fields(self):
        """Create parameter input fields in a 2-column layout"""
        # Create main frame for 2-column layout
        main_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        main_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Create left and right columns
        left_column = tk.Frame(main_frame, bg=self.current_theme['bg'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_column = tk.Frame(main_frame, bg=self.current_theme['bg'])
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Left column entries
        self.create_column_entries(left_column, [
            ("class", "Name of a class column:", "Name of the class column in your dataset"),
            ("epochs", "Epoch count:", "Number of training epochs for the GAN"),
            ("latent_dim", "Latent dimension values (Comma separated):", 
             "Dimensionality of the latent space. Provide multiple values separated by commas for grid search."),
            ("batch_size", "Batch size values (Comma separated):",
             "Batch size for training the GAN. Provide multiple values separated by commas for grid search.")
        ])
        
        # Right column entries
        self.create_column_entries(right_column, [
            ("learning_rate", "Learning rate values (Comma separated):",
             "Learning rate for training the GAN. Provide multiple values separated by commas for grid search."),
            ("beta1", "Beta1 values (Comma separated):",
             "Beta1 for Adam optimizer. Provide multiple values separated by commas for grid search.")
        ])
        
        # Add iterations field to right column (will be enabled/disabled based on search type)
        self.numIterations_label = tk.Label(
            right_column, 
            text="Number of iterations:",
            font=("Arial", 8), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        self.numIterations_label.pack(pady=(10, 2), anchor='w')
        
        self.numIterations_entry = tk.Entry(right_column, font=("Arial", 8), width=40)
        self.numIterations_entry.pack(pady=(0, 10), fill='x')
        self.entries['iterations'] = self.numIterations_entry
        
        # Layer configurations (full width)
        self.create_layer_config_fields(right_column)
    
    def create_column_entries(self, parent, entry_configs):
        """Create entries for a specific column"""
        for key, label_text, tooltip_text in entry_configs:
            # Create label
            label = tk.Label(
                parent, 
                text=label_text,
                font=("Arial", 8), 
                bg=self.current_theme['bg'], 
                fg=self.current_theme['text']
            )
            label.pack(pady=(10, 2), anchor='c')
            
            # Create entry
            entry = tk.Entry(parent, font=("Arial", 8), width=40)
            entry.pack(pady=(0, 10), fill='x')
            
            # Store entry and add tooltip
            self.entries[key] = entry
            ToolTip(entry, tooltip_text)
    
    def create_layer_config_fields(self, parent):
        """Create layer configuration fields (full width)"""
        # Create a separate frame for layer configs
        layer_frame = tk.Frame(parent, bg=self.current_theme['bg'])
        layer_frame.pack(pady=20, fill='x')
        
        # Generator layers
        gen_layers_label = tk.Label(
            layer_frame,
            text="Generator layers:",
            font=("Arial", 8), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        gen_layers_label.pack(pady=(0, 2), anchor='c')
        
        gen_layers_entry = tk.Entry(layer_frame, font=("Arial", 8))
        gen_layers_entry.pack(pady=(0, 10), fill='x')
        self.entries['gen_layers'] = gen_layers_entry
        
        gen_layers_tooltip = """Generator layer configuration:
        - Format: config1;config2;...
        - Each config is a comma-separated list of integers
        - Example: 256,512,1024;128,256,512
        - Each configuration will be tested separately
        - Leave empty for default configuration
        - Layers are applied from input to output"""
        ToolTip(gen_layers_entry, gen_layers_tooltip)
        
        # Discriminator layers
        disc_layers_label = tk.Label(
            layer_frame,
            text="Discriminator layers:",
            font=("Arial", 8), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        disc_layers_label.pack(pady=(0, 2), anchor='c')
        
        disc_layers_entry = tk.Entry(layer_frame, font=("Arial", 8))
        disc_layers_entry.pack(pady=(0, 10), fill='x')
        self.entries['disc_layers'] = disc_layers_entry
        
        disc_layers_tooltip = """Discriminator layer configuration:
        - Format: config1;config2;...
        - Each config is a comma-separated list of integers
        - Example: 768,512,256;512,256,128
        - Each configuration will be tested separately
        - Leave empty for default configuration
        - Layers are applied from input to output"""
        ToolTip(disc_layers_entry, disc_layers_tooltip)
    
    def create_labeled_entry(self, key, label_text, font_size=8):
        """Create a labeled entry widget (legacy method for compatibility)"""
        label = tk.Label(
            self.window, 
            text=label_text,
            font=("Arial", font_size), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        label.pack(pady=5)
        
        entry = tk.Entry(self.window, font=("Arial", font_size))
        entry.pack(pady=5)
        
        self.entries[key] = entry
        return entry
    
    def create_control_buttons(self):
        """Create control buttons"""
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=20)
        
        search_button = tk.Button(
            button_frame, 
            text="Start the search",
            command=self.search_parameters,
            font=("Arial", 12), 
            width=20, 
            height=2, 
            bg=self.current_theme['generate_bg']
        )
        search_button.pack(side='left', padx=10)
        
        cancel_button = tk.Button(
            button_frame, 
            text="Cancel",
            command=self.window.destroy,
            font=("Arial", 12), 
            width=15, 
            height=2, 
            bg='red'
        )
        cancel_button.pack(side='left', padx=10)
    
    def on_search_type_change(self):
        """Callback function to update UI when search type changes"""
        search_type = self.search_var.get()
        
        if search_type == "grid":
            # For grid search, disable iterations entry and update label
            self.numIterations_entry.config(state="disabled", disabledbackground='gray')
            self.numIterations_label.config(
                text="Number of iterations (disabled for grid search)",
                fg=self.current_theme['text']
            )
            # Update info label
            self.info_label.config(
                text="Grid search will try ALL parameter combinations",
                font=("Arial", 9, 'bold')
            )
        else:  # random search
            # For random search, enable iterations entry and update label
            self.numIterations_entry.config(state="normal", bg='white')
            self.numIterations_label.config(
                text="Number of iterations (required for random search)",
                fg=self.current_theme['text']
            )
            # Update info label
            self.info_label.config(
                text="Random search will try RANDOM parameter combinations",
                font=("Arial", 9, 'bold')
            )
    
    def update_progress(self, progress_var, progress_label, current, total):
        """Update progress bar and label"""
        progress = (current / total) * 100
        progress_var.set(progress)
        progress_label.config(text=f"Progress: {current}/{total} trials completed ({progress:.1f}%)")
        self.window.update()
    
    def parse_parameter_lists(self):
        """Parse and validate all parameter lists"""
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
        
        # Parse all parameters
        return {
            'latent_dim': parse_int_list(self.entries['latent_dim'].get(), "Latent dimension"),
            'batch_size': parse_int_list(self.entries['batch_size'].get(), "Batch size"),
            'learning_rate': parse_float_list(self.entries['learning_rate'].get(), "Learning rate"),
            'beta1': parse_float_list(self.entries['beta1'].get(), "Beta1"),
            'gen_layers': parse_layer_config(self.entries['gen_layers'].get()),
            'disc_layers': parse_layer_config(self.entries['disc_layers'].get())
        }
    
    def search_parameters(self):
        """Start the parameter search process"""
        try:
            if not globals.FILENAME:
                messagebox.showerror("Error", "Please select a data file first!")
                return
            if not globals.SAVEPATH:
                messagebox.showerror("Error", "Please select a save path first!")
                return
            
            class_label = self.entries['class'].get().strip()
            if not class_label:
                messagebox.showerror("Error", "Please enter a class column name!")
                return
            
            epoch_str = self.entries['epochs'].get().strip()
            if not epoch_str:
                messagebox.showerror("Error", "Please enter epoch count!")
                return
            try:
                epoch = int(epoch_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid epoch count! Please enter an integer.")
                return
            
            # Parse and validate iterations (only for random search)
            search_type = self.search_var.get()
            num_iterations = 0
            if search_type == "random":
                iterations_str = self.entries['iterations'].get().strip()
                if not iterations_str:
                    messagebox.showerror("Error", "Please enter number of iterations for random search!")
                    return
                num_iterations = int(iterations_str)
            
            # Parse parameter lists
            params = self.parse_parameter_lists()
            
            # Show progress message
            searching_label = tk.Label(
                self.window, 
                text="Starting parameter search...",
                font=("Arial", 10), 
                bg=self.current_theme['bg'], 
                fg="blue"
            )
            searching_label.pack(pady=10)
            self.window.update()
            
            progress_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
            progress_frame.pack(pady=10, padx=20, fill='x')
            
            progress_var = tk.DoubleVar()
            progress_label = tk.Label(
                progress_frame, 
                text="Progress: 0/0 trials completed (0%)",
                font=("Arial", 9), 
                bg=self.current_theme['bg'], 
                fg=self.current_theme['text']
            )
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
            search(
                class_label, epoch, num_iterations,
                params['latent_dim'], params['batch_size'], 
                params['learning_rate'], params['beta1'],
                data_path=globals.FILENAME,
                results_dir=globals.SAVEPATH,
                search_type=search_type,
                integer_columns=globals.INTEGER_COLUMNS,
                gen_layers=params['gen_layers'],
                disc_layers=params['disc_layers'],
                progress_callback=lambda current, total: self.update_progress(
                    progress_var, progress_label, current, total
                )
            )
            
            self.window.destroy()
            messagebox.showinfo("Success", "Parameter search completed!")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except ImportError as e:
            messagebox.showerror("Error", f"Module not found: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Legacy function for backward compatibility
def findParameters(gui):
    """Legacy function for backward compatibility"""
    FindParametersWindow(gui)