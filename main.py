from flask import Flask, render_template, session
from flask_socketio import SocketIO
import graphing

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def home():
    return render_template("main.html")

@socketio.on("file-upload")
def getFileUpload(data):
    file_data = data["data"]
    session["data"] = file_data
    file_data = graphing.getHeaders(file_data)
    socketio.emit("headers", file_data)

# Receives headers and returns a graph image
@socketio.on("header-selection")
def getHeaders(data):
    graph = graphing.makeGraph(session["data"], data["created"], data["resolved"], data["category"])
    socketio.emit("graph_response", {"image_data": graph})

if __name__ == "__main__":
    app.debug = True
    socketio.run(app)