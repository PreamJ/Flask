from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os
import ggsheet

information = ggsheet.main()

app = Flask(__name__)
app.secret_key = os.urandom(12)

oauth = OAuth(app)

def renderPage(path):
    pageHTML = render_template("tmpl-head.html")
    pageHTML += render_template(path)
    pageHTML += render_template("tmpl-foot.html")
    return pageHTML

@app.route("/")
def index():
    return renderPage("index.html")

@app.route("/static/styles.css")
def styles():
    return render_template("static/styles.css")

@app.route("/google/")
def google():

    GOOGLE_CLIENT_ID = "client_id"
    GOOGLE_CLIENT_SECRET = "client_secret"
    CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
    oauth.register(
        name="google",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            "scope": "openid email profile"
        }
    )

    redirect_uri = url_for("google_auth", _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route("/google/auth/")
def google_auth():
    token = oauth.google.authorize_access_token()
    authuser = token["userinfo"]
    distinguished_name = authuser["given_name"]
    print(distinguished_name)
    for row in information:
        if(row[0] == distinguished_name):
            link = "https://docs.google.com/forms/d/e/" + (row[1]) + "/viewform?authuser=" + authuser["email"]
    return redirect(link)