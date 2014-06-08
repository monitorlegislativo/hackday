#!/usr/bin/env python2
# coding: utf-8

from lxml.html import parse
from urllib import urlretrieve

if '__main__' == __name__:

    url = ('http://www.camara.sp.gov.br/index.php?option=com_content'
           '&view=article&id=10008:detalhes-tramitacao-projetos-dados-abertos'
           '&catid=119')
    root = parse(url).getroot()

    arquivos_de_dados = root.xpath(
        '//p[contains(., "de arquivos")]/following-sibling::p/a/@href')

    for arquivo in arquivos_de_dados:
        urlretrieve(arquivo, arquivo.split('/').pop())
