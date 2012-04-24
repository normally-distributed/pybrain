function pybrain_train(options, options_file_location, training_data_location, output_location)
%SIMPLE_CALL_PYBRAIN pybrain_train(options, options_file_location, training_data_location, output_location)
%   Detailed explanation goes here



%write options out to .ini (key=val) file
options_file_handle = fopen(options_file_location,'w');
for i = 1:size(options,1)
    option_key = options{i,1};
    option_value = options{i,2};
    
    if(strcmp(class(option_value),'char'))
        option_string = mystrcat(option_key,'=',option_value);
    else
        option_string = mystrcat(option_key,'=',int2str(option_value));
    end
    fprintf(options_file_handle,'%s\n',option_string);
end
fclose(options_file_handle);

root_source_folder = get_root_source_folder();

%brittle
if(get_option('regression',options)==1)
    script_relative_path = 'my_libs/LSTM/python/monohiddenlayer_regression_LSTM.py';
else
    assert(get_option('classification',options)==1)
    script_relative_path = 'my_libs/LSTM/python/monohiddenlayer_classification_LSTM.py';
end

script_path = strcat(root_source_folder, script_relative_path);

train_or_predict = '-train';
args_string = train_or_predict;

args_string = mystrcat(args_string,' ',add_double_quotes(options_file_location));
args_string = mystrcat(args_string,' ',add_double_quotes(training_data_location));
args_string = mystrcat(args_string,' ',add_double_quotes(output_location));

shell_string = mystrcat('start python',' ',add_double_quotes(script_path),' ',args_string);

global cache_cmd;
cache_cmd = shell_string;

[status,result] = system(shell_string,'-echo') 

end


