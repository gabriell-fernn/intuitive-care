import requests
from bs4 import BeautifulSoup
import os
import zipfile

url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

requisicao = requests.get(url, timeout=10)
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
os.makedirs(pasta_download, exist_ok=True)

pdfs_baixados = []

for link_pdf in links_pdf:
    nome_arquivo = os.path.join(pasta_download, os.path.basename(link_pdf))

    if os.path.exists(nome_arquivo):
        print(f'Arquivo já existe, pulando download: {nome_arquivo}')
        pdfs_baixados.append(nome_arquivo)
        continue

    try:
        resposta_pdf = requests.get(link_pdf, timeout=10, stream=True)

        if resposta_pdf.status_code == 200:
            with open(nome_arquivo, 'wb') as arquivo:
                arquivo.write(resposta_pdf.content)

            pdfs_baixados.append(nome_arquivo)
            print(f'Download concluído: {nome_arquivo}')
        
        else: 
            print(f'Erro ao baixar {link_pdf}: Código {resposta_pdf.status_code}')

    except Exception as erro:
        print(f'Erro ao baixar {link_pdf}: {erro}')

if pdfs_baixados:
    caminho_zip = os.path.join(os.getcwd(), 'arquivos_ans.zip')

    with zipfile.ZipFile(caminho_zip, 'w') as arquivo_zip:
        for pdf in pdfs_baixados:
            arquivo_zip.write(pdf, os.path.basename(pdf))

    print(f'Arquivos compactados em {caminho_zip}')

else:
    print('Nenhum PDF encontrado')