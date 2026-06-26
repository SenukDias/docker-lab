from flask import Flask, jsonify
import os, platform

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Multi-stage build sample 🏗️",
        "image_size": "~145MB (vs ~1.1GB single-stage)",
        "host": platform.node()
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
