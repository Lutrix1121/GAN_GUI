import tkinter as tk
from GUI_tooltip import ToolTip
from GUI_setup_paths import SetupPathsWindow
from GUI_generate_samples import GenerateSamplesWindow
from GUI_find_parameters import FindParametersWindow
import GUI_globals as globals
from GUI_theme import toggle_theme


class BaseWindow:
    """Base class for all GUI windows with common functionality"""
    
    def __init__(self, parent=None, title="Window", geometry="600x400"):
        self.parent = parent
        self.current_theme = globals.CURRENT_THEME
        
        if parent:
            self.window = tk.Toplevel(parent)
            self.window.transient(parent)
            self.window.grab_set()
            self.window.focus_set()
        else:
            self.window = tk.Tk()
            
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.configure(bg=self.current_theme['bg'])
        self.window.resizable(width=False, height=False)
    
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def create_button_frame(self, buttons_config):
        """Create a frame with buttons based on configuration"""
        button_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        button_frame.pack(pady=20)
        
        for config in buttons_config:
            button = tk.Button(
                button_frame,
                text=config['text'],
                command=config['command'],
                font=config.get('font', ("Arial", 12)),
                width=config.get('width', 15),
                height=config.get('height', 2),
                bg=config.get('bg', self.current_theme['button_bg'])
            )
            button.pack(side='left', padx=10)
        
        return button_frame


class MainGUI(BaseWindow):
    """Main GUI window class"""
    
    def __init__(self):
        super().__init__(None, "GAN synthetic data generator", "800x600")
        self.file_label = None
        self.path_label = None
        self.theme_button = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main user interface"""
        self.create_theme_button()
        self.create_title()
        self.create_setup_section()
        self.create_action_buttons()
        self.create_terminate_button()
    
    def create_theme_button(self):
        """Create theme toggle button"""
        self.theme_button = tk.Button(
            self.window,
            text='🌙',
            font=("Arial", 12),
            width=3,
            bg=globals.LIGHT_MODE['button_bg'],
            fg=globals.LIGHT_MODE['text'],
            border=0,
            command=self.toggle_theme
        )
        self.theme_button.place(relx=0.97, rely=0.02, anchor='ne')
        ToolTip(self.theme_button, "Toggle Light/Dark mode")
    
    def create_title(self):
        """Create title label"""
        title_label = tk.Label(
            self.window, 
            text="GAN Synthetic Data Generator",
            font=("Arial", 24), 
            bg=self.current_theme['bg'], 
            fg=self.current_theme['text']
        )
        title_label.pack(pady=30)
        globals.WIDGETS.append((title_label, 'label'))
    
    def create_setup_section(self):
        """Create setup section with file and path labels"""
        setup_frame = tk.Frame(self.window, bg=self.current_theme['bg'])
        setup_frame.pack(pady=25)
        globals.WIDGETS.append((setup_frame, 'frame'))
        
        # Setup button
        setup_button = tk.Button(
            setup_frame, 
            text="Setup Paths",
            command=self.open_setup_paths,
            font=("Arial", 16), 
            width=20, 
            height=2, 
            bg=self.current_theme['button_bg']
        )
        setup_button.pack(pady=5)
        ToolTip(setup_button, "Define data file path and save path")
        globals.WIDGETS.append((setup_button, 'setup_button'))
        
        # Path label
        self.path_label = tk.Label(
            setup_frame, 
            text="No save path selected",
            font=("Arial", 10), 
            bg=self.current_theme['bg'],
            fg=self.current_theme['text']
        )
        self.path_label.pack(pady=5)
        globals.WIDGETS.append((self.path_label, 'label'))
        
        # File label
        self.file_label = tk.Label(
            setup_frame, 
            text="No file selected",
            font=("Arial", 10), 
            bg=self.current_theme['bg'],
            fg=self.current_theme['text']
        )
        self.file_label.pack(pady=5)
        globals.WIDGETS.append((self.file_label, 'label'))
    
    def create_action_buttons(self):
        """Create main action buttons"""
        # Generate samples button
        generate_button = tk.Button(
            self.window, 
            text="Generate Samples",
            command=self.open_generate_samples,
            font=("Arial", 16), 
            width=20, 
            height=2, 
            bg=self.current_theme['generate_bg']
        )
        generate_button.pack(pady=10)
        globals.WIDGETS.append((generate_button, 'generate_button'))
        ToolTip(generate_button, "Run the GAN to generate synthetic samples based on the selected data file and parameters")
        
        # Find parameters button
        find_params_button = tk.Button(
            self.window, 
            text="Find Parameters",
            command=self.open_find_parameters,
            font=("Arial", 16), 
            width=20, 
            height=2, 
            bg=self.current_theme['generate_bg']
        )
        find_params_button.pack(pady=10)
        globals.WIDGETS.append((find_params_button, 'generate_button'))
        ToolTip(find_params_button, "Do the grid or random search for GAN parameters to optimize the model performance based on the lowest discriminator or generator loss saved in the results directory")
    
    def create_terminate_button(self):
        """Create terminate button"""
        terminate_button = tk.Button(
            self.window, 
            text="End Program",
            command=self.window.destroy,
            font=("Arial", 16), 
            width=20, 
            height=2, 
            bg='red'
        )
        terminate_button.pack(pady=10)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        toggle_theme(self.window, self.theme_button, widgets=globals.WIDGETS)
        self.current_theme = globals.CURRENT_THEME
    
    def open_setup_paths(self):
        """Open setup paths window"""
        SetupPathsWindow(self.window, self.file_label, self.path_label)
    
    def open_generate_samples(self):
        """Open generate samples window"""
        GenerateSamplesWindow(self.window)
    
    def open_find_parameters(self):
        """Open find parameters window"""
        FindParametersWindow(self.window)
    
    def run(self):
        """Start the main GUI loop"""
        self.window.mainloop()


# Factory function to maintain compatibility with existing code
def create_main_gui():
    """Create and run the main GUI - maintains compatibility with existing code"""
    app = MainGUI()
    app.run()


if __name__ == "__main__":
    create_main_gui()