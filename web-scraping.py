import requests
from bs4 import BeautifulSoup
import os
import zipfile

url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

requisicao = requests.get(url)
html = BeautifulSoup(requisicao.text, 'html.parser')
links = html.find_all('a')

links_pdf = []

for link in links:
    href = link.get('href', '')
    if href.lower().endswith('.pdf'):
        if 'Anexo_I' in href or 'Anexo_II' in href:
            links_pdf.append(href)
            print(f'Link encontrado: {href}')

pasta_download = 'arquivos_ans'
if not os.path.exists(pasta_download):
    os.mkdir(pasta_download)

pdfs_baixados = []

for link_pdf in links_pdf:
    nome_arquivo = os.path.join(pasta_download, link_pdf.split('/')[-1])

    try:
        resposta_pdf = requests.get(link_pdf)

        with open(nome_arquivo, 'wb') as arquivo:
            arquivo.write(resposta_pdf.content)

        pdfs_baixados.append(nome_arquivo)
        print(f'Download concluído: {nome_arquivo}')

    except Exception as erro:
        print(f'Erro ao baixar {link_pdf}: {erro}')

if pdfs_baixados:
    pasta_raiz = os.getcwd()
    caminho_zip = os.path.join(pasta_raiz, 'arquivos_ans.zip')

    with zipfile.ZipFile(caminho_zip, 'w') as arquivo_zip:
        for pdf in pdfs_baixados:
            arquivo_zip.write(pdf, os.path.basename(pdf))

    print(f'Arquivos compactados em {caminho_zip}')

else:
    print('Nenhum PDF encontrado')