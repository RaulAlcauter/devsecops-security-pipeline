from flask import Flask, request

app = Flask(__name__)



@app.route("/")
def show_message():
    return "<h1>DevSecOps Security Pipeline</h1>"

@app.route("/health")
def show_health():
    return {"status":"ok"}
"""

@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    query = "SELECT * FROM users WHERE id = " + user_id
    return query

"""

if __name__ == "__main__":
    app.run()