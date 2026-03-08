import sys
import ctypes
import os
from pathlib import Path
from time import sleep

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def Adm():
    script_path = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
    sys.exit()

def modfile():
    if not is_admin():
        print("[!] Solicitando privilégios de Administrador...")
        Adm()

    script_dir = Path(__file__).parent.resolve()

    NewFile = script_dir.parent / "hosts"
    hostPath = r"C:\Windows\System32\drivers\etc\hosts"

    if NewFile.exists():
        print(f"[✓] Arquivo {NewFile} encontrado. Prosseguindo...")
    else:
        print(f"[X] Arquivo {NewFile} NÃO encontrado!")
        input("\nPressione Enter para sair...")
        sys.exit()

    try:
        # Tira a trava de leitura do Windows
        if os.path.exists(hostPath):
            os.system(f"attrib -r -s -h {hostPath}")

        # Lê o texto do seu arquivo novo
        with open(NewFile, 'r', encoding='utf-8') as src:
            conteudo = src.read()

        # Escreve o texto direto no hosts do Windows
        with open(hostPath, 'w', encoding='utf-8') as dst:
            print("Bloqueando as BETS...")
            sleep(5)
            dst.write(conteudo)

        print(f"\n[✓] Sucesso! Arquivo Hosts modificado em {hostPath}\n e BETS bloqueadas neste computador!.")

    except PermissionError:
        print("\n[!] Permissão Negada! O seu Antivírus (ex: Windows Defender) está bloqueando a alteração.")
        print("-> Tente desativar a proteção em tempo real rapidamente ou coloque a pasta nas exclusões.")
    except Exception as e:
        print(f"\n[!] Ocorreu um erro: {e}")

    input("\nPressione Enter para sair...")


if __name__ == "__main__":
    modfile()