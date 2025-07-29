import tkinter as tk
from tkinter import messagebox
import os
import GUI_globals as globals
from GUI_tooltip import ToolTip


class GenerateSamplesWindow:
    """Window for generating samples"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_theme = globals.CURRENT_THEME
        self.entries = {}
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Generate Samples")
        self.window.geometry("500x900")
        self.window.configure(bg=self.current_theme['bg'])
        self.window.resizable(width=False, height=False)
        
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.create_required_fields()
        self.create_optional_parameters()
        self.create_network_architecture()
        self.create_control_buttons()
    
    def create_required_fields(self):
        """Create required input fields"""
        # Class column input
        self.create_labeled_entry("class", "Name of class column", font_size=10, required=True)
        
        # Target class input
        target_entry = self.create_labeled_entry("target_class", "Target class (optional)", font_size=10)
        ToolTip(target_entry, "Specific class to generate. Leave empty to generate mixed classes.")
        
        # Sample size input
        sample_entry = self.create_labeled_entry("sample_size", "Number of samples to generate", 
                                                font_size=10, default_value="1000")
    
    def create_optional_parameters(self):
        """Create optional parameter fields"""
        tk.Label(
            self.window, 
            text="Optional Parameters (leave empty for defaults)",
            font=("Arial", 9, 'bold'), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        ).pack(pady=(10, 5))
        
        # Create optional parameter entries
        optional_params = [
            ("epochs", "Epochs", "Number of training epochs for the GAN. Default is 1000."),
            ("batch_size", "Batch size", "Batch size for training the GAN. Default is 96."),
            ("latent_dim", "Latent dimension", "Dimensionality of the latent space. Default is 20."),
            ("learning_rate", "Learning rate", "Learning rate for the GAN optimizer. Default is 0.0001."),
            ("beta1", "Beta1", "Beta1 parameter for the Adam optimizer. Default is 0.5.")
        ]
        
        for param_key, label_text, tooltip_text in optional_params:
            entry = self.create_labeled_entry(param_key, label_text, font_size=9)
            ToolTip(entry, tooltip_text)
    
    def create_network_architecture(self):
        """Create network architecture configuration"""
        tk.Label(
            self.window, 
            text="Network Architecture",
            font=("Arial", 9, 'bold'), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        ).pack(pady=(10, 5))
        
        # Generator layers
        gen_entry = self.create_labeled_entry("gen_layers", "Generator layers", font_size=9)
        ToolTip(gen_entry, "Generator hidden layers as comma-separated values (e.g., '256,512,1024'). Default is [256, 512, 1024].")
        
        # Discriminator layers
        disc_entry = self.create_labeled_entry("disc_layers", "Discriminator layers", font_size=9)
        ToolTip(disc_entry, "Discriminator hidden layers as comma-separated values (e.g., '768,512,256'). Default is [768, 512, 256].")
    
    def create_labeled_entry(self, key, label_text, font_size=10, default_value="", required=False):
        """Create a labeled entry widget"""
        label = tk.Label(
            self.window, 
            text=label_text,
            font=("Arial", font_size), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        label.pack(pady=2 if font_size == 9 else 5)
        
        entry = tk.Entry(self.window, font=("Arial", font_size), width=30)
        if default_value:
            entry.insert(0, default_value)
        entry.pack(pady=2 if font_size == 9 else 5)
        
        self.entries[key] = entry
        return entry
    
    def create_control_buttons(self):
        """Create control buttons"""
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=20)
        
        generate_button = tk.Button(
            button_frame, 
            text="Generate Samples",
            command=self.start_generation,
            font=("Arial", 12), 
            width=20, 
            height=2, 
            bg=self.current_theme['generate_bg']
        )
        generate_button.pack(side='left', padx=10, pady=20)
        
        cancel_button = tk.Button(
            button_frame, 
            text="Cancel",
            command=self.window.destroy,
            font=("Arial", 12), 
            width=15, 
            height=2, 
            bg='red'
        )
        cancel_button.pack(side='left', padx=10, pady=20)
    
    def parse_layer_input(self, layer_string):
        """Parse comma-separated layer string into list of integers"""
        if not layer_string.strip():
            return None
        try:
            layers = [int(x.strip()) for x in layer_string.split(',')]
            return layers if layers else None
        except ValueError:
            raise ValueError("Layer configuration must be comma-separated integers (e.g., '256,512,1024')")
    
    def start_generation(self):
        """Start the sample generation process"""
        try:
            if not globals.FILENAME:
                messagebox.showerror("Error", "Please select a data file first!")
                return
            if not globals.SAVEPATH:
                messagebox.showerror("Error", "Please select a save path first!")
                return
            
            # Get required parameters
            class_label = self.entries['class'].get()
            if not class_label:
                messagebox.showerror("Error", "Please enter a class column name!")
                return
            
            sample_size = int(self.entries['sample_size'].get())
            if sample_size <= 0:
                messagebox.showerror("Error", "Sample size must be a positive integer!")
                return
            
            # Get optional parameters with defaults
            target_class = int(self.entries['target_class'].get()) if self.entries['target_class'].get() else None
            epochs = int(self.entries['epochs'].get()) if self.entries['epochs'].get() else 1000
            batch_size = int(self.entries['batch_size'].get()) if self.entries['batch_size'].get() else 96
            latent_dim = int(self.entries['latent_dim'].get()) if self.entries['latent_dim'].get() else 20
            learning_rate = float(self.entries['learning_rate'].get()) if self.entries['learning_rate'].get() else 0.0001
            beta1 = float(self.entries['beta1'].get()) if self.entries['beta1'].get() else 0.5
            
            # Parse generator and discriminator layers
            gen_layers = self.parse_layer_input(self.entries['gen_layers'].get())
            disc_layers = self.parse_layer_input(self.entries['disc_layers'].get())
            
            # Show progress message
            progress_label = tk.Label(
                self.window, 
                text="Training GAN and generating samples...",
                font=("Arial", 10), 
                fg="blue"
            )
            progress_label.pack(pady=10)
            self.window.update()
            
            from tabular_gan_modified import TabularGAN
            
            # Initialize and train GAN
            gan = TabularGAN(
                globals.FILENAME, 
                class_column=class_label,
                integer_columns=globals.INTEGER_COLUMNS,
                latent_dim=latent_dim,
                learning_rate=learning_rate,
                beta1=beta1
            )
            
            # Rebuild GAN with custom layers if specified
            if gen_layers is not None or disc_layers is not None:
                gan.rebuild_with_params(
                    gen_layers=gen_layers,
                    disc_layers=disc_layers,
                    learning_rate=learning_rate,
                    beta1=beta1
                )
            
            # Train the GAN
            history = gan.train(epochs=epochs, batch_size=batch_size, verbose=1)
            
            # Generate samples
            generated_samples = gan.generate_samples(sample_size, target_class=target_class)
            
            # Save generated samples
            output_filename = f"Generated_Samples_{sample_size}.csv"
            output_path = os.path.join(globals.SAVEPATH, output_filename)
            os.makedirs(globals.SAVEPATH, exist_ok=True)
            generated_samples.to_csv(output_path, sep=';', index=False)
            
            progress_label.config(text=f"Generation completed! Saved to: {output_filename}", fg="green")
            messagebox.showinfo("Success", f"Generated {sample_size} samples successfully!\nSaved to: {output_path}")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except ImportError as e:
            messagebox.showerror("Error", f"Module not found: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Legacy function for backward compatibility
def generateSamples(gui):
    """Legacy function for backward compatibility"""
    GenerateSamplesWindow(gui)