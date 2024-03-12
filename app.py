from flask import Flask,render_template,redirect,request,flash,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

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
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    data_added = db.Column(db.DateTime,default=datetime.utcnow)
    # create a string 
    def __init__(self,name,email):
        self.name = name
        self.email = email

# Create the database tables
with app.app_context():
    db.create_all()

# create form class
class UserForm(FlaskForm):
    name = StringField("What's Your Name ",validators=[DataRequired()])
    email = StringField("What's Your Email Man",validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/name',methods=['GET','POST'])
def user():
    name = None
    email = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(name=form.name.data).first()
        name = form.name.data
        email = form.email.data
        form.name.data = ''
        form.email.data = ''
        # Add the name to the database
        new_name = Users(name,email)
        db.session.add(new_name)
        db.session.commit()
    # return users list
    users = Users.query.all()
    flash('The Name Added Successfily.')
    return(render_template('name.html',form=form,name=name,email=email,users=users))

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

if __name__ == "__main__":
    app.run(debug=True)