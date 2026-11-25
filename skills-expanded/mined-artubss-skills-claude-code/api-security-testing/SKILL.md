---
name: api-security-testing
description: "Workflow de teste de segurança de API para APIs REST e GraphQL cobrindo autenticação, autorização, limitação de taxa, validação de entrada e práticas recomendadas de segurança."
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Workflow de Teste de Segurança de API

## Visão Geral

Workflow especializado para testar segurança de APIs REST e GraphQL incluindo autenticação, autorização, limitação de taxa, validação de entrada e vulnerabilidades específicas de API.

## Quando Usar Este Workflow

Use este workflow quando:
- Testar segurança de API REST
- Avaliar endpoints GraphQL
- Validar autenticação de API
- Testar limitação de taxa de API
- Testar API em bug bounty

## Fases do Workflow

### Fase 1: Descoberta de API

#### Habilidades a Invocar
- `api-fuzzing-bug-bounty` - Fuzzing de API
- `scanning-tools` - Scanning de API

#### Ações
1. Enumerar endpoints
2. Documentar métodos de API
3. Identificar parâmetros
4. Mapear fluxos de dados
5. Revisar documentação

#### Prompts para Copiar e Colar
```
Use @api-fuzzing-bug-bounty to discover API endpoints
```

### Fase 2: Teste de Autenticação

#### Habilidades a Invocar
- `broken-authentication` - Teste de autenticação
- `api-security-best-practices` - Autenticação de API

#### Ações
1. Testar validação de chave de API
2. Testar tokens JWT
3. Testar fluxos OAuth2
4. Testar expiração de token
5. Testar refresh de token

#### Prompts para Copiar e Colar
```
Use @broken-authentication to test API authentication
```

### Fase 3: Teste de Autorização

#### Habilidades a Invocar
- `idor-testing` - Teste de IDOR

#### Ações
1. Testar autorização no nível de objeto
2. Testar autorização no nível de função
3. Testar acesso baseado em função
4. Testar escalação de privilégio
5. Testar isolamento multi-tenant

#### Prompts para Copiar e Colar
```
Use @idor-testing to test API authorization
```

### Fase 4: Validação de Entrada

#### Habilidades a Invocar
- `api-fuzzing-bug-bounty` - Fuzzing de API
- `sql-injection-testing` - Teste de injeção

#### Ações
1. Testar validação de parâmetro
2. Testar injeção SQL
3. Testar injeção NoSQL
4. Testar injeção de comando
5. Testar injeção XXE

#### Prompts para Copiar e Colar
```
Use @api-fuzzing-bug-bounty to fuzz API parameters
```

### Fase 5: Limitação de Taxa

#### Habilidades a Invocar
- `api-security-best-practices` - Limitação de taxa

#### Ações
1. Testar headers de limite de taxa
2. Testar proteção contra brute force
3. Testar esgotamento de recursos
4. Testar técnicas de bypass
5. Documentar limitações

#### Prompts para Copiar e Colar
```
Use @api-security-best-practices to test rate limiting
```

### Fase 6: Teste GraphQL

#### Habilidades a Invocar
- `api-fuzzing-bug-bounty` - Fuzzing GraphQL

#### Ações
1. Testar introspection
2. Testar profundidade de query
3. Testar complexidade de query
4. Testar batch queries
5. Testar sugestões de campo

#### Prompts para Copiar e Colar
```
Use @api-fuzzing-bug-bounty to test GraphQL security
```

### Fase 7: Tratamento de Erros

#### Habilidades a Invocar
- `api-security-best-practices` - Tratamento de erro

#### Ações
1. Testar mensagens de erro
2. Verificar divulgação de informação
3. Testar stack traces
4. Verificar logging
5. Documentar resultados

#### Prompts para Copiar e Colar
```
Use @api-security-best-practices to audit API error handling
```

## Checklist de Segurança de API

- [ ] Autenticação funcionando
- [ ] Autorização forçada
- [ ] Entrada validada
- [ ] Limitação de taxa ativa
- [ ] Erros sanitizados
- [ ] Logging habilitado
- [ ] CORS configurado
- [ ] HTTPS forçado

## Quality Gates

- [ ] Todos os endpoints testados
- [ ] Vulnerabilidades documentadas
- [ ] Remediação fornecida
- [ ] Relatório gerado

## Workflow Bundles Relacionados

- `security-audit` - Auditoria de segurança
- `web-security-testing` - Teste de segurança web
- `api-development` - Desenvolvimento de API