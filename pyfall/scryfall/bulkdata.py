from ..scryobject import processapiresponse
from .api import apiget

def bulk_data():
    return processapiresponse(apiget("bulk-data"))
