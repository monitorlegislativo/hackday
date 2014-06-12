#!/usr/bin/env python2
# coding: utf-8

"""
Agrega informações da tramitação de processos legislativos da Câmara
Municipal de São Paulo, como publicados em http://www.camara.sp.gov.br/
index.php?option=com_content&view=article&id=10008:detalhes-tramitacao-projetos-dados-abertos&catid=119
"""

from __future__ import print_function

import io
import json
import time
import re
from datetime import datetime

RAW = '../raw/legis/'
FINAL = '../data/'

def data_br(data):
    '''Intepreta datas no formato brasileiro DD/MM/YYYY'''
    data = data.replace('l', '1').replace('o', '0').replace('O', '0')  # XXX
    try:
        return time.mktime(
            datetime.strptime(data.strip(), '%d/%m/%Y').timetuple())
    except ValueError:
        return data.split('/').pop()


def identificador(dados):
    '''Gera identificadores a partir dos primeiros campos na tabela'''
    dados = dados.split('#')
    tipo = dados[0].strip().lower()
    numero = dados[1].strip().zfill(4)
    data = dados[2].strip().split('/').pop().split('-').pop()
    return "{tipo}-{numero}-{data}".format(tipo=tipo, numero=numero, data=data)


def identificador_relator(dados):
    '''Gera identificador para os dados do arquivo de relatores'''
    dados = dados.split(';')
    tipo = dados[2].strip().lower()
    numero = dados[3].strip().zfill(4)
    data = dados[4].strip()
    return "{tipo}-{numero}-{data}".format(tipo=tipo, numero=numero, data=data)


def processa_arquivo(arquivo, callback):
    
    with io.open(arquivo, 'r',
                 encoding='iso-8859-1', newline='\r\n') as arquivo_raw:
        for dados in arquivo_raw.readlines()[2:]:
            if dados.strip():
                try:
                    if arquivo.split('/').pop() == 'relatores.csv':
                        getattr(projetos[identificador_relator(dados)], callback)(dados)
                    else:
                        getattr(projetos[identificador(dados)], callback)(dados)
                except KeyError:
                    print('Erro in processa_arquivo!' ,dados)


