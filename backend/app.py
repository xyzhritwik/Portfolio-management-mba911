from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from utils.parser import parse_reports
from utils.stats import calculate_portfolio_stats
from utils.ml_model import generate_recommendations

app = Flask(__name__)
CORS(app)

from flask import Flask, request, jsonify, send_from_directory, render_template

@app.route("/")
def serve_react():
    return render_template("index.html")

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


@app.route("/upload", methods=["POST"])
def upload_reports():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    saved_paths = []
    for file in files:
        path = os.path.join("temp", file.filename)
        file.save(path)
        saved_paths.append(path)

    try:
        portfolio_df = parse_reports(saved_paths)
        stats = calculate_portfolio_stats(portfolio_df)
        recommendations = generate_recommendations(portfolio_df)
        return jsonify({"stats": stats, "recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
