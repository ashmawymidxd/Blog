from flask import Flask,render_template,redirect,Request

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('index.html'))

@app.route('/user/<name>')
def user(name):
    return "<h1>hello {}</h1>".format(name)


if __name__ == "__main__":
    app.run(debug=True)