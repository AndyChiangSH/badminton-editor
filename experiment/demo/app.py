import flask


app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/pipeline", methods=['POST'])
def pipeline():
    response = {
        "state": "success",
        "content": "Some quick example text to build on the card title and make up the bulk of the card's content."
    }
    
    return response


if __name__ == '__main__':
    app.run(debug=True)