from flask import Flask, make_response
import datetime

app = Flask('main')


@app.route('/')
def main_view():
    time = datetime.datetime.now()
    year, month, day = time.year, time.month, time.day

    return make_response(f'{year}.{month:02d}.{day:02d}')
