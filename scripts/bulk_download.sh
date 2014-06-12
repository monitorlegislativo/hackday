#!/bin/bash

# Cria dirs!
mkdir -p ../raw
mkdir -p ../raw/legis
mkdir -p ../raw/vereador
mkdir -p ../raw/rh
mkdir -p ../data

# Produção Legislativa
cd ../raw
cd legis
encerra.txtprojetos/
wget -N http://www2.camara.sp.gov.br/projetos/catalogo_assuntos.xml
wget -N http://www2.camara.sp.gov.br/projetos/tipo_materia_legislativa.xml
wget -N http://www2.camara.sp.gov.br/projetos/unidades.xml

wget -N http://www2.camara.sp.gov.br/Dados_abertos/LEIA-ME.TXT
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/assunto.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/autor.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/comdes.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/delibera.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/encami.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/encerra.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/tramita.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/prolege.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/prolegm.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/prolegpa.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/prolegs.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/prolegt.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/prolegp.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/projetos.txt
wget -N http://www2.camara.sp.gov.br/Dados_abertos/projetos/relatores.csv

cd ..

# Vereadores
cd vereador
wget -N http://www2.camara.sp.gov.br/Dados_abertos/vereador/vereador.txt

# Ocupação dos Gabinetes pelos Vereadores
wget -N http://www2.camara.sp.gov.br/Dados_abertos/vereador/SSP_HISTORICO_VEREADORES.csv
cd ..

#Updated
date > UPDATED.md
