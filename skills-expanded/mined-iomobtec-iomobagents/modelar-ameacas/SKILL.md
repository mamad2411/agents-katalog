---
name: modelar-ameacas
description: "Analisa componentes com a metodologia STRIDE e produz um threat model com os controles obrigatórios por camada. Use quando o dev-security ou o arquiteto vai modelar ameaças antes do desenvolvimento."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: modelar-ameacas

Modela ameaças de segurança de um microsserviço com a metodologia STRIDE e define os controles obrigatórios por camada antes do desenvolvimento.

**Agente:** `dev-security`, `arquiteto`  
**Output:** `plans/dev-security/<ticket>-threat-model.md`  
**Referências rápidas:** `References/security-checklist.md`

---

## Quando usar

Após o arquiteto definir os componentes de um microsserviço (endpoints, eventos, dados, integrações). Executar antes do início do desenvolvimento para identificar controles obrigatórios por camada.

---

## Processo

### Passo 1 — Inventariar superfície de ataque

Listar todos os componentes que receberão entrada externa ou processarão dados sensíveis:

```
Para cada componente, identificar:
- Tipo: endpoint REST | consumer de evento | formulário de UI | webhook | upload
- Dados de entrada: quais campos, de quem vêm (usuário, sistema externo, fila)
- Dados de saída: o que retorna, para quem — quais propriedades do objeto são expostas?
- Dados persistidos: tabelas, campos, sensibilidade (PII? financeiro? credencial?)
- Integrações: sistemas externos chamados, serviços internos dependentes
- Perfil de acesso: público | autenticado | role específica | apenas sistemas internos
- Fluxo de negócio: é fluxo sensível a automação? (compra, reserva, cupom, registro)
```

Para a **superfície de API** especificamente, também responder:

```
- Quantas versões da API existem? As versões antigas estão documentadas e monitoradas?
- Há endpoints de terceiros que este serviço consome? Como os dados são validados?
- Os DTOs de response expõem apenas os campos necessários para cada consumidor?
```

### Passo 2 — Aplicar STRIDE por componente

Para cada componente listado no Passo 1, responder as 6 perguntas STRIDE:

| Ameaça | Pergunta a responder |
|---|---|
| **S**poofing | Um atacante pode se passar por usuário legítimo ou sistema confiável para acessar este componente? |
| **T**ampering | Um atacante pode modificar dados em trânsito (request/response) ou em repouso (banco, fila) para alterar o comportamento? |
| **R**epudiation | Um usuário pode executar uma ação e depois negar que a executou? Há audit trail suficiente? |
| **I**nformation Disclosure | Dados sensíveis podem vazar na response, nos logs, em mensagens de erro ou em headers? |
| **D**enial of Service | Um atacante pode tornar este componente indisponível ou degradar seu desempenho enviando requisições fabricadas? |
| **E**levation of Privilege | Um usuário comum pode ganhar acesso a dados ou ações que deveriam ser restritas a outro papel? |

Para **endpoints REST**, responder também as perguntas adicionais do OWASP API Security Top 10 2023:

| Vetor API | Pergunta a responder | Referência |
|---|---|---|
| BOLA (API1) | Um usuário autenticado pode acessar ou modificar objetos de outro usuário manipulando IDs no request? | `appsec.md §4` |
| BOPLA (API3) | A response expõe propriedades que este consumidor não deveria ver? O input aceita campos privilegiados como `role` ou `isAdmin`? | `appsec.md §14` |
| Função (API5) | A função tem guard de role declarado? Um usuário sem privilégio consegue chamar esta função via HTTP? | `appsec.md §15` |
| Business Flow (API6) | Este endpoint faz parte de fluxo sensível a automação? O rate limit específico é suficiente contra bots? | `appsec.md §16` |
| Inventário (API9) | Este endpoint está documentado? Existe versão anterior sem os mesmos controles de segurança? | `appsec.md §17` |
| Consumo externo (API10) | Este componente consome API de terceiro? Os dados externos são validados antes de persistir ou repassar? | `appsec.md §18` |

### Passo 3 — Classificar risco

Para cada ameaça identificada como presente (Passo 2), classificar a severidade:

| Severidade | Critério |
|---|---|
| 🔴 CRITICAL | Exploração direta possível sem autenticação, ou com credenciais de usuário comum: RCE, SQL injection, acesso a dados de outros usuários |
| 🟠 HIGH | Exploração requer contexto específico mas o vetor está claro: IDOR com conta válida, JWT sem exp, XSS stored |
| 🟡 MEDIUM | Endurecimento necessário, mas exploração é difícil ou requer várias condições favoráveis: falta de rate limit em endpoint não-crítico, log com campo sensível |
| 🟢 LOW | Melhoria defensiva sem impacto direto: header de segurança ausente mas com CSP configurado, campo de log desnecessário mas não PII |

