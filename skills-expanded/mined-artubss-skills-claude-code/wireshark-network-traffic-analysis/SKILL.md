---
name: Wireshark Network Traffic Analysis
description: Esta habilidade deve ser usada quando o usuário solicita "analisar tráfego de rede com Wireshark", "capturar pacotes para troubleshooting", "filtrar arquivos PCAP", "acompanhar fluxos TCP/UDP", "detectar anomalias de rede", "investigar tráfego suspeito", ou "realizar análise de protocolos". Fornece técnicas abrangentes para captura de pacotes de rede, filtragem e análise usando Wireshark.
metadata:
  author: zebbern
  version: "1.1"
---

# Wireshark Network Traffic Analysis

## Purpose

Execute análise abrangente de tráfego de rede usando Wireshark para capturar, filtrar e examinar pacotes de rede para investigações de segurança, otimização de desempenho e troubleshooting. Esta habilidade permite análise sistemática de protocolos de rede, detecção de anomalias e reconstrução de conversas de rede a partir de arquivos PCAP.

## Inputs / Prerequisites

### Required Tools
- Wireshark instalado (Windows, macOS ou Linux)
- Interface de rede com permissões de captura
- Arquivos PCAP/PCAPNG para análise offline
- Privilégios de administrador/root para captura ao vivo

### Technical Requirements
- Compreensão de protocolos de rede (TCP, UDP, HTTP, DNS)
- Familiaridade com endereçamento IP e portas
- Conhecimento do modelo OSI em camadas
- Compreensão de padrões comuns de ataque

### Use Cases
- Troubleshooting de rede e problemas de conectividade
- Investigação de incidentes de segurança
- Análise de tráfego de malware
- Monitoramento e otimização de desempenho
- Aprendizado de protocolos e educação

## Outputs / Deliverables

### Primary Outputs
- Capturas de pacotes filtradas para tráfego específico
- Fluxos de comunicação reconstruídos
- Estatísticas de tráfego e visualizações
- Documentação de evidências para incidentes

## Core Workflow

### Phase 1: Capturing Network Traffic

#### Start Live Capture
Comece a capturar pacotes na interface de rede:

```
1. Launch Wireshark
2. Select network interface from main screen
3. Click shark fin icon or double-click interface
4. Capture begins immediately
```

#### Capture Controls
| Action | Shortcut | Description |
|--------|----------|-------------|
| Start/Stop Capture | Ctrl+E | Toggle capture on/off |
| Restart Capture | Ctrl+R | Stop and start new capture |
| Open PCAP File | Ctrl+O | Load existing capture file |
| Save Capture | Ctrl+S | Save current capture |

#### Capture Filters
Aplique filtros antes da captura para limitar a coleta de dados:

```
# Capture only specific host
host 192.168.1.100

# Capture specific port
port 80

# Capture specific network
net 192.168.1.0/24

# Exclude specific traffic
not arp

# Combine filters
host 192.168.1.100 and port 443
```

### Phase 2: Display Filters

#### Basic Filter Syntax
Filtre pacotes capturados para análise:

```
# IP address filters
ip.addr == 192.168.1.1              # All traffic to/from IP
ip.src == 192.168.1.1               # Source IP only
ip.dst == 192.168.1.1               # Destination IP only

# Port filters
tcp.port == 80                       # TCP port 80
udp.port == 53                       # UDP port 53
tcp.dstport == 443                   # Destination port 443
tcp.srcport == 22                    # Source port 22
```

#### Protocol Filters
Filtre por protocolos específicos:

```
# Common protocols
http                                  # HTTP traffic
https or ssl or tls                   # Encrypted web traffic
dns                                   # DNS queries and responses
ftp                                   # FTP traffic
ssh                                   # SSH traffic
icmp                                  # Ping/ICMP traffic
arp                                   # ARP requests/responses
dhcp                                  # DHCP traffic
smb or smb2                          # SMB file sharing
```

#### TCP Flag Filters
Identifique estados de conexão específicos:

```
tcp.flags.syn == 1                   # SYN packets (connection attempts)
tcp.flags.ack == 1                   # ACK packets
tcp.flags.fin == 1                   # FIN packets (connection close)
tcp.flags.reset == 1                 # RST packets (connection reset)
tcp.flags.syn == 1 && tcp.flags.ack == 0  # SYN-only (initial connection)
```

#### Content Filters
Procure por conteúdo específico:

