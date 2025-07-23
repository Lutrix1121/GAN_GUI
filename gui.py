import tkinter as tk
from GUI_tooltip import ToolTip
from GUI_setup_paths import setupPaths
from GUI_generate_samples import generateSamples
from GUI_find_parameters import findParameters

def create_main_gui():
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
    setup_button = tk.Button(setup_frame, text="Setup Paths", 
                            command=lambda: setupPaths(gui, file_label, path_label), 
                            font=("Arial", 16), width=20, height=2, bg='lightblue')
    setup_button.pack(pady=5)
    ToolTip(setup_button, "Define data file path and save path")

    path_label = tk.Label(setup_frame, text="No save path selected", font=("Arial", 10), bg='white')
    path_label.pack(pady=5)

    # Label to show selected file
    file_label = tk.Label(setup_frame, text="No file selected", font=("Arial", 10), bg='white')
    file_label.pack(pady=5)

    setParameters_button = tk.Button(gui, text="Generate Samples", 
                                   command=lambda: generateSamples(gui), 
                                   font=("Arial", 16), width=20, height=2, bg='lightgreen')
    setParameters_button.pack(pady=10)
    ToolTip(setParameters_button, "Run the GAN to generate synthetic samples based on the selected data file and parameters")

    findParameters_button = tk.Button(gui, text="Find Parameters", 
                                    command=lambda: findParameters(gui), 
                                    font=("Arial", 16), width=20, height=2, bg='lightgreen')
    findParameters_button.pack(pady=10)
    ToolTip(findParameters_button, "Do the grid or random search for GAN parameters to optimize the model performance based on the lowest " \
                                    "discriminator or generator loss saved in the results directory")
    
    terminate_button = tk.Button(gui, text="End Program", command=gui.destroy, font=("Arial", 16), width=20, height=2, bg='red')
    terminate_button.pack(pady=10)

    gui.mainloop()

if __name__ == "__main__":
    create_main_gui()