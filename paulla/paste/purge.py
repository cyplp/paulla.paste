import couchdbkit

from paulla.paste.models import Paste

settings = {
    'couchdb.url': 'http://0.0.0.0:5984/',
    'couchdb.db': 'paste',
    }

def main():
    """
    Purge old paste.
    """
    server = couchdbkit.Server(settings['couchdb.url'])
    db = server.get_or_create_db(settings['couchdb.db'])
    Paste.set_db(db)

    oldPastes = Paste.view('old/all').all()

    for paste in oldPastes:
        print paste._id
        paste.delete()
