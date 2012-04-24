import pybrain
import numpy as np
import scipy
from pybrain.datasets import SupervisedDataSet
from pybrain.datasets import SequentialDataSet
from pybrain.structure.networks import RecurrentNetwork
from pybrain.structure.modules import LinearLayer
from pybrain.structure.modules import LSTMLayer
from pybrain.structure.modules import SoftmaxLayer
from pybrain.structure.modules import SigmoidLayer
from pybrain.structure.connections import FullConnection
import pybrain.tools.shortcuts as shortcuts
import pdb
from numpy.random import permutation
from numpy import array, array_split, apply_along_axis, concatenate, ones, dot, delete, append, zeros, argmax
import copy
from pybrain.datasets.importance import ImportanceDataSet
from pybrain.datasets.sequential import SequentialDataSet
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.validation import ModuleValidator
from pybrain.tools.validation import Validator
from pybrain.tools.validation import SequenceHelper

def evalRNNOnSeqClassificationDataset(net, testing_dataset, verbose = False, silent = False):
   
    # Fetch targets and calculate the modules output on dataset.
    # Output and target are in one-of-many format. The class for each sequence is
    # determined by first summing the probabilities for each individual sample over
    # the sequence, and then finding its maximum.
    target = testing_dataset.getField("target")
    
    outputs = []
    
    # print net
    
    for seq in testing_dataset._provideSequences():
        net.reset()
        # print 'seq:'
        # print seq
        for i in xrange(len(seq)):
            output = net.activate(seq[i][0])
            outputs.append(output.copy())
    outputs = array(outputs)
    
    

    # determine last indices of the sequences inside dataset
    ends = SequenceHelper.getSequenceEnds(testing_dataset)
    ##format = "%d"*len(ends)
    summed_output = zeros(testing_dataset.outdim)
    # class_output and class_target will store class labels instead of
    # one-of-many values
    class_output = []
    class_target = []
    for j in xrange(len(outputs)):
        # sum up the output values of one sequence
        # print outputs[j]
        summed_output += outputs[j]
#            print j, output[j], " --> ", summed_output
        # if we reached the end of the sequence
        if j in ends:
            # print '------------------------------------------'
            # convert summed_output and target to class labels
            class_output.append(argmax(summed_output))
            class_target.append(argmax(target[j]))

            # reset the summed_output to zeros
            summed_output = zeros(testing_dataset.outdim)

    ##print format % tuple(class_output)
    ##print format % tuple(class_target)

    class_output = array(class_output)
    class_target = array(class_target)
#    print class_target
#    print class_output
    accuracy =  Validator.classificationPerformance(class_output, class_target)
    return (class_output, class_target, accuracy)

    

def evalRNNOnSeqDataset(net, testing_dataset, verbose = False, silent = False):
#   evaluate the network on all the sequences of a dataset. 

    results_array = scipy.zeros((len(testing_dataset), testing_dataset.outdim), float)

    targets = testing_dataset.getField("target")
    
    r = 0
    samples = 0
    for seq in testing_dataset:
        net.reset()
        print 'reset!'
        for i, t in seq:
            res = net.activate(i)
            results_array[samples,:] = res
            if verbose:
                print t, res
            r += sum((t-res)**2)
            samples += 1
        if verbose:
            print '-'*20
         
    r /= samples
    if not silent:
        print 'MSE:', r
        
    targets_array = array(targets)
      
    return (results_array, targets_array, r)
  
  #untested
def compoundEvalRNNOnSeqDataset(net, testing_dataset, teacher_forced_transient, verbose = False, silent = False):


#   evaluate the network on all the sequences of a dataset. 

    #results_array = scipy.zeros((len(testing_dataset)-teacher_forced_transient, testing_dataset.outdim), float)
    results_array = scipy.zeros((len(testing_dataset), testing_dataset.outdim), float)
    targets = testing_dataset.getField("target")
     
    r = 0
    samples = 0
    for seq in testing_dataset:
        net.reset()
        print 'reset!'
        
        seq_counter = 0;
        for i, t in seq:
            
            if seq_counter<teacher_forced_transient:
                res = net.activate(i)
            else:
                res = net.activate(prev_res)
         
            prev_res = res
            results_array[samples,:] = res
            
            if verbose:
                print t, res
            
            r += sum((t-res)**2)
            
            # if seq_counter<teacher_forced_transient:
                # samples += 1
            samples += 1
            
            seq_counter += 1
        if verbose:
            print '-'*20
         
    r /= samples
    
    targets_array = array(targets)
    
    if not silent:
        print 'MSE:', r
      
    return (results_array, targets_array, r)
    
