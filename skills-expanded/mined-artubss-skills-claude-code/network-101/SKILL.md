---
name: Network 101
description: Esta competência deve ser usada quando o usuário solicita "configurar um servidor web", "configurar HTTP ou HTTPS", "executar enumeração SNMP", "configurar compartilhamentos SMB", "testar serviços de rede", ou precisa de orientação sobre como configurar e testar serviços de rede para labs de teste de penetração.
metadata:
  author: zebbern
  version: "1.1"
---

# Network 101

## Propósito

Configurar e testar serviços de rede comuns (HTTP, HTTPS, SNMP, SMB) para ambientes de lab de teste de penetração. Permitir prática prática com enumeração de serviços, análise de logs e testes de segurança contra sistemas alvo devidamente configurados.

## Entradas/Pré-requisitos

- Windows Server ou sistema Linux para hospedagem de serviços
- Kali Linux ou similar para testes
- Acesso administrativo ao sistema alvo
- Conhecimento básico de redes (endereçamento IP, portas)
- Acesso ao firewall para configuração de portas

## Saídas/Entregas

- Servidor web HTTP/HTTPS configurado
- Serviço SNMP com comunidades acessíveis
- Compartilhamentos de arquivo SMB com vários níveis de permissão
- Logs capturados para análise
- Resultados de enumeração documentados

## Fluxo de Trabalho Principal

### 1. Configurar Servidor HTTP (Porta 80)

Configure um servidor web HTTP básico para testes:

**Configuração IIS no Windows:**
1. Abra o Gerenciador do IIS (Internet Information Services)
2. Clique com botão direito em Sites → Adicionar Site
3. Configure nome do site e caminho físico
4. Associe a um endereço IP e porta 80

**Configuração Apache no Linux:**

```bash
# Instalar Apache
sudo apt update && sudo apt install apache2

# Iniciar serviço
sudo systemctl start apache2
sudo systemctl enable apache2

# Criar página de teste
echo "<html><body><h1>Test Page</h1></body></html>" | sudo tee /var/www/html/index.html

# Verificar serviço
curl http://localhost
```

**Configurar Firewall para HTTP:**

```bash
# Linux (UFW)
sudo ufw allow 80/tcp

# Windows PowerShell
New-NetFirewallRule -DisplayName "HTTP" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
```

### 2. Configurar Servidor HTTPS (Porta 443)

Configure HTTPS seguro com SSL/TLS:

**Gerar Certificado Auto-Assinado:**

```bash
# Linux - Gerar certificado
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/apache-selfsigned.key \
  -out /etc/ssl/certs/apache-selfsigned.crt

# Ativar módulo SSL
sudo a2enmod ssl
sudo systemctl restart apache2
```

**Configurar Apache para HTTPS:**

```bash
# Editar host virtual SSL
sudo nano /etc/apache2/sites-available/default-ssl.conf

# Ativar site
sudo a2ensite default-ssl
sudo systemctl reload apache2
```

**Verificar Configuração HTTPS:**

```bash
# Verificar se porta 443 está aberta
nmap -p 443 192.168.1.1

# Testar conexão SSL
openssl s_client -connect 192.168.1.1:443

# Verificar certificado
curl -kv https://192.168.1.1
```

### 3. Configurar Serviço SNMP (Porta 161)

Configure SNMP para prática de enumeração:

**Configuração SNMP no Linux:**

```bash
# Instalar daemon SNMP
sudo apt install snmpd snmp

# Configurar community strings
sudo nano /etc/snmp/snmpd.conf

# Adicionar estas linhas:
# rocommunity public
# rwcommunity private

# Reiniciar serviço
sudo systemctl restart snmpd
```

**Configuração SNMP no Windows:**
1. Abra Gerenciador do Servidor → Adicionar Recursos
2. Selecione Serviço SNMP
3. Configure community strings em Serviços → Serviço SNMP → Propriedades

**Comandos de Enumeração SNMP:**

```bash
# SNMP walk básico
snmpwalk -c public -v1 192.168.1.1

# Enumerar informações de sistema
snmpwalk -c public -v1 192.168.1.1 1.3.6.1.2.1.1

# Obter processos em execução
snmpwalk -c public -v1 192.168.1.1 1.3.6.1.2.1.25.4.2.1.2

# Ferramenta de verificação SNMP
snmp-check 192.168.1.1 -c public

# Força bruta de community strings
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt 192.168.1.1
```

### 4. Configurar Serviço SMB (Porta 445)

Configure compartilhamentos de arquivo SMB para enumeração:

**Compartilhamento SMB no Windows:**
1. Crie uma pasta para compartilhar
2. Clique com botão direito → Propriedades → Compartilhamento → Compartilhamento Avançado
3. Ative o compartilhamento e defina permissões
4. Configure permissões NTFS

