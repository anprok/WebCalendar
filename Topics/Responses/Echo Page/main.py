from flask import Flask, make_response

app = Flask('main')

@app.route('/<string:arg>')
def main_view(arg):
    code = 204
    return make_response(arg, code)