import argparse
import ConfigParser
import logging
import logging.config

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf',
                        help='paulla.paste conf file')

    args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    config.read(args.conf)

    logging.config.fileConfig(args.conf)
    logger = logging.getLogger('purge')

    server = couchdbkit.Server(config.get('app:main', 'couchdb.url'))
    db = server.get_or_create_db(config.get('app:main','couchdb.db'))
    Paste.set_db(db)

    oldPastes = Paste.view('old/all').all()

    for paste in oldPastes:
        logger.info("deleting %s", paste._id)
        paste.delete()
