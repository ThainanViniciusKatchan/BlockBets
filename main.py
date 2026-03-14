from Core.writeFile import WriteFile
from Core.ModFile import modfile, is_admin, is_sudo ,Adm, sudo
import Core.VersionControl as VC
from sys import platform

if __name__ == '__main__':
    if platform == "win32":
        if not is_admin():
            Adm()
    if platform == "linux":
        if not is_sudo():
            sudo()
    VC.execute()
    WriteFile()
    modfile()
