function [ output_string ] = remove_double_quotes( input_string )
%REMOVE_DOUBLE_QUOTES Summary of this function goes here
%   Detailed explanation goes here

output_string = regexprep(input_string,'"','');


end

