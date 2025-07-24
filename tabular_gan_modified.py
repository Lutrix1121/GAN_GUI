import pandas as pd
import numpy as np

# Tensorflow compatibility settings
np.object = object
np.bool = bool
np.int = int
np.float = float

from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from tensorflow.keras import layers, models, optimizers

class TabularGAN:
    def __init__(self, data_path, class_column, integer_columns = None, latent_dim=20, learning_rate=0.0001, beta1=0.5):
        self.data_path = data_path
        self.class_column = class_column
        self.latent_dim = latent_dim
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        
        # Integer columns can be specified or defaulted
        
        if integer_columns is not None:
            self.integer_columns = integer_columns
        else:
            # Default integer columns (fallback)
            self.integer_columns = [
                'age',
                'education_num',
                'capital_gain',
                'capital_loss',
                'hours_per_week'
        ]
        self._load_and_preprocess_data()
        self._build_gan()
        
    def _load_and_preprocess_data(self):
        #Load data
        data = pd.read_csv(self.data_path, sep=';')
        
        # Keep the original types of columns for later usage
        self.column_types = {}
        for col in data.columns:
            if col in self.integer_columns or col == self.class_column:
                try:
                    data[col] = data[col].astype(int)
                    self.column_types[col] = 'int'
                except:
                    self.column_types[col] = 'object'
        
        numeric_columns = data.columns.drop(self.class_column)
        data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        # Separate features and labels
        X = data.drop(self.class_column, axis=1)
        y = data[self.class_column].astype(str)

        # Delete rows with NaN values
        mask = X.isna().any(axis=1)
        X = X[~mask]
        y = y[~mask]
        
        # Keep the ranges of values of integer columns
        self.column_ranges = {}
        for col in self.integer_columns:
            if col in X.columns:
                self.column_ranges[col] = {
                    'min': int(X[col].min()),
                    'max': int(X[col].max())
                }
        
        # Numeric columns scaling
        self.numerical_columns = X.columns.tolist()
        X_scaled = self.scaler.fit_transform(X)
        
        # Class labels encoding
        y_2d = y.values.reshape(-1, 1)
        self.classes_ = y.unique()
        y_encoded = self.encoder.fit_transform(y_2d).astype(np.float32)
        
        # Connect the scaled features and encoded labels
        self.preprocessed_data = np.hstack((X_scaled, y_encoded)).astype(np.float32)
        self.num_numerical = X_scaled.shape[1]
        self.num_classes = y_encoded.shape[1]
        self.input_dim = self.preprocessed_data.shape[1]
        
    def _build_generator(self, hidden_layers=None):
        if hidden_layers is None:
            hidden_layers = [256, 512, 1024]
            
        inputs = layers.Input(shape=(self.latent_dim,))
        x = inputs
        
        for units in hidden_layers:
            x = layers.Dense(units)(x)
            x = layers.LeakyReLU(alpha=0.2)(x)
            x = layers.BatchNormalization()(x)
        
        numerical_output = layers.Dense(self.num_numerical, activation='tanh')(x)
        class_output = layers.Dense(self.num_classes, activation='softmax')(x)
        
        return models.Model(inputs, layers.concatenate([numerical_output, class_output]))
    
    def _build_discriminator(self, hidden_layers=None):
        if hidden_layers is None:
            hidden_layers = [768, 512, 256]
            
        inputs = layers.Input(shape=(self.input_dim,))
        x = inputs
        
        for units in hidden_layers:
            x = layers.Dense(units)(x)
            x = layers.LeakyReLU(alpha=0.2)(x)
            # Optional dropout layer for regularization
            # x = layers.Dropout(0.3)(x)
            
        outputs = layers.Dense(1, activation='sigmoid')(x)
        
        return models.Model(inputs, outputs)
    
    def _build_gan(self):
        # Building and compiling discriminator
        self.discriminator = self._build_discriminator()
        self.discriminator.compile(
            loss='binary_crossentropy',
            optimizer=optimizers.Adam(self.learning_rate, self.beta1),
            metrics=['accuracy']
        )
        
        # Building generator
        self.generator = self._build_generator()
        
        # Building and compiling GAN
        self.discriminator.trainable = False
        gan_input = layers.Input(shape=(self.latent_dim,))
        gan_output = self.discriminator(self.generator(gan_input))
        self.gan = models.Model(gan_input, gan_output)
        self.gan.compile(
            loss='binary_crossentropy',
            optimizer=optimizers.Adam(self.learning_rate, self.beta1)
        )
        
    def rebuild_with_params(self, gen_layers=None, disc_layers=None, learning_rate=None, beta1=None):
        """Rebuild the GAN with the specified parameters."""
        if learning_rate is not None:
            self.learning_rate = learning_rate
        if beta1 is not None:
            self.beta1 = beta1
            
        # Building and compiling discriminator
        self.discriminator = self._build_discriminator(hidden_layers=disc_layers)
        self.discriminator.compile(
            loss='binary_crossentropy',
            optimizer=optimizers.Adam(self.learning_rate, self.beta1),
            metrics=['accuracy']
        )
        
        # Generator building
        self.generator = self._build_generator(hidden_layers=gen_layers)
        
        # Building and compiling GAN
        self.discriminator.trainable = False
        gan_input = layers.Input(shape=(self.latent_dim,))
        gan_output = self.discriminator(self.generator(gan_input))
        self.gan = models.Model(gan_input, gan_output)
        self.gan.compile(
            loss='binary_crossentropy',
            optimizer=optimizers.Adam(self.learning_rate, self.beta1)
        )
        
    def train(self, epochs, batch_size, patience=5, verbose=1, callbacks=None):
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
            # Discriminator training
            idx = np.random.randint(0, self.preprocessed_data.shape[0], batch_size)
            real_data = self.preprocessed_data[idx]
        
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            fake_data = self.generator.predict(noise, verbose=0)
        
            d_loss_real = self.discriminator.train_on_batch(real_data, valid)
            d_loss_fake = self.discriminator.train_on_batch(fake_data, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
            # Generator training
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            g_loss = self.gan.train_on_batch(noise, valid)
            
            # History update
            history['d_loss'].append(float(d_loss[0]))
            history['d_accuracy'].append(float(d_loss[1]))
            history['g_loss'].append(float(g_loss))
        
            if verbose and (epoch + 1) % 100 == 0:
                print(f"Epoch {epoch+1} [D loss: {d_loss[0]:.4f} | D accuracy: {100*d_loss[1]:.2f}%] [G loss: {g_loss:.4f}]")
        
            # Callbacks execution
            if callbacks:
                for callback in callbacks:
                    callback(epoch, history)
        
            if g_loss > best_loss:
                patience_counter += 1
            else:
                best_loss = g_loss
                patience_counter = 0
            
            if patience_counter >= patience:
                if verbose:
                    print(f"Early stopping at epoch {epoch+1}")
                break
                
        return history

    def generate_samples(self, num_samples, target_class=None):
        generated_samples = pd.DataFrame()
        
        while len(generated_samples) < num_samples:
            batch_size = num_samples * 2
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            generated_data = self.generator.predict(noise)
            
            # Split the generated data into numerical and categorical parts
            generated_numerical = generated_data[:, :self.num_numerical]
            generated_class = generated_data[:, self.num_numerical:]
            
            # Reversing the scaling of numerical features
            generated_numerical = self.scaler.inverse_transform(generated_numerical)
            
            # Class labels transformation
            class_labels = self.encoder.inverse_transform(generated_class)
            
            # Creating dataframe with generated samples
            samples_df = pd.DataFrame(generated_numerical, columns=self.numerical_columns)
            samples_df[self.class_column] = class_labels.ravel()

            if target_class is not None:
                samples_df = samples_df[samples_df[self.class_column].astype(str) == str(target_class)]
            
            
            # Conversion of integer columns to integers
            for col in self.integer_columns:
                if col in samples_df.columns:
                    col_min = self.column_ranges.get(col, {}).get('min', 0)
                    col_max = self.column_ranges.get(col, {}).get('max', 1)
                    samples_df[col] = np.round(samples_df[col]).clip(col_min, col_max).astype(int)
            
            # Adding generated samples to the final dataframe
            generated_samples = pd.concat([generated_samples, samples_df])
            
            # Limit the number of generated samples to the required amount
            generated_samples = generated_samples.head(num_samples)

            if target_class and len(generated_samples) == 0:
                raise ValueError(f"Unable to generate samples for target class {target_class}")

        # Conversion of integer columns to integers
        if self.class_column in self.integer_columns:
            try:
                generated_samples[self.class_column] = generated_samples[self.class_column].astype(int)
            except:
                pass
                
        return generated_samples
    
'''
if __name__ == "__main__":
    # GAN initialization
    gan = TabularGAN('balanced_Dataset_cleaned.csv', class_column="DRK_YN")
    
    # GAN training
    history = gan.train(epochs=1000, batch_size=96)
    
    # New samples generation
    new_samples = gan.generate_samples(1339)
    print("\nGenerated Samples:")
    print(new_samples)
    new_samples.to_csv("Generated_Samples.csv", sep=';', index=False)
'''