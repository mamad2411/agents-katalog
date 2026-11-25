---
name: web-security-testing
description: "Fluxo de trabalho de teste de segurança de aplicações web para vulnerabilidades OWASP Top 10, incluindo injection, XSS, falhas de autenticação e problemas de controle de acesso."
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Fluxo de Trabalho de Teste de Segurança Web

## Visão Geral

Fluxo de trabalho especializado para testar aplicações web contra vulnerabilidades OWASP Top 10, incluindo ataques de injection, XSS, autenticação quebrada e problemas de controle de acesso.

## Quando Usar Este Fluxo de Trabalho

Use este fluxo de trabalho quando:
- Testando segurança de aplicações web
- Realizando avaliação OWASP Top 10
- Conduzindo testes de penetração
- Validando controles de segurança
- Participando de bug bounty

## Fases do Fluxo de Trabalho

### Fase 1: Reconhecimento

#### Habilidades a Invocar
- `scanning-tools` - Varredura de segurança
- `top-web-vulnerabilities` - Conhecimento OWASP

#### Ações
1. Mapear superfície da aplicação
2. Identificar tecnologias
3. Descobrir endpoints
4. Encontrar subdomínios
5. Documentar descobertas

#### Prompts para Copiar e Colar
```
Use @scanning-tools to perform web application reconnaissance
```

### Fase 2: Teste de Injection

#### Habilidades a Invocar
- `sql-injection-testing` - SQL injection
- `sqlmap-database-pentesting` - SQLMap

#### Ações
1. Testar SQL injection
2. Testar NoSQL injection
3. Testar command injection
4. Testar LDAP injection
5. Documentar vulnerabilidades

#### Prompts para Copiar e Colar
```
Use @sql-injection-testing to test for SQL injection
```

```
Use @sqlmap-database-pentesting to automate SQL injection testing
```

### Fase 3: Teste de XSS

#### Habilidades a Invocar
- `xss-html-injection` - Teste de XSS
- `html-injection-testing` - Teste de HTML injection

#### Ações
1. Testar reflected XSS
2. Testar stored XSS
3. Testar DOM-based XSS
4. Testar filtros XSS
5. Documentar descobertas

#### Prompts para Copiar e Colar
```
Use @xss-html-injection to test for cross-site scripting
```

### Fase 4: Teste de Autenticação

#### Habilidades a Invocar
- `broken-authentication` - Teste de autenticação

#### Ações
1. Testar credential stuffing
2. Testar proteção contra força bruta
3. Testar gerenciamento de sessão
4. Testar políticas de senha
5. Testar implementação de MFA

#### Prompts para Copiar e Colar
```
Use @broken-authentication to test authentication security
```

### Fase 5: Teste de Controle de Acesso

#### Habilidades a Invocar
- `idor-testing` - Teste de IDOR
- `file-path-traversal` - Traversal de path

#### Ações
1. Testar escalação de privilégio vertical
2. Testar escalação de privilégio horizontal
3. Testar vulnerabilidades IDOR
4. Testar traversal de diretório
5. Testar acesso não autorizado

#### Prompts para Copiar e Colar
```
Use @idor-testing to test for insecure direct object references
```

```
Use @file-path-traversal to test for path traversal
```

### Fase 6: Security Headers

#### Habilidades a Invocar
- `api-security-best-practices` - Security headers

#### Ações
1. Verificar implementação de CSP
2. Validar configuração de HSTS
3. Testar X-Frame-Options
4. Verificar X-Content-Type-Options
5. Validar política de referrer

#### Prompts para Copiar e Colar
```
Use @api-security-best-practices to audit security headers
```

### Fase 7: Relatório

#### Habilidades a Invocar
- `reporting-standards` - Relatório de segurança

#### Ações
1. Documentar vulnerabilidades
2. Avaliar níveis de risco
3. Fornecer remediação
4. Criar proof of concept
5. Gerar relatório

#### Prompts para Copiar e Colar
```
Use @reporting-standards to create security report
```

## Checklist OWASP Top 10

- [ ] A01: Broken Access Control
- [ ] A02: Cryptographic Failures
- [ ] A03: Injection
- [ ] A04: Insecure Design
- [ ] A05: Security Misconfiguration
- [ ] A06: Vulnerable Components
- [ ] A07: Authentication Failures
- [ ] A08: Software/Data Integrity
- [ ] A09: Logging/Monitoring
- [ ] A10: SSRF

## Portais de Qualidade

- [ ] Todos os OWASP Top 10 testados
- [ ] Vulnerabilidades documentadas
- [ ] Proof of concepts capturados
- [ ] Remediação fornecida
- [ ] Relatório gerado

## Bundles de Fluxo de Trabalho Relacionados

- `security-audit` - Auditoria de segurança
- `api-security-testing` - Segurança de API
- `wordpress-security` - Segurança de WordPress