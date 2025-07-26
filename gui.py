import tkinter as tk
from GUI_tooltip import ToolTip
from GUI_setup_paths import setupPaths
from GUI_generate_samples import generateSamples
from GUI_find_parameters import findParameters
import GUI_globals as globals
from GUI_theme import toggle_theme

def create_main_gui():
    current_theme = globals.CURRENT_THEME
    gui = tk.Tk()
    gui.title("GAN synthetic data generator")
    gui.configure(bg=current_theme['bg'])
    gui.geometry("800x600")
    gui.resizable(width=False, height=False)


    # Add theme toggle button in top right
    theme_button = tk.Button(
        gui, 
        text='🌙',
        font=("Arial", 12),
        width=3,
        bg=globals.LIGHT_MODE['button_bg'],
        fg=globals.LIGHT_MODE['text'],
        border=0
    )
    theme_button.place(relx=0.97, rely=0.02, anchor='ne')
    ToolTip(theme_button, "Toggle Light/Dark mode")
    
    title_label = tk.Label(gui, text="GAN Synthetic Data Generator", font=("Arial", 24), bg=current_theme['bg'], fg=current_theme['text'])
    title_label.pack(pady=30)
    globals.WIDGETS.append((title_label, 'label'))

    setup_frame = tk.Frame(gui, bg=current_theme['bg'])
    setup_frame.pack(pady=25)
    globals.WIDGETS.append((setup_frame, 'frame'))
    
    # Create buttons for different functionalities
    setup_button = tk.Button(setup_frame, text="Setup Paths", 
                            command=lambda: setupPaths(gui, file_label, path_label), 
                            font=("Arial", 16), width=20, height=2, bg=current_theme['button_bg'])
    setup_button.pack(pady=5)
    ToolTip(setup_button, "Define data file path and save path")
    globals.WIDGETS.append((setup_button, 'setup_button'))

    path_label = tk.Label(setup_frame, text="No save path selected", font=("Arial", 10), bg=current_theme['bg'], 
                       fg=current_theme['text'])
    path_label.pack(pady=5)
    globals.WIDGETS.append((path_label, 'label'))

    # Label to show selected file
    file_label = tk.Label(setup_frame, text="No file selected", font=("Arial", 10), bg=current_theme['bg'], 
                       fg=current_theme['text'])
    file_label.pack(pady=5)
    globals.WIDGETS.append((file_label, 'label'))
    
    setParameters_button = tk.Button(gui, text="Generate Samples", 
                                   command=lambda: generateSamples(gui), 
                                   font=("Arial", 16), width=20, height=2, bg=current_theme['generate_bg'])
    setParameters_button.pack(pady=10)
    globals.WIDGETS.append((setParameters_button, 'generate_button'))
    ToolTip(setParameters_button, "Run the GAN to generate synthetic samples based on the selected data file and parameters")

    findParameters_button = tk.Button(gui, text="Find Parameters", 
                                    command=lambda: findParameters(gui), 
                                    font=("Arial", 16), width=20, height=2, bg=current_theme['generate_bg'])
    findParameters_button.pack(pady=10)
    globals.WIDGETS.append((findParameters_button, 'generate_button'))
    ToolTip(findParameters_button, "Do the grid or random search for GAN parameters to optimize the model performance based on the lowest " \
                                    "discriminator or generator loss saved in the results directory")
    
    theme_button.configure(
        command=lambda: toggle_theme(gui, theme_button,widgets=globals.WIDGETS)
    )

    terminate_button = tk.Button(gui, text="End Program", command=gui.destroy, font=("Arial", 16), width=20, height=2, bg='red')
    terminate_button.pack(pady=10)

    gui.mainloop()

if __name__ == "__main__":
    create_main_gui()