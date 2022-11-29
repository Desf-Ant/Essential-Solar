from flask import Flask
from flask import render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("pages/index.html")


@app.route("/form")
def form():
    return render_template("pages/form.html")







@app.route("/hello/")
@app.route("/hello/<name>")
def hello_world(name=None):
    #return f"<p>Hello {escape(name)}</p>"
    return render_template("test_pages/hello.html",name=name)


if __name__ == "__main__" :
    app.run(debug=True, host='0.0.0.0', port=5000)