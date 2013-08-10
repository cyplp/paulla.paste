import couchdbkit

from paulla.paste.models import Paste


class PastePredicate(object):
    """
    Check and get Paste.
    """
    def __init__(self, val, config):
        pass

    def text(self):
           return 'predicat on paste'

    phash = text

    def __call__(self,  context, request):
        try:
            request.paste = Paste.get(request.matchdict['idContent'])
            return True
        except couchdbkit.exceptions.ResourceNotFound:
            return False
