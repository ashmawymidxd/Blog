from flask import Flask,render_template,redirect,Request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# create form class
app.config['SECRET_KEY'] = "my super secret key"

class NamerForm(FlaskForm):
    name = StringField("What's Your Name ",validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/name',methods=['GET','POST'])
def user():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return(render_template('name.html',form=form,name=name))


if __name__ == "__main__":
    app.run(debug=True)