```
frame contains "password"            # Packets containing string
http.request.uri contains "login"    # HTTP URIs with string
tcp contains "GET"                   # TCP packets with string
```

#### Analysis Filters
Identifique problemas potenciais:

```
tcp.analysis.retransmission          # TCP retransmissions
tcp.analysis.duplicate_ack           # Duplicate ACKs
tcp.analysis.zero_window             # Zero window (flow control)
tcp.analysis.flags                   # Packets with issues
dns.flags.rcode != 0                 # DNS errors
```

#### Combining Filters
Use operadores lógicos para consultas complexas:

```
# AND operator
ip.addr == 192.168.1.1 && tcp.port == 80

# OR operator
dns || http

# NOT operator
!(arp || icmp)

# Complex combinations
(ip.src == 192.168.1.1 || ip.src == 192.168.1.2) && tcp.port == 443
```

### Phase 3: Following Streams

#### TCP Stream Reconstruction
Visualize conversa TCP completa:

```
1. Right-click on any TCP packet
2. Select Follow > TCP Stream
3. View reconstructed conversation
4. Toggle between ASCII, Hex, Raw views
5. Filter to show only this stream
```

#### Stream Types
| Stream | Access | Use Case |
|--------|--------|----------|
| TCP Stream | Follow > TCP Stream | Web, file transfers, any TCP |
| UDP Stream | Follow > UDP Stream | DNS, VoIP, streaming |
| HTTP Stream | Follow > HTTP Stream | Web content, headers |
| TLS Stream | Follow > TLS Stream | Encrypted traffic (if keys available) |

#### Stream Analysis Tips
- Revise pares de solicitação/resposta
- Identifique arquivos ou dados transmitidos
- Procure por credenciais em texto simples
- Observe padrões ou comandos incomuns

### Phase 4: Statistical Analysis

#### Protocol Hierarchy
Visualize distribuição de protocolos:

```
Statistics > Protocol Hierarchy

Shows:
- Percentage of each protocol
- Packet counts
- Bytes transferred
- Protocol breakdown tree
```

#### Conversations
Analise pares de comunicação:

```
Statistics > Conversations

Tabs:
- Ethernet: MAC address pairs
- IPv4/IPv6: IP address pairs
- TCP: Connection details (ports, bytes, packets)
- UDP: Datagram exchanges
```

#### Endpoints
Visualize participantes de rede ativos:

```
Statistics > Endpoints

Shows:
- All source/destination addresses
- Packet and byte counts
- Geographic information (if enabled)
```

#### Flow Graph
Visualize sequência de pacotes:

```
Statistics > Flow Graph

Options:
- All packets or displayed only
- Standard or TCP flow
- Shows packet timing and direction
```

#### I/O Graphs
Plote tráfego ao longo do tempo:

```
Statistics > I/O Graph

Features:
- Packets per second
- Bytes per second
- Custom filter graphs
- Multiple graph overlays
```

### Phase 5: Security Analysis

#### Detect Port Scanning
Identifique atividade de reconhecimento:

```
# SYN scan detection (many ports, same source)
ip.src == SUSPECT_IP && tcp.flags.syn == 1

# Review Statistics > Conversations for anomalies
# Look for single source hitting many destination ports
```

#### Identify Suspicious Traffic
Filtre anomalias:

```
# Traffic to unusual ports
tcp.dstport > 1024 && tcp.dstport < 49152

# Traffic outside trusted network
!(ip.addr == 192.168.1.0/24)

# Unusual DNS queries
dns.qry.name contains "suspicious-domain"

# Large data transfers
frame.len > 1400
```

#### ARP Spoofing Detection
Identifique ataques ARP:

```
# Duplicate ARP responses
arp.duplicate-address-frame

# ARP traffic analysis
arp

# Look for:
# - Multiple MACs for same IP
# - Gratuitous ARP floods
# - Unusual ARP patterns
```

#### Examine Downloads
Analise transferências de arquivo:

```
# HTTP file downloads
http.request.method == "GET" && http contains "Content-Disposition"

# Follow HTTP Stream to view file content
# Use File > Export Objects > HTTP to extract files
```

#### DNS Analysis
Investigue atividade de DNS:

```
# All DNS traffic
dns

# DNS queries only
dns.flags.response == 0

# DNS responses only
dns.flags.response == 1

# Failed DNS lookups
dns.flags.rcode != 0

# Specific domain queries
dns.qry.name contains "domain.com"
```

### Phase 6: Expert Information

