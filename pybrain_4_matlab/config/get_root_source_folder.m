function [ root_source_folder ] = get_root_source_folder()
%GET_ROOT_SOURCE_FOLDER Summary of this function goes here
%   Detailed explanation goes here

%    THIS IS NECESSARY TO SET. otherwise the matlab script won't know where to find the python script, there'll be red error text, and the Sun will explode.


[status,result] = system('hostname');

%convert char array to char string (my god matlab...)
result = cellstr(result);
result = result{1};

%put your hostnames and corresponding primary script source tree locations here...

if(strcmp(result,'$YOUR_FIRST_COMPUTER'))
    root_source_folder = 'C:\Users\****\Desktop\work\code';  % <-- as an example. replace with your own.
elseif(strcmp(result,'$YOUR_SECOND_COMPUTER'))
    root_source_folder = 'C:\...';
elseif(strcmp(result,'$YOUR_THIRD_COMPUTER'))
    root_source_folder = 'C:\...';
end

root_source_folder = fix_path_slashes(root_source_folder);

end