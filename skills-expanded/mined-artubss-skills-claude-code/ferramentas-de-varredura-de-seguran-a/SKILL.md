---
name: Ferramentas de Varredura de Segurança
description: Esta skill deve ser utilizada quando o usuário solicita "realizar varredura de vulnerabilidades", "escanear redes em busca de portas abertas", "avaliar segurança de aplicações web", "escanear redes sem fio", "detectar malware", "verificar segurança em nuvem" ou "avaliar conformidade do sistema". Oferece orientação abrangente sobre ferramentas e metodologias de varredura de segurança.
metadata:
  author: zebbern
  version: "1.1"
---

# Ferramentas de Varredura de Segurança

## Propósito

Dominar ferramentas essenciais de varredura de segurança para descoberta de redes, avaliação de vulnerabilidades, testes de aplicações web, segurança wireless e validação de conformidade. Esta skill aborda seleção de ferramentas, configuração e uso prático em diferentes categorias de varredura.

## Pré-requisitos

### Ambiente Necessário
- Sistema baseado em Linux (Kali Linux recomendado)
- Acesso à rede para sistemas alvo
- Autorização apropriada para atividades de varredura

### Conhecimento Necessário
- Conceitos básicos de redes (TCP/IP, portas, protocolos)
- Compreensão de vulnerabilidades comuns
- Familiaridade com interfaces de linha de comando

## Resultados e Entregáveis

1. **Relatórios de Descoberta de Rede** - Hosts, portas e serviços identificados
2. **Relatórios de Avaliação de Vulnerabilidades** - CVEs, configurações incorretas, classificações de risco
3. **Relatórios de Segurança de Aplicações Web** - Descobertas OWASP Top 10
4. **Relatórios de Conformidade** - Verificações CIS benchmarks, PCI-DSS, HIPAA

## Fluxo de Trabalho Principal

### Fase 1: Ferramentas de Varredura de Rede

#### Nmap (Network Mapper)

Ferramenta principal para descoberta de rede e auditoria de segurança:

```bash
# Descoberta de hosts
nmap -sn 192.168.1.0/24              # Ping scan (sem varredura de portas)
nmap -sL 192.168.1.0/24              # List scan (resolução DNS)
nmap -Pn 192.168.1.100               # Pular descoberta de hosts

# Técnicas de varredura de portas
nmap -sS 192.168.1.100               # TCP SYN scan (stealth)
nmap -sT 192.168.1.100               # TCP connect scan
nmap -sU 192.168.1.100               # UDP scan
nmap -sA 192.168.1.100               # ACK scan (detecção de firewall)

# Especificação de portas
nmap -p 80,443 192.168.1.100         # Portas específicas
nmap -p- 192.168.1.100               # Todas as 65535 portas
nmap -p 1-1000 192.168.1.100         # Intervalo de portas
nmap --top-ports 100 192.168.1.100   # Top 100 portas comuns

# Detecção de serviço e SO
nmap -sV 192.168.1.100               # Detecção de versão de serviço
nmap -O 192.168.1.100                # Detecção de SO
nmap -A 192.168.1.100                # Agressivo (SO, versão, scripts)

# Timing e performance
nmap -T0 192.168.1.100               # Paranoid (mais lento, evasão de IDS)
nmap -T4 192.168.1.100               # Agressivo (mais rápido)
nmap -T5 192.168.1.100               # Insano (mais rápido possível)

# NSE Scripts
nmap --script=vuln 192.168.1.100     # Scripts de vulnerabilidade
nmap --script=http-enum 192.168.1.100  # Enumeração web
nmap --script=smb-vuln* 192.168.1.100  # Vulnerabilidades SMB
nmap --script=default 192.168.1.100  # Conjunto de scripts padrão

# Formatos de saída
nmap -oN scan.txt 192.168.1.100      # Saída normal
nmap -oX scan.xml 192.168.1.100      # Saída XML
nmap -oG scan.gnmap 192.168.1.100    # Saída Grepable
nmap -oA scan 192.168.1.100          # Todos os formatos
```

#### Masscan

Varredura de portas de alta velocidade para grandes redes:

