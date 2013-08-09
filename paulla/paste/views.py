import datetime

import couchdbkit

import bcrypt

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_registry
from pyramid.events import NewRequest
from pyramid.events import subscriber

from beaker.cache import cache_region

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers

from paulla.paste.models import Paste


settings = get_current_registry().settings

expireChoice = {"never": None,
                "1day": datetime.timedelta(days=1),
                "1week": datetime.timedelta(days=7),
                "1month": datetime.timedelta(days=31)
                }

# couchdb connection
server = couchdbkit.Server(settings['couchdb.url'])
db = server.get_or_create_db(settings['couchdb.db'])
Paste.set_db(db)

formatter = HtmlFormatter(linenos=True, full=True, cssclass="source")

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    """
    Home page.

    first page to be called.
    """
    return {'lexers': lexers()}

@view_config(route_name='addContent', renderer='json')
def add(request):
    """
    Adding a new content.

    if ok return to the oneContent page.
    """
    username = request.POST['username']
    password = ''


    now = datetime.datetime.now()
    expire = request.POST['expire']

    expireDate = None

    if expire:
        delta = expireChoice[expire]

        if delta:
            expireDate = now + delta

    if username:
        password = bcrypt.hashpw(request.POST['password'], bcrypt.gensalt())

    paste = Paste(title=request.POST['title'],
                  content=request.POST['content'],
                  created=now,
                  typeContent=request.POST['type'],
                  username=username,
                  password=password,
                  expire=expireDate)
    paste.save()

    request.session.flash(u"Add ok") # TODO translatoion

    return HTTPFound(request.route_path('oneContent', idContent=paste._id))


@view_config(route_name='oneContent', renderer='templates/content.pt')
def content(request):
    """
    Display a content Paste.
    """
    paste = Paste.get(request.matchdict['idContent'])
    lexer = get_lexer_by_name(paste.typeContent, stripall=True)

    result = highlight(paste['content'], lexer, formatter)

    return {'paste': paste,
            'content': result,}

@view_config(route_name='oneContentRaw', renderer='string' )
def contentRaw(request):
    """
    Display a raw content paste.
    """
    paste = Paste.get(request.matchdict['idContent'])
    # TODO type/mime
    return paste.content


@cache_region('short_term', 'previous')
def previous():
    """
    Return the list of the 10 previous paste.
    """
    previousPastes = Paste.view('paste/all',  limit=10).all()
    return previousPastes

@cache_region('long_term', 'lexers')
def lexers():
    """
    Return the list of the pigments lexers.
    """
    result = [(lexer[0], lexer[1][0]) for lexer in get_all_lexers()]
    result.sort()
    return result

@subscriber(NewRequest)
def previousEvent(event):
    """
    subscriber of newRequest.
    """
    event.request.previous = previous()

@view_config(route_name='edit', renderer='templates/edit.pt')
def edit(request):
    """
    Edit a paste.
    """
    paste = Paste.get(request.matchdict['idContent'])

    return {'lexers': lexers(),
            'paste': paste,}

@view_config(route_name='update')
def update(request):
    """
    Updating a paste.

    return to display if succed.
    return to edit if fail.
    """
    paste = Paste.get(request.matchdict['idContent'])

    if bcrypt.hashpw(request.POST['password'], paste.password) == paste.password:
        paste.title = request.POST['title']
        paste.content = request.POST['content']

        paste.save()

        request.session.flash(u"Updated") # TODO translatoion

        return HTTPFound(request.route_path('oneContent', idContent=paste._id))

    request.session.flash(u"Wrong password") # TODO translatoion

    return HTTPFound(request.route_path('edit', idContent=paste._id))


@view_config(route_name='deleteConfirm', renderer='templates/delete_confirm.pt')
def deleteConfirm(request):
    """
    Ask confirmation on delete.
    """
    paste = Paste.get(request.matchdict['idContent'])

    if not(paste.username and paste.password):
        return HTTPFound(request.route_path('oneContent', idContent=paste._id))

    lexer = get_lexer_by_name(paste.typeContent, stripall=True)

    result = highlight(paste['content'], lexer, formatter)

    return {'paste': paste,
            'content': result,}


@view_config(route_name='delete')
def delete(request):
    """
    Delete a paste.

    return to / if succed
    return to deleteConfigm is fail.
    """
    paste = Paste.get(request.matchdict['idContent'])

    if bcrypt.hashpw(request.POST['password'], paste.password) == paste.password:
        paste.delete()

        request.session.flash(u"Deleted") # TODO translatoion

        return HTTPFound(request.route_path('home', ))

    request.session.flash(u"Wrong password") # TODO translatoion

    return HTTPFound(request.route_path('deleteConfirm', idContent=paste._id))

@view_config(route_name='rss2', renderer='templates/rss2.pt')
def rss2(request):
    """
    Yeah we have rss !
    """
    return {'pastes': previous()}
