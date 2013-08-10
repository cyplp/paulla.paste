import couchdbkit

settings = {
    'couchdb.url' = 'http://0.0.0.0:5984/',
    }

def main():
    """
    Purge old paste.
    """
    server = couchdbkit.Server(settings['couchdb.url'])
    db = server.get_or_create_db(settings['couchdb.db'])
    Paste.set_db(db)
