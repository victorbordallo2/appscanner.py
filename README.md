# 🔍 App Scanner (APK & Files)

## 📱 Sobre o projeto

O App Scanner é uma ferramenta simples em Python e Bash que analisa aplicativos (APK e outros arquivos) para detectar informações suspeitas como:

* URLs escondidas
* Tokens e API Keys
* Strings suspeitas
* Estrutura interna do APK
* Hash SHA256 para verificação de segurança

Ideal para uso em:

* Termux (Android)
* Linux
* PC (Windows/Linux)
* Projetos de segurança

---

## ⚙️ Como funciona

O scanner realiza as seguintes etapas:

1. Verifica se o arquivo existe
2. Gera hash SHA256 do aplicativo
3. Extrai strings ocultas do arquivo
4. Detecta palavras suspeitas (api, token, login, password)
5. Analisa a estrutura interna do APK (se for APK)

---

## 🚀 Instalação (GitHub)

### 1) Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/app-scanner.git
cd app-scanner
```

### 2) Instalar dependências

#### No Termux:

```bash
pkg update -y
pkg install python git file grep coreutils -y
```

#### No Linux/PC:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como usar (Python)

Execute:

```bash
python app_scanner.py
```

Depois digite o caminho do APK:

```
/storage/emulated/0/Download/app.apk
```

---

## 🐧 Como usar (Bash)

Dar permissão:

```bash
chmod +x scan_app.sh
```

Executar:

```bash
./scan_app.sh app.apk
```

---

## 📲 Como integrar em um aplicativo

Você pode integrar o scanner em:

* Apps Android (backend Python)
* Bots
* Sistemas de análise de arquivos
* Painéis web

Fluxo de integração:
App → envia arquivo → scanner analisa → retorna resultado

---

## 📌 Requisitos

* Python 3.8+
* Termux ou Linux (opcional)
* Git instalado

---

## 🛡️ Aviso

Este projeto é apenas para análise de segurança e estudo.
Não substitui antivírus profissional.
