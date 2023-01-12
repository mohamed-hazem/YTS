from flask import Flask, render_template, request
from API.API import main, download_subtitle

import threading, webbrowser, os, signal
# ----------------------------------- #

app = Flask(__name__)

# -- Home Page -- #
@app.route('/')
def home():
    return render_template('index.html')

# -- Search -- #
@app.route('/search', methods=['GET'])
def search():
    if (request.method == "GET"):
        search_key = request.args.get('search_key')

        results = main(search_key)

        return results

# -- Subtitle -- #
@app.route('/subtitle', methods=['GET'])
def subtitle():
    data = dict()
    if (request.method == "GET"):
        imdb_id = request.args.get('imdb_id')
        name = request.args.get('name')
        year = request.args.get('year')

        try:
            data['success'], data['msg'] = download_subtitle(imdb_id, name, year)
        except Exception as e:
            data['success'], data['msg'] = False, str(e)

        return data

# -- Shutdown Server -- #
@app.route('/stop_server', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return
# ========================== #
if (__name__ == '__main__'):
    port = 8000
    url = f"http://127.0.0.1:{port}"

    threading.Timer(1, lambda: webbrowser.open(url)).start()

    app.run(port=port, debug=False)
# ========================== #