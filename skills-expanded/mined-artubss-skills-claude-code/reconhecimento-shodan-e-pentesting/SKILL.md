---
name: Reconhecimento Shodan e Pentesting
description: Esta skill deve ser usada quando o usuário pedir para "procurar dispositivos expostos na internet," "realizar reconhecimento com Shodan," "encontrar serviços vulneráveis usando Shodan," "escanear intervalos de IP com Shodan," ou "descobrir dispositivos IoT e portas abertas." Fornece orientação abrangente para usar o mecanismo de busca, CLI e API do Shodan em testes de penetração de reconhecimento.
metadata:
  author: zebbern
  version: "1.1"
---

# Reconhecimento Shodan e Pentesting

## Propósito

Oferecer metodologias sistemáticas para aproveitar o Shodan como ferramenta de reconhecimento durante engajamentos de teste de penetração. Esta skill abrange a interface web do Shodan, interface de linha de comando (CLI), REST API, filtros de busca, scanning sob demanda e capacidades de monitoramento de rede para descobrir serviços expostos, sistemas vulneráveis e dispositivos IoT.

## Inputs / Pré-requisitos

- **Conta Shodan**: Conta gratuita ou paga em shodan.io
- **API Key**: Obtida no painel de controle da conta Shodan
- **Informações do Alvo**: Endereços IP, domínios ou intervalos de rede a investigar
- **Shodan CLI**: Ferramenta de linha de comando baseada em Python instalada
- **Autorização**: Permissão escrita para reconhecimento nas redes de destino

## Outputs / Deliverables

- **Inventário de Ativos**: Lista de hosts, portas e serviços descobertos
- **Relatório de Vulnerabilidades**: CVEs identificadas e serviços vulneráveis expostos
- **Dados de Banner**: Banners de serviço revelando versões de software
- **Mapeamento de Rede**: Distribuição geográfica e organizacional de ativos
- **Galeria de Screenshots**: Reconhecimento visual de interfaces expostas
- **Dados Exportados**: Arquivos JSON/CSV para análise posterior

## Fluxo de Trabalho Principal

### 1. Setup e Configuração

#### Instalar Shodan CLI
```bash
# Usando pip
pip install shodan

# Ou easy_install
easy_install shodan

# No BlackArch/Arch Linux
sudo pacman -S python-shodan
```

#### Inicializar API Key
```bash
# Define sua API key
shodan init YOUR_API_KEY

# Verifica setup
shodan info
# Output: Query credits available: 100
#         Scan credits available: 100
```

#### Verificar Status da Conta
```bash
# Visualiza créditos e info do plano
shodan info

# Verifica seu IP externo
shodan myip

# Verifica versão da CLI
shodan version
```

### 2. Reconhecimento Básico de Host

#### Consultar Host Único
```bash
# Obtém todas as informações sobre um IP
shodan host 1.1.1.1

# Example output:
# 1.1.1.1
# Hostnames: one.one.one.one
# Country: Australia
# Organization: Mountain View Communications
# Number of open ports: 3
# Ports:
#   53/udp
#   80/tcp
#   443/tcp
```

#### Verificar se Host é Honeypot
```bash
# Obtém pontuação de probabilidade de honeypot
shodan honeyscore 192.168.1.100

# Output: Not a honeypot
#         Score: 0.3
```

### 3. Consultas de Busca

#### Busca Básica (Gratuita)
```bash
# Busca simples por palavra-chave (sem créditos consumidos)
shodan search apache

# Especifica campos de saída
shodan search --fields ip_str,port,os smb
```

#### Busca Filtrada (1 Crédito)
```bash
# Busca específica de produto
shodan search product:mongodb

# Busca com múltiplos filtros
shodan search product:nginx country:US city:"New York"
```

#### Contar Resultados
```bash
# Obtém contagem de resultados sem consumir créditos
shodan count openssh
# Output: 23128

shodan count openssh 7
# Output: 219
```

