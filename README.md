# GAN_GUI - GUI for GAN Synthetic Data Generator
A comprehensive GUI application for generating synthetic tabular data using Generative Adversarial Networks (GANs). This tool provides an intuitive interface for training GANs on CSV datasets and generating high-quality synthetic samples with automated parameter optimization capabilities.

## Architecture:  
- Generator: [256, 512, 1024] hidden layers with LeakyReLU and BatchNorm,  
- Discriminator: [768, 512, 256] hidden layers with LeakyReLU,  
- Activation: Tanh for numerical, Softmax for categorical outputs.  

## 🚀 Features:
- User-Friendly GUI: Intuitive Tkinter-based interface for easy interaction,  
- Flexible Data Input: Support for CSV files with customizable column types,  
- Intelligent Preprocessing: Automatic handling of numerical and categorical data,  
- Parameter Optimization: Grid search and random search for hyperparameter tuning,  
- Synthetic Data Generation: Generate any number of synthetic samples,  
- Integer Column Support: Proper handling and preservation of integer data types,  
- Early Stopping: Prevents overfitting with configurable patience,  
- Comprehensive Results: Detailed training history and parameter analysis.

## 🛠️ Built With:  
- Python 3.x,  
- TensorFlow/Keras - Deep learning framework for GAN implementation,  
- Tkinter - GUI framework,  
- Pandas - Data manipulation and analysis,  
- NumPy - Numerical computing,  
- Scikit-learn - Data preprocessing (MinMaxScaler, OneHotEncoder).
 
## 📋 Requirements:  
- tensorflow>=2.0.0,  
- pandas>=1.0.0,  
- numpy>=1.18.0,  
- scikit-learn>=0.22.0,  
- tkinter (usually comes with Python).

 ## 🚀 Installation:  
 
1. Clone the repository:
```
git clone https://github.com/Lutrix1121/GAN_GUI.git
```
2. Install the dependencies:  
```
cd GAN_GUI  
pip install -r requirements.txt
```
3. Run the application:  
```
python gui.py
```
## 📖 Usage  

1. Setup Paths:   
 
- Click "Setup Paths" to configure your data file and save location,   
- Select your CSV file (semicolon-separated),   
- Specify integer columns (optional) - columns that should be treated as integers,  
- Choose where to save generated results.  
	
2. Generate Samples:  

- Click "Generate Samples" to create synthetic data,  
- Enter the class column name (target variable),  
- Specify number of samples to generate,  
- Configure optional parameters:  
	- Epochs: Training iterations (default: 1000),  
	- Batch Size: Training batch size (default: 96),  
	- Size of noise vector (default: 20),  
	- Learning Rate: Optimizer learning rate (default: 0.0001),
 	- Beta1: Adam optimizer parameter (default: 0.5).  
 
3. Find Optimal Parameters:  

- Click "Find Parameters" for automated hyperparameter optimization,  
- Choose between Grid Search (exhaustive) or Random Search (efficient),  
- Define parameter ranges for optimization:  
	- Latent dimensions,  
	- Batch sizes,  
	- Learning rates,  
	- Beta1 values,  
- Results are saved with detailed analysis and best parameters  
 
## 🏗️ Architecture  

Core Components:  
1. TabularGAN Class (tabular_gan_modified.py):  
- Data Preprocessing: Handles mixed data types, scaling, and encoding,  
- Generator Network: Creates synthetic samples from random noise,  
- Discriminator Network: Distinguishes real from synthetic data,  
- Training Loop: Adversarial training with early stopping,  
- Sample Generation: Produces realistic synthetic data.  

2. GANTuner Class (gan_parameter_tuning.py):  
- Grid Search: Exhaustive parameter space exploration,  
- Random Search: Efficient random sampling of parameters,  
- Results Management: Comprehensive logging and analysis,  
- Performance Metrics: Tracks discriminator/generator losses,  

3. GUI Interface:  
- Setup Wizard: File selection and configuration,  
- Parameter Input: User-friendly forms with tooltips,  
- Progress Tracking: Real-time training updates,  
- Results Display: Success notifications and error handling,  

## Data Flow: 

1. Input: CSV file with mixed data types,  
2. Preprocessing:  
	- Numerical scaling (MinMax to [-1, 1]),  
	- Categorical encoding (One-hot),  
	- Integer type preservation.    
3. Training: Adversarial training loop,  
4. Generation: Synthetic sample creation,  
5. Post-processing: Type restoration and range clipping,  

## 📊 Output Files  

- Generated_Samples_[N].csv - Synthetic dataset with N samples,  
- all_results.csv - Complete parameter search results,  
- best_params.json - Optimal hyperparameters,  
- summary.txt - Human-readable summary,  
- trial_[N]/ - Individual trial results with:  
	- params.json - Trial parameters,  
	- history.csv - Training metrics,  
	- samples.csv - Generated samples.  

## To do List:  

- Bug fixing,  
- ~~Dark mode,~~  
- ~~Progress bar for the process of finding parameters,~~  
- ~~Allowing user to choose the class for which samples should be generated,~~  
- ~~Splitting the gui file into smaller functions for easier editing,~~  
- ~~Providing the option in GUI to change generator and discriminator layers,~~  
- ~~Visualization of training results viewable from GUI~~ (Partially done, program informs where are the visualizations stored),  
- In further future: GUI for transformer synthetic data generator (I have the transformer, just need to implement GUI into it).  
