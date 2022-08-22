from flask import Flask, abort

app = Flask(__name__)


@app.route("/capital/<country>")
def capital(country):

    capitals_dictionary = {
        "Russia": "Moscow",
        "Ukraine": "Kiev",
        "USA": "Washington",
    }
    code = 404
    if country not in capitals_dictionary.keys():
        return abort(code, "Resource not found")
    return capitals_dictionary[country]

