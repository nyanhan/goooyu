"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class Feed(ndb.Model):
    """Example Model"""
    feed_address = ndb.StringProperty(required=True)
    feed_link = ndb.StringProperty(required=True)
    feed_title = ndb.StringProperty(default="")
    is_push = ndb.BooleanProperty(default=False)
    num_sub = ndb.IntegerProperty(default=-1)
    next_scheduled_update = ndb.DateTimeProperty()

#added_by = ndb.UserProperty()
    last_update = ndb.DateTimeProperty(auto_now=True)
    create = ndb.DateTimeProperty(auto_now_add=True)
