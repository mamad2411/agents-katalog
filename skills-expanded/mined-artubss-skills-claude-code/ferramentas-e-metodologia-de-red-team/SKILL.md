---
name: Ferramentas e Metodologia de Red Team
description: Esta habilidade deve ser usada quando o usuário pede para "seguir metodologia de red team", "realizar caça de bugs", "automatizar reconhecimento", "caçar vulnerabilidades XSS", "enumerar subdomínios", ou necessita de técnicas de pesquisador de segurança e configurações de ferramentas de principais caçadores de bugs.
metadata:
  author: zebbern
  version: "1.1"
---

# Ferramentas e Metodologia de Red Team

## Propósito

Implementar metodologias comprovadas e fluxos de trabalho de ferramentas de principais pesquisadores de segurança para reconhecimento efetivo, descoberta de vulnerabilidades e caça de bugs. Automatizar tarefas comuns mantendo cobertura completa de superfícies de ataque.

## Entradas/Pré-requisitos

- Definição de escopo do alvo (domínios, faixas de IP, aplicações)
- Máquina de ataque baseada em Linux (Kali, Ubuntu)
- Regras e escopo do programa de bug bounty
- Dependências de ferramentas instaladas (Go, Python, Ruby)
- Chaves de API para vários serviços (Shodan, Censys, etc.)

## Saídas/Entregas

- Enumeração abrangente de subdomínios
- Descoberta de hosts ativos e fingerprinting de tecnologia
- Vulnerabilidades identificadas e vetores de ataque
- Saídas de pipeline de recon automatizado
- Descobertas documentadas para relatório

## Fluxo de Trabalho Principal

### 1. Rastreamento de Projetos e Aquisições

Configure rastreamento de reconhecimento:

```bash
# Criar estrutura de projeto
mkdir -p target/{recon,vulns,reports}
cd target

# Find acquisitions using Crunchbase
# Search manually for subsidiary companies

# Get ASN for targets
amass intel -org "Target Company" -src

# Alternative ASN lookup
curl -s "https://bgp.he.net/search?search=targetcompany&commit=Search"
```

### 2. Enumeração de Subdomínios

Descoberta abrangente de subdomínios:

```bash
# Create wildcards file
echo "target.com" > wildcards

# Run Amass passively
amass enum -passive -d target.com -src -o amass_passive.txt

# Run Amass actively
amass enum -active -d target.com -src -o amass_active.txt

# Use Subfinder
subfinder -d target.com -silent -o subfinder.txt

# Asset discovery
cat wildcards | assetfinder --subs-only | anew domains.txt

# Alternative subdomain tools
findomain -t target.com -o

# Generate permutations with dnsgen
cat domains.txt | dnsgen - | httprobe > permuted.txt

# Combine all sources
cat amass_*.txt subfinder.txt | sort -u > all_subs.txt
```

### 3. Descoberta de Hosts Ativos

Identificar hosts respondendo:

```bash
# Check which hosts are live with httprobe
cat domains.txt | httprobe -c 80 --prefer-https | anew hosts.txt

# Use httpx for more details
cat domains.txt | httpx -title -tech-detect -status-code -o live_hosts.txt

# Alternative with massdns
massdns -r resolvers.txt -t A -o S domains.txt > resolved.txt
```

### 4. Fingerprinting de Tecnologia

Identificar tecnologias para ataques direcionados:

```bash
# Whatweb scanning
whatweb -i hosts.txt -a 3 -v > tech_stack.txt

# Nuclei technology detection
nuclei -l hosts.txt -t technologies/ -o tech_nuclei.txt

# Wappalyzer (if available)
# Browser extension for manual review
```

### 5. Descoberta de Conteúdo

Encontrar endpoints e arquivos ocultos:

```bash
# Directory bruteforce with ffuf
ffuf -ac -v -u https://target.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt

# Historical URLs from Wayback
waybackurls target.com | tee wayback.txt

# Find all URLs with gau
gau target.com | tee all_urls.txt

# Parameter discovery
cat all_urls.txt | grep "=" | sort -u > params.txt

# Generate custom wordlist from historical data
cat all_urls.txt | unfurl paths | sort -u > custom_wordlist.txt
```

### 6. Análise de Aplicação (Método Jason Haddix)

**Áreas de Prioridade do Mapa de Calor:**

1. **Uploads de Arquivo** - Teste injeção, XXE, SSRF, upload de shell
2. **Tipos de Conteúdo** - Filtrar Burp para formulários multipart
3. **APIs** - Procurar por métodos ocultos, falta de autenticação
4. **Seções de Perfil** - Stored XSS, campos personalizados
5. **Integrações** - SSRF através de terceiros
6. **Páginas de Erro** - Pontos de injeção exóticos

