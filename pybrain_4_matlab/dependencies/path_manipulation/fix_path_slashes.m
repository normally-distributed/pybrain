function [ new_path ] = fix_path_slashes( path )
%REPLACE_PATH_SLASHES Summary of this function goes here
%   Detailed explanation goes here

new_path = regexprep(path,'\','/');

if(~strcmp(new_path(end),'/'))
    new_path = mystrcat(new_path,'/');

end

