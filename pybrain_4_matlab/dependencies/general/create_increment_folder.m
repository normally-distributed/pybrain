function [ new_folder_path ] = create_increment_folder( folder_prefix, parent_folder )
%CREATE_INCREMENT_FOLDER Summary of this function goes here
%   Detailed explanation goes here
    parent_folder = fix_path_slashes(parent_folder);
    folders = dir(parent_folder);
    matching_folders_numbers = [];
    
    for i = 1:length(folders)
        folder_name = folders(i).name;
        contains_pattern = regexpi(folder_name, mystrcat(folder_prefix,'.*'));

        if(~isempty(contains_pattern))
            split_result = str2num(regexprep(folder_name,folder_prefix,''));
            matching_folders_numbers = [matching_folders_numbers split_result];
        end
    end
        
    matching_folders_numbers = sort(matching_folders_numbers);
    
    if(~isempty(matching_folders_numbers))
        highest_folder = matching_folders_numbers(end);
    else
        highest_folder = 0;
    end
        
    new_folder_path = mystrcat(parent_folder,folder_prefix,int2str(highest_folder+1),'/');
    mkdir(new_folder_path)
end

