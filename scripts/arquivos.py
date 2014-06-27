#!/usr/bin/env python2
# coding: utf-8

'''
Baixa todos os arquivos de dados de tramitação de projetos da
Câmara Municipal de São Paulo.
'''

import os
from lxml.html import parse
from urllib import urlretrieve
from configura import RAW_PATH
from util import mkdir_p

if '__main__' == __name__:

    url = ('http://www.camara.sp.gov.br/index.php?option=com_content'
           '&view=article&id=10008:detalhes-tramitacao-projetos-dados-abertos'
           '&catid=119')
    root = parse(url).getroot()

    arquivos_de_dados = root.xpath(
        '//p[contains(., "de arquivos")]/following-sibling::p/a/@href')

    for arquivo in arquivos_de_dados:
        path = os.path.join(RAW_PATH, 'tramitacoes')
        mkdir_p(path)
        urlretrieve(arquivo, os.path.join(path, arquivo.split('/').pop()))