### Passo 4 — Definir controles obrigatórios

Para cada ameaça CRITICAL ou HIGH, definir o controle específico que deve ser implementado:

```
Controle deve incluir:
- O que implementar (ex: "@Throttle(5, 60) no endpoint de login")
- Por qual agente (dev-backend, dev-frontend, dev-bff)
- Referência ao guardrail (ex: appsec.md §12 — Rate limiting)
- Como verificar que foi implementado (critério testável)
```

### Passo 5 — Produzir o arquivo de threat model

Criar `plans/dev-security/<ticket>-<funcionalidade>-threat-model.md` com o template abaixo:

```markdown
# Threat Model — <ticket> — <funcionalidade>

**Data:** <data>
**Analista:** dev-security
**Baseado em:** spec do arquiteto + Guidelines/security/README.md

---

## Componentes analisados

| Componente | Tipo | Dados sensíveis | Integração externa |
|---|---|---|---|
| `POST /auth/login` | endpoint REST | email, senha | — |
| `OrderConsumer` | event consumer | userId, valor, PII do endereço | — |

---

## Riscos identificados

| Severidade | Componente | Ameaça STRIDE | Descrição | Controle necessário |
|---|---|---|---|---|
| 🔴 CRITICAL | `POST /auth/login` | D — DoS | Sem rate limit → brute force | `@Throttle(5, 60)` no endpoint |
| 🟠 HIGH | `GET /orders/:id` | E — Elev. Priv. | Sem verificação de ownership | Filtrar por `userId` do JWT |
| 🟡 MEDIUM | `OrderConsumer` | I — Info Disc. | Endereço completo nos logs | Mascarar endereço no log |

---

## Controles obrigatórios por agente de dev

### dev-backend
- [ ] Rate limit `@Throttle(5, 60)` no `POST /auth/login` — `appsec.md §12`
- [ ] Verificação de ownership em `GET /orders/:id`: `WHERE userId = req.user.id` — `appsec.md §4`
- [ ] Audit log em login bem-sucedido e falho com IP + userId — `appsec.md §9`

### dev-frontend
- [ ] (nenhum controle crítico identificado nesta entrega)

### dev-bff
- [ ] JWT validado antes de repassar ao upstream — `appsec.md §2`

---

## Riscos residuais aceitos

| Risco | Motivo de aceitação | Revisar em |
|---|---|---|
| <risco> | <justificativa de negócio ou técnica> | <data ou milestone> |

---

## Referências

- `Guardrails/appsec.md`
- `Guidelines/security/README.md §2` — Metodologia STRIDE
```

### Passo 6 — Reportar ao tech-lead

Após produzir o arquivo, reportar ao orquestrador com:

```
✅ Threat model concluído: plans/dev-security/<ticket>-threat-model.md

Resumo de riscos:
- 🔴 CRITICAL: <qtd> — <lista curta dos vetores>
- 🟠 HIGH: <qtd> — <lista curta>
- 🟡 MEDIUM: <qtd>

Controles obrigatórios que devem ser incluídos nos planos de dev:
- dev-backend: <lista de controles>
- dev-frontend: <lista de controles>
- dev-bff: <lista de controles>

Recomendação: tech-lead inclui os controles obrigatórios nas seções §2 ou §4.7
dos planos gerados pelo gerar-plano-tarefa para cada agente de dev.
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "O sistema é simples, não precisa de threat model" | Sistemas simples têm superfícies de ataque simples — mas ainda têm. 20 minutos de STRIDE podem evitar meses de breach response. |
| "Vou fazer o threat model depois da implementação" | O ponto do threat model é identificar controles ANTES de implementar. Fazer depois transforma-o em pentest tardio — mais caro de corrigir. |
| "O arquiteto já pensou em segurança no design" | Arquitetura e segurança são perspectivas distintas. O arquiteto pensa em conectividade; o threat model pensa em adversário. |
| "STRIDE é burocracia para sistemas pequenos" | STRIDE gasta 6 perguntas por componente. Cada pergunta não respondida é um vetor potencialmente aberto. |
| "Esse serviço é interno, sem exposição à internet" | Serviços internos são alvos de movimentação lateral após comprometimento inicial. "Interno" não elimina o modelo de ameaças. |

---

## Anti-padrões bloqueados

- Marcar ameaça como "Não se aplica" sem justificativa — toda ameaça deve ter resposta explícita
- Definir controle vago ("implementar autenticação") em vez de específico ("JWT com exp=15min via JwtModule")
- Omitir componentes de UI do threat model — formulários e telas têm superfície de ataque (XSS, CSRF)
- Produzir threat model sem listar responsável por cada controle
