#non-linear functions can be represented with muli layering of perceptrons 
#the more layers/connection, the more fitted the data can become

import random, math, copy

class mlp:
    def __init__(self, ins = 2, h_layers = [3, 2, 3], outs = 4):
        #constants defining the layers of the network
        self.inputs = ins
        self.hidden_layers = h_layers
        self.outputs = outs
        
        #to be constructed during the forward pass
        self.activations_matrixes = []
        
        #to be constructed during the backpropogation, and initialised next++
        self.weight_derivatives = []
        
        #to be constructed next
        self.weight_matrix = []
        
        weight_layer_0 = []
        derivatives_0 = []
        for i in range(self.inputs):
            partition_0 = []
            d_partitions_0 = []
            for ii in range(self.hidden_layers[0]):
                #to be used after testing: random_weight = 2 * random.random() - 1
                partition_0.append(1)
                d_partitions_0.append(0)
            weight_layer_0.append(partition_0)
            derivatives_0.append(d_partitions_0)
        self.weight_matrix.append(weight_layer_0)
        self.weight_derivatives.append(derivatives_0)
        
        #initialising hidden layers
        if len(self.hidden_layers) > 1:
            for i in range(1, len(self.hidden_layers)):
                weight_layer_i_hidden = []
                derivatives_layer_i_hidden = []
                for ii in range(self.hidden_layers[i - 1]):
                    partition_i = []
                    d_partitions_i = []
                    for iii in range(self.hidden_layers[i]):
                        #to be used after testing: random_weight = 2 * random.random() - 1
                        partition_i.append(1)
                        d_partitions_i.append(0)
                    weight_layer_i_hidden.append(partition_i)
                    derivatives_layer_i_hidden.append(d_partitions_i)
                self.weight_matrix.append(weight_layer_i_hidden)
                self.weight_derivatives.append(derivatives_layer_i_hidden)
                
        #initialising output weights layer
        weight_layer_last = []
        derivatives_layer_last = []
        for i in range(self.hidden_layers[len(self.hidden_layers) - 1]):
            partition_last = []
            d_partitions_last = []
            for ii in range(self.outputs):
                #to be used after testing: random_weight = 2 * random.random() - 1
                partition_last.append(1)
                d_partitions_last.append(0)
            weight_layer_last.append(partition_last)
            derivatives_layer_last.append(d_partitions_last)
        self.weight_matrix.append(weight_layer_last)
        self.weight_derivatives.append(derivatives_layer_last)
        
        #here we initialise the inverse weight matrix in preparation for back-propogation 
        self.inverse_weight_matrix = copy.copy(self.weight_matrix)
        self.inverse_weight_matrix.reverse()
        
        inverse = []
        for i in range(len(self.inverse_weight_matrix)):
            cell_size_previous = len((self.inverse_weight_matrix[i]))
            cell_size = len(self.inverse_weight_matrix[i][0])
            new_cell = []
            for ii in range(cell_size):
                partition_0 = []
                for iii in range(cell_size_previous):
                    partition_0.append(self.inverse_weight_matrix[i][iii][ii])
                new_cell.append(partition_0)
            inverse.append(new_cell)
        self.inverse_weight_matrix = inverse
        
        return
    
    #defining the dot product on two vectors
    def dot(self, set_0, set_1):
        product = []
        for element in range(len(set_0)):
            product.append(set_0[element] * set_1[element])
        return product
    
    #method to add position-wise elements in a tensor
    def add(self, set_0):
        sums = []
        for i in range(len(set_0[0])):
            added = 0
            for ii in range(len(set_0)):
                added += set_0[ii][i]
            sums.append(added)
        return sums
    
    #neuron activation function
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    
    #method for passing new datum through the network, in the form [x,y,z ...]
    def forward_propogate_single(self, inputs):
        size = len(inputs)
        running_activations = [inputs]
        for i in range(0, len(self.weight_matrix)):
            weighted_layer = []
            for ii in range(len(self.weight_matrix[i])):
                weighted = copy.copy(self.weight_matrix[i][ii])
                for iii in range(len(weighted)):
                    weighted[iii] = weighted[iii] * running_activations[i][ii]
                weighted_layer.append(weighted)
            dot_prod = []
            for ii in range(len(weighted_layer)):
                dot_prod = self.add(weighted_layer)
            activations = dot_prod
            for ii in range(len(activations)):
                #activations[ii] = self.sigmoid(activations[ii])
                pass
            running_activations.append(activations)
        return running_activations
            
    #defining the derivative of the sigmoid        
    def ddx_sigmoid(self, x):
        return x * (1 - x)
    
    #method for feeding errors backward in network
    def back_propogate_single(self, activations, target):
        reverse_activations = copy.copy(activations)
        reverse_activations.reverse()
        print("reverese activations", reverse_activations)
        reversed_weight_matrix = copy.copy(self.inverse_weight_matrix)
        print("inverse weights", reversed_weight_matrix)
        current_errors = []
        for i in range(len(reverse_activations) - 1):
            derivatives = []
            for ii in range(len(reverse_activations[i])):
                derivatives.append(self.ddx_sigmoid(reverse_activations[i][ii]))
            print(derivatives)
            
        return 
