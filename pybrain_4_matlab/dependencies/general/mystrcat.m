function [ out_string ] = mystrcat(varargin)

string_accumulator = {''};

for i = 1:nargin
   string = varargin{i}; 
   boxed_string = {string};
   string_accumulator = strcat(string_accumulator,boxed_string);   
end

out_string = string_accumulator{1};

end