```bash
# Varredura básica
masscan -p80 192.168.1.0/24 --rate=1000
masscan -p80,443,8080 192.168.1.0/24 --rate=10000

# Intervalo completo de portas
masscan -p0-65535 192.168.1.0/24 --rate=5000

# Varredura em larga escala
masscan 0.0.0.0/0 -p443 --rate=100000 --excludefile exclude.txt

# Formatos de saída
masscan -p80 192.168.1.0/24 -oG results.gnmap
masscan -p80 192.168.1.0/24 -oJ results.json
masscan -p80 192.168.1.0/24 -oX results.xml

# Banner grabbing
masscan -p80 192.168.1.0/24 --banners
```

### Fase 2: Ferramentas de Varredura de Vulnerabilidades

#### Nessus

Avaliação de vulnerabilidades de nível empresarial:

```bash
# Iniciar serviço Nessus
sudo systemctl start nessusd

# Acessar interface web
# https://localhost:8834

# Linha de comando (nessuscli)
nessuscli scan --create --name "Internal Scan" --targets 192.168.1.0/24
nessuscli scan --list
nessuscli scan --launch <scan_id>
nessuscli report --format pdf --output report.pdf <scan_id>
```

Principais recursos Nessus:
- Detecção abrangente de CVEs
- Verificações de conformidade (PCI-DSS, HIPAA, CIS)
- Templates de varredura personalizados
- Varredura credenciada para análise mais profunda
- Atualizações regulares de plugins

#### OpenVAS (Greenbone)

Varredura de vulnerabilidades open-source:

```bash
# Instalar OpenVAS
sudo apt install openvas
sudo gvm-setup

# Iniciar serviços
sudo gvm-start

# Acessar interface web (Greenbone Security Assistant)
# https://localhost:9392

# Operações de linha de comando
gvm-cli socket --xml "<get_version/>"
gvm-cli socket --xml "<get_tasks/>"

# Criar e executar varredura
gvm-cli socket --xml '
<create_target>
  <name>Test Target</name>
  <hosts>192.168.1.0/24</hosts>
</create_target>'
```

### Fase 3: Ferramentas de Varredura de Aplicações Web

#### Burp Suite

Testes abrangentes de aplicações web:

```
# Configuração de proxy
1. Configurar proxy do navegador para 127.0.0.1:8080
2. Importar certificado CA do Burp para HTTPS
3. Adicionar alvo ao escopo

# Módulos principais:
- Proxy: Interceptar e modificar requisições
- Spider: Rastrear aplicações web
- Scanner: Detecção automatizada de vulnerabilidades
- Intruder: Ataques automatizados (fuzzing, brute-force)
- Repeater: Manipulação manual de requisições
- Decoder: Codificar/decodificar dados
- Comparer: Comparar respostas
```

Fluxo de trabalho de testes principais:
1. Configurar proxy e escopo
2. Rastrear a aplicação
3. Analisar mapa do site
4. Executar scanner ativo
5. Testes manuais com Repeater/Intruder
6. Revisar descobertas e gerar relatório

#### OWASP ZAP

Scanner de aplicação web open-source:

```bash
# Iniciar ZAP
zaproxy

# Varredura automatizada pela CLI
zap-cli quick-scan https://target.com

# Varredura completa
zap-cli spider https://target.com
zap-cli active-scan https://target.com

# Gerar relatório
zap-cli report -o report.html -f html

# Modo API
zap.sh -daemon -port 8080 -config api.key=<your_key>
```

Automação ZAP:
```bash
# Varredura baseada em Docker
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t https://target.com -r report.html

# Baseline scan (apenas passivo)
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://target.com -r report.html
```

#### Nikto

Scanner de vulnerabilidades de servidor web:

```bash
# Varredura básica
nikto -h https://target.com

# Varredura de porta específica
nikto -h target.com -p 8080

# Varredura com SSL
nikto -h target.com -ssl

# Múltiplos alvos
nikto -h targets.txt

# Formatos de saída
nikto -h target.com -o report.html -Format html
nikto -h target.com -o report.xml -Format xml
nikto -h target.com -o report.csv -Format csv

# Opções de tuning
nikto -h target.com -Tuning 123456789  # Todos os testes
nikto -h target.com -Tuning x          # Excluir testes específicos
```

### Fase 4: Ferramentas de Varredura Wireless

#### Aircrack-ng Suite

Testes de penetração de rede wireless:

