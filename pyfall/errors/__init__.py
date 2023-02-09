class APIError(Exception):
    """An error returned by Scryfall itseslf.
    
    Attributes include: object, code, status, warnings, details
    
    object value is "error". code, status are HTTP-like.
    warnings, details include further info from scryfall."""
    def __init__(self, *args):
        super().__init__(*args)
        for key in args[0].keys():
            setattr(self, key, args[0][key])

class RequestError(Exception):
    """A Scryfall-related error caused by something this library, or the user, did."""
    def __init__(self, *args):
        super().__init__(*args)

class AmbiguityError(Exception):
    """An error related to this program's inability to determine which of multiple things to pick."""
    def __init__(self, *args):
        super().__init__(*args)