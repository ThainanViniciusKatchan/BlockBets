import os

import requests
import pandas as pd
from os import path, remove
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from time import sleep

ua = UserAgent() # UserAgents para evitar bloqueio de acesso

session = requests.Session()

headers = {'User-Agent': ua.random}

session.headers.update(headers)

def Check_folder():
    if path.exists("List"):
        print("[✓] Pasta /List encontrada, continuando...")
    else:
        print("[!] Pasta /List não encontrada, criando pasta...")
        sleep(1)
        os.mkdir("List")
        print("[✓] Pasta /List criada com sucesso")

def Get_local_file_name():
    '''
    Obtém o nome do arquivo csv atualmente baixado e compara com o nome do arquivo
    no site da secretaria de fazenda.
    :return:
    '''

    LocalFileName = str()

    for file in os.listdir("List"):
        if file.endswith(".csv"):
            if "planilha-de-autorizacoes" in file:
                LocalFileName = file[25:33]
                break

    return LocalFileName

def Get_last_update() -> str:
    '''
    Realiza um WebScraping do site da secretaria de Prêmios e Apostas para obter a
    data da última atualização do arquivo CSV.
    :return:
    '''
    URL = "https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/lista-de-empresas"
    Class_search = "documentModified"
    response = session.get(URL, timeout=30)

    soup = BeautifulSoup(response.text, "html.parser")

    result = soup.find("span", class_=Class_search)
    result = result.text.strip().replace('/', '-').split('em')[1]

    return result[:7]

year = str(datetime.now().year)

Get_Update = Get_last_update().strip()
Get_Update = f"{Get_Update}{year[2:]}"

URL = (f"https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/lista-de-empresas"
       f"/planilha-de-autorizacoes-{Get_Update}.csv")
FILENAME = f"planilha-de-autorizacoes-{Get_Update}.csv"

def Downloading_file():
    '''
    Baixa o arquivo CSV diretamente do site da Secretaria de Prêmios e Apostas,
    mantendo a lista sempre atualizada.
    :return:
    '''
    global Get_Update, session, headers, URL, FILENAME, Get_Update
    response = session.get(URL, timeout=30)
    currentFile = Get_local_file_name()

    if response.status_code == 200:
        if path.exists(f"List/{FILENAME}") or currentFile == Get_Update:
            print(f"\n[!] Arquivo já existe ou está na ultima versão disponível: {FILENAME}")
        else:
            with open(f"List/{FILENAME}", "wb") as file:
                if path.exists(f"List/planilha-de-autorizacoes-{currentFile}.csv"):
                    print(f"\n[!] Arquivo antigo encontrado, removendo: {currentFile}")
                    sleep(0.9)
                    remove(f"List/planilha-de-autorizacoes-{currentFile}.csv")
                    print(f"\n[✓] Arquivo antigo removido com sucesso: {currentFile}")

                print(f"\n[►] Baixando o arquivo ou atualizando o arquivo: {FILENAME}")
                sleep(1)
                file.write(response.content)
            print(f"\n[✓] Arquivo baixado com sucesso: {FILENAME}")
    else:
        print(f"\n[!] Falha ao realizar o download, Código do erro: {response.status_code}")

def renamefile():
    '''
    Renomeia o arquivo CSV para ListaBets.csv
    :param FILENAME:
    :return None:
    '''
    global Get_Update, session, headers, URL, FILENAME

    df = pd.read_csv(f"List/{FILENAME}", sep=";", encoding="utf-8", engine="python")
    df_dominios = df[["Unnamed: 5"]]
    df_dominios = df_dominios.dropna()
    df_dominios = df_dominios.drop_duplicates()
    df_dominios = df_dominios.drop([0], axis=0)
    df_dominios = df_dominios.reset_index(drop=True)
    df_dominios.to_csv("List/ListaBets.csv", index=False, header=None)

def execute():
    Check_folder()
    Get_last_update()
    Get_local_file_name()
    Downloading_file()
    # Verifica se o arquivo CSV existe, se existir, remove o arquivo antigo e renomeia o novo
    if path.exists(f"List/{FILENAME}"):
        if path.exists("List/ListaBets.csv"):
            print("\n[X] Removendo a lista antiga...")
            sleep(1)
            remove("List/ListaBets.csv")
            print("\n[✓] Lista antiga removida com sucesso")
            print("[►] Criando nova lista...")
            sleep(2)
            renamefile()
            print(f"[✓] Nova lista criada com sucesso: ListaBets.csv")
        else:
            print("[!] Lista não encontrada, criando lista...")
            print("\n[►] Criando lista...")
            sleep(2)
            renamefile()
            print(f"[✓] Lista criada com sucesso: ListaBets.csv")
    else:
        print("\n[X] Arquivo Não encontrado")

if __name__ == "__main__":
    execute()