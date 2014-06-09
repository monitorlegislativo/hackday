import codecs

DATA = '../data/'
arquivo = codecs.open(DATA+'explicacoes.csv', encoding='utf-8')

explicacoes = []
for linha in arquivo.readlines()[1:]:
	linha = linha.split(',')
	explicacao = {
		'_id' : linha[0],
		'sigla' : linha[0],
		'nome' : linha[1],
		'descricao' : linha[2].strip()
	}
	explicacoes.append(explicacao)

def mongo_save(explicacoes, clear=False):
    from pymongo import MongoClient
    client = MongoClient()
    db = client.monitorlegislativo
    collection = db.explicacoes
    if (clear):
        collection.drop()
    for e in explicacoes:
        collection.update({'_id' : e['_id']}, e, upsert=True)

mongo_save(explicacoes)