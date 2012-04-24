function [ root_data_folder ] = get_root_data_folder()
%GET_ROOT_DATA_FOLDER Summary of this function goes here

%    This is not necessary to set. It's just a nice organizational tool to separate your library code, your experiment code, and your experimental results.

[status,result] = system('hostname');

%convert char array to char string (my god matlab...)
result = cellstr(result);
result = result{1};

%put your hostnames and corresponding primary data locations here...

if(strcmp(result,'$YOUR_FIRST_COMPUTER'))
    root_data_folder = 'C:\...';
elseif(strcmp(result,'$YOUR_SECOND_COMPUTER'))
    root_data_folder = 'C:\...';
elseif(strcmp(result,'$YOUR_THIRD_COMPUTER'))
    root_data_folder = 'C:\...';
end

root_data_folder = fix_path_slashes(root_data_folder);

end

