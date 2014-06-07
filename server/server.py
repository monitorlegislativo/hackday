from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"


@app.route('/legis/<tipo>/<numero>/<ano>')
def projeto(tipo, numero, ano):
	pid = tipo + '-' + numero + '-' + ano
	return pid

if __name__ == "__main__":
    app.run(debug=True)