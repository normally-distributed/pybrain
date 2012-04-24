import pybrain
from pybrain.structure.networks import RecurrentNetwork
from pybrain.structure.networks import FeedForwardNetwork
from pybrain.structure.modules import LinearLayer
from pybrain.structure.modules import LSTMLayer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.structure.modules import SigmoidLayer
import os
import sys
import pdb

def get_layer_types(options_dictionary):
    hidden_layer_type_string = options_dictionary['hidden_neuron_type']
    output_layer_type_string = options_dictionary['output_neuron_type']
    
    
    output_layer_type = get_layer_type(output_layer_type_string);
    hidden_layer_type = get_layer_type(hidden_layer_type_string);
    
    return (hidden_layer_type,output_layer_type)
    
    
def get_layer_type(layer_type_string):
   
    if layer_type_string == 'lstm\n':
        layer_type = LSTMLayer
    elif layer_type_string == 'linear\n':
        layer_type = LinearLayer
    elif layer_type_string == 'softmax\n':
        layer_type = SoftmaxLayer
    elif layer_type_string == 'sigmoid\n':
        layer_type = SigmoidLayer
 
    return layer_type