#### Baixar Resultados
```bash
# Baixa 1000 resultados (padrão)
shodan download results.json.gz "apache country:US"

# Baixa número específico de resultados
shodan download --limit 5000 results.json.gz "nginx"

# Baixa todos os resultados disponíveis
shodan download --limit -1 all_results.json.gz "query"
```

#### Parse de Dados Baixados
```bash
# Extrai campos específicos de dados baixados
shodan parse --fields ip_str,port,hostnames results.json.gz

# Filtra por critério específico
shodan parse --fields location.country_code3,ip_str -f port:22 results.json.gz

# Exporta para formato CSV
shodan parse --fields ip_str,port,org --separator , results.json.gz > results.csv
```

### 4. Referência de Filtros de Busca

#### Filtros de Rede
```
ip:1.2.3.4                  # Endereço IP específico
net:192.168.0.0/24          # Intervalo de rede (CIDR)
hostname:example.com        # Hostname contém
port:22                     # Porta específica
asn:AS15169                 # Número do Sistema Autônomo
```

#### Filtros Geográficos
```
country:US                  # Código de país de duas letras
country:"United States"     # Nome do país completo
city:"San Francisco"        # Nome da cidade
state:CA                    # Estado/região
postal:94102                # Código postal
geo:37.7,-122.4             # Coordenadas lat/long
```

#### Filtros de Organização
```
org:"Google"                # Nome da organização
isp:"Comcast"               # Nome do ISP
```

#### Filtros de Serviço/Produto
```
product:nginx               # Produto de software
version:1.14.0              # Versão do software
os:"Windows Server 2019"    # Sistema operacional
http.title:"Dashboard"      # Título da página HTTP
http.html:"login"           # Conteúdo HTML
http.status:200             # Código de status HTTP
ssl.cert.subject.cn:*.example.com  # Certificado SSL
ssl:true                    # Tem SSL habilitado
```

#### Filtros de Vulnerabilidade
```
vuln:CVE-2019-0708          # CVE específico
has_vuln:true               # Tem alguma vulnerabilidade
```

#### Filtros de Screenshot
```
has_screenshot:true         # Tem screenshot disponível
screenshot.label:webcam     # Tipo de screenshot
```

### 5. Scanning Under Demand

#### Submeter Scan
```bash
# Escaneia IP único (1 crédito por IP)
shodan scan submit 192.168.1.100

# Escaneia com saída verbosa (mostra ID do scan)
shodan scan submit --verbose 192.168.1.100

# Escaneia e salva resultados
shodan scan submit --filename scan_results.json.gz 192.168.1.100
```

#### Monitorar Status do Scan
```bash
# Lista scans recentes
shodan scan list

# Verifica status de scan específico
shodan scan status SCAN_ID

# Baixa resultados do scan mais tarde
shodan download --limit -1 results.json.gz scan:SCAN_ID
```

#### Protocolos de Scan Disponíveis
```bash
# Lista protocolos/módulos disponíveis
shodan scan protocols
```

### 6. Estatísticas e Análise

#### Obter Estatísticas de Busca
```bash
# Estatísticas padrão (top 10 países, orgs)
shodan stats nginx

# Facetas customizadas
shodan stats --facets domain,port,asn --limit 5 nginx

# Salva em CSV
shodan stats --facets country,org -O stats.csv apache
```

### 7. Monitoramento de Rede

#### Configurar Alertas (Interface Web)
```
1. Navegue até o Painel de Monitoramento
2. Adicione IP, intervalo ou domínio para monitorar
3. Configure serviço de notificação (email, Slack, webhook)
4. Selecione eventos de acionamento (novo serviço, vulnerabilidade, etc.)
5. Visualize dashboard para serviços expostos
```

### 8. Uso de REST API

#### Chamadas de API Diretas
```bash
# Obtém info da API
curl -s "https://api.shodan.io/api-info?key=YOUR_KEY" | jq

# Lookup de host
curl -s "https://api.shodan.io/shodan/host/1.1.1.1?key=YOUR_KEY" | jq

# Query de busca
curl -s "https://api.shodan.io/shodan/host/search?key=YOUR_KEY&query=apache" | jq
```

