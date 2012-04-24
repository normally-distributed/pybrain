function [ root_experisults_folder ] = get_root_experisults_folder( input_args )
%GET_ROOT_EXPERISULTS_FOLDER

%    This is not necessary to set. It's just a nice organizational tool to separate your library code, your experiment code, and your experimental results.

[status,result] = system('hostname');

%convert char array to char string (my god matlab...)
result = cellstr(result);
result = result{1};

%put your hostnames and corresponding primary data locations here...

if(strcmp(result,'$YOUR_FIRST_COMPUTER'))
    root_experisults_folder = 'C:\...';
elseif(strcmp(result,'$YOUR_SECOND_COMPUTER'))

elseif(strcmp(result,'$YOUR_THIRD_COMPUTER')) 
    
end

root_experisults_folder = fix_path_slashes(root_experisults_folder);

end

