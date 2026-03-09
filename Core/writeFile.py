import pandas as pd
from pathlib import *
import sys
from shutil import get_terminal_size
from time import sleep

def WriteFile():
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent.resolve()
    else:
        base_dir = Path(__file__).parent.parent.resolve()

    # Força a buscar/salvar os arquivos a partir da pasta real do projeto
    core_dir = Path(__file__).parent.resolve()
    project_dir = core_dir.parent

    csv_path = base_dir / "List" / "ListaBets.csv"
    hosts_path = base_dir / "hosts"

    if not csv_path.exists():
        print(f"[!] Erro: Lista não encontrada em {csv_path}")
        return

    # header=None impede que o primeiro link do CSV seja apagado
    df = pd.read_csv(csv_path, header=None)

    try:
        with open(hosts_path, "w", encoding="utf-8") as f:
            percent = 0
            # Recebe o tamanho do terminal aberto assim a barra de progresso não consome duas linhas
            terminalSize = get_terminal_size(fallback=(80, 24)).columns
            maxProgress = terminalSize - 20

            for i, site in enumerate(df.to_string(index=False, header=False).split('\n')):
                # Calcula a porcentagem de progresso
                percent += ((i + 8) / len(df))
                progess = int((percent / 100) * maxProgress)
                bar = "▀" * progess + " " * (maxProgress - progess)

                '''Adiciona o www. ao site, pois no arquivo .csv que vem do
                site da secretaria de fazendo os sites não tem www. no começo, 
                 além de remover um grande espaço que é adicionado entre o www. e o site'''
                site = "www." + site.strip()

                f.write(f"127.0.0.1 {site}\n")
                print(f"\nAdicionando site: {site}", end="")
                print(f" - Progresso: {percent:.2f}%\n", bar, end="")
                sleep(0.009)

            print()
            print(f"\n[✓] Arquivo hosts gerado com sucesso em {hosts_path}")
            print(f"\nTotal de sites adicionados: {len(df)}")

    except Exception as e:
        print(f"\n[!] Ocorreu um erro: {e}")

if __name__ == "__main__":
    WriteFile()