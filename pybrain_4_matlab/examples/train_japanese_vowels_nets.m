%for this to work, you must set the root_data_folder in get_root_data_folder() to $some_path_to_this_folder/examples_data

data_folder = mystrcat(get_root_data_folder(),'/japanese_vowels/');

training_data_file_location = mystrcat(data_folder,'training_data.csv');
testing_data_file_location = mystrcat(data_folder,'testing_data.csv');

if(~(exist(training_data_file_location,'file')==2....
    && exist(testing_data_file_location,'file')==2))
    japanese_vowel_data_path = remove_double_quotes(mystrcat(data_folder,'vowel_data1.mat'));
    load(japanese_vowel_data_path);

    dlmwrite(training_data_file_location,japanese_vowel_training_data)
    dlmwrite(testing_data_file_location,japanese_vowel_testing_data)

end

experisults_folder = % folder where you want your experimental results to go
experiment_set_dir = %eg. '150_neurons_1000_epochs/' would be the folder containing the results for the set of experiments using networks with 150 hidden neurons trained for 1k epochs

experisults_folder = fix_path_slashes(experisults_folder);
experiment_set_dir = mystrcat(experisults_folder,experiment_set_dir);

mkdir(experiment_set_dir)

output_location = create_increment_folder('run_',experiment_set_dir);
options_file_location = mystrcat(experiment_set_dir,'options.ini');
% num_predictors = 12;
% num_outputs = 1;

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

pybrain_train(options, options_file_location, training_data_file_location, output_location)