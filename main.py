from Core.writeFile import WriteFile
from Core.ModFile import modfile, is_admin, Adm
import Core.VersionControl as VC

if __name__ == '__main__':
    if not is_admin():
        Adm()
    VC.execute()
    WriteFile()
    modfile()
