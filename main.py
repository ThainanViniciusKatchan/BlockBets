from Core.writeFile import WriteFile
from Core.ModFile import modfile, is_admin, Adm

if __name__ == '__main__':
    if not is_admin():
        Adm()
    WriteFile()
    modfile()
