import json
import time
import random
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, render_template, redirect, url_for
from recent_tweets_predict import predict_negaposi, get_latest_data, get_user_data, get_24hours_from, get_7days_from

app = Flask(__name__)
app.config.from_object(__name__)

#---------------------------------------------------------------
# index page
#---------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

#---------------------------------------------------------------
# update negaposi on index.html
#---------------------------------------------------------------
@app.route('/negaposi')
def negaposi():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            time.sleep(1)
            message = ws.receive()
            if message is None:
                break
            data_time, pos, neg = get_latest_data()
            data = {
                "time": data_time,
                "pos" : pos,
                "neg" : neg
            }
            ws.send(json.dumps(data))
    return

#---------------------------------------------------------------
# tree page
#---------------------------------------------------------------
@app.route('/tree', methods = ['POST'])
def tree():
    try:
        user_name = request.form.get('user_name')
    except:
        return render_template('index.html')
    if len(user_name)==0:
        return render_template('index.html')
    if user_name[0] != '@':
        user_name = '@' + user_name
    return render_template('tree.html', user_name=user_name)

@app.route('/tree')
def tree_to_index():
    return redirect(url_for('index'))


#---------------------------------------------------------------
# for line chart
#---------------------------------------------------------------
@app.route('/chart')
def chart():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            time.sleep(1)
            message = ws.receive()
            if message is None:
                break
            ws.send(get_24hours_from(message))
    return

@app.route('/chart_week')
def chart_week():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            time.sleep(1)
            message = ws.receive()
            if message is None:
                break
            ws.send(get_7days_from(message))
    return

#---------------------------------------------------------------
# show user negaposi data
#---------------------------------------------------------------
@app.route('/tree_negaposi')
def tree_negaposi():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            time.sleep(1)
            user_name = ws.receive()
            if user_name is None:
                break
            pos, neg = get_user_data(user_name)
            data = {
                "pos" : pos,
                "neg" : neg
            }
            ws.send(json.dumps(data))
    return

#---------------------------------------------------------------
# user not found
#---------------------------------------------------------------
@app.route('/user_not_found')
def user_not_found():
    return render_template('user_not_found.html')

#---------------------------------------------------------------
# main function
#---------------------------------------------------------------
if __name__ == '__main__':
    app.debug = True
    host = 'localhost'
    port = 8080
    host_port = (host, port)
    server = WSGIServer(host_port,
                        app,
                        handler_class=WebSocketHandler
    )
    server.serve_forever()