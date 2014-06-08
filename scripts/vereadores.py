#!/usr/bin/env python2
# coding: utf-8

"""
Organiza os dados dos veredores da Câmara Municipal de São Paulo, como
publicados em http://www.camara.sp.gov.br/index.php?
option=com_content&view=article&id=10008:detalhes-tramitacao-projetos-dados-abertos&catid=119
"""

from __future__ import print_function

import io
import json
import time
from datetime import datetime
from subfield import expand


def data_br(data):
    '''Intepreta datas no formato brasileiro DD/MM/YYYY'''
    data = data.replace('l', '1').replace('o', '0').replace('O', '0')  # XXX
    return time.mktime(datetime.strptime(data.strip(), '%d/%m/%Y').timetuple())


def data_ano(data):
    '''Isola o ano em datas no formato brasileiro DD/MM/YYYY'''
    return data.split('/').pop()


class Vereador(object):
    def __init__(self, registro, nome, nomes_parlamentares, outros_nomes,
                 liderancas, mesas, eleicoes, vereancas, comissoes):
        self.registro = registro.strip()
        self.nome = nome.strip()

        self.nomes_parlamentares = [
            _ for _ in nomes_parlamentares.split('%') if _.strip()]
        self.nomes_parlamentares.extend(
            [_ for _ in outros_nomes.split('%') if _.strip()])

        self.liderancas = [self.dados_lideranca(_) for _
                           in liderancas.split('%') if _.strip()]

        self.mesas = [self.dados_mesa(_) for _
                      in mesas.split('%') if _.strip()]

        self.eleicoes = [self.dados_eleicao(_) for _
                         in eleicoes.split('%') if _.strip()]

        self.vereancas = [self.dados_vereanca(_) for _
                      in vereancas.split('%') if _.strip()]

        self.comissoes = [self.dados_comissao(_) for _
                         in comissoes.split('%') if _.strip()]

    def pega_dados(self, dados, campos, datas):
        dados = dict(expand(dados))
        dados = {
            nome_campo: dados[chave_campo] if chave_campo in dados else None
            for chave_campo, nome_campo in campos.iteritems()}

        for campo in datas:
            try:
                dados[campo] = data_br(dados[campo])
            except ValueError:
                dados[campo] = data_ano(dados[campo])
            except AttributeError:
                pass

        # Remove campos vazios
        dados.pop('xxx', None)

        if None in dados:
            self.error = True

        return dados

    def dados_lideranca(self, dados):
        campos = {'_': 'partido', 'c': 'cargo', 'f': 'fim', 'i': 'inicio'}
        return self.pega_dados(dados, campos, ['inicio', 'fim'])

    def dados_mesa(self, dados):
        campos = {'_': 'xxx', 'b': 'observacao', 'c': 'cargo',
                  'f': 'fim', 'i': 'inicio'}
        return self.pega_dados(dados, campos, ['inicio', 'fim'])

    def dados_eleicao(self, dados):
        campos = {'_': 'xxx', 'n': 'legislatura',
                  'p': 'xxx', 'q': 'votos', 's': 'situacao'}
        return self.pega_dados(dados, campos, [])

    def dados_vereanca(self, dados):
        campos = {'_': 'xxx', 'b': 'vereador_substituido', 'c': 'ObsPartido',
                  'd': 'ObsVereanca', 'f': 'fim', 'i': 'inicio',
                  'p': 'partido', 's': 'situacao'}
        return self.pega_dados(dados, campos, ['inicio', 'fim'])

    def dados_comissao(self, dados):
        campos = {'_': 'xxx', 'c': 'cargo', 'd': 'observacao',
                  'f': 'fim', 'i': 'inicio', 'n': 'nome'}
        return self.pega_dados(dados, campos, ['inicio', 'fim'])


if '__main__' == __name__:
    with io.open('../raw/vereador.txt', 'r',
                 encoding='iso-8859-1', newline='\r\n') as arquivo_raw:
        vereadores = [Vereador(*dados.split('#'))
                      for dados in arquivo_raw.readlines()
                      if len(dados.split('#')) == 9]

    with open('vereadores.json', 'w') as out:
        json.dump({v.registro: v.__dict__ for v in vereadores}, out, indent=4)
