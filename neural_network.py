import numpy as np
import random
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set network architecture
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.learning_rate = learning_rate
        
        # Initialize weight matrices (using normal distribution)
        self.weights_input_hidden = np.random.normal(0.0, pow(self.hidden_nodes, -0.5), 
                                                    (self.hidden_nodes, self.input_nodes))
        self.weights_hidden_output = np.random.normal(0.0, pow(self.output_nodes, -0.5), 
                                                     (self.output_nodes, self.hidden_nodes))
        
        # Activation function (sigmoid)
        self.activation_function = lambda x: 1 / (1 + np.exp(-x))
        
        # Record training progress
        self.epoch_list = []
        self.loss_list = []
        self.accuracy_list = []
    
    def train(self, inputs_list, targets_list):
        """Train the network with one sample"""
        # Convert to 2D arrays
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T
        
        # Forward propagation - hidden layer
        hidden_inputs = np.dot(self.weights_input_hidden, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # Forward propagation - output layer
        final_inputs = np.dot(self.weights_hidden_output, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        # Calculate output layer errors
        output_errors = targets - final_outputs
        
        # Calculate hidden layer errors
        hidden_errors = np.dot(self.weights_hidden_output.T, output_errors)
        
        # Update hidden to output weights
        self.weights_hidden_output += self.learning_rate * np.dot(
            (output_errors * final_outputs * (1.0 - final_outputs)), 
            hidden_outputs.T
        )
        
        # Update input to hidden weights
        self.weights_input_hidden += self.learning_rate * np.dot(
            (hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), 
            inputs.T
        )
    
    def query(self, inputs_list):
        """Query the network for predictions"""
        inputs = np.array(inputs_list, ndmin=2).T
        
        # Calculate hidden layer outputs
        hidden_inputs = np.dot(self.weights_input_hidden, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # Calculate output layer outputs
        final_inputs = np.dot(self.weights_hidden_output, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs
    
    def calculate_loss(self, outputs, targets):
        """Calculate loss function (Mean Squared Error)"""
        return np.mean((targets - outputs) ** 2)
    
    def calculate_accuracy(self, test_data):
        """Calculate accuracy on test data"""
        correct = 0
        total = len(test_data)
        
        for record in test_data:
            inputs = record[1:]
            targets = int(record[0])
            
            outputs = self.query(inputs)
            predicted = np.argmax(outputs)
            
            if predicted == targets:
                correct += 1
        
        return correct / total
    
    def plot_training_progress(self):
        """Plot training progress (loss and accuracy)"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot loss curve
        ax1.plot(self.epoch_list, self.loss_list)
        ax1.set_title('Training Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.grid(True)
        
        # Plot accuracy curve
        ax2.plot(self.epoch_list, self.accuracy_list)
        ax2.set_title('Training Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()
