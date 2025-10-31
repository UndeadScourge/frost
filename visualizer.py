import numpy as np
import matplotlib.pyplot as plt

class NetworkVisualizer:
    def __init__(self, neural_network):
        self.nn = neural_network
    
    def visualize_weights(self):
        """Visualize weight matrices"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Input to hidden layer weights
        im1 = ax1.imshow(self.nn.weights_input_hidden, cmap='coolwarm', aspect='auto')
        ax1.set_title('Input to Hidden Layer Weights')
        ax1.set_xlabel('Input Nodes')
        ax1.set_ylabel('Hidden Nodes')
        plt.colorbar(im1, ax=ax1)
        
        # Hidden to output layer weights
        im2 = ax2.imshow(self.nn.weights_hidden_output, cmap='coolwarm', aspect='auto')
        ax2.set_title('Hidden to Output Layer Weights')
        ax2.set_xlabel('Hidden Nodes')
        ax2.set_ylabel('Output Nodes')
        plt.colorbar(im2, ax=ax2)
        
        plt.tight_layout()
        plt.show()
    
    def visualize_sample(self, sample_data, predicted=None):
        """Visualize sample and prediction"""
        digit = int(sample_data[0])
        image_data = sample_data[1:]
        
        # Reshape to 28x28 image
        image = image_data.reshape(28, 28)
        
        plt.figure(figsize=(6, 6))
        plt.imshow(image, cmap='Greys', interpolation='None')
        
        if predicted is not None:
            title = f"True digit: {digit}, Predicted: {predicted}"
        else:
            title = f"Digit: {digit}"
        
        plt.title(title)
        plt.axis('off')
        plt.show()

# Usage example
if __name__ == "__main__":
    # Add test code here
    pass
