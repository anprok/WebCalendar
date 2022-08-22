from flask import Flask

app = Flask('main')
app.app_context()


@app.route('/videos/<name>')
def render_videos(name):
    return f'Here will be a video with {name}'
