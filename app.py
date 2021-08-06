# Importing required libraries
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os

app = Flask(__name__)
base_dir = os.getcwd()


@app.route("/", methods= ['GET'])
def show():
    return render_template("index.html")

@app.route("/submit", methods=['POST', 'GET'])
def submit():
    """
    To submit user input account urls to database
    :return: renders the index.html with parsed data
    """
    if request.method == "POST":
        username = request.form.get("username")
        repository_name = request.form.get("repository")
        token = request.form.get("token")
        user_data = {
            "username": username,
            "repository_name": repository_name,
            "token": token
        }
        print(user_data)
        request_url = f'git clone https://{username}:{token}@github.com/{username}/{repository_name}.git'
        if not os.path.exists(os.path.join(base_dir + f'/{repository_name}')):
            os.system(f"{request_url}")
            return jsonify({
                "status": 200,
                "message": f"{repository_name} has been cloned!"
            })
        else:
            return jsonify({
                "status": 502,
                "message": f"{repository_name} already there!"
            })
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)