#### Biblioteca Python
```python
import shodan

api = shodan.Shodan('YOUR_API_KEY')

# Busca
results = api.search('apache')
print(f'Results found: {results["total"]}')
for result in results['matches']:
    print(f'IP: {result["ip_str"]}')

# Lookup de host
host = api.host('1.1.1.1')
print(f'IP: {host["ip_str"]}')
print(f'Organization: {host.get("org", "n/a")}')
for item in host['data']:
    print(f'Port: {item["port"]}')
```

## Referência Rápida

### Comandos Essenciais da CLI

| Comando | Descrição | Créditos |
|---------|-----------|----------|
| `shodan init KEY` | Inicializa API key | 0 |
| `shodan info` | Mostra info da conta | 0 |
| `shodan myip` | Mostra seu IP | 0 |
| `shodan host IP` | Detalhes do host | 0 |
| `shodan count QUERY` | Contagem de resultados | 0 |
| `shodan search QUERY` | Busca básica | 0* |
| `shodan download FILE QUERY` | Salva resultados | 1/100 resultados |
| `shodan parse FILE` | Extrai dados | 0 |
| `shodan stats QUERY` | Estatísticas | 1 |
| `shodan scan submit IP` | Scan sob demanda | 1/IP |
| `shodan honeyscore IP` | Verificação honeypot | 0 |

*Filtros consomem 1 crédito por query

### Queries de Busca Comuns

| Propósito | Query |
|-----------|-------|
| Encontrar webcams | `webcam has_screenshot:true` |
| Bancos de dados MongoDB | `product:mongodb` |
| Servidores Redis | `product:redis` |
| Elasticsearch | `product:elastic port:9200` |
| Senhas padrão | `"default password"` |
| RDP vulnerável | `port:3389 vuln:CVE-2019-0708` |
| Sistemas industriais | `port:502 modbus` |
| Dispositivos Cisco | `product:cisco` |
| VNC aberto | `port:5900 authentication disabled` |
| FTP exposto | `port:21 anonymous` |
| Sites WordPress | `http.component:wordpress` |
| Impressoras | `"HP-ChaiSOE" port:80` |
| Câmeras (RTSP) | `port:554 has_screenshot:true` |
| Servidores Jenkins | `X-Jenkins port:8080` |
| APIs Docker | `port:2375 product:docker` |

### Combinações de Filtro Úteis

| Cenário | Query |
|---------|-------|
| Reconhecimento de org de destino | `org:"Company Name"` |
| Enumeração de domínio | `hostname:example.com` |
| Scan de intervalo de rede | `net:192.168.0.0/24` |
| Busca de certificado SSL | `ssl.cert.subject.cn:*.target.com` |
| Servidores vulneráveis | `vuln:CVE-2021-44228 country:US` |
| Painéis admin expostos | `http.title:"admin" port:443` |
| Exposição de banco de dados | `port:3306,5432,27017,6379` |

### Sistema de Créditos

| Ação | Tipo de Crédito | Custo |
|------|-----------------|-------|
| Busca básica | Query | 0 (sem filtros) |
| Busca filtrada | Query | 1 |
| Download de 100 resultados | Query | 1 |
| Gerar relatório | Query | 1 |
| Escanear 1 IP | Scan | 1 |
| Monitoramento de rede | IPs Monitorados | Depende do plano |

## Restrições e Limitações

### Limites Operacionais
- Taxa limitada a 1 requisição por segundo
- Resultados de scan não são imediatos (assíncrono)
- Não é possível re-escanear o mesmo IP em 24 horas (não-Enterprise)
- Contas gratuitas têm créditos limitados
- Alguns dados requerem assinatura paga

### Atualização de Dados
- Shodan faz crawl continuamente mas dados podem ter dias/semanas
- Scans sob demanda fornecem dados atuais mas custam créditos
- Dados históricos disponíveis com planos pagos

### Requisitos Legais
- Realize reconhecimento apenas em alvos autorizados
- Reconhecimento passivo geralmente é legal mas verifique jurisdição
- Scanning ativo (scan submit) requer autorização
- Documente todas as atividades de reconhecimento

## Exemplos

