from gluon.tools import Crud
crud = Crud(globals(), db)

def user():
    return dict(form=auth())
    
def index():
    topics = db().select(db.topic.ALL, orderby=db.topic.id)
    return dict(topics=topics)

def show():
    ## show
    if not request.args(0).isdigit():
        redirect( URL (r=request, f='index') )    
    topic = db.topic[request.args(0)]
    if not topic:
        redirect( URL (r=request, f='index') )
    comments = db(db.comment.topic_id==topic.id).select()
    db.comment.topic_id.default = topic.id
    return dict(topic=topic, comments=comments)

@auth.requires_login()
def add_topic():
    form = crud.create(db.topic, next=URL(r=request, f='index'), message='your topic is created.')
    return dict(form=form)

@auth.requires_login()
def edit_topic():
    if not request.args(0).isdigit():
        redirect( URL (r=request, f='index') )    
    this_topic = db.topic[request.args(0)]
    if not this_topic or this_topic.userid != auth.user.id:
        redirect( URL (r=request, f='index') )
    form = crud.update(db.topic, request.args(0), next=URL(r=request, f='show', args=request.args(0)), message='your topic is updated.')
    return dict(form=form)

@auth.requires_login()
def reply():
    if not request.args(0).isdigit():
        redirect( URL (r=request, f='index') )    
    this_topic = db.topic[request.args(0)]
    if not this_topic:
        redirect( URL(r=request, f='index') )
    db.comment.topic_id.default = request.args(0)
    form = crud.create(db.comment, next=URL(r=request, f='show', args=request.args(0)), message='your comment is created')
    return dict(form=form)

@auth.requires_login()
def edit_comment():
    if not request.args(0).isdigit():
        redirect( URL (r=request, f='index') )    
    this_comment = db.comment[request.args(0)]
    if not this_comment or this_comment.userid != auth.user.id:
        redirect( URL (r=request, f='index') )
    form = crud.update(db.comment, request.args(0), next=URL(r=request, f='show', args=this_comment.topic_id), message='your comment is updated.')
    return dict(form=form)
