function pybrain_predict(options, options_file_location, prediction_data_location, output_location, network_location )
%PYBRAIN_PREDICT pybrain_predict(options_file_location, prediction_data_location, output_location, network_location )
%   Detailed explanation goes here

root_source_folder = get_root_source_folder();

%brittle
if(get_option('regression',options)==1)
    script_relative_path = 'my_libs/LSTM/python/monohiddenlayer_regression_LSTM.py';
else
    assert(get_option('classification',options)==1)
    script_relative_path = 'my_libs/LSTM/python/monohiddenlayer_classification_LSTM.py';
end

script_path = strcat(root_source_folder, script_relative_path);

train_or_predict = '-predict';
args_string = train_or_predict;

args_string = mystrcat(args_string,' ',add_double_quotes(options_file_location));
args_string = mystrcat(args_string,' ',add_double_quotes(prediction_data_location));
args_string = mystrcat(args_string,' ',add_double_quotes(output_location));
args_string = mystrcat(args_string,' ',add_double_quotes(network_location));

shell_string = mystrcat('start python',' ',add_double_quotes(script_path),' ',args_string);

global cache_cmd;
cache_cmd = shell_string;

[status,result] = system(shell_string,'-echo') 


end

