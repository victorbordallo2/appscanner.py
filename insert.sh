#!/bin/bash

# =========================
#   APPSCANNER INSTALLER
# =========================

VERSION="2.0"

echo "================================="
echo "     APPSCANNER INSTALLER"
echo "================================="
echo "Versão: $VERSION"
echo ""

# Detectar se é Termux
if [ -d "/data/data/com.termux" ]; then
    echo "[+] Ambiente detectado: Termux"
    echo "[+] Atualizando pacotes..."
    pkg update -y

    echo "[+] Instalando dependências..."
    pkg install python git file coreutils -y
else
    echo "[+] Ambiente Linux/PC detectado"
fi

# Verifica Python3
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado!"
    echo "Instale manualmente antes de continuar."
    exit 1
fi

echo "[+] Python3 detectado ✔"

# Dar permissão no main.py
if [ -f "main.py" ]; then
    chmod +x main.py
    echo "[+] Permissão concedida ao main.py"
else
    echo "[ERRO] main.py não encontrado!"
    exit 1
fi

# Criar alias opcional
echo ""
echo "[+] Deseja criar comando global 'appscan'? (s/n)"
read -r resposta

if [ "$resposta" = "s" ]; then
    echo "alias appscan='python3 $(pwd)/main.py'" >> ~/.bashrc
    source ~/.bashrc
    echo "[✔] Comando 'appscan' criado!"
fi

echo ""
echo "================================="
echo "  Instalação finalizada!"
echo "================================="
echo ""
echo "Para usar:"
echo "python3 main.py -f arquivo.apk --pretty"
echo ""
echo "Ou se criou alias:"
echo "appscan -f arquivo.apk --pretty"
