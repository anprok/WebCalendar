from flask import Flask

app = Flask('main')
app.app_context()

city_dict = {10001: "New York",
             20001: "Washington",
             101000: "Moscow"}


@app.route("/index/<int:code>")
def render_city(code):
    return city_dict.get(code, "There is no city with this index")