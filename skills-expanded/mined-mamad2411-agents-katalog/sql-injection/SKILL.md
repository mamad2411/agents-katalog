---
name: sql-injection
description: Detecção e remediação de injeção de SQL em aplicações web.
domain: web
subdomain: injection
tags: [owasp, injection, database]
cwe: CWE-89
owasp: "A03:2021"
mitre_attack: T1190
nist_csf: PR.DS
---

# When to Use
Aplique quando um finding indicar entrada de usuário concatenada em consultas
SQL, erros de banco expostos, ou quando ferramentas (nuclei/sqlmap) reportarem
injeção. Injeção de SQL permite ler/alterar dados e, por vezes, executar código.

# Prerequisites
- Escopo autorizado incluindo a aplicação e seu backend.
- Ambiente de teste isolado (nunca contra produção de terceiros).

# Workflow
1. Identificar parâmetros que chegam ao banco (query, POST, headers, cookies).
2. Testar payloads de detecção (aspas, operadores booleanos, time-based) apenas
   em escopo autorizado.
3. Confirmar com evidência reproduzível (diferença de resposta / tempo).
4. Classificar impacto (leitura, escrita, RCE via stacked queries).

# Verification
Confirme que consultas parametrizadas/prepared statements bloqueiam os payloads
que antes tinham efeito. Sem resposta anômala = mitigado.

# Remediation
Use consultas parametrizadas (prepared statements) ou ORM com binding de
parâmetros; nunca concatene entrada do usuário em SQL. Aplique validação de
entrada (allow-list), menor privilégio no usuário de banco e tratamento de erro
que não vaze detalhes internos. Referência: OWASP SQL Injection Prevention
Cheat Sheet.
