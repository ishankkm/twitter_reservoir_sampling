'''
Created on Aug 24, 2018
@author: ishank
'''

from flask import Flask
from flask import jsonify
from flask import render_template

# create the Flask application
app = Flask(__name__)

app.static_folder = './ui/build/static'
app.template_folder = './ui/build'

# ROUTING:
@app.route("/api", methods=["GET"])
def list_routes():
    result = []
    for rt in app.url_map.iter_rules():
        result.append({
            "methods": list(rt.methods),
            "route": str(rt)
        })
    return jsonify({"routes": result, "total": len(result)})

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)