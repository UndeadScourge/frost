import numpy as np
import os
import random
import urllib.request
import gzip
import shutil
from neural_network import NeuralNetwork
from data_loader import MNISTDataLoader

def download_mnist_data():
    """Download MNIST dataset from alternative sources"""
    # 使用不同的镜像源
    mirrors = [
        "https://ossci-datasets.s3.amazonaws.com/mnist/",
        "https://storage.googleapis.com/cvdf-datasets/mnist/",
        "http://yann.lecun.com/exdb/mnist/"
    ]
    
    files = [
        "train-images-idx3-ubyte.gz",
        "train-labels-idx1-ubyte.gz", 
        "t10k-images-idx3-ubyte.gz",
        "t10k-labels-idx1-ubyte.gz"
    ]
    
    # Create data directory
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Try different mirrors
    for mirror in mirrors:
        print(f"Trying mirror: {mirror}")
        success_count = 0
        
        for file in files:
            output_path = f'data/{file.replace(".gz", "")}'
            if os.path.exists(output_path):
                success_count += 1
                continue
                
            try:
                url = mirror + file
                print(f"Downloading {file}...")
                urllib.request.urlretrieve(url, f'data/{file}')
                
                # Extract gzip file
                with gzip.open(f'data/{file}', 'rb') as f_in:
                    with open(output_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # Remove the gz file after extraction
                os.remove(f'data/{file}')
                success_count += 1
                print(f"Successfully downloaded and extracted: {file}")
                
            except Exception as e:
                print(f"Failed to download {file} from {mirror}: {e}")
                # Remove partial file if exists
                if os.path.exists(f'data/{file}'):
                    os.remove(f'data/{file}')
        
        if success_count == len(files):
            print("All files downloaded successfully!")
            return True
    
    print("All mirrors failed. Using synthetic data.")
    return False

def create_synthetic_data(num_samples=1000):
    """Create realistic synthetic handwritten digit data"""
    print("Creating realistic synthetic handwritten digit data...")
    
    training_data = []
    
    # Define patterns for each digit (simplified versions)
    digit_patterns = {
        0: lambda row, col: 100 if (8 <= row <= 20 and 8 <= col <= 20 and 
                                   (row-14)**2 + (col-14)**2 <= 36) else 0,
        1: lambda row, col: 200 if (10 <= col <= 12 and row >= 6) else 0,
        2: lambda row, col: 180 if ((8 <= row <= 10) or (18 <= row <= 20) or 
                                   (row + col >= 25 and row + col <= 35)) else 0,
        3: lambda row, col: 190 if ((8 <= row <= 10) or (14 <= row <= 16) or 
                                   (18 <= row <= 20) or (col >= 20)) else 0,
        4: lambda row, col: 170 if ((col >= 18) or (row <= 14 and col >= 10) or 
                                   (14 <= row <= 16)) else 0,
        5: lambda row, col: 160 if ((8 <= row <= 10) or (14 <= row <= 16) or 
                                   (18 <= row <= 20) or (row >= 14 and col <= 8)) else 0,
        6: lambda row, col: 150 if ((8 <= row <= 10) or (18 <= row <= 20) or 
                                   (col <= 8 and row >= 10) or (14 <= row <= 16)) else 0,
        7: lambda row, col: 140 if ((8 <= row <= 10) or (col >= 18 and row <= 18)) else 0,
        8: lambda row, col: 130 if ((8 <= row <= 10) or (14 <= row <= 16) or 
                                   (18 <= row <= 20) or (col <= 8) or (col >= 18)) else 0,
        9: lambda row, col: 120 if ((8 <= row <= 10) or (14 <= row <= 16) or 
                                   (col >= 18) or (row <= 14 and col <= 8)) else 0
    }
    
    for digit in range(10):
        samples_per_digit = num_samples // 10
        for sample_idx in range(samples_per_digit):
            # Create empty image
            image = np.zeros(784)
            
            # Get the pattern function for this digit
            pattern_func = digit_patterns[digit]
            
            # Apply the pattern
            for i in range(784):
                row, col = i // 28, i % 28
                base_value = pattern_func(row, col)
                if base_value > 0:
                    # Add some noise and variation
                    noise = np.random.normal(0, 20)
                    image[i] = max(10, min(255, base_value + noise))
                else:
                    # Background with some noise
                    image[i] = np.random.normal(10, 5)
            
            # Normalize to 0.01-0.99 range
            image = image / 255.0 * 0.98 + 0.01
            image = np.clip(image, 0.01, 0.99)
            
            training_data.append(np.concatenate(([digit], image)))
    
    print(f"Created {len(training_data)} synthetic samples")
    return training_data

def load_local_mnist_if_exists():
    """Check if MNIST files already exist locally"""
    files = [
        "train-images-idx3-ubyte",
        "train-labels-idx1-ubyte", 
        "t10k-images-idx3-ubyte",
        "t10k-labels-idx1-ubyte"
    ]
    
    all_exist = all(os.path.exists(f'data/{file}') for file in files)
    if all_exist:
        print("Found existing MNIST files locally")
        return True
    return False

def main():
    # Network parameters
    input_nodes = 784
    hidden_nodes = 100
    output_nodes = 10
    learning_rate = 0.3
    epochs = 5
    
    # Create neural network
    n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    
    # Try to load data
    training_data = []
    test_data = []
    
    try:
        # First check if files exist locally
        if load_local_mnist_if_exists():
            loader = MNISTDataLoader()
            
            # Load training data
            train_images, train_labels = loader.load_data(
                'data/train-images-idx3-ubyte', 
                'data/train-labels-idx1-ubyte',
                max_samples=1000
            )
            
            # Load test data
            test_images, test_labels = loader.load_data(
                'data/t10k-images-idx3-ubyte',
                'data/t10k-labels-idx1-ubyte', 
                max_samples=200
            )
            
            # Prepare data
            training_data = loader.prepare_training_data(train_images, train_labels)
            test_data = loader.prepare_training_data(test_images, test_labels)
            
            print("Successfully loaded MNIST dataset from local files")
            
        else:
            # Try to download
            print("No local MNIST files found. Attempting to download...")
            if download_mnist_data():
                # If download successful, load the data
                loader = MNISTDataLoader()
                
                train_images, train_labels = loader.load_data(
                    'data/train-images-idx3-ubyte', 
                    'data/train-labels-idx1-ubyte',
                    max_samples=1000
                )
                
                test_images, test_labels = loader.load_data(
                    'data/t10k-images-idx3-ubyte',
                    'data/t10k-labels-idx1-ubyte', 
                    max_samples=200
                )
                
                training_data = loader.prepare_training_data(train_images, train_labels)
                test_data = loader.prepare_training_data(test_images, test_labels)
                
                print("Successfully downloaded and loaded MNIST dataset")
            else:
                raise Exception("Download failed from all mirrors")
                
    except Exception as e:
        print(f"Error loading MNIST data: {e}")
        print("Using high-quality synthetic data instead...")
        # Create synthetic data
        synthetic_data = create_synthetic_data(1200)
        # Split into training and test
        split_idx = len(synthetic_data) * 4 // 5
        training_data = synthetic_data[:split_idx]
        test_data = synthetic_data[split_idx:]
    
    print(f"Training samples: {len(training_data)}")
    print(f"Test samples: {len(test_data)}")
    
    if len(training_data) == 0:
        print("Error: No training data available!")
        return
    
    # Train the network
    print("\nStarting neural network training...")
    print("Epoch Progress: Loss, Accuracy")
    print("-" * 50)
    
    for epoch in range(epochs):
        # Shuffle training data
        random.shuffle(training_data)
        
        # Train on each sample
        for i, record in enumerate(training_data):
            inputs = record[1:]
            targets = np.zeros(output_nodes) + 0.01
            targets[int(record[0])] = 0.99
            n.train(inputs, targets)
            
            # Show progress for large datasets
            if len(training_data) > 500 and i % 100 == 0:
                print(f"Epoch {epoch}: Processed {i}/{len(training_data)} samples")
        
        # Calculate accuracy and loss
        accuracy = n.calculate_accuracy(test_data)
        
        # Calculate average loss on test set
        total_loss = 0
        test_samples = min(20, len(test_data))
        for i in range(test_samples):
            record = test_data[i]
            inputs = record[1:]
            targets_array = np.zeros(output_nodes) + 0.01
            targets_array[int(record[0])] = 0.99
            outputs = n.query(inputs)
            loss = n.calculate_loss(outputs, targets_array)
            total_loss += loss
        
        avg_loss = total_loss / test_samples
        
        n.epoch_list.append(epoch)
        n.loss_list.append(avg_loss)
        n.accuracy_list.append(accuracy)
        
        print(f"Epoch {epoch}: Loss = {avg_loss:.4f}, Accuracy = {accuracy:.4f}")
    
    # Final testing
    final_accuracy = n.calculate_accuracy(test_data)
    print("-" * 50)
    print(f"Training completed!")
    print(f"Final test accuracy: {final_accuracy:.4f} ({final_accuracy*100:.2f}%)")
    
    # Show training progress
    try:
        n.plot_training_progress()
    except Exception as e:
        print(f"Could not display plot: {e}")
    
    # Test some samples
    print("\nSample Predictions:")
    print("-" * 40)
    test_samples = min(8, len(test_data))
    for i in range(test_samples):
        record = test_data[i]
        inputs = record[1:]
        target = int(record[0])
        outputs = n.query(inputs)
        predicted = np.argmax(outputs)
        confidence = outputs[predicted][0]
        
        status = "✓ CORRECT" if predicted == target else "✗ WRONG"
        print(f"Sample {i+1}: True={target}, Predicted={predicted} | {status} | Confidence={confidence:.4f}")

if __name__ == "__main__":
    main()