#### Access Expert Analysis
Visualize achados automatizados do Wireshark:

```
Analyze > Expert Information

Categories:
- Errors: Critical issues
- Warnings: Potential problems
- Notes: Informational items
- Chats: Normal conversation events
```

#### Common Expert Findings
| Finding | Meaning | Action |
|---------|---------|--------|
| TCP Retransmission | Packet resent | Check for packet loss |
| Duplicate ACK | Possible loss | Investigate network path |
| Zero Window | Buffer full | Check receiver performance |
| RST | Connection reset | Check for blocks/errors |
| Out-of-Order | Packets reordered | Usually normal, excessive is issue |

## Quick Reference

### Keyboard Shortcuts
| Action | Shortcut |
|--------|----------|
| Open file | Ctrl+O |
| Save file | Ctrl+S |
| Start/Stop capture | Ctrl+E |
| Find packet | Ctrl+F |
| Go to packet | Ctrl+G |
| Next packet | ↓ |
| Previous packet | ↑ |
| First packet | Ctrl+Home |
| Last packet | Ctrl+End |
| Apply filter | Enter |
| Clear filter | Ctrl+Shift+X |

### Common Filter Reference
```
# Web traffic
http || https

# Email
smtp || pop || imap

# File sharing  
smb || smb2 || ftp

# Authentication
ldap || kerberos

# Network management
snmp || icmp

# Encrypted
tls || ssl
```

### Export Options
```
File > Export Specified Packets    # Save filtered subset
File > Export Objects > HTTP       # Extract HTTP files
File > Export Packet Dissections   # Export as text/CSV
```

## Constraints and Guardrails

### Operational Boundaries
- Capture apenas tráfego de rede autorizado
- Manipule dados capturados de acordo com políticas de privacidade
- Evite capturar credenciais sensíveis desnecessariamente
- Proteja adequadamente arquivos PCAP contendo dados sensíveis

### Technical Limitations
- Capturas grandes consomem memória significativa
- Conteúdo de tráfego criptografado não é visível sem chaves
- Redes de alta velocidade podem descartar pacotes
- Alguns protocolos requerem plugins para decodificação completa

### Best Practices
- Use filtros de captura para limitar coleta de dados
- Salve capturas regularmente durante sessões longas
- Use filtros de exibição em vez de deletar pacotes
- Documente achados e metodologia de análise

## Examples

### Example 1: HTTP Credential Analysis

**Scenario**: Investigue possível transmissão de credencial em texto simples

```
1. Filter: http.request.method == "POST"
2. Look for login forms
3. Follow HTTP Stream
4. Search for username/password parameters
```

**Finding**: Credenciais transmitidas em dados de formulário em texto simples.

### Example 2: Malware C2 Detection

**Scenario**: Identifique tráfego de comando e controle

```
1. Filter: dns
2. Look for unusual query patterns
3. Check for high-frequency beaconing
4. Identify domains with random-looking names
5. Filter: ip.dst == SUSPICIOUS_IP
6. Analyze traffic patterns
```

**Indicators**:
- Regular timing intervals
- Encoded/encrypted payloads
- Unusual ports or protocols

### Example 3: Network Troubleshooting

**Scenario**: Diagnostique aplicação web lenta

```
1. Filter: ip.addr == WEB_SERVER
2. Check Statistics > Service Response Time
3. Filter: tcp.analysis.retransmission
4. Review I/O Graph for patterns
5. Check for high latency or packet loss
```

**Finding**: Retransmissões TCP indicando congestionamento de rede.

## Troubleshooting

### No Packets Captured
- Verifique se interface correta está selecionada
- Confirme permissões de admin/root
- Verifique se adaptador de rede está ativo
- Desabilite modo promíscuo se problemas persistirem

### Filter Not Working
- Verifique sintaxe de filtro (vermelho = erro)
- Procure por erros de digitação em nomes de campo
- Use botão Expression para campos válidos
- Limpe filtro e reconstrua incrementalmente

### Performance Issues
- Use filtros de captura para limitar tráfego
- Divida capturas grandes em arquivos menores
- Desabilite resolução de nomes durante captura
- Feche dissecadores de protocolo desnecessários

### Cannot Decrypt TLS/SSL
- Obtenha chave privada do servidor
- Configure em Edit > Preferences > Protocols > TLS
- Para chaves efêmeras, capture pré-master secret do navegador
- Algumas cifras modernas não podem ser descriptografadas passivamente