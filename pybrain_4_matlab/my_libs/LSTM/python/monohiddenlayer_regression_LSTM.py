import pybrain
import numpy as np
import csv
import evalRNN
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets import SequentialDataSet
from pybrain.datasets import SequenceClassificationDataSet
from pybrain.structure.networks import RecurrentNetwork
from pybrain.structure.networks import FeedForwardNetwork
from pybrain.structure.modules import LinearLayer
from pybrain.structure.modules import LSTMLayer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.structure.modules import SigmoidLayer
from pybrain.structure.connections import FullConnection
from pybrain.supervised.trainers import RPropMinusTrainer
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader
import pybrain.tools.shortcuts as shortcuts
import matplotlib
import matplotlib.pyplot as plt
import pickle
import datetime
import os
import sys
import math
import pdb
import time
import sys
import network_topologies as net_topol

def train_network(options_file_location,training_data_location,output_location):

    training_file_handle = open(training_data_location,"r")
    training_reader = csv.reader(training_file_handle)
    
    stdout_file = output_location+'training_console_output.txt'
    stderr_file = output_location+'training_console_errput.txt'
    
    sys.stdout = open(stdout_file,"w")
    sys.stderr = open(stderr_file,"w")
    
    options_file_handle = open(options_file_location,'r')
    options_dictionary = {}

    for option in options_file_handle.readlines():
        key,val = option.split('=')
        print key
        print val
        options_dictionary[key] = val;

    num_predictors = int(options_dictionary['num_predictors'])
    num_outputs = int(options_dictionary['num_outputs'])
    num_training_epochs = int(options_dictionary['num_training_epochs'])
    num_hidden_neurons = int(options_dictionary['num_hidden_neurons'])
    compound_prediction = int(options_dictionary['compound_prediction'])
    #teacher_forced_transient = int(options_dictionary['teacher_forced_transient'])
    teacher_forced_transient = 0
    hidden_neuron_type_str = options_dictionary['hidden_neuron_type']
    output_neuron_type_str = options_dictionary['output_neuron_type']
    
    hidden_layer_type,output_layer_type = net_topol.get_layer_types(options_dictionary)
    
    training_dataset = SequentialDataSet(num_predictors, num_outputs)
    
    print 'reach'

    previous_sequence_number = 1
    
    #read data into dataset objects
    print 'reading in training data...'
    for row in training_reader:
        #convert list of strings to list of floats
        list = [float(s) for s in row]
        
        #split input line
        predictors = list[0:num_predictors]
        outputs = list[num_predictors+1:num_predictors+1+num_outputs]
        
        #convert from python list to numpy array
        predictors = np.array(predictors)
        outputs = np.array(outputs)
        
        sequence_number = math.trunc(list[num_predictors])
        
        if not sequence_number==previous_sequence_number:
            # print sequence_number
            # print previous_sequence_number
            training_dataset.newSequence()
        
        previous_sequence_number = sequence_number
        
        #add to dataset
        training_dataset.appendLinked(predictors, outputs)
        
    network = shortcuts.buildNetwork(num_predictors, num_hidden_neurons, num_outputs, hiddenclass=LSTMLayer, outclass=LinearLayer)
    network.sortModules();
    
    trainer = RPropMinusTrainer(module=network, dataset=training_dataset)

    for i in range(num_training_epochs):
        print 'Starting training epoch: '+str(i)
        trainer.trainEpochs(1)
        sys.stdout.flush()

    #brittle
    network_file_path = output_location+'trained_network.xml'
    NetworkWriter.writeToFile(network, network_file_path)
    done_file_handle = open(output_location+'training_done.txt',"w")
    done_file_handle.write('%s' % 'done!')
    done_file_handle.close()

def network_predict(options_file_location,prediction_data_location,output_location,network_location):

    prediction_data_file_handle = open(prediction_data_location,"r")
    prediction_data_reader = csv.reader(prediction_data_file_handle)
    
    stdout_file = output_location+'prediction_console_output.txt'
    stderr_file = output_location+'prediction_console_errput.txt'
    
    sys.stdout = open(stdout_file,"w")
    sys.stderr = open(stderr_file,"w")
    
    prediction_results_file_location = output_location+'prediction_results.csv'
    prediction_results_file_handle = open(prediction_results_file_location,"w")
    
    options_file_handle = open(options_file_location,'r')
    options_dictionary = {}

    for option in options_file_handle.readlines():
        key,val = option.split('=')
        print key
        print val
        options_dictionary[key] = val;

    num_predictors = int(options_dictionary['num_predictors'])
    num_outputs = int(options_dictionary['num_outputs'])
    num_training_epochs = int(options_dictionary['num_training_epochs'])
    num_hidden_neurons = int(options_dictionary['num_hidden_neurons'])
    compound_prediction = int(options_dictionary['compound_prediction'])
    # teacher_forced_transient = int(options_dictionary['teacher_forced_transient'])
    teacher_forced_transient = 0
    
    prediction_dataset = SequentialDataSet(num_predictors, num_outputs)
    
    previous_sequence_number = 1
    print 'reading in prediction data...'
    for row in prediction_data_reader:
        #convert list of strings to list of floats
        list = [float(s) for s in row]
        
        #split input line
        predictors = list[0:num_predictors]
        #+1 is to skip over the sequence column
        outputs = list[num_predictors+1:num_predictors+1+num_outputs]

        
        #convert from python list to numpy array
        predictors = np.array(predictors)
        outputs = np.array(outputs)
        
        sequence_number = math.trunc(list[num_predictors])
        
        if not sequence_number==previous_sequence_number:
            # print 'sequence_number '+str(sequence_number)
            # print 'previous_sequence_number '+str(previous_sequence_number)
            # frame_number_debug = 0;
            prediction_dataset.newSequence()
        
        previous_sequence_number = sequence_number
        
        #add to dataset
        prediction_dataset.appendLinked(predictors, outputs)
    
    network = NetworkReader.readFrom(network_location)
    
    if compound_prediction==0:
        results, targets, mse = evalRNN.evalRNNOnSeqDataset(network,prediction_dataset)
    elif compound_prediction==1:
        results, targets, mse = evalRNN.compoundEvalRNNOnSeqDataset(network,prediction_dataset, teacher_forced_transient)
                
    results_length, results_width = results.shape
 
    np.savetxt(prediction_results_file_location,results,delimiter=" ",fmt='%9.9f')
    
    done_file_handle = open(output_location+'predicting_done.txt',"w")
    done_file_handle.write('%s' % 'done!')
    done_file_handle.close()
    

if __name__ == '__main__':
    train_or_predict = sys.argv[1]
    
    if train_or_predict=='-train':
        options_file_location = sys.argv[2]
        training_data_location = sys.argv[3]
        output_location = sys.argv[4]
        
        print train_or_predict
        print options_file_location
        print training_data_location
        print output_location
        
        train_network(options_file_location,training_data_location,output_location)
    
    elif train_or_predict=='-predict':
        options_file_location = sys.argv[2]
        prediction_data_location = sys.argv[3]
        output_location = sys.argv[4]
        network_location = sys.argv[5]
        
        network_predict(options_file_location,prediction_data_location,output_location,network_location)