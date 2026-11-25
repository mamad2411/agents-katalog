---
name: route-security-tester
description: >
  Testa rotas de API e faz varredura de segurança (DAST leve) contra alvos
  autorizados. Use para testar rotas, route testing, exercitar endpoints via
  curl, mapear rotas de um backend (Express/Fastify/Nest, Flask/FastAPI/Django,
  Go, Spring, Rails, Laravel, .NET, actix-web e outros), rodar matriz de auth
  testing e access control, detectar vulnerabilidades — SQLi, NoSQLi, XSS,
  command injection, path traversal — via fuzzing e injection em nível de
  detecção, gerar coleções Insomnia/Postman v2.1/OpenAPI (swagger), e produzir
  relatório com achados de segurança e sugestões. Dispare quando o usuário
  mencionar: testar rotas, route testing, curl endpoints, DAST, fuzzing,
  injection, SQLi, XSS, auth testing, access control, insomnia, postman,
  openapi, swagger, vulnerabilidade, coleção de rotas, testar minha API,
  varredura de segurança, pentest da própria aplicação. Agnóstica de
  linguagem e framework: tudo específico do alvo é declarado em runtime.
user-invocable: true
argument-hint: "[modo: discovery|collections|functional|auth|injection|report] [--src <path>] [--url <baseUrl>] [--out <path>]"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# /route-security-tester

Skill neutra e agnóstica de linguagem para testar rotas de API e avaliar a
segurança de **aplicações próprias ou explicitamente autorizadas**. Opera em 6
modos independentes. Nada específico do alvo é hardcoded — o usuário declara
tudo em runtime.

---

## ⛔ GUARDRAIL — leia e aplique ANTES de qualquer requisição

Estas regras são inegociáveis. Não gere nem dispare tráfego que as viole.

1. **Alvo autorizado apenas.** Só execute testes contra `localhost`,
   `127.0.0.1`, ambientes de `staging`/`dev`, OU um host que o usuário declarar
   **explicitamente** como autorizado nesta conversa. Se o alvo não se encaixa,
   **pare e pergunte** — não assuma.
2. **Rate limit sempre.** Insira atraso entre requisições (padrão: ≥150ms,
   `--rate` configurável) e limite concorrência para não sobrecarregar o alvo.
3. **Verbos destrutivos exigem confirmação.** `DELETE`, e `PUT`/`PATCH` que
   alterem estado em massa, só disparam após confirmação **explícita** do
   usuário, rota a rota. Nunca em lote silencioso.
4. **Nunca aponte fuzzing/injection para produção** sem autorização explícita e
   registrada nesta conversa. Na dúvida, trate como produção e pare.
5. **Propósito.** Esta skill serve para o dono testar a própria API ou um alvo
   sob autorização. Os probes são vetores canônicos de **detecção** (do tipo
   usado por ferramentas DAST legítimas), não exploits armados. Não gere
   malware nem payloads de exploração.

Se qualquer entrada obrigatória (alvo, auth, autorização) estiver faltando,
**pergunte antes de agir**.

---

## Entradas (o usuário declara em runtime — nunca hardcode)

- **`--src <path>`** — caminho do código-fonte a analisar (para DISCOVERY).
- **`--url <baseUrl>`** — base URL do alvo (ex.: `http://localhost:3000`).
- **Config de auth** — esquema + papéis/escopos existentes. Esquemas suportados:
  `Bearer token`, `cookie de sessão`, `API key` (header/query), `Basic`,
  `OAuth`, ou `header custom`. Auth por wallet ou qualquer modelo incomum entra
  **apenas** como "esquema custom" configurável — jamais assumido por padrão.
