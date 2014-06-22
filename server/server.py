from flask import Flask, render_template, request, url_for, redirect, abort
from tools import jsonify, diasatras, futuro
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'monitorlegislativo'
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.jinja_env.filters['diasatras'] = diasatras

mongo = PyMongo(app)


@app.route("/")
def index():
	return render_template('front.html')

@app.route("/busca/<termo>")
@app.route("/busca/<termo>/<int:pagina>")
def busca(termo, pagina=0):
	perpage = 15
	try:
		t = termo.split()
		tipo = 'pl'
		numero = str(int(t[0].strip())).zfill(4) #transforma em int e depois em str de novo com 4 casas
		ano = str(int(t[1].strip()))
		pid = tipo.lower() + '-' + numero + '-' + ano
		projeto = mongo.db.legis.find_one({"_id": pid})
		if projeto:
			return redirect(url_for("projeto", tipo='pl',numero=numero, ano=ano))
		else:
			abort(404)
	except:
		query = { "$text" : { "$search" : termo }}
				
		projetos = mongo.db.legis.find(query)
		misc = { "size" : projetos.count(),
				 "perpagina" : perpage,
				 "pagina" : pagina }
		return render_template("busca.html", projetos=projetos.skip(pagina*perpage).limit(perpage), misc=misc, termo=termo) #todo

@app.route('/vereador/<nome>')
@app.route('/vereador/<nome>/<json>')
def _vereador(nome, json=False):
	vereador = mongo.db.vereadores.find_one({"nomes_parlamentares" : nome})
	if not (vereador):
		abort(404)
	
	vereador['assuntos'] = []
	if not json:
		return render_template('vereador.html', v=vereador)
	elif json == 'json':
		return jsonify(v)



@app.route('/legis/<tipo>/<numero>/<ano>')
@app.route('/legis/<tipo>/<numero>/<ano>/<json>')
def _projeto(tipo, numero, ano, json=False):
	pid = tipo.lower() + '-' + numero + '-' + ano
	projeto = mongo.db.legis.find_one({"_id": pid})
	explicacoes = mongo.db.explicacoes.find()
	
	# Monta tramitacao
	for p in projeto['tramitacoes']:
		if p['data_inicio'] == '':
			p['data_inicio'] = futuro()
		p['tipo'] = 'tramita'

	if projeto.has_key('encerramento'):
		projeto['tramitacoes'].append({
				'data_inicio' : projeto['data_encerramento'], #pensar
				'tramitacao' : projeto['encerramento'],
				'tipo' : 'encerramento'
			})
		for p in projeto['tramitacoes']:
			if p['data_inicio'] > projeto['data_encerramento'] and p['tipo'] == 'tramita':
				p['tipo'] = 'arquivo'
	
	for c in projeto['comissoes']:
		if not any(p['tramitacao'] == c for p in projeto['tramitacoes']) and not projeto.has_key('encerramento'): #adicionar tramitacao conjunta
			projeto['tramitacoes'].append({
				'tipo' : 'comdes',
				'tramitacao' : c,
				'data_inicio' : futuro()
				})

	if not projeto:
		abort(404)
	if json == 'json':
		return jsonify(projeto)
	elif json == False:
		return render_template('legis.html', p=projeto, explicacoes=explicacoes)

if __name__ == "__main__":
	app.run(debug=True)