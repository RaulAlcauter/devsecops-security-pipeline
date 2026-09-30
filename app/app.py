from flask import Flask

app = Flask(__name__)



@app.route("/")
def show_message():
    return "<h1>DevSecOps Security Pipeline</h1>"

@app.route("/health")
def show_health():
    return {"status":"ok"}

if __name__ == "__main__":
    app.run()