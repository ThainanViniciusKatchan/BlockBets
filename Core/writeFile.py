import pandas as pd
from pathlib import Path

def WriteFile():
    # Força a buscar/salvar os arquivos a partir da pasta real do projeto
    core_dir = Path(__file__).parent.resolve()
    project_dir = core_dir.parent

    csv_path = project_dir / "List" / "ListaBets.csv"
    hosts_path = project_dir / "hosts"

    if not csv_path.exists():
        print(f"[!] Erro: Lista não encontrada em {csv_path}")
        return

    # header=None impede que o primeiro link do CSV seja apagado
    df = pd.read_csv(csv_path, header=None)

    with open(hosts_path, "w", encoding="utf-8") as f:
        lines = 0
        percent = 0
        for site in df.to_string(index=False, header=False).split('\n'):
            lines += 1
            percent += 100 / len(df)
            site = "www." + site.strip()
            f.write(f"127.0.0.1 {site}\n")
            print(f"\nAdicionando site: {site}", end="")
            print(f"Progresso: {percent:.2f}%\n","▀"*lines, end="")
    print(f"\n[✓] Arquivo hosts gerado com sucesso em {hosts_path}")
    print(f"\nTotal de sites adicionados: {lines-1}")

if __name__ == "__main__":
    WriteFile()