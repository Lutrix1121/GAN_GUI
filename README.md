# GAN_GUI - GAN Synthetic Data Generator
A comprehensive GUI application for generating synthetic tabular data using Generative Adversarial Networks (GANs). This tool provides an intuitive interface for training GANs on CSV datasets and generating high-quality synthetic samples with automated parameter optimization capabilities.

Architecture:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Generator: [256, 512, 1024] hidden layers with LeakyReLU and BatchNorm,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Discriminator: [768, 512, 256] hidden layers with LeakyReLU,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Activation: Tanh for numerical, Softmax for categorical outputs.  

🚀 Features:  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• User-Friendly GUI: Intuitive Tkinter-based interface for easy interaction,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Flexible Data Input: Support for CSV files with customizable column types,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Intelligent Preprocessing: Automatic handling of numerical and categorical data,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Parameter Optimization: Grid search and random search for hyperparameter tuning,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Synthetic Data Generation: Generate any number of synthetic samples,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Integer Column Support: Proper handling and preservation of integer data types,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Early Stopping: Prevents overfitting with configurable patience,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Comprehensive Results: Detailed training history and parameter analysis.

🛠️ Built With:  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Python 3.x,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• TensorFlow/Keras - Deep learning framework for GAN implementation,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Tkinter - GUI framework,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Pandas - Data manipulation and analysis,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• NumPy - Numerical computing,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Scikit-learn - Data preprocessing (MinMaxScaler, OneHotEncoder).
 
📋 Requirements:  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• tensorflow>=2.0.0,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• pandas>=1.0.0,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• numpy>=1.18.0,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• scikit-learn>=0.22.0,  
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• tkinter (usually comes with Python).

 🚀 Installation:  
 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Clone the repository:  
  
	git clone https://github.com/Lutrix1121/GAN_GUI.git

   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Install the dependencies:  

	cd GAN_GUI  
	pip install -r requirements.txt

   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Run the application:  

	python gui.py

📖 Usage  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Setup Paths:   
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Click "Setup Paths" to configure your data file and save location,   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Select your CSV file (semicolon-separated),   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Specify integer columns (optional) - columns that should be treated as integers,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Choose where to save generated results.  
	
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Generate Samples:  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Click "Generate Samples" to create synthetic data,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Enter the class column name (target variable),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Specify number of samples to generate,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Configure optional parameters:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Epochs: Training iterations (default: 1000),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Batch Size: Training batch size (default: 96),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Latent Dimension: Size of noise vector (default: 20),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Learning Rate: Optimizer learning rate (default: 0.0001),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Beta1: Adam optimizer parameter (default: 0.5).  
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Find Optimal Parameters:  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Click "Find Parameters" for automated hyperparameter optimization,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Choose between Grid Search (exhaustive) or Random Search (efficient),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Define parameter ranges for optimization:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Latent dimensions,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Batch sizes,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Learning rates,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Beta1 values,  
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Results saved with detailed analysis and best parameters  
 
🏗️ Architecture  

Core Components:  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. TabularGAN Class (tabular_gan_modified.py):  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Data Preprocessing: Handles mixed data types, scaling, and encoding,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Generator Network: Creates synthetic samples from random noise,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Discriminator Network: Distinguishes real from synthetic data,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Training Loop: Adversarial training with early stopping,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Sample Generation: Produces realistic synthetic data.  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. GANTuner Class (gan_parameter_tuning.py):  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Grid Search: Exhaustive parameter space exploration,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Random Search: Efficient random sampling of parameters,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Results Management: Comprehensive logging and analysis,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Performance Metrics: Tracks discriminator/generator losses,  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. GUI Interface:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Setup Wizard: File selection and configuration,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Parameter Input: User-friendly forms with tooltips,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Progress Tracking: Real-time training updates,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Results Display: Success notifications and error handling,  

Data Flow: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Input: CSV file with mixed data types,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Preprocessing:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Numerical scaling (MinMax to [-1, 1]),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Categorical encoding (One-hot),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Integer type preservation.    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Training: Adversarial training loop,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. Generation: Synthetic sample creation,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. Post-processing: Type restoration and range clipping,  

📊 Output Files  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Generated_Samples_[N].csv - Synthetic dataset with N samples,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• all_results.csv - Complete parameter search results,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• best_params.json - Optimal hyperparameters,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• summary.txt - Human-readable summary,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• trial_[N]/ - Individual trial results with:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• params.json - Trial parameters,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• history.csv - Training metrics,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• samples.csv - Generated samples.  

To do List:  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Bug fixing, 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Progress bar for the process of finding parameters, 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Allowing user to choose the class for which samples should be generated, 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Making an executable file for easier launching,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Splitting the gui file into smaller functions for easier editing,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Providing the option in GUI to change generator and discriminator layers and activation functions,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Visualization of training results viewable from GUI,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• In further future: GUI for transformer synthetic data generator (I have the transformer, just need to implement GUI into it).  
