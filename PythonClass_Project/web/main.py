from flask import Flask,render_template,url_for
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dash_file.dash_app1 import dash1
from dash_file.dash_app2 import dash2
from dash_file.dash_app3 import dash3

app = Flask(__name__)

application = DispatcherMiddleware(
    app,
    {"/dash/app1": dash1.server,
     "/dash/app2": dash2.server,
     "/dash/app3": dash3.server}
)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)