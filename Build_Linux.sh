#!/bin/bash

echo [1/3] Limpando build anterior...
if [ -d "build" ]; then
  sudo rm -rf "build"
fi

if [ -d "dist" ]; then
  sudo rm -rf "dist/BlockBetsLinux"
fi

echo [2/2] Gerando executavel com PyInstaller...
echo [Instalando Dependencias]

python.exe -m pip install --upgrade pip
pip install pyinstaller
pip install pandas openpyxl
pip install Pillow
echo [COMPILANDO PROJETO]
pyinstaller --onefile --clean --icon assets/256x256.ico --distpath ./dist/BlockBetsLinux --name BlockBets ./main.py
echo Criando Script de execução

cat <<EOF > ./dist/BlockBetsLinux/StartBlockBet.sh
#!/bin/bash
# Pede permissão de administrador (root) e executa o binário do BlockBets
sudo ./BlockBets
echo ""
read -p "Pressione Enter para sair..."
EOF

echo Tornando o script executável
chmod +x ./dist/BlockBetsLinux/StartBlockBet.sh
echo Tudo Pronto!

if [ $? -eq 0 ]; then
    echo "Build finalizada com sucesso."
else
    echo "Erro ao compilar"
    exit 1
fi