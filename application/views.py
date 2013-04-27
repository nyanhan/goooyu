"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
#from oauth2client.appengine import OAuth2Decorator
from oauth2client.appengine import StorageByKeyName
from oauth2client.appengine import OAuth2WebServerFlow
from oauth2client.appengine import CredentialsNDBModel

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache

from application import app
from application.settings import G_CLIENT_ID, G_CLIENT_SECRET, G_REDIRECT_URI
from decorators import login_required, admin_required
from models import Feed

from libgreader import GoogleReader
from libgreader.auth import GAPDecoratorAuthMethod


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

GOOGLE_URL = 'https://accounts.google.com'
AUTHORIZATION_URL = GOOGLE_URL + '/o/oauth2/auth'
ACCESS_TOKEN_URL = GOOGLE_URL + '/o/oauth2/token'

FLOW = OAuth2WebServerFlow(
    client_id       = G_CLIENT_ID,
    client_secret   = G_CLIENT_SECRET,
    redirect_uri    = G_REDIRECT_URI,
    user_agent      = 'Goooyu app',
    auth_uri        = AUTHORIZATION_URL,
    token_uri       = ACCESS_TOKEN_URL,
    scope=[
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.google.com/reader/api/',
    ],
)

def home():
    return 'hello world'
#return redirect(url_for('list_examples'))


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username


@login_required
def google_login():
    user = users.get_current_user()
    credentials = StorageByKeyName(CredentialsNDBModel, user.user_id(), 'credentials').get()

    if credentials is None or credentials.invalid == True:
        authorize_url = FLOW.step1_get_authorize_url(G_REDIRECT_URI)
        return redirect(authorize_url)

    return redirect(url_for('import'))


@login_required
def oauth2callback():
    user = users.get_current_user()
    credentials = FLOW.step2_exchange(request.args)
    StorageByKeyName(CredentialsNDBModel, user.user_id(), 'credentials').put(credentials)
    #code = request.args.get('code', '')
    #credentials = Credentials(credentials=code)
    #storage = StorageByKeyName(Credentials, user.user_id(), 'credentials').put(credentials)
    return redirect(url_for('import'))
    #return redirect(url_for('login'))


@login_required
def import_reader():
    if request.method == 'GET':
        return render_template('import.html')
    else:
        user = users.get_current_user()
        storage = StorageByKeyName(CredentialsNDBModel, user.user_id(), 'credentials')
        credentials = storage.get()
        auth = GAPDecoratorAuthMethod(credentials)
        reader = GoogleReader(auth)
        reader.buildSubscriptionList()
        feeds = reader.getSubscriptionList()
        for feed in feeds:
            f = Feed(
                feed_address=feed.feedUrl,
                feed_link=feed.siteUrl,
                feed_title=feed.title,
            )
            f.put()
        return 'Import OK! '


@login_required
def feeds():
    user = users.get_current_user()

    if user:
        storage = StorageByKeyName(CredentialsNDBModel, user.user_id(), 'credentials')
        credentials = storage.get()

        # Use the new AuthMethod to decorate all the requests with correct credentials
        auth = GAPDecoratorAuthMethod(credentials)
        reader = GoogleReader(auth)
        reader.buildSubscriptionList()
        feeds = reader.getSubscriptionList()
        return '\n'.join([f.title for f in feeds])


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