```bash
# Verificar interface wireless
airmon-ng

# Habilitar modo monitor
sudo airmon-ng start wlan0

# Escanear redes
sudo airodump-ng wlan0mon

# Capturar rede específica
sudo airodump-ng -c <channel> --bssid <target_bssid> -w capture wlan0mon

# Ataque de desautenticação
sudo aireplay-ng -0 10 -a <bssid> wlan0mon

# Quebrar handshake WPA
aircrack-ng -w wordlist.txt -b <bssid> capture*.cap

# Quebrar WEP
aircrack-ng -b <bssid> capture*.cap
```

#### Kismet

Detecção wireless passiva:

```bash
# Iniciar Kismet
kismet

# Especificar interface
kismet -c wlan0

# Acessar interface web
# http://localhost:2501

# Detectar redes ocultas
# Kismet coleta passivamente todos os beacon frames
# incluindo aqueles de SSIDs ocultos
```

### Fase 5: Varredura de Malware e Exploits

#### ClamAV

Scanner de antivírus open-source:

```bash
# Atualizar definições de vírus
sudo freshclam

# Escanear diretório
clamscan -r /path/to/scan

# Escanear com saída verbosa
clamscan -r -v /path/to/scan

# Mover arquivos infectados
clamscan -r --move=/quarantine /path/to/scan

# Remover arquivos infectados
clamscan -r --remove /path/to/scan

# Escanear tipos de arquivo específicos
clamscan -r --include='\.exe$|\.dll$' /path/to/scan

# Saída para log
clamscan -r -l scan.log /path/to/scan
```

#### Validação de Vulnerabilidades com Metasploit

Validar vulnerabilidades com exploração:

```bash
# Iniciar Metasploit
msfconsole

# Configuração de banco de dados
msfdb init
db_status

# Importar resultados Nmap
db_import /path/to/nmap_scan.xml

# Varredura de vulnerabilidades
use auxiliary/scanner/smb/smb_ms17_010
set RHOSTS 192.168.1.0/24
run

# Exploração automática
vulns                           # Ver vulnerabilidades
analyze                         # Sugerir exploits
```

### Fase 6: Varredura de Segurança em Nuvem

#### Prowler (AWS)

Avaliação de segurança AWS:

```bash
# Instalar Prowler
pip install prowler

# Varredura básica
prowler aws

# Verificações específicas
prowler aws -c iam s3 ec2

# Framework de conformidade
prowler aws --compliance cis_aws

# Formatos de saída
prowler aws -M html json csv

# Região específica
prowler aws -f us-east-1

# Asumir role
prowler aws -R arn:aws:iam::123456789012:role/ProwlerRole
```

#### ScoutSuite (Multi-cloud)

Auditoria de segurança multi-cloud:

```bash
# Instalar ScoutSuite
pip install scoutsuite

# Varredura AWS
scout aws

# Varredura Azure
scout azure --cli

# Varredura GCP
scout gcp --user-account

# Gerar relatório
scout aws --report-dir ./reports
```

### Fase 7: Varredura de Conformidade

#### Lynis

Auditoria de segurança para Unix/Linux:

```bash
# Executar auditoria
sudo lynis audit system

# Varredura rápida
sudo lynis audit system --quick

# Perfil específico
sudo lynis audit system --profile server

# Saída de relatório
sudo lynis audit system --report-file /tmp/lynis-report.dat

# Verificar seção específica
sudo lynis show profiles
sudo lynis audit system --tests-from-group malware
```

#### OpenSCAP

Varredura de conformidade de segurança:

```bash
# Listar perfis disponíveis
oscap info /usr/share/xml/scap/ssg/content/ssg-<distro>-ds.xml

# Executar varredura com perfil
oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_pci-dss \
  --report report.html \
  /usr/share/xml/scap/ssg/content/ssg-rhel8-ds.xml

# Gerar script de correção
oscap xccdf generate fix \
  --profile xccdf_org.ssgproject.content_profile_pci-dss \
  --output remediation.sh \
  /usr/share/xml/scap/ssg/content/ssg-rhel8-ds.xml
```

### Fase 8: Metodologia de Varredura

Abordagem estruturada de varredura:

1. **Planejamento**
   - Definir escopo e objetivos
   - Obter autorização apropriada
   - Selecionar ferramentas adequadas

