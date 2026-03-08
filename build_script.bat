@echo off
setlocal

echo [1/3] Limpando build anterior...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [2/3] Gerando executavel com PyInstaller...
echo [Instalando Dependencias]
pip install pyinstaller
pip install pandas openpyxl
pyinstaller --onefile ./main.py

if errorlevel 1 (
    echo Erro durante a build com PyInstaller.
    exit /b 1
)

echo [3/3] Copiando ListaBets.csv para a pasta dist...
if not exist dist mkdir dist
copy /Y List\ListaBets.csv dist\ListaBets.csv

if errorlevel 1 (
    echo Erro ao copiar ListaBets.csv para dist.
    exit /b 1
)

echo Build finalizada com sucesso.
endlocal
pause
