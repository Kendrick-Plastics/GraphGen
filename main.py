from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("main.html")

@socketio.on("message")
def gen_image(message):
    print("Received", message)
    socketio.emit("response", message)


if __name__ == "__main__":
    app.debug = True
    socketio.run(app)