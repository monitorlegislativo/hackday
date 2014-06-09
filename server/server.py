from flask import Flask, render_template, request, url_for, redirect, abort
from tools import jsonify, diasatras
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'monitorlegislativo'
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.jinja_env.filters['diasatras'] = diasatras

mongo = PyMongo(app)

@app.route("/")
def index():
	return render_template('front.html')

@app.route("/busca")
def busca():
	termo = request.args.get('termo', '')
	try:
		t = termo.split()
		numero = str(int(t[0].strip())).zfill(4) #transforma em int e depois em str de novo com 4 casas
		ano = str(int(t[1].strip()))
		return redirect(url_for("projeto", tipo='pl',numero=numero, ano=ano))
	except:
		return termo #todo


@app.route('/legis/<tipo>/<numero>/<ano>')
@app.route('/legis/<tipo>/<numero>/<ano>/<json>')
def projeto(tipo, numero, ano, json=False):
	pid = tipo + '-' + numero + '-' + ano
	projeto = mongo.db.legis.find_one({"_id": pid})
	if not projeto:
		abort(404)
	if json == 'json':
		return jsonify(projeto)
	elif json == False:
		return render_template('legis.html', p=projeto)

if __name__ == "__main__":
	app.run(debug=True)