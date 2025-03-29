import pdfplumber
import pandas as pd
import zipfile	
import os

arquivo_pdf = "arquivos_ans/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
arquivo_csv = "Rol_de_Procedimentos.csv"
arquivo_zip = "Teste_Gabriell_Fernandes_de_Oliveira.zip"

abreviacoes = {
    "OD": "Segmento Odontológico",
    "AMB": "Segmento Ambulatorial"
}

def extrair_dados(caminho_pdf):
    dados = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pag in pdf.pages:
            tabela = pag.extract_table()
            if tabela:
                dados.extend(tabela)
    return dados

dados_extraidos = extrair_dados(arquivo_pdf)

def formatar_tabelas(dados):
    df = pd.DataFrame(dados)
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.dropna(how="all")

    df.replace(abreviacoes, inplace=True)

    return df

tabela_formatada = formatar_tabelas(dados_extraidos)

def salvar_csv(df, arquivo_saida):
    if os.path.exists(arquivo_csv):
        print(f'Arquivo {arquivo_csv} já existe, pulando download')
        return False
    else:
        df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")
        print(f"Arquivos gerados com sucesso: {arquivo_csv}")
        return True

def salvar_zip(arquivo_csv, arquivo_zip, forcar_zip=False):
    if os.path.exists(arquivo_zip) and not forcar_zip:
        print(f'O arquivo {arquivo_zip} já existe, pulando a compactação.')
    else:
        with zipfile.ZipFile(arquivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(arquivo_csv)
            print(f"Arquivo compactado com sucesso: {arquivo_zip}")


csv_foi_criado = salvar_csv(tabela_formatada, arquivo_csv)
salvar_zip(arquivo_csv, arquivo_zip, forcar_zip=csv_foi_criado)

