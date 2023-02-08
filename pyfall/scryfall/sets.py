from pyfall.scryfall.API import StrPrototypes, callapi
from pyfall.scryobject import processapiresponse, scryObject

def callsets(code:str|None=None, type:str|None=None, **kwargs) -> scryObject:
    """Calls /sets, /sets/:code, /sets/:id, or /sets/tcgplayer/:id
    
    With no code or type argument, calls /sets and returns a scryList of scrySet objects
    
    type can be one of 'setcode', 'tcgplayerid', or 'scryfallid'
    
    For setcode, code should be the 3-5 character set code. For tcgplayerid, code should
    be the relevant set's tcgplayer id. For scryfallid, code should be the set's scryfall id.
    In all cases, this returns a scryList or a scrySet.
    """
    type_calls = {
        None:'/sets',
        'setcode':'/sets/{}',
        'tcgplayerid':'/sets/tcgplayer/{}',
        'scryfallid':'/sets/{}'
    }
    if type not in type_calls.keys():
        raise ValueError(StrPrototypes.VALUEERROR.format("type", type_calls.keys(), type))
    
    call = type_calls[type].format(code)

    return processapiresponse(callapi(call, **kwargs))

def sets():
    return callsets()

def setcode(code:str):
    return callsets(code=code, type=None)

def setcode(code:str):
    return callsets(code=code, type="setcode")

def tcdplayer(code:str):
    return callsets(code=code, type="tcgplayerid")

def scryfallid(code:str):
    return callsets(code=code, type="scryfallid")