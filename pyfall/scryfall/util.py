from .API import StrPrototypes

def validate_kwargs(kwarg_dict, valid_keywords):
    for keyword in kwarg_dict:
        if keyword not in valid_keywords:
            raise ValueError("Invalid keyword")
    return kwarg_dict

def validate_param_value(param:str, kwarg_dict:dict, valid_values:list):
    if (param in kwarg_dict):
        if (kwarg_dict[param] not in valid_values):
            raise ValueError(StrPrototypes.VALUEERROR.format(param,valid_values,kwarg_dict[param]))
        else:
            return {param:kwarg_dict[param]}
    else:
        return {param:None}