### Exemplo 1: Reconhecimento de Organização
```bash
# Encontra todos os hosts pertencentes à organização de destino
shodan search 'org:"Target Company"'

# Obtém estatísticas sobre sua infraestrutura
shodan stats --facets port,product,country 'org:"Target Company"'

# Baixa dados detalhados
shodan download target_data.json.gz 'org:"Target Company"'

# Parse para informações específicas
shodan parse --fields ip_str,port,product target_data.json.gz
```

### Exemplo 2: Descoberta de Serviço Vulnerável
```bash
# Encontra hosts vulneráveis a BlueKeep (CVE RDP)
shodan search 'vuln:CVE-2019-0708 country:US'

# Encontra Elasticsearch exposto sem auth
shodan search 'product:elastic port:9200 -authentication'

# Encontra sistemas vulneráveis a Log4j
shodan search 'vuln:CVE-2021-44228'
```

### Exemplo 3: Descoberta de Dispositivo IoT
```bash
# Encontra webcams expostas
shodan search 'webcam has_screenshot:true country:US'

# Encontra sistemas de controle industrial
shodan search 'port:502 product:modbus'

# Encontra impressoras expostas
shodan search '"HP-ChaiSOE" port:80'

# Encontra dispositivos de casa inteligente
shodan search 'product:nest'
```

### Exemplo 4: Análise de Certificado SSL/TLS
```bash
# Encontra hosts com certificado SSL específico
shodan search 'ssl.cert.subject.cn:*.example.com'

# Encontra certificados expirados
shodan search 'ssl.cert.expired:true org:"Company"'

# Encontra certificados auto-assinados
shodan search 'ssl.cert.issuer.cn:self-signed'
```

### Exemplo 5: Script de Automação Python
```python
#!/usr/bin/env python3
import shodan
import json

API_KEY = 'YOUR_API_KEY'
api = shodan.Shodan(API_KEY)

def recon_organization(org_name):
    """Realiza reconhecimento em uma organização"""
    try:
        # Busca a organização
        query = f'org:"{org_name}"'
        results = api.search(query)
        
        print(f"[*] Found {results['total']} hosts for {org_name}")
        
        # Coleta IPs únicos e portas
        hosts = {}
        for result in results['matches']:
            ip = result['ip_str']
            port = result['port']
            product = result.get('product', 'unknown')
            
            if ip not in hosts:
                hosts[ip] = []
            hosts[ip].append({'port': port, 'product': product})
        
        # Saída de descobertas
        for ip, services in hosts.items():
            print(f"\n[+] {ip}")
            for svc in services:
                print(f"    - {svc['port']}/tcp ({svc['product']})")
        
        return hosts
        
    except shodan.APIError as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    recon_organization("Target Company")
```

### Exemplo 6: Avaliação de Intervalo de Rede
```bash
# Escaneia uma rede /24
shodan search 'net:192.168.1.0/24'

# Obtém distribuição de portas
shodan stats --facets port 'net:192.168.1.0/24'

# Encontra vulnerabilidades específicas no intervalo
shodan search 'net:192.168.1.0/24 vuln:CVE-2021-44228'

# Exporta todos os dados para o intervalo
shodan download network_scan.json.gz 'net:192.168.1.0/24'
```

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Nenhuma API Key Configurada | Key não inicializada | Execute `shodan init YOUR_API_KEY` depois verifique com `shodan info` |
| Créditos de Query Esgotados | Créditos mensais consumidos | Use queries sem créditos (sem filtros), aguarde reset ou faça upgrade |
| Host Recentemente Escaneado | Não é possível re-escanear IP em 24h | Use `shodan host IP` para dados existentes, ou aguarde 24 horas |
| Rate Limit Excedido | >1 requisição/segundo | Adicione `time.sleep(1)` entre requisições de API |
| Resultados de Busca Vazios | Muito específico ou erro de sintaxe | Use aspas para frases: `'org:"Company Name"'`; amplie critérios |
| Arquivo Baixado Não Abre | Corrompido ou formato errado | Verifique com `gunzip -t file.gz`, re-baixe com `--limit` |