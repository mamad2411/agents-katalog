<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-filipebcs
description: CTF writeups and security challenges by filipebcs.
---

# Writeups by filipebcs

Source repository: `/repos/filipebcs`

## Repository Index

- recon-tool/README.md

## Writeup Content


### File: recon-tool/README.md

# 🕵️ Recon Tool — Automated Domain Reconnaissance for Pentesting

`recon-tool` é uma ferramenta de **reconhecimento automatizado de domínios**, desenvolvida em Python, com foco em **pentests, bug bounty e security assessments**.

Ela consolida **enumeração ativa e passiva**, **enriquecimento HTTP**, **fingerprinting de tecnologias**, **integração com Shodan** e **priorização por risco**, gerando **relatórios em JSON, Markdown e HTML**.

---

## ✨ Principais Funcionalidades

### 🔍 Reconhecimento de Domínio
- WHOIS
- ASN
- CIDR
- IP público
- Name servers

### 🌐 DNS Recon
- Registros A, AAAA, MX, NS, TXT
- Tentativa de zone transfer
- Detecção de **DNS wildcard**

### 📡 Enumeração de Subdomínios
#### Passiva
- DNS records
- Shodan hostnames
- Certificate Transparency logs
- Enumeração por ASN e CIDR

#### Ativa (Bruteforce)
- Wordlists customizáveis
- Execução paralela
- Proteção contra wildcard DNS

### 🌍 Enriquecimento HTTP
- Checagem de reachability (HTTP/HTTPS)
- Headers HTTP
- Status code
- Redirects
- Detecção de páginas de login

### 🧠 Fingerprinting de Tecnologias
- Baseado em headers HTTP
- Detecção com **nível de confiança**
- Estrutura preparada para expansão futura

### 📊 Risk Scoring (Priorização)
Cada subdomínio recebe:
- **Score (0–100)**
- **Nível de risco**: LOW / MEDIUM / HIGH / CRITICAL
- **Sinais detectados**, como:
  - Palavras sensíveis (`admin`, `vpn`, `internal`, etc.)
  - Tecnologias críticas (Jenkins, Grafana, Kibana, etc.)
  - Exposição HTTP
  - Descoberta passiva
  - Portas abertas via Shodan

### 📄 Relatórios
- ✅ JSON (machine-readable)
- ✅ Markdown
- ✅ HTML (priorizado para análise manual)

---

## 🗂 Estrutura do Projeto

# 🕵️ Recon Tool — Automated Domain Reconnaissance for Pentesting

`recon-tool` é uma ferramenta de **reconhecimento automatizado de domínios**, desenvolvida em Python, com foco em **pentests, bug bounty e security assessments**.

Ela consolida **enumeração ativa e passiva**, **enriquecimento HTTP**, **fingerprinting de tecnologias**, **integração com Shodan** e **priorização por risco**, gerando **relatórios em JSON, Markdown e HTML**.

---

## ✨ Principais Funcionalidades

### 🔍 Reconhecimento de Domínio
- WHOIS
- ASN
- CIDR
- IP público
- Name servers

### 🌐 DNS Recon
- Registros A, AAAA, MX, NS, TXT
- Tentativa de zone transfer
- Detecção de **DNS wildcard**

### 📡 Enumeração de Subdomínios
#### Passiva
- DNS records
- Shodan hostnames
- Certificate Transparency logs
- Enumeração por ASN e CIDR

#### Ativa (Bruteforce)
- Wordlists customizáveis
- Execução paralela
- Proteção contra wildcard DNS

### 🌍 Enriquecimento HTTP
- Checagem de reachability (HTTP/HTTPS)
- Headers HTTP
- Status code
- Redirects
- Detecção de páginas de login

### 🧠 Fingerprinting de Tecnologias
- Baseado em headers HTTP
- Detecção com **nível de confiança**
- Estrutura preparada para expansão futura

### 📊 Risk Scoring (Priorização)
Cada subdomínio recebe:
- **Score (0–100)**
- **Nível de risco**: LOW / MEDIUM / HIGH / CRITICAL
- **Sinais detectados**, como:
  - Palavras sensíveis (`admin`, `vpn`, `internal`, etc.)
  - Tecnologias críticas (Jenkins, Grafana, Kibana, etc.)
  - Exposição HTTP
  - Descoberta passiva
  - Portas abertas via Shodan

### 📄 Relatórios
- ✅ JSON (machine-readable)
- ✅ Markdown
- ✅ HTML (priorizado para análise manual)

---

## 🗂 Estrutura do Projeto

```text
recon-tool/
│
├── recon_tool/
│   ├── core/
│   │   ├── domain.py
│   │   ├── dns.py
│   │   ├── subdomains.py
│   │   ├── passive_subdomains.py
│   │   ├── http.py
│   │   ├── tech.py
│   │   ├── shodan.py
│   │   └── scoring.py
│   │
│   ├── reports/
│   │   ├── html.py
│   │   ├── markdown.py
│   │   └── templates/
│   │       └── report.html
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── concurrency.py
│   │   └── wordlist.py
│   │
│   ├── main.py
│   └── __main__.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── output/
│   ├── recon-example_com.json
│   ├── recon-example_com.md
│   └── recon-example_com.html
│
├── .env
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

## ⚙️ Requisitos

- Python **3.13+**
- Poetry
- Conta no Shodan (opcional, mas recomendada)

---

## 🚀 Instalação

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/filipebcs/recon-tool.git
cd recon-tool
```

---

## ⚙️ Requisitos

- Python **3.13+**
- Poetry
- Conta no Shodan (opcional, mas recomendada)

---

### 2️⃣ Instalar dependências
```bash
poetry install
```

### 3️⃣ Ativar ambiente virtual
```bash
poetry shell
```

## 🔐 Configuração (.env)

Crie um arquivo .env na raiz do projeto:

```env
SHODAN_API_KEY=SEU_TOKEN_AQUI
```

⚠️ O arquivo .env não deve ser commitado.

## ▶️ Uso
Execução básica

```bash
poetry run python -m recon_tool --domain example.com
```

Com wordlists customizadas

```bash
poetry run python -m recon_tool \
  --domain example.com \
  --subdomain-wordlist wordlists/common.txt \
  --subdomain-wordlist wordlists/cloud.txt \
  --subdomain-workers 20
```

## 📤 Outputs

Os arquivos são gerados na pasta output/:

* recon-example_com.json

* recon-example_com.md

* recon-example_com.html

O relatório HTML inclui:

1. Sumário executivo

2. Subdomínios priorizados por risco

3. Indicadores visuais por severidade

4. Links clicáveis

5. Sinais de login detectado

6. Informações do Shodan (quando disponíveis)

## 🧪 Testes Rápidos
Execução completa

```bash
poetry run python -m recon_tool --domain example.com
```

Testar módulos isolados

```bash
poetry run python -c "from recon_tool.core.dns import collect_dns_info; print(collect_dns_info('example.com'))"
```

## ⚠️ Aviso Legal

Esta ferramenta é destinada exclusivamente para uso ético e autorizado.
O autor não se responsabiliza por uso indevido.

## 👤 Autor

Filipe de Castro Borges da Silveira
Engenheiro Eletricista • Pentester • Perito Judicial
GitHub: https://github.com/filipebcs

## ⭐ Contribuições

Pull requests são bem-vindos.
Sugestões, issues e discussões são incentivadas.