class PL(object):
    '''Projeto de Lei da Camara Municipal de São Paulo'''

    url_base = 'http://camaramunicipalsp.qaplaweb.com.br/iah/fulltext/projeto/'

    def __init__(self, dados):
        tipo, numero, data, ementa, \
            tipo_norma, numero_norma, data_norma = dados.split('#')
        self.norma = {'tipo': tipo_norma.strip(),
                      'numero': numero_norma.strip(),
                      'data': data_norma.strip()}
        self.tipo = tipo.lower()
        self.numero = numero.zfill(4)
        self.ementa = ementa.strip()
        self.data_apresentacao = data_br(data)
        self.error = False
        self.tramitacoes = []
        self.comissoes = []
        self.relatores = []
        self.pareceres = []
        self.deliberacoes = []
        self.assuntos = []
        self.autores = [] # Talvez seja o caso de ja normalizar e achar um id unico aqui

        try:
            data = datetime.fromtimestamp(
                self.data_apresentacao).strftime('%Y')

        except TypeError:
            data = self.data_apresentacao  # data_br has returned a string
            self.error = True

        self._id = "{tipo}-{numero}-{data}".format(
            tipo=self.tipo, numero=self.numero, data=data)
        self.ano = data

    def dados_encerramentos(self, dados):
        '''Agrega os dados dos encerramentos'''
        __, __, __, data, status = dados.split('#')
        self.data_encerramento = data_br(data)
        self.encerramento = status.strip()

    def dados_arquivos_brutos(self, dados):
        '''Agrega os dados dos arquivos brutos'''
        __, __, __, nome_de_arquivo = dados.split('#')
        nome, extensao = nome_de_arquivo.split('.')
        self.url_pdf = self.url_base + "{nome}.{ext}".format(
            nome=nome.upper(), ext=extensao)
        self.url_pdf = self.url_pdf.strip()

    def dados_tramitacoes(self, dados):
        '''Agrega os dados das tramitações'''
        __, __, __, tramitacao, inicio, fim = dados.split('#')
        self.tramitacoes.append({
            'tramitacao': tramitacao.strip().upper(),
            'data_inicio': data_br(inicio.strip()),
            'data_fim': data_br(fim.strip())
        })

    def dados_comissoes(self, dados):
        '''Agrega os dados das comissões designadas'''
        __, __, __, comissao = dados.split('#')
        self.comissoes.append(comissao.split('-')[1].strip())

    def dados_assuntos(self, dados):
        '''Agrega os dados dos assuntos legislativos'''
        __, __, __, assunto = dados.split('#')
        self.assuntos.append(assunto.strip())

    def dados_autores(self, dados):
        '''Agrega os dados dos assuntos legislativos'''
        __, __, __, autor = dados.split('#')
        self.autores.append(autor.strip())

    def dados_relatores(self,dados):
        '''Agrega os dados dos relatores'''
        try:
            linha = dados.split(';')
            if len(linha) == 13:
                comissao = linha[5].strip().lower()
                vereador = linha[7].strip().lower()
                relator = {'comisso':comissao, 'vereador':vereador}
                self.relatores.append(relator)
            else:
                print ('linha bizarrra (relatores.csv) = ', linha)
            
        except KeyError:
            print('Erro in dados_relatores! ', dados)

    def dados_pareceres(self, dados):
        '''Agrega os dados dos pareceres'''
        try:
            linha = dados.split('#')
            arquivo = linha[3].strip().upper()
            linha = arquivo.split('-')

            p = re.compile('(JUST|URB|FIN|EDUC|ECON|SAUDE|ADM|CONJ|CULT|ABAST|SERV|TRANS)([A-Z]*)([0-9]*)')
            m = p.match(linha[0])
            comissao = m.group(1)
            complemento = m.group(2)
            numero = m.group(3)

            # Alguns projetos possuem mais de uma versão do parecer na mesma Comissão. Ex: CONJPL0127-1992-2
            if len(linha) == 2:
                ano = linha[1].replace('.PDF','')
                versao = '1'
            if len(linha) == 3:
                ano = linha[1]
                versao = linha[2].replace('.PDF','')

            parecer = {'arquivo': arquivo, 'comissao': comissao, 'complemento': complemento, 'numero': numero, 'ano': ano, 'versao': versao}

            self.pareceres.append(parecer)

        except:
            print('Erro in dados_pareceres! ', dados)


    def dados_deliberacoes(self, dados):
        '''Agrega os dados das deliberacoes'''
        try:
            __, __, __, linha = dados.split('#')

            dados = linha.split('-')

            delibera = dados[0].strip()
            tam = len(dados)

            linha = dados[tam-1].strip()
            tam2 = len(linha)

            data = linha[tam2-11:].replace('.','')

            deliberacao = {'delibera':delibera, 'data': data_br(data)}

            self.deliberacoes.append(deliberacao)

        except:
            print('Erro in dados_deliberacoes! ', dados)



def local_save(projetos):
    with open(FINAL+'legis.json', 'w') as output:
        json.dump(
            [projeto.__dict__ for projeto in projetos.values()],
            output, indent=4)


def mongo_save(projetos, clear=False):
    from pymongo import MongoClient
    client = MongoClient()
    db = client.monitorlegislativo
    legis = db.legis
    if (clear):
        legis.drop()
    for p in projetos:
        legis.update({'_id' : projetos[p]._id}, projetos[p].__dict__, upsert=True)

if '__main__' == __name__:
    print('Processando projetos.')
    with io.open(RAW+'projetos.txt', 'r',
                 encoding='iso-8859-1', newline='\r\n') as projetos_raw:
        projetos = {pl._id: pl for pl in
                    (PL(dados) for dados in projetos_raw.readlines()[2:]
                     if dados.strip())
                    if pl._id is not None}

    print('Processando encerramentos.')
    processa_arquivo(RAW+'encerra.txt', 'dados_encerramentos')

    print('Processando arquivos brutos.')
    processa_arquivo(RAW+'prolegt.txt', 'dados_arquivos_brutos')

    print('Processando tramitações.')
    processa_arquivo(RAW+'tramita.txt', 'dados_tramitacoes')

    print('Processando comissões.')
    processa_arquivo(RAW+'comdes.txt', 'dados_comissoes')

    print('Processando relatores.')
    processa_arquivo(RAW+'relatores.csv', 'dados_relatores')

    print('Processando pareceres.')
    processa_arquivo(RAW+'prolegpa.txt', 'dados_pareceres')

    print('Processando deliberações.')
    processa_arquivo(RAW+'delibera.txt', 'dados_deliberacoes')

    print('Processando assuntos.')
    processa_arquivo(RAW+'assunto.txt', 'dados_assuntos')

    print('Processando autores.')
    processa_arquivo(RAW+'autor.txt', 'dados_autores')

    #mongo_save(projetos)
    local_save(projetos)
