from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings

from pyramid.threadlocal import get_current_registry

#from paulla.paste.xmlrpc import XmlRPC

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    sessionFactory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)

    config = Configurator(settings=settings)
    config.set_session_factory(sessionFactory)

    get_current_registry().settings = settings

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('addContent', '/add')
    config.add_route('xmlrpc', '/xmlrpc')
    config.add_route('oneContent', '/{idContent}')
    config.add_route('oneContentRaw', '/{idContent}/raw')
    config.add_route('update', '/{idContent}/update')
    config.add_route('edit', '/{idContent}/edit')
    config.add_route('deleteConfirm', '/{idContent}/deleteConfirm')
    config.add_route('delete', '/{idContent}/delete')

    config.add_route('rss2', '/feeds/rss2')


    #config.add_view(XmlRPC, name='xmlrpc')


    config.add_fanstatic_resources([resource.strip() for resource in settings['resources'].split(',')]
                                   , r'.*\.pt')

    config.scan()
    return config.make_wsgi_app()
