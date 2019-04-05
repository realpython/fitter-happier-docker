from flask import Flask
from redis import Redis


app = Flask(__name__)
redis = Redis(host="redis_1", port=6379)


@app.route("/")
def hello():
    redis.incr("views")
    return "Hello! This page has been seen {0} times.".format(int(redis.get("views")))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
