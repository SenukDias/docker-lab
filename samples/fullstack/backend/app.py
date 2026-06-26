from flask import Flask, jsonify
import redis, os
app = Flask(__name__)
r = redis.Redis.from_url(os.environ.get("REDIS_URL","redis://redis:6379"), decode_responses=True)

@app.route("/")
def index():
    visits = r.incr("visits")
    return jsonify({"message":"Fullstack Docker App 🐳","visits":visits})

@app.route("/health")
def health():
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
