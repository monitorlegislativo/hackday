from flask import Flask
from tools import jsonify
from flask.ext.pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'monitorlegislativo'
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"

mongo = PyMongo(app)

@app.route("/")
def index():
    return "Hello World!"


@app.route('/legis/<tipo>/<numero>/<ano>')
def projeto(tipo, numero, ano):
	pid = tipo + '-' + numero + '-' + ano
	projeto = mongo.db.legis.find_one({"id": pid})
	return jsonify(projeto)

if __name__ == "__main__":
    app.run(debug=True)