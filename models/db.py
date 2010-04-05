db = DAL("sqlite://storage.db")

from gluon.tools import Auth
auth = Auth(globals(), db)
auth.define_tables()
auth.settings.registration_requires_approval = True

if auth.is_logged_in():
    user_id = auth.user.id
else:
    user_id = None
    
db.define_table('topic',
    Field('title'),
    Field('body', 'text'),
    Field('userid', db.auth_user, default=user_id),
    Field('created_on', 'datetime', default=request.now)
)

db.topic.title.requires = IS_NOT_EMPTY()
db.topic.body.requires = IS_NOT_EMPTY()
db.topic.created_on.writable=False
db.topic.created_on.readable=False
db.topic.userid.writable=False
db.topic.userid.readable=False

db.define_table('comment',
    Field('userid', db.auth_user, default=user_id),
    Field('body', 'text'),
    Field('topic_id', db.topic),
    Field('created_on', 'datetime', default=request.now)
)
db.comment.body.requires = IS_NOT_EMPTY()
db.comment.topic_id.requires = IS_IN_DB(db, db.topic.id, '%(title)s')
db.comment.topic_id.writable = False
db.comment.topic_id.readable = False
db.comment.created_on.writable=False
db.comment.created_on.readable=False
db.comment.userid.writable=False
db.comment.userid.readable=False
