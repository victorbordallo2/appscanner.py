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
                results.append(m.decode(errors="ignore"))
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

    result = {
        "file_name": os.path.basename(filepath),
        "full_path": os.path.abspath(filepath),
        "size_bytes": os.path.getsize(filepath),
        "sha256": calculate_sha256(filepath),
        "is_apk_or_zip": zipfile.is_zipfile(filepath),
        "structure_preview": analyze_structure(filepath),
        "suspicious_strings": [],
        "scan_time": datetime.utcnow().isoformat() + "Z"
    }

    strings = extract_strings(filepath)
    result["suspicious_strings"] = find_suspicious(strings)[:30]

    return result

def main():
    parser = argparse.ArgumentParser(
        description="AppScanner - Scan de APK e arquivos"
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Caminho do arquivo para escanear"
    )
    parser.add_argument(
        "-o", "--output",
        help="Salvar resultado em JSON"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="JSON formatado"
    )

    args = parser.parse_args()

    try:
        data = scan_file(args.file)

        if args.pretty:
            output = json.dumps(data, indent=4, ensure_ascii=False)
        else:
            output = json.dumps(data, ensure_ascii=False)

        print(output)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=4))

if __name__ == "__main__":
    main()