- **Autorização** — confirmação de que o alvo pode ser testado (guardrail #1).
- **`--out <path>`** (opcional) — diretório onde o REPORT será salvo. Se
  omitido, usa o default descrito no Modo 6.

Colete o que faltar perguntando de forma objetiva antes de rodar o modo pedido.

---

## Roteamento de modos

Cada modo é invocável isoladamente. Determine o modo a partir do argumento ou
da intenção do usuário. Se nenhum modo for dado, sugira começar por DISCOVERY.

| Modo | Quando | Reference a ler |
|---|---|---|
| DISCOVERY | Mapear rotas a partir do código | `references/discovery.md` |
| COLLECTIONS | Exportar Insomnia/Postman/OpenAPI (on-demand) | `references/collections-export.md` |
| FUNCTIONAL | Exercitar rotas via curl (status/tempo/shape) | `references/functional-testing.md` |
| AUTH | Matriz de auth & access control | `references/auth-access-control.md` |
| INJECTION | Fuzzing + injection nível detecção | `references/injection-fuzzing.md` |
| REPORT | Consolidar tabela + notas + bloco agent-ready | `references/report-templates.md` |

Leia o reference correspondente **sob demanda**, só quando entrar no modo
(progressive disclosure). Não pré-carregue todos.

---

## Modo 1 — DISCOVERY

Objetivo: extrair o **mapa de rotas** do código-fonte, sem chutar.

1. Confirme `--src`. Detecte a linguagem/framework por arquivos-âncora e
   padrões de rota (ver `references/discovery.md`).
2. Reconheça frameworks comuns: Node (Express/Fastify/Nest), Python
   (Flask/FastAPI/Django), Go, Java/Spring, Ruby/Rails, PHP/Laravel, .NET,
   Rust (actix-web).
3. Para cada rota, extraia: **método HTTP**, **path** (com params de path),
   **query params**, **body/schema esperado**, e **requisito de auth**
   (rota pública vs. protegida, papel/escopo exigido).
4. **Fallback genérico** quando o framework não for reconhecido (inclui outros
   de Rust como axum/rocket, ou stacks exóticas): ler spec OpenAPI existente no
   repo, anotações/macros/decorators de rota, ou aceitar uma **lista manual**
   de rotas fornecida pelo usuário.
5. Produza um mapa estruturado (uma linha por rota) que alimenta todos os
   outros modos. Guarde-o em memória para a sessão.

Detalhes e assinaturas por framework: **`references/discovery.md`**.

---

## Modo 2 — COLLECTIONS EXPORT (on-demand — NÃO roda automático)

**ANTES de gerar qualquer arquivo, PERGUNTE ao usuário se ele quer gerar as
coleções agora.** Só prossiga após confirmação explícita — isso evita gasto
desnecessário de tokens quando ele só quer testar ou reportar.

Ao confirmar, gere a partir do mapa do DISCOVERY:

- `insomnia.json` — export nativo Insomnia.
- `postman_collection.json` — **formato v2.1**.
- `openapi.yaml` — **OpenAPI 3.x**.

Regras:
- Organize por **recurso** (agrupar rotas do mesmo prefixo/entidade).
- Use env vars **genéricas**: `{{baseUrl}}`, `{{authToken}}`, `{{apiKey}}`.
- **NUNCA hardcode segredos** — tokens/keys ficam como variáveis vazias.

Schemas e templates prontos: **`references/collections-export.md`**.

---

## Modo 3 — FUNCTIONAL

Objetivo: exercitar cada rota **ao vivo** via curl, nos caminhos válidos e
inválidos, e registrar o comportamento observado.

1. Reafirme o guardrail (alvo autorizado, rate limit). Para verbos destrutivos,
   **peça confirmação** antes de disparar (guardrail #3).
2. Para cada rota, dispare requisições cobrindo o espectro de status esperado:
   `200/201/204`, `400/401/403/404/405/409/422`, `429`, `500/502/503`.
3. Registre por requisição: **status**, **tempo de resposta (ms)**, **tamanho
   do body**, e **shape** (estrutura/campos-chave, não o dump inteiro).
4. Use inputs válidos e inválidos por rota (payloads faltando, tipos errados,
   valores fora de range) para provocar os 4xx corretos.

Matriz de status, receitas de curl e padrões de input: **`references/functional-testing.md`**.

---

## Modo 4 — AUTH & ACCESS CONTROL

Objetivo: rodar uma **matriz configurável** sobre o esquema de auth **declarado
pelo usuário** — nunca assumir um modelo específico.

Cenários da matriz (adaptados ao esquema declarado):
- Sem credencial.
- Credencial inválida (malformada).
- Credencial expirada.
- Credencial adulterada (assinatura/claim alterada).
- Papel/escopo insuficiente tentando acessar rota privilegiada.
- Escalonamento de privilégio **horizontal** (acessar recurso de outro usuário
  do mesmo nível).
- Escalonamento de privilégio **vertical** (usuário comum tentando ação de
  admin).

Para cada célula: status esperado vs. observado. Divergência (ex.: `200` onde
deveria ser `401/403`) é um achado de segurança — classifique a severidade.

Matriz completa por esquema (Bearer/cookie/API key/Basic/OAuth/custom):
**`references/auth-access-control.md`**.

---

## Modo 5 — INJECTION & FUZZING

**Reforce o guardrail: só em alvo autorizado; nunca produção sem autorização.**

Objetivo: revelar se o input é **sanitizado** — nível de **detecção**, não
exploração armada.

Classes de probe (wordlists no reference):
- SQL injection (SQLi)
- NoSQL injection (NoSQLi)
- XSS refletido
- Command injection
- Path traversal
- Input malformado / oversized (limites, encoding, tipos)

Para cada param injetável (query/body/path), envie os probes com rate limit e
interprete os **sinais de vulnerabilidade** na resposta (erro de SQL vazado,
reflexão do payload sem escape, delay anômalo, stack trace, mudança de status
inesperada). Reporte sinal + probe + rota; não tente encadear exploração.

Wordlists e tabela de sinais→veredito: **`references/injection-fuzzing.md`**.

---

## Modo 6 — REPORT

Consolide os resultados dos modos rodados em **2 arquivos + 1 saída opcional**.

**Sempre** salve os arquivos dentro de uma pasta dedicada, nunca soltos na raiz
do projeto:

- **Default:** `security-reports/<AAAA-MM-DD>-<alvo-slug>/` (criada via `mkdir -p`
  antes de escrever os arquivos). `<alvo-slug>` deriva do `--url`/host testado
  (ex.: `staging`, `localhost-3000`).
- **Override:** se `--out <path>` foi informado, use esse diretório em vez do
  default.
- Se a pasta `security-reports/` for nova no repo, verifique se existe
  `.gitignore` e sugira adicionar a entrada `security-reports/` (achados de
  segurança não devem ir para o histórico do git).

1. **`responses-table.md`** — tabela com colunas exatamente:
   `Rota | Método | Cenário | Status | Tempo(ms) | Tamanho | Observação`

2. **`notes.md`** — seções **nesta ordem fixa**:
   1. Visão geral do teste (escopo, alvo, o que foi rodado)
   2. Comportamento por rota
   3. Achados de segurança — cada um com severidade: `baixa` / `média` /
      `alta` / `crítica`
   4. Sugestões de performance
   5. Sugestões de segurança
   6. Sugestões de estrutura

3. **Saída AGENT-READY (opcional)** — um bloco de prompt reutilizável, já
   formatado, resumindo achados e ações sugeridas, pronto para outra
   skill/agente consumir. **Esta skill APENAS produz o bloco de texto; NÃO cria
   nem orquestra agentes.**

Templates exatos dos três: **`references/report-templates.md`**.

---

## Success Criteria

- [ ] Guardrail confirmado (alvo autorizado, rate limit) antes de qualquer tráfego.
- [ ] Modo pedido roda isoladamente sem exigir os outros.
- [ ] DISCOVERY produz mapa de rotas com método, params e requisito de auth.
- [ ] COLLECTIONS só roda após confirmação explícita; sem segredos hardcoded.
- [ ] Verbos destrutivos só disparam com confirmação rota a rota.
- [ ] REPORT gera `responses-table.md` + `notes.md` nas seções fixas; bloco
      agent-ready só se solicitado.
- [ ] Nenhuma referência a projeto/env/rota/convenção específica — 100% neutra.