2. **Descoberta**
   - Descoberta de hosts (Nmap ping sweep)
   - Varredura de portas
   - Enumeração de serviços

3. **Avaliação de Vulnerabilidades**
   - Varredura automatizada (Nessus/OpenVAS)
   - Varredura de aplicação web (Burp/ZAP)
   - Verificação manual

4. **Análise**
   - Correlacionar descobertas
   - Eliminar falsos positivos
   - Priorizar por severidade

5. **Relatório**
   - Documentar descobertas
   - Fornecer orientação de remediação
   - Resumo executivo

### Fase 9: Guia de Seleção de Ferramentas

Escolha a ferramenta certa para cada cenário:

| Cenário | Ferramentas Recomendadas |
|---------|--------------------------|
| Descoberta de Rede | Nmap, Masscan |
| Avaliação de Vulnerabilidades | Nessus, OpenVAS |
| Testes de Aplicação Web | Burp Suite, ZAP, Nikto |
| Segurança Wireless | Aircrack-ng, Kismet |
| Detecção de Malware | ClamAV, YARA |
| Segurança em Nuvem | Prowler, ScoutSuite |
| Conformidade | Lynis, OpenSCAP |
| Análise de Protocolo | Wireshark, tcpdump |

### Fase 10: Relatórios e Documentação

Gerar relatórios profissionais:

```bash
# Nmap XML para HTML
xsltproc nmap-output.xml -o report.html

# Exportação de relatório OpenVAS
gvm-cli socket --xml '<get_reports report_id="<id>" format_id="<pdf_format>"/>'

# Combinar múltiplos resultados de varredura
# Usar ferramentas como Faraday, Dradis ou scripts personalizados

# Template de resumo executivo:
# 1. Escopo e metodologia
# 2. Resumo de principais descobertas
# 3. Gráfico de distribuição de risco
# 4. Vulnerabilidades críticas
# 5. Recomendações de remediação
# 6. Descobertas técnicas detalhadas
```

## Referência Rápida

### Cheat Sheet Nmap

| Tipo de Varredura | Comando |
|-------------------|---------|
| Ping Scan | `nmap -sn <target>` |
| Varredura Rápida | `nmap -T4 -F <target>` |
| Varredura Completa | `nmap -p- <target>` |
| Varredura de Serviço | `nmap -sV <target>` |
| Detecção de SO | `nmap -O <target>` |
| Agressivo | `nmap -A <target>` |
| Scripts Vuln | `nmap --script=vuln <target>` |
| Varredura Stealth | `nmap -sS -T2 <target>` |

### Referência de Portas Comuns

| Porta | Serviço |
|-------|---------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 445 | SMB |
| 3306 | MySQL |
| 3389 | RDP |

## Restrições e Limitações

### Considerações Legais
- Sempre obter autorização por escrito
- Respeitar limites de escopo
- Seguir práticas de divulgação responsável
- Cumprir leis e regulações locais

### Limitações Técnicas
- Algumas varreduras podem disparar alertas de IDS/IPS
- Varreduras intensas podem impactar performance de rede
- Falsos positivos requerem verificação manual
- Tráfego criptografado pode limitar análise

### Práticas Recomendadas
- Começar com varreduras não-intrusivas
- Aumentar gradualmente a intensidade de varredura
- Documentar todas as atividades de varredura
- Validar descobertas antes de relatar

## Solução de Problemas

### Varredura Não Detectando Hosts

**Soluções:**
1. Tentar diferentes métodos de descoberta: `nmap -Pn` ou `nmap -sn -PS/PA/PU`
2. Verificar regras de firewall bloqueando ICMP
3. Usar TCP SYN scan: `nmap -PS22,80,443`
4. Verificar conectividade de rede

### Performance Lenta de Varredura

**Soluções:**
1. Aumentar timing: `nmap -T4` ou `-T5`
2. Reduzir intervalo de portas: `--top-ports 100`
3. Usar Masscan para descoberta inicial
4. Desabilitar resolução DNS: `-n`

### Scanner Web Perdendo Vulnerabilidades

**Soluções:**
1. Autenticar para acessar áreas protegidas
2. Aumentar profundidade de rastreamento
3. Adicionar pontos de injeção personalizados
4. Usar múltiplas ferramentas para cobertura
5. Realizar testes manuais