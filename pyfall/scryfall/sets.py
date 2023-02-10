from pyfall.util import validate_param_value
from pyfall.scryobject import scryObject, getscryobject

# Not available as a catalog; check scryfall docs for up-to-date list
# Good a/o February 2023
SET_TYPES = [
    "core",
    "expansion",
    "masters",
    "alchemy",
    "masterpiece",
    "arsenal",
    "from_the_vault",
    "spellbook",
    "premium_deck",
    "duel_deck",
    "draft_innovation",
    "treasure_chest",
    "commander",
    "planechase",
    "archenemy",
    "vanguard",
    "funny",
    "starter",
    "box",
    "promo",
    "token",
    "memorabilia",
]

def callsets(**kwargs) -> scryObject:
    """Calls /sets, /sets/:code, /sets/:id, or /sets/tcgplayer/:id
    
    With no code or type argument, calls /sets and returns a scryList of scrySet objects
    
    `type` can be one of 'setcode', 'tcgplayerid', or 'scryfallid'
    
    For setcode, code should be the 3-5 character set code. For tcgplayerid, code should
    be the relevant set's tcgplayer id. For scryfallid, code should be the set's scryfall id.
    In all cases, this returns a scryList or a scrySet.
    """
    valid_types = [None, '', 'setcode', 'tcgplayerid', 'scryfallid']
    type_calls = {
        None:'/sets',
        '':'/sets',
        'setcode':'/sets/{}',
        'tcgplayerid':'/sets/tcgplayer/{}',
        'scryid':'/sets/{}'
    }

    kwarg_dict = {"type":None,"code":None}
    kwarg_dict.update(kwargs)
    validate_param_value("type", kwarg_dict, valid_types)
    call = type_calls[kwarg_dict["type"]].format(kwarg_dict["code"])

    return getscryobject(call, **kwarg_dict)

def sets(code:str|None=None, **kwargs):
    return callsets(code, **kwargs)

def setcode(code:str):
    return callsets(code=code, type="setcode")

def tcgplayer(code:str):
    return callsets(code=code, type="tcgplayerid")

def scryid(code:str):
    return callsets(code=code, type="scryid")