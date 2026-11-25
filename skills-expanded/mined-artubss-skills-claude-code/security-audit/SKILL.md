---
name: security-audit
description: "Fluxo de auditoria de segurança abrangente cobrindo testes de aplicações web, segurança de API, testes de penetração, varredura de vulnerabilidades e endurecimento de segurança."
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Pacote de Fluxo de Trabalho de Auditoria de Segurança

## Visão Geral

Fluxo de trabalho de auditoria de segurança abrangente para aplicações web, APIs e infraestrutura. Este pacote orquestra skills para testes de penetração, avaliação de vulnerabilidades, varredura de segurança e remediação.

## Quando Usar Este Fluxo de Trabalho

Use este fluxo de trabalho quando:
- Realizando auditorias de segurança em aplicações web
- Testando segurança de API
- Conduzindo testes de penetração
- Fazendo varredura de vulnerabilidades
- Endurecendo segurança de aplicações
- Avaliações de segurança de conformidade

## Fases do Fluxo de Trabalho

### Fase 1: Reconhecimento

#### Skills a Invocar
- `scanning-tools` - Varredura de segurança
- `shodan-reconnaissance` - Buscas no Shodan
- `top-web-vulnerabilities` - OWASP Top 10

#### Ações
1. Identificar escopo do alvo
2. Coletar inteligência
3. Mapear superfície de ataque
4. Identificar tecnologias
5. Documentar achados

#### Prompts Prontos para Copiar
```
Use @scanning-tools to perform initial reconnaissance
```

```
Use @shodan-reconnaissance to find exposed services
```

### Fase 2: Varredura de Vulnerabilidades

#### Skills a Invocar
- `vulnerability-scanner` - Análise de vulnerabilidades
- `security-scanning-security-sast` - Análise estática
- `security-scanning-security-dependencies` - Varredura de dependências

#### Ações
1. Executar scanners automatizados
2. Realizar análise estática
3. Varredura de dependências
4. Identificar configurações incorretas
5. Documentar vulnerabilidades

#### Prompts Prontos para Copiar
```
Use @vulnerability-scanner to scan for OWASP Top 10 vulnerabilities
```

```
Use @security-scanning-security-dependencies to audit dependencies
```

### Fase 3: Testes de Aplicação Web

#### Skills a Invocar
- `top-web-vulnerabilities` - Vulnerabilidades OWASP
- `sql-injection-testing` - SQL injection
- `xss-html-injection` - Testes XSS
- `broken-authentication` - Testes de autenticação
- `idor-testing` - Testes IDOR
- `file-path-traversal` - Traversal de caminho
- `burp-suite-testing` - Testes com Burp Suite

#### Ações
1. Testar falhas de injeção
2. Testar mecanismos de autenticação
3. Testar gerenciamento de sessão
4. Testar controles de acesso
5. Testar validação de entrada
6. Testar headers de segurança

#### Prompts Prontos para Copiar
```
Use @sql-injection-testing to test for SQL injection vulnerabilities
```

```
Use @xss-html-injection to test for cross-site scripting
```

```
Use @broken-authentication to test authentication security
```

### Fase 4: Testes de Segurança de API

#### Skills a Invocar
- `api-fuzzing-bug-bounty` - Fuzzing de API
- `api-security-best-practices` - Segurança de API

#### Ações
1. Enumerar endpoints de API
2. Testar autenticação/autorização
3. Testar rate limiting
4. Testar validação de entrada
5. Testar tratamento de erros
6. Documentar vulnerabilidades de API

#### Prompts Prontos para Copiar
```
Use @api-fuzzing-bug-bounty to fuzz API endpoints
```

### Fase 5: Testes de Penetração

#### Skills a Invocar
- `pentest-commands` - Comandos de testes de penetração
- `pentest-checklist` - Planejamento de pentest
- `ethical-hacking-methodology` - Metodologia de ethical hacking
- `metasploit-framework` - Metasploit

#### Ações
1. Planejar teste de penetração
2. Executar cenários de ataque
3. Explorar vulnerabilidades
4. Documentar prova de conceito
5. Avaliar impacto

#### Prompts Prontos para Copiar
```
Use @pentest-checklist to plan penetration test
```

```
Use @pentest-commands to execute penetration testing
```

### Fase 6: Endurecimento de Segurança

#### Skills a Invocar
- `security-scanning-security-hardening` - Endurecimento de segurança
- `auth-implementation-patterns` - Autenticação
- `api-security-best-practices` - Segurança de API

#### Ações
1. Implementar controles de segurança
2. Configurar headers de segurança
3. Configurar autenticação
4. Implementar autorização
5. Configurar logging
6. Aplicar patches

#### Prompts Prontos para Copiar
```
Use @security-scanning-security-hardening to harden application security
```

### Fase 7: Relatório

#### Skills a Invocar
- `reporting-standards` - Relatórios de segurança

#### Ações
1. Documentar achados
2. Avaliar níveis de risco
3. Fornecer passos de remediação
4. Criar resumo executivo
5. Gerar relatório técnico

## Lista de Verificação de Testes de Segurança

### OWASP Top 10
- [ ] Injeção (SQL, NoSQL, OS, LDAP)
- [ ] Autenticação Quebrada
- [ ] Exposição de Dados Sensíveis
- [ ] XML External Entities (XXE)
- [ ] Controle de Acesso Quebrado
- [ ] Configuração de Segurança Inadequada
- [ ] Cross-Site Scripting (XSS)
- [ ] Desserialização Insegura
- [ ] Usando Componentes com Vulnerabilidades Conhecidas
- [ ] Logging e Monitoramento Insuficientes

### Segurança de API
- [ ] Mecanismos de autenticação
- [ ] Verificações de autorização
- [ ] Rate limiting
- [ ] Validação de entrada
- [ ] Tratamento de erros
- [ ] Headers de segurança

## Portais de Qualidade

- [ ] Todos os testes planejados executados
- [ ] Vulnerabilidades documentadas
- [ ] Provas de conceito capturadas
- [ ] Avaliações de risco concluídas
- [ ] Passos de remediação fornecidos
- [ ] Relatório gerado

## Pacotes de Fluxo de Trabalho Relacionados

- `development` - Práticas seguras de desenvolvimento
- `wordpress` - Segurança WordPress
- `cloud-devops` - Segurança em nuvem
- `testing-qa` - Testes de segurança