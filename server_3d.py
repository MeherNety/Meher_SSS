from unicodedata import name
from bottle import route, run ,template,view, post, request,redirect,response
from peewee import *
import datetime


##############################################################
######       DATABASE SCHEMES 
##############################################################
db = SqliteDatabase('msg_board.db')

class BaseModel(Model):
    class Meta:
        database = db

class Administrator(BaseModel):
    username        = CharField(unique=True)
    password_hash   = CharField()

class Message(BaseModel):
    id          = PrimaryKeyField()
    name        = TextField()
    message     = TextField()
    posted_date = DateTimeField(default=datetime.datetime.now)
    is_approved = BooleanField(default=False)
##############################################################



##############################################################
## CONTROLLERS
##############################################################


# ENCRYPTING COOKIE
import hashlib
from hashlib import blake2b
from hmac import compare_digest

def sign(cookie):
	cookie_bytes = cookie.encode('ascii')
	encrypt_bytes = hashlib.sha256encode(cookie_bytes)
	encrypt_msg = encrypt_bytes.decode('ascii')
	return encrypt_msg

def verify(cookie):
	cookie_bytes = cookie.encode('ascii')
	decrypt_bytes = hashlib.sha256decode(cookie_bytes)
	decrypt_msg = decode_bytes.decode('ascii')
	if(decrypt_msg[-1]=='i'):
		return True
	else:
		return False

@route('/')
@view('index')
def index():
    msgs = Message.select().where(Message.is_approved==True) 
    msgs = [msg for msg in msgs]
    print(msgs)
    return dict({'msgs':msgs})

@post('/post_message')
def do_post_message():
    poster = request.forms.get('name')
    message = request.forms.get('message')
    Message.create(name=poster,
                   message=message)
    return "<p>Thank you, your message is received and pending approval of the administrator!</p>"
    



@route('/login')
def login():
    return '''
        <center>
        <h1>Admin Control Panel</h1>
        <form action='/login' method="post">
            <div style="padding-top:10px;">Username: <input name="username" type="text" /></div>
            <div style="padding-top:10px;">Password: <input name="password" type="password" /></div>
            <div style="padding-top:10px;"><input value="Login" type="submit" /></div>
        </form>
        </center>
    '''

@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    #not using the ORM but custom RAW SQL
    cursor = db.execute_sql(f"SELECT COUNT(*) FROM administrator WHERE username='{username}' AND password_hash='{password}';")
    found = cursor.fetchone()[0]==1
    if found:
        cookie='i'+username+password
        encode_cookie = sign(cookie)
        response.set_cookie("admin",encode_cookie)
        redirect('/admin')
    else:
        return '''<h2>Username and password did not match!</h2>'''

@route('/admin')
@view('admin') 
def admin():
    cookie = request.get_cookie('admin')
    authenticate_cookie=verify(cookie)
    if cookie == None or authenticate_cookie==False:
        redirect('/login')
    else:
        msgs = Message.select().where(Message.is_approved==False) 
        msgs = [msg for msg in msgs] 
        return dict({'msgs':msgs})


@post('/admin')
def do_admin():
    cookie = request.get_cookie('admin')
    authenticate_cookie=verify(cookie)
    if cookie == None or authenticate_cookie==False:
        redirect('/login')
    else:
        action = request.forms['action']
        id = request.forms['id']
        if action=='Approve':
            db.execute_sql(f"UPDATE message SET is_approved=1 WHERE id={id};")
        elif action=='Remove':
            db.execute_sql(f"DELETE FROM message WHERE id={id};")
        redirect('/admin')
        
##############################################################################################################################################


##############################################################
### WEB SERVER CONFIGS. & MISC.
##############################################################
db.connect()
db.create_tables([Message,Administrator])

#----- Pre-populate the tables with some data! ----------
if Administrator.select().count() == 0:
    Administrator.create(username='admin',
                        password_hash="SuperSecurePwd")

if Message.select().count() == 0:
    Message.create(name='Prof. Madani',
                   message='Welcome to MITS 5400G Message Board!',
                   is_approved=True)
#-------------------------------------------------------

run(host='localhost',port=8080,reloader=True)
##############################################################
