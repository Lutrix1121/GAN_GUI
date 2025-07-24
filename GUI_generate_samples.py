import tkinter as tk
import os
import GUI_globals as globals
from GUI_tooltip import ToolTip

def generateSamples(gui):
    new_window = tk.Toplevel(gui)
    new_window.title("Generate Samples")
    new_window.geometry("500x700")
    new_window.resizable(width=False, height=False)
    
    def startGeneration():
        try:
            if not globals.FILENAME:
                tk.messagebox.showerror("Error", "Please select a data file first!")
                return
            if not globals.SAVEPATH:
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
                
            targetClass = int(target_class_entry.get()) if target_class_entry.get() else None
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
            gan = TabularGAN(globals.FILENAME, class_column=classLabel, integer_columns=globals.INTEGER_COLUMNS, latent_dim=latentDim, 
                           learning_rate=learningRate, beta1=beta1)
            
            # Train the GAN
            history = gan.train(epochs=epochs, batch_size=batchSize, verbose=1)
            
            # Generate samples
            generated_samples = gan.generate_samples(sampleSize, target_class=targetClass)
            
            # Save generated samples
            output_filename = f"Generated_Samples_{sampleSize}.csv"
            output_path = os.path.join(globals.SAVEPATH, output_filename)
            os.makedirs(globals.SAVEPATH, exist_ok=True)
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

    # Target class input
    target_class_label = tk.Label(new_window, text="Target class (optional)", font=("Arial", 10))
    target_class_label.pack(pady=5)
    target_class_entry = tk.Entry(new_window, font=("Arial", 10), width=30)
    target_class_entry.pack(pady=5)
    ToolTip(target_class_entry, "Specific class to generate. Leave empty to generate mixed classes.")

    # Sample size input
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