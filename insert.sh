#!/bin/bash

# ==============================
#   APP SCANNER - GITHUB VERSION
# ==============================

VERSION="1.0"

show_help() {
    echo "Uso: ./scan_app.sh -f arquivo.apk [-o resultado.json]"
    echo ""
    echo "Opções:"
    echo "  -f  Caminho do arquivo (obrigatório)"
    echo "  -o  Salvar saída em JSON"
    echo "  -h  Mostrar ajuda"
}

while getopts "f:o:h" opt; do
    case $opt in
        f) FILE="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        h) show_help; exit 0 ;;
        *) show_help; exit 1 ;;
    esac
done

if [ -z "$FILE" ]; then
    echo "[ERRO] Tu precisa passar um arquivo com -f"
    show_help
    exit 1
fi

if [ ! -f "$FILE" ]; then
    echo "[ERRO] Arquivo não encontrado!"
    exit 1
fi

echo "[+] Iniciando scan do arquivo: $FILE"

# Informações básicas
SIZE=$(stat -c%s "$FILE" 2>/dev/null || stat -f%z "$FILE")
SHA256=$(sha256sum "$FILE" | awk '{print $1}')
TYPE=$(file -b "$FILE")

# Strings suspeitas
SUSPICIOUS=$(strings "$FILE" | grep -Ei "http|https|token|api|key|password|login" | head -n 20)

# Verifica se é APK/ZIP
if unzip -tq "$FILE" >/dev/null 2>&1; then
    IS_ZIP=true
    STRUCTURE=$(unzip -l "$FILE" | head -n 20)
else
    IS_ZIP=false
    STRUCTURE="Não é APK/ZIP ou não foi possível ler."
fi

# JSON de saída
JSON_OUTPUT=$(cat <<EOF
{
  "file": "$(basename "$FILE")",
  "path": "$(realpath "$FILE" 2>/dev/null || echo "$FILE")",
  "size_bytes": $SIZE,
  "sha256": "$SHA256",
  "file_type": "$TYPE",
  "is_apk_or_zip": $IS_ZIP,
  "scan_version": "$VERSION"
}
EOF
)

echo ""
echo "$JSON_OUTPUT"

# Salvar se tiver opção -o
if [ ! -z "$OUTPUT" ]; then
    echo "$JSON_OUTPUT" > "$OUTPUT"
    echo ""
    echo "[+] Resultado salvo em: $OUTPUT"
fi

echo ""
echo "[✔] Scan finalizado, pai!"
