@echo off
setlocal

echo [1/3] Limpando build anterior...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist/Win

echo [2/2] Gerando executavel com PyInstaller...
echo [Instalando Dependencias]
python.exe -m pip install --upgrade pip
pip install pyinstaller
pip install pandas openpyxl
pip install Pillow

echo [COMPILANDO PROJETO]
pyinstaller --onefile --clean --icon assets/256x256.ico --distpath ./dist/Win  --name BlockBets ./main.py

if errorlevel 1 (
    echo Erro durante a build com PyInstaller.
    exit /b 1
)

echo Build finalizada com sucesso.
endlocal
exit /b