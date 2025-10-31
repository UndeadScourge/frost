import numpy as np
import struct

class MNISTDataLoader:
    def __init__(self):
        pass
    
    def load_data(self, images_path, labels_path, max_samples=None):
        """Load MNIST dataset from binary files"""
        # Load labels
        with open(labels_path, 'rb') as f:
            magic, num = struct.unpack(">II", f.read(8))
            labels = np.fromfile(f, dtype=np.uint8)
        
        # Load images
        with open(images_path, 'rb') as f:
            magic, num, rows, cols = struct.unpack(">IIII", f.read(16))
            images = np.fromfile(f, dtype=np.uint8).reshape(len(labels), rows * cols)
        
        # Limit number of samples for faster training
        if max_samples:
            labels = labels[:max_samples]
            images = images[:max_samples]
        
        return images, labels
    
    def normalize_data(self, data):
        """Normalize data to range 0.01-1.00"""
        return data / 255.0 * 0.99 + 0.01
    
    def create_targets(self, labels, num_classes=10):
        """Create target output matrix (one-hot encoding)"""
        targets = np.zeros((len(labels), num_classes)) + 0.01
        for i, label in enumerate(labels):
            targets[i, label] = 0.99
        return targets
    
    def prepare_training_data(self, images, labels):
        """Prepare training data in required format"""
        # Normalize image data
        normalized_images = self.normalize_data(images)
        
        # Create target outputs
        targets = self.create_targets(labels)
        
        # Combine data into training format
        training_data = []
        for i in range(len(labels)):
            training_data.append(np.concatenate(([labels[i]], normalized_images[i])))
        
        return training_data
