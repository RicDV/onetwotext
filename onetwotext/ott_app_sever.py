"""Module that expose onetwotext server application"""

from os.path import *
from pathlib import Path
from flask import *
from flask_session import Session
from waitress import serve
from datetime import datetime, timedelta
from sqlite3 import OperationalError

from onetwotext.db_lib import *
from onetwotext.utils import credential_check
from onetwotext.word_calculator import *

_APP = Flask(__name__)
__WORK_DIR__ = dirname(__file__)


@_APP.route("/", methods=["GET", "POST"])
def index():
    print(
        request.remote_addr,
        " Connected to Server at ",
        datetime.now().strftime("%H:%M:%S on %d %b %Y"),
    )

    return render_template("ott_login.html")


@_APP.route("/access_control", methods=["GET", "POST"])
def access_control():
    """Route to control user credentials"""

    if request.method == "POST":
        username = (request.form["username"]).strip().lower()
        password = request.form["password"]

        try:
            user = get_user_data(username)
        except OperationalError as error:
            print(error)
            print("Try to create ott_users Table...")
            create_db_and_default_user()
            user = get_user_data(username)

        if not user or not credential_check(user, password):
            return render_template(
                "ott_login.html",
                res="Wrong username or password.",
                css="crash",
            )
        else:
            import secrets

            token = secrets.token_hex(6)
            session["my_var"] = token

    try:
        token
    except:
        token = session.get("my_var", None)

    if token is not None:
        return redirect(url_for("onetwotext"))
    else:
        abort(404)


@_APP.route("/onetwotext", methods=["GET", "POST"])
def onetwotext():
    if session.get("my_var", None):
        return render_template("onetwotext.html")
    else:
        abort(404)


@_APP.route("/count-text", methods=["GET", "POST"])
def count_text():
    if session.get("my_var", None):
        text = (request.json.get("text")).lower()
        response = python_count(text)
        return jsonify(response)
    else:
        abort(404)


@_APP.route("/count-from-ai", methods=["GET", "POST"])
def count_from_ai():
    if session.get("my_var", None):
        text = (request.json.get("text")).lower()
        response = nn_completion_count(text)
        return jsonify(response)
    else:
        abort(404)


def start_server(host: str, port: str) -> None:
    """Basic function to start onetwotext app as a server with users credentials
    and session handling

    Input:
    ------
    - host:str
      string variable to set exopsing host for server.
    - port:str
      string variable to set exopsing port for server.
    """

    session_dir = Path(expanduser("~")) / "ott_server_sessions"

    if not session_dir.exists():
        session_dir.mkdir(parents=True)

    _APP.secret_key = "super secret key"
    _APP.config["SESSION_TYPE"] = "filesystem"
    _APP.config["SESSION_FILE_DIR"] = session_dir
    _APP.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)

    sess = Session()
    sess.init_app(_APP)

    serve(_APP, host=host, port=port)
