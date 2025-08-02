import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid
import json
import os
from datetime import datetime
from tabular_gan_modified import TabularGAN
from matplotlib import pyplot as plt

def convert_numpy_types(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

class GANTuner:
    def __init__(self, data_path, class_column, integer_columns = None, results_dir="tuning_results"):
        self.data_path = data_path
        self.class_column = class_column
        self.integer_columns = integer_columns
        self.results_dir = results_dir
        
        # Create results directory if it doesn't exist
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            
        # For storing results
        self.results = []
        
    def run_grid_search(self, param_grid, n_samples=500, epochs=1000, early_stop_patience=10, progress_callback=None):
        """
        Run grid search over parameter combinations
        
        Args:
            param_grid: Dictionary with parameter names as keys and lists of parameter values to try
            n_samples: Number of samples to generate for evaluation
            epochs: Maximum number of epochs for each trial
            early_stop_patience: Patience for early stopping
        """
        # Create parameter combinations
        param_combinations = list(ParameterGrid(param_grid))
        total_trials = len(param_combinations)
        print(f"Running grid search with {len(param_combinations)} parameter combinations")
        
        for i, params in enumerate(param_combinations):
            print(f"\nTrial {i+1}/{total_trials}")
            print(f"Parameters: {params}")
            
            if progress_callback:
                progress_callback(i, total_trials)
        

            params = convert_numpy_types(params)
            # Create and train GAN with current parameters
            gan = TabularGAN(
                self.data_path, 
                self.class_column,
                integer_columns=self.integer_columns,
                latent_dim=params.get('latent_dim', 100),
                learning_rate=params.get('learning_rate', 0.0001),
                beta1=params.get('beta1', 0.5)
            )
            
            # Modify GAN architecture if needed
            self._modify_gan_architecture(gan, params)
            
            # Train GAN and collect metrics
            history = self._train_with_history(
                gan, 
                epochs=epochs, 
                batch_size=params.get('batch_size', 32),
                patience=early_stop_patience
            )
            
            history = convert_numpy_types(history)
            # Save results
            result = {
                'params': params,
                'history': history,
                'final_d_loss': history['d_loss'][-1],
                'final_d_accuracy': history['d_accuracy'][-1],
                'final_g_loss': history['g_loss'][-1],
                'n_epochs': len(history['d_loss']),
            }
            self.results.append(result)
            
            # Generate samples for this model
            samples = gan.generate_samples(n_samples)
            
            # Save this trial
            self._save_trial_results(i, params, history, samples)
        
        # Save overall results
        self._save_overall_results()
        
        return self.results
    
    def run_random_search(self, param_distributions, n_iter=10, n_samples=5, epochs=1000, early_stop_patience=10, progress_callback=None):
        """
        Run random search over parameter space
        
        Args:
            param_distributions: Dictionary with parameter names as keys and lists/distributions of values
            n_iter: Number of random combinations to try
            n_samples: Number of samples to generate for evaluation
            epochs: Maximum number of epochs for each trial
            early_stop_patience: Patience for early stopping
        """
        # Sample random parameter combinations
        param_combinations = []
        for _ in range(n_iter):
            params = {}
            for param, values in param_distributions.items():
                params[param] = np.random.choice(values)
            params = convert_numpy_types(params)
            param_combinations.append(params)
        
        print(f"Running random search with {n_iter} parameter combinations")
        
        for i, params in enumerate(param_combinations):
            print(f"\nTrial {i+1}/{n_iter}")
            print(f"Parameters: {params}")
            
            if progress_callback:
                progress_callback(i, n_iter)

            # Create and train GAN with current parameters
            gan = TabularGAN(
                self.data_path, 
                self.class_column,
                integer_columns=self.integer_columns,
                latent_dim=params.get('latent_dim', 100),
                learning_rate=params.get('learning_rate', 0.0001),
                beta1=params.get('beta1', 0.5)
            )
            
            # Modify GAN architecture if needed
            self._modify_gan_architecture(gan, params)
            
            # Train GAN and collect metrics
            history = self._train_with_history(
                gan, 
                epochs=epochs, 
                batch_size=params.get('batch_size', 32),
                patience=early_stop_patience
            )
            
            history = convert_numpy_types(history)
            # Save results
            result = {
                'params': params,
                'history': history,
                'final_d_loss': history['d_loss'][-1],
                'final_d_accuracy': history['d_accuracy'][-1],
                'final_g_loss': history['g_loss'][-1],
                'n_epochs': len(history['d_loss']),
            }
            self.results.append(result)
            
            # Generate samples for this model
            samples = gan.generate_samples(n_samples)
            
            # Save this trial
            self._save_trial_results(i, params, history, samples)
        
        # Save overall results
        self._save_overall_results()
        
        return self.results
            
    def _train_with_history(self, gan, epochs, batch_size, patience=5):
        """Modified train method to collect training history"""
        history = {
            'd_loss': [],
            'd_accuracy': [],
            'g_loss': []
        }
        
        best_loss = float('inf')
        patience_counter = 0
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
    
        for epoch in range(epochs):
            # Train discriminator
            idx = np.random.randint(0, gan.preprocessed_data.shape[0], batch_size)
            real_data = gan.preprocessed_data[idx]
        
            noise = np.random.normal(0, 1, (batch_size, gan.latent_dim))
            fake_data = gan.generator.predict(noise, verbose=0)
        
            d_loss_real = gan.discriminator.train_on_batch(real_data, valid)
            d_loss_fake = gan.discriminator.train_on_batch(fake_data, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
            # Train generator
            noise = np.random.normal(0, 1, (batch_size, gan.latent_dim))
            g_loss = gan.gan.train_on_batch(noise, valid)
            
            # Record history
            history['d_loss'].append(float(d_loss[0]))
            history['d_accuracy'].append(float(d_loss[1]))
            history['g_loss'].append(float(g_loss))
        
            if (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch+1} [D loss: {d_loss[0]:.4f} | D accuracy: {100*d_loss[1]:.2f}%] [G loss: {g_loss:.4f}]")
        
            if g_loss > best_loss:
                patience_counter += 1
            else:
                best_loss = g_loss
                patience_counter = 0
            
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch+1}")
                break
                
        return history
    
    def _modify_gan_architecture(self, gan, params):
        """Modify GAN architecture based on parameters"""
        gen_layers = params.get('gen_layers')
        disc_layers = params.get('disc_layers')
        learning_rate = params.get('learning_rate')
        beta1 = params.get('beta1')
        
        # Rebuild the GAN with new architecture if layer configurations are provided
        gan.rebuild_with_params(
            gen_layers=gen_layers,
            disc_layers=disc_layers,
            learning_rate=learning_rate,
            beta1=beta1
    )
    
    def _save_trial_results(self, trial_num, params, history, samples):
        """Save results from a single trial"""
        trial_dir = os.path.join(self.results_dir, f"trial_{trial_num}")
        if not os.path.exists(trial_dir):
            os.makedirs(trial_dir)

        params_to_save = convert_numpy_types(params)    
        # Save parameters
        with open(os.path.join(trial_dir, "params.json"), "w") as f:
            json.dump(params, f, indent=4)
            
        # Save history
        history_df = pd.DataFrame({
            'epoch': range(1, len(history['d_loss']) + 1),
            'd_loss': history['d_loss'],
            'd_accuracy': history['d_accuracy'],
            'g_loss': history['g_loss']
        })
        history_df.to_csv(os.path.join(trial_dir, "history.csv"), index=False)
        
        # Save generated samples
        samples.to_csv(os.path.join(trial_dir, "samples.csv"), sep=";", index=False)

        # Generate and save plots
        self._create_learning_curves(history, os.path.join(trial_dir, "learning_curves.png"))
    
    def _save_overall_results(self):
        """Save overall results from all trials"""
        # Convert results to DataFrame for easier analysis
        results_df = pd.DataFrame([
            {
                **{f"param_{k}": v for k, v in r['params'].items()},
                'final_d_loss': r['final_d_loss'],
                'final_d_accuracy': r['final_d_accuracy'],
                'final_g_loss': r['final_g_loss'],
                'n_epochs': r['n_epochs']
            }
            for r in self.results
        ])
        
        # Save to CSV
        results_df.to_csv(os.path.join(self.results_dir, "all_results.csv"), index=False)
        
        # Find best parameters
        best_idx = results_df['final_g_loss'].idxmin()
        best_params = self.results[best_idx]['params']
        best_params = convert_numpy_types(best_params)
        # Save best parameters
        with open(os.path.join(self.results_dir, "best_params.json"), "w") as f:
            json.dump(best_params, f, indent=4)
            
        # Save summary report
        with open(os.path.join(self.results_dir, "summary.txt"), "w") as f:
            f.write("TabularGAN Parameter Tuning Summary\n")
            f.write(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total trials: {len(self.results)}\n\n")
            f.write("Best parameters:\n")
            for param, value in best_params.items():
                f.write(f"  {param}: {value}\n")
            f.write("\nBest performance metrics:\n")
            f.write(f"  Generator loss: {self.results[best_idx]['final_g_loss']:.4f}\n")
            f.write(f"  Discriminator loss: {self.results[best_idx]['final_d_loss']:.4f}\n")
            f.write(f"  Discriminator accuracy: {self.results[best_idx]['final_d_accuracy']:.4f}\n")
            f.write(f"  Training epochs: {self.results[best_idx]['n_epochs']}\n")
    
    def _create_learning_curves(self, history, save_path):
        """Create and save learning curves"""
        epochs = range(1, len(history['d_loss']) + 1)
        
        plt.figure(figsize=(15, 10))
        
        # Plot discriminator loss
        plt.subplot(3, 1, 1)
        plt.plot(epochs, history['d_loss'])
        plt.title('Discriminator Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.grid(True)
        
        # Plot discriminator accuracy
        plt.subplot(3, 1, 2)
        plt.plot(epochs, history['d_accuracy'])
        plt.title('Discriminator Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.grid(True)
        
        # Plot generator loss
        plt.subplot(3, 1, 3)
        plt.plot(epochs, history['g_loss'])
        plt.title('Generator Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
    
    def visualize_results(self):
        """Visualize results from the tuning process"""
        try:
            results_df = pd.read_csv(os.path.join(self.results_dir, "all_results.csv"))
        
        # Create output directory for visualizations
            viz_dir = os.path.join(self.results_dir, "visualizations")
            if not os.path.exists(viz_dir):
                os.makedirs(viz_dir)
            
            # Visualize impact of different parameters on generator loss
            param_cols = [col for col in results_df.columns if col.startswith('param_')]
            
            for param in param_cols:
                param_name = param[6:]  # Remove 'param_' prefix
                
                plt.figure(figsize=(10, 6))
                plt.scatter(results_df[param], results_df['final_g_loss'])
                plt.title(f'Impact of {param_name} on Generator Loss')
                plt.xlabel(param_name)
                plt.ylabel('Final Generator Loss')
                plt.grid(True)
                plt.savefig(os.path.join(viz_dir, f"{param_name}_vs_g_loss.png"))
                plt.close()
                
                plt.figure(figsize=(10, 6))
                plt.scatter(results_df[param], results_df['final_d_accuracy'])
                plt.title(f'Impact of {param_name} on Discriminator Accuracy')
                plt.xlabel(param_name)
                plt.ylabel('Final Discriminator Accuracy')
                plt.grid(True)
                plt.savefig(os.path.join(viz_dir, f"{param_name}_vs_d_accuracy.png"))
                plt.close()

                plt.figure(figsize=(10, 6))
                plt.scatter(results_df[param], results_df['final_d_loss'])
                plt.title(f'Impact of {param_name} on Discriminator Loss')
                plt.xlabel(param_name)
                plt.ylabel('Final Discriminator Loss')
                plt.grid(True)
                plt.savefig(os.path.join(viz_dir, f"{param_name}_vs_d_loss.png"))
                plt.close()
            
            print(f"Visualizations saved to {viz_dir}/")
        except Exception as e:
            print(f"Error creating visualizations: {str(e)}")

def search(classLabel, epoch, numIterations, latentDim, batchSize, learningRate, beta1, data_path=None, 
           gen_layers=None, disc_layers=None, results_dir=None, search_type='grid', integer_columns=None,
            progress_callback=None):
    '''
    parser = argparse.ArgumentParser(description='TabularGAN Parameter Tuning')
    parser.add_argument('--data', type=str, default=gui.pickingTheFile, help='Path to data CSV file')
    parser.add_argument('--class_column', type=str, default=classLabel, help='Name of class column')
    parser.add_argument('--search_type', type=str, default='grid', choices=['grid', 'random'], help='Search method')
    parser.add_argument('--n_iter', type=int, default=numIterations, help='Number of iterations for random search')
    parser.add_argument('--max_epochs', type=int, default=epoch, help='Maximum epochs per trial')
    parser.add_argument('--results_dir', type=str, default=gui.savingPath, help='Directory to save results')
    
    args = parser.parse_args()
    '''
    if data_path is None:
        raise ValueError("Data path must be provided")
    if results_dir is None:
        results_dir = "tuning_results"

    # Create tuner
    tuner = GANTuner(data_path, classLabel, integer_columns=integer_columns, results_dir = results_dir)
    
    # Define parameter grid for search
    param_grid = {
        'latent_dim': [int(x) for x in latentDim],
        'batch_size': [int(x) for x in batchSize],
        'learning_rate': [float(x) for x in learningRate],
        'beta1': [float(x) for x in beta1]
    }

    if gen_layers:
        param_grid['gen_layers'] = gen_layers
    if disc_layers:
        param_grid['disc_layers'] = disc_layers
    
    # Run search
    if search_type == 'grid':
        results = tuner.run_grid_search(
            param_grid, 
            epochs=epoch,
            early_stop_patience=10,
            progress_callback=progress_callback
            )
    
    else:
        results = tuner.run_random_search(
            param_grid, 
            n_iter=numIterations, 
            epochs=epoch,
            early_stop_patience=10,
            progress_callback=progress_callback
        )
    
    # Visualize results
    tuner.visualize_results()
    
    print(f"\nParameter tuning complete! Results saved to {results_dir}/")
    print(f"Best parameters saved to {results_dir}/best_params.json")
