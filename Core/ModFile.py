#!/usr/bin/env python3

import sys
import ctypes
import os
from pathlib import Path
from time import sleep
from datetime import datetime
from sys import platform
import subprocess

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def is_sudo():
    return os.getuid() == 0

def Adm():
    if getattr(sys, 'frozen', False):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
    else:
        script_path = os.path.abspath(sys.argv[0])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
    sys.exit()

def sudo():
    if not is_sudo():
        print("[!] Solicitando Privilégio Root")
        comand = [sys.executable] + sys.argv

        try:
            print("[✓] Privilégio Root obtido com sucesso!")
            os.execv("pkexec", ["pkexec"] + comand)
        except Exception as e:
            print(f"[X] Falha ao obter privilégio root: {e}")
            print("[!] Tentando novamente...")
            sleep(2)
            os.execvp("sudo", ["sudo -S"] + comand)
    else:
        print("[✓] Privilégio Root obtido.")

def modfile():
    if platform == "win32":
        if not is_admin():
            print("[!] Solicitando privilégios de Administrador...")
            Adm()
    elif platform == "linux":
        if is_sudo():
            print("[!] Solicitando privilégios de Root...")
            sudo()
    else:
        print("[X] Sistema operacional não suportado!")
        sys.exit()

    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).parent.resolve()
    else:
        base_dir = Path(__file__).parent.parent.resolve()

    if platform == "win32":
        NewFile = base_dir / "hosts"
        hostPath = r"C:\Windows\System32\drivers\etc\hosts"
    elif platform == "linux":
        NewFile = base_dir / "hosts"
        hostPath = "/etc/hosts"
    else:
        print("[X] Sistema operacional não suportado!")
        sys.exit()

    if NewFile.exists():
        print(f"[✓] Arquivo {NewFile} encontrado. Prosseguindo...")
    else:
        print(f"[X] Arquivo {NewFile} NÃO encontrado!")
        input("\nPressione Enter para sair...")
        sys.exit()

    try:
        # Tira a trava de leitura do Windows
        if platform == "win32":
            if os.path.exists(hostPath):
                os.system(f"attrib -r -s -h {hostPath}")
        else:
            pass

        # Lê o texto do arquivo hosts temporário
        with open(NewFile, 'r', encoding='utf-8') as src:
            conteudo = src.read()

        # Escreve o texto direto no hosts do Windows
        with open(hostPath, 'w', encoding='utf-8') as dst:
            print("Bloqueando as BETS...")
            sleep(5)
            if platform == "win32":
                dst.write(f"# Bets Bloqueadas por BlockBets em {datetime.now().strftime('%d-%m-%y %H:%M:%S')}\n")
                dst.write(conteudo)
            elif platform == "linux":
                dst.write(f"""127.0.0.1	localhost
127.0.1.1	thainan-B550M-AORUS-ELITE

# Bets Bloqueadas por BlockBets em {datetime.now().strftime('%d-%m-%y %H:%M:%S')}

{conteudo}

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters""")
            dst.write("\n")

        print(f"\n[✓] Sucesso! Arquivo Hosts modificado em {hostPath}\n e BETS bloqueadas neste computador!.")

    except PermissionError:
        print("\n[!] Permissão Negada! O seu Antivírus (ex: Windows Defender) está bloqueando a alteração.")
        print("-> Tente desativar a proteção em tempo real rapidamente ou coloque a pasta nas exclusões.")
    except Exception as e:
        print(f"\n[!] Ocorreu um erro: {e}")

    input("\nPressione Enter para sair...")


if __name__ == "__main__":
    ...