**Perguntas de Análise:**
- Como a aplicação passa dados? (Parâmetros, API, Híbrido)
- Onde a aplicação fala sobre usuários? (UID, endpoints UUID)
- O site tem multi-tenancy ou níveis de usuário?
- Ele tem um modelo de ameaça único?
- Como o site trata XSS/CSRF?
- O site teve writeups/exploits anteriores?

### 7. Caça Automatizada de XSS

```bash
# ParamSpider for parameter extraction
python3 paramspider.py --domain target.com -o params.txt

# Filter with Gxss
cat params.txt | Gxss -p test

# Dalfox for XSS testing
cat params.txt | dalfox pipe --mining-dict params.txt -o xss_results.txt

# Alternative workflow
waybackurls target.com | grep "=" | qsreplace '"><script>alert(1)</script>' | while read url; do
    curl -s "$url" | grep -q 'alert(1)' && echo "$url"
done > potential_xss.txt
```

### 8. Varredura de Vulnerabilidades

```bash
# Nuclei comprehensive scan
nuclei -l hosts.txt -t ~/nuclei-templates/ -o nuclei_results.txt

# Check for common CVEs
nuclei -l hosts.txt -t cves/ -o cve_results.txt

# Web vulnerabilities
nuclei -l hosts.txt -t vulnerabilities/ -o vuln_results.txt
```

### 9. Enumeração de API

**Listas de palavras para fuzzing de API:**

```bash
# Enumerate API endpoints
ffuf -u https://target.com/api/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt

# Test API versions
ffuf -u https://target.com/api/v1/FUZZ -w api_wordlist.txt
ffuf -u https://target.com/api/v2/FUZZ -w api_wordlist.txt

# Check for hidden methods
for method in GET POST PUT DELETE PATCH; do
    curl -X $method https://target.com/api/users -v
done
```

### 10. Script de Recon Automatizado

```bash
#!/bin/bash
domain=$1

if [[ -z $domain ]]; then
    echo "Usage: ./recon.sh <domain>"
    exit 1
fi

mkdir -p "$domain"

# Subdomain enumeration
echo "[*] Enumerating subdomains..."
subfinder -d "$domain" -silent > "$domain/subs.txt"

# Live host discovery
echo "[*] Finding live hosts..."
cat "$domain/subs.txt" | httpx -title -tech-detect -status-code > "$domain/live.txt"

# URL collection
echo "[*] Collecting URLs..."
cat "$domain/live.txt" | waybackurls > "$domain/urls.txt"

# Nuclei scanning
echo "[*] Running Nuclei..."
nuclei -l "$domain/live.txt" -o "$domain/nuclei.txt"

echo "[+] Recon complete!"
```

## Referência Rápida

### Ferramentas Essenciais

| Ferramenta | Propósito |
|------|---------|
| Amass | Enumeração de subdomínios |
| Subfinder | Descoberta rápida de subdomínios |
| httpx/httprobe | Detecção de hosts ativos |
| ffuf | Descoberta de conteúdo |
| Nuclei | Varredura de vulnerabilidades |
| Burp Suite | Testes manuais |
| Dalfox | Automação de XSS |
| waybackurls | Mineração de URLs históricas |

### Endpoints de API Principais para Verificar

```
/api/v1/users
/api/v1/admin
/api/v1/profile
/api/users/me
/api/config
/api/debug
/api/swagger
/api/graphql
```

### Teste de Filtro XSS

```html
<!-- Test encoding handling -->
<h1><img><table>
<script>
%3Cscript%3E
%253Cscript%253E
%26lt;script%26gt;
```

## Restrições

- Respeite limites de escopo do programa
- Evite DoS ou fuzzing em produção sem permissão
- Limite taxa de requisições para evitar bloqueios
- Algumas ferramentas podem gerar falsos positivos
- Chaves de API necessárias para funcionalidade completa de algumas ferramentas

## Exemplos

### Exemplo 1: Recon Rápido de Subdomínio

```bash
subfinder -d target.com | httpx -title | tee results.txt
```

### Exemplo 2: Pipeline de Caça de XSS

```bash
waybackurls target.com | grep "=" | qsreplace "test" | httpx -silent | dalfox pipe
```

### Exemplo 3: Scan Abrangente

```bash
# Full recon chain
amass enum -d target.com | httpx | nuclei -t ~/nuclei-templates/
```

## Solução de Problemas

| Problema | Solução |
|-------|----------|
| Taxa limitada | Use rotação de proxy, reduza concorrência |
| Muitos resultados | Foque em stacks de tecnologia específicos |
| Falsos positivos | Verifique manualmente descobertas antes de relatar |
| Subdomínios faltando | Combine múltiplas fontes de enumeração |
| Erros de chave de API | Verifique chaves em arquivos de configuração |
| Ferramentas não encontradas | Instale ferramentas Go com `go install` |