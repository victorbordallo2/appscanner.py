#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
import zipfile
import re
import argparse
import json
from datetime import datetime

SUSPICIOUS_KEYWORDS = [
    "http", "https", "token", "api", "key",
    "password", "login", "auth", "secret"
]

def calculate_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def extract_strings(filepath, limit=100):
    results = []
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            matches = re.findall(rb"[ -~]{6,}", data)
            for m in matches[:limit]:
                try:
                    results.append(m.decode(errors="ignore"))
                except:
                    pass
    except Exception as e:
        results.append(f"Erro ao extrair strings: {e}")
    return results

def find_suspicious(strings):
    found = []
    for s in strings:
        if any(k in s.lower() for k in SUSPICIOUS_KEYWORDS):
            found.append(s)
    return found

def analyze_structure(filepath):
    structure = []
    if zipfile.is_zipfile(filepath):
        try:
            with zipfile.ZipFile(filepath, "r") as z:
                structure = z.namelist()[:50]
        except Exception as e:
            structure.append(f"Erro ao ler estrutura: {e}")
    return structure

def scan_file(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError("Arquivo não encontrado")

    file_size = os.path.getsize(filepath)
    sha256 = calculate_sha256(filepath)
    strings = extract_strings(filepath)
    suspicious = find_suspicious(strings)
    structure = analyze_structure(filepath)

    result = {
        "file": os.path.basename(filepath),
        "path": os.path.abspath(filepath),
        "size_bytes": file_size,
        "sha256": sha256,
        "is_apk_or_zip": zipfile.is_zipfile(filepath),
        "suspicious_strings": suspicious[:30],
        "structure_preview": structure,
        "scan_time": datetime.utcnow().isoformat() + "Z"
    }

    return result

def main():
    parser = argparse.ArgumentParser(
        description="App Scanner - Scan de APK e arquivos suspeitos"
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Caminho do arquivo (APK ou app)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Salvar resultado em JSON (ex: resultado.json)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Saída JSON formatada"
    )

    args = parser.parse_args()

    try:
        result = scan_file(args.file)

        if args.pretty:
            output_data = json.dumps(result, indent=4, ensure_ascii=False)
        else:
            output_data = json.dumps(result, ensure_ascii=False)

        print(output_data)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_data)

    except Exception as e:
        error = {"error": str(e)}
        print(json.dumps(error, indent=4))
        exit(1)

if __name__ == "__main__":
    main()
