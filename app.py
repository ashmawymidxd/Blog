from flask import Flask,render_template,redirect,request,flash,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired ,EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.widgets import TextArea

# create a flask instance
app = Flask(__name__)

# create an secret key
app.config['SECRET_KEY'] = "my super secret key"

# create an sqlalchemy instance
# conect with sqlite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# conect with mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/Blog_flask'

# create an model
db = SQLAlchemy(app)
# make user migration
migrate = Migrate(app,db)

# create a model user
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    data_added = db.Column(db.DateTime,default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is no redable')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self) -> str:
        return '<Name %r>'% self.name

    # create a String
    # def __repr__(self) -> str:
    #     return '<name %r>'% self.name
    # create a string 
    def __init__(self,name,email,password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash

# create a posts model
class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(100),nullable=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    slug = db.Column(db.String(100),nullable=False)

    def __repr__(self) -> str:
        return '<Title %r>'% self.title
    
    def __init__(self,title,content):
        self.title = title
        self.content = content

# Create the database tables
with app.app_context():
    db.create_all()

# create form class user
class UserForm(FlaskForm):
    name = StringField("What's Your Name ",validators=[DataRequired()])
    email = StringField("What's Your Email Man",validators=[DataRequired()])
    password_hash = PasswordField("What's Your password",validators=[DataRequired(),EqualTo('password_hash2',message='Password Must Match')])
    password_hash2 = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

# create form class post
class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = StringField("Content",validators=[DataRequired()],widget=TextArea())
    author = StringField("thwe author",validators=[DataRequired()])
    slug = StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return(render_template('index.html'))

# Json data return route
@app.route('/json')
def json():
    return {
        "name":"Rahul",
        "age":23,
        "email":"uyu@gmail.com",
        "date":date.today(),
    }

# create a post route
@app.route('/post',methods=['GET','POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        author = form.author.data
        slug = form.slug.data
        new_post = Posts(title,content,author,slug)
        db.session.add(new_post)
        db.session.commit()
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        flash('The Post Added Successfily.')
    return(render_template('post.html',form=form))

@app.route('/name',methods=['GET','POST'])
def user():
    name = None
    email = None
    password_hash = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data).first()
        name = form.name.data
        email = form.email.data
        password_hash = generate_password_hash(form.password_hash.data)
        new_name = Users(name,email,password_hash)
        db.session.add(new_name)
        db.session.commit()
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        # Add the name to the database
    # return users list
    users = Users.query.all()
    flash('The Name Added Successfily.')
    return(render_template('name.html',form=form,name=name,email=email,users=users))

# @app.route('/name', methods=['GET', 'POST'])
# def user():
#     name = None
#     email = None
#     password_hash = None  # Remove this line, password is hashed later
#     form = UserForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(name=form.name.data).first()
#         name = form.name.data
#         email = form.email.data

#         # Hash the password before creating the user object
#         password_hash = generate_password_hash(form.password_hash.data)

#         new_name = Users(name, email, password_hash)  # Use only 3 arguments here
#         db.session.add(new_name)
#         db.session.commit()
#         form.name.data = ''
#         form.email.data = ''
#         form.password_hash.data = ''
#         form.password_hash2.data = ''  # Clear confirmed password field as well
#         flash('The Name Added Successfully.')
#     return render_template('name.html', form=form, name=name, email=email, users=Users.query.all())

# update user based on id
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    form = UserForm()
    user = Users.query.get_or_404(id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash('The Name Updated Successfily.')
        return redirect(url_for('user'))
    elif request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
    return(render_template('update.html',form=form))

# delete use routes
@app.route('/delete/<int:id>')
def delete(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('The Name Deleted Successfily.')
    return redirect(url_for('user'))

if __name__ == "__main__":
    app.run(debug=True)