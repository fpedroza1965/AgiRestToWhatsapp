import json
from json import JSONEncoder

class DtoModel(object):

    class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
