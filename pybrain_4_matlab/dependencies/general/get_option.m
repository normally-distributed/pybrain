function [ option_val ] = get_option( option_name, options )
%GET_OPTION Summary of this function goes here
%   Detailed explanation goes here
for i=1:size(options,1)

    if(strcmp(option_name,options{i,1}))
        option_val = options{i,2};
        break;
    end
    
end
    


end

