from flask import Flask, render_template, session
from flask_socketio import SocketIO
import graphing

app = Flask(__name__)
socketio = SocketIO(app)


# Serves up the home page
@app.route("/")
def home():
    return render_template("main.html")

# Handles the excel file upload
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

# RUN IT BABYYYYY
if __name__ == "__main__":
    socketio.run(app)
