from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', methods=["post", "get"])

@app.route('/GetTopicsForProfiles', methods=["post", "get"]):


@app.route('/GetTopicsForProfileFollowers', methods=["post", "get"]):


@app.route('/GetProfilesForTopic', methods=["post", "get"]):


@app.route('/GetTweetMetricsForTopic', methods=["post", "get"]):


@app.route("/Error", methods=["get"])