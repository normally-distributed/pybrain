function [output_args] = test_japanese_vowels_nets(run_index)
    %the run index is just the index of the experiment you've run for this set of experiments. so if you have a experiment which created folder 
    % 'some_path_to_this_folder/150_neurons_1000_epochs/run_1' and you want to gather the results for it, use run_index=1

    %for this to work, you must set the root_data_folder in get_root_data_folder() to $some_path_to_this_folder/examples_data
    data_folder = mystrcat(get_root_data_folder(),'/japanese_vowels/');


    prediction_data_location = mystrcat(data_folder,'testing_data.csv');

    if(~exist(prediction_data_location,'file')==2)
        japanese_vowel_data_path = remove_double_quotes(mystrcat(data_folder,'vowel_data1.mat'));
        load(japanese_vowel_data_path);
        dlmwrite(prediction_data_location,japanese_vowel_testing_data)
    end

    
    experisults_folder = % folder where you want your experimental results to go
    experiment_set_dir = %eg. '150_neurons_1000_epochs/' would be the folder containing the results for the set of experiments using networks with 150 hidden neurons trained for 1k epochs
    
    experisults_folder = fix_path_slashes(experisults_folder);
    experiment_set_dir = mystrcat(experisults_folder,experiment_set_dir);

    output_location = fix_path_slashes(mystrcat(experiment_set_dir,'run_',num2str(run_index)));
    options_file_location = mystrcat(experiment_set_dir,'options.ini');
    network_location = mystrcat(output_location,'trained_network.xml');
    
    options = {'num_predictors',12;
               'num_outputs',9;
               'num_training_epochs',1000;
               'num_hidden_neurons',150;
               'hidden_neuron_type','lstm';
               'output_neuron_type','softmax';
               'compound_prediction',0;
               'teacher_forced_transient',0;
               'classification',1;
               'regression',0;
               'num_classes',9;
              };

    pybrain_predict(options, options_file_location, prediction_data_location, output_location, network_location)
    
end