from flask import Flask

app = Flask(__name__)


def handle_403(e):
    return 'You shall not pass'


app.register_error_handler(403, handle_403)
