from ..errors import STR_VALUEERROR
from .. import scryobject
from .API import apiget

def validate_kwargs(kwarg_dict:dict, valid_keywords:list) -> dict:
    for keyword in kwarg_dict:
        if keyword not in valid_keywords:
            raise ValueError("Invalid keyword")
    return kwarg_dict

def validate_param_value(param:str, kwarg_dict:dict, valid_values:list) -> None:
    if (param in kwarg_dict):
        value = kwarg_dict[param].lower() if type(kwarg_dict[param]) == str else kwarg_dict[param]
        if (value not in valid_values):
            raise ValueError(STR_VALUEERROR.format(param,valid_values,value))
    return None

def validate_standard_params(kwarg_dict, valid_format=['json', 'csv', 'text', 'image', 'file']):
    valid_version = [
        'small',
        'normal',
        'large',
        'png',
        'art_crop',
        'border_crop',
    ]
    valid_face = [None, 'back']
    validate_param_value("version", kwarg_dict, valid_version)
    validate_param_value("face", kwarg_dict, valid_face)
    validate_param_value("format", kwarg_dict, valid_format)

# Can't typehint this one's output -- it returns scryobject.scryObject, and that's a circular import
def getscryobject(call:str, **kwargs):
    return scryobject.processapiresponse(apiget(call, **kwargs))