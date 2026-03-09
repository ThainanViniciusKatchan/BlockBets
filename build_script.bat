@echo off
setlocal

echo [1/3] Limpando build anterior...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [2/3] Gerando executavel com PyInstaller...
echo [Instalando Dependencias]7
python.exe -m pip install --upgrade pip
pip install pyinstaller
pip install pandas openpyxl
pip install Pillow

echo [COMPILANDO PROJETO]
pyinstaller --onefile --clean --icon assets/256x256.ico --name BlockBets ./main.py

if errorlevel 1 (
    echo Erro durante a build com PyInstaller.
    exit /b 1
)

echo [3/3] Copiando ListaBets.csv para a pasta dist...
if not exist dist mkdir dist
if not exist dist\List mkdir dist\List
copy /Y List\ListaBets.csv dist\List\ListaBets.csv

if errorlevel 1 (
    echo Erro ao copiar ListaBets.csv para dist.
    exit /b 1
)

echo Build finalizada com sucesso.
endlocal
pause
exit /b
