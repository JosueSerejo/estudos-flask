from flask import Flask, request, render_template
from markupsafe import escape


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lista')
def sobre():
    return render_template('lista.html')

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)