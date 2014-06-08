from flask import Flask, render_template
from tools import jsonify, datefromunix
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'monitorlegislativo'
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.jinja_env.filters['datefromunix'] = datefromunix

mongo = PyMongo(app)

@app.route("/")
def index():
    return render_template('front.html')

@app.route('/legis/<tipo>/<numero>/<ano>')
@app.route('/legis/<tipo>/<numero>/<ano>/<json>')
def projeto(tipo, numero, ano, json=False):
	pid = tipo + '-' + numero + '-' + ano
	projeto = mongo.db.legis.find_one({"id": pid})
	if json == 'json':
		return jsonify(projeto)
	elif json == False:
		return render_template('legis.html', p=projeto)

if __name__ == "__main__":
    app.run(debug=True)