4from flask import Flask

app = Flask(__name__)

@app.route("/pullrequest1")
def pullrequest1():
	return 'Pull request 1'

@app.route("/pullrequest2")
def pullrequest2():
	return 'Pull request 2'

@app.route("/pullrequest3")
dev pullrequest3():
	return 'Pull request 3'

@app.route("/hello/<name>")
def hello_name(name):
	return f'Hello, {name}!'

@app.route('/')
def hello_world():
	return 'Hello World'

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)