**Configuração Samba no Linux:**

```bash
# Instalar Samba
sudo apt install samba

# Criar diretório de compartilhamento
sudo mkdir -p /srv/samba/share
sudo chmod 777 /srv/samba/share

# Configurar Samba
sudo nano /etc/samba/smb.conf

# Adicionar compartilhamento:
# [public]
#    path = /srv/samba/share
#    browsable = yes
#    guest ok = yes
#    read only = no

# Reiniciar serviço
sudo systemctl restart smbd
```

**Comandos de Enumeração SMB:**

```bash
# Listar compartilhamentos anonimamente
smbclient -L //192.168.1.1 -N

# Conectar a compartilhamento
smbclient //192.168.1.1/share -N

# Enumerar com smbmap
smbmap -H 192.168.1.1

# Enumeração completa
enum4linux -a 192.168.1.1

# Verificar vulnerabilidades
nmap --script smb-vuln* 192.168.1.1
```

### 5. Analisar Logs de Serviço

Revise logs para análise de segurança:

**Logs HTTP/HTTPS:**

```bash
# Log de acesso Apache
sudo tail -f /var/log/apache2/access.log

# Log de erro Apache
sudo tail -f /var/log/apache2/error.log

# Logs IIS do Windows
# Local: C:\inetpub\logs\LogFiles\W3SVC1\
```

**Analisar Log para Credenciais:**

```bash
# Procurar requisições POST
grep "POST" /var/log/apache2/access.log

# Extrair user agents
awk '{print $12}' /var/log/apache2/access.log | sort | uniq -c
```

## Referência Rápida

### Portas Essenciais

| Serviço | Porta | Protocolo |
|---------|-------|-----------|
| HTTP | 80 | TCP |
| HTTPS | 443 | TCP |
| SNMP | 161 | UDP |
| SMB | 445 | TCP |
| NetBIOS | 137-139 | TCP/UDP |

### Comandos de Verificação de Serviço

```bash
# Verificar HTTP
curl -I http://target

# Verificar HTTPS
curl -kI https://target

# Verificar SNMP
snmpwalk -c public -v1 target

# Verificar SMB
smbclient -L //target -N
```

### Ferramentas Comuns de Enumeração

| Ferramenta | Propósito |
|-----------|-----------|
| nmap | Varredura de portas e scripts |
| nikto | Varredura de vulnerabilidades web |
| snmpwalk | Enumeração SNMP |
| enum4linux | Enumeração SMB/NetBIOS |
| smbclient | Conexão SMB |
| gobuster | Força bruta de diretórios |

## Limitações

- Certificados auto-assinados disparam avisos do navegador
- Communities SNMP v1/v2c são transmitidas em texto simples
- Acesso SMB anônimo é frequentemente desabilitado por padrão
- Regras de firewall devem permitir conexões de entrada
- Ambientes de lab devem ser isolados da produção

## Exemplos

### Exemplo 1: Configuração Completa de Lab HTTP

```bash
# Instalar e configurar
sudo apt install apache2
sudo systemctl start apache2

# Criar página de login
cat << 'EOF' | sudo tee /var/www/html/login.html
<html>
<body>
<form method="POST" action="login.php">
Username: <input type="text" name="user"><br>
Password: <input type="password" name="pass"><br>
<input type="submit" value="Login">
</form>
</body>
</html>
EOF

# Permitir através do firewall
sudo ufw allow 80/tcp
```

### Exemplo 2: Configuração de Teste SNMP

```bash
# Configuração SNMP rápida
sudo apt install snmpd
echo "rocommunity public" | sudo tee -a /etc/snmp/snmpd.conf
sudo systemctl restart snmpd

# Testar enumeração
snmpwalk -c public -v1 localhost
```

### Exemplo 3: Acesso Anônimo SMB

```bash
# Configurar compartilhamento anônimo
sudo apt install samba
sudo mkdir /srv/samba/anonymous
sudo chmod 777 /srv/samba/anonymous

# Testar acesso
smbclient //localhost/anonymous -N
```

## Solução de Problemas

| Problema | Solução |
|----------|---------|
| Porta não acessível | Verificar regras de firewall (ufw, iptables, Windows Firewall) |
| Serviço não inicia | Verificar logs com `journalctl -u service-name` |
| Timeout SNMP | Verificar se UDP 161 está aberto, verificar community string |
| Acesso SMB negado | Verificar permissões de compartilhamento e credenciais de usuário |
| Erro de certificado HTTPS | Aceitar certificado auto-assinado ou adicionar ao armazenamento confiável |
| Não consegue conectar remotamente | Associar serviço a 0.0.0.0 em vez de localhost |