---
name: esclarecer-antes-de-planejar
description: Use when product intent, feature shape, or RF/acceptance is still vague before Track task breakdown — key clarifying questions and a short approved design; also when planejar-no-track detects ambiguous scope
---

# Esclarecer antes de planejar

## Visão geral

Fechar **o quê** e **por quê** antes de decompor em tasks no Track.

**Anuncie:** "Usando esclarecer-antes-de-planejar para fechar o escopo."

**Princípio:** perguntas-chave + desenho curto aprovado → só então `planejar-no-track`.  
Não é o Superpowers `brainstorming` (sem design doc obrigatório, sem `writing-plans`).

## Lei de ferro

```
NÃO CRIAR TASKS / NÃO IMPLEMENTAR ENQUANTO O DESENHO NÃO ESTIVER APROVADO
NÃO PULAR PARA A TABELA DE TASKS DO planejar-no-track
```

`create_feature_tasks`, `implementar-task` e edições de código de produção ficam **bloqueados** até o humano aprovar o desenho deste skill.

## Quando usar

- Ideia / pedido ainda em linguagem de produto (“quero X”), sem RFs claros
- Feature no Track existe, mas RF/acceptance é vago, contraditório ou genérico demais
- Há trade-offs reais (escopo, persona, superfície, critério de pronto) sem decisão
- `planejar-no-track` detectou ambiguidade e redirecionou para cá

**Quando NÃO usar**

- RFs e acceptance já estão claros → vá direto a `planejar-no-track`
- Task já escopada pronta para código → `implementar-task`
- Só falta auth MCP → `setup`

## Processo

### 1. Contexto (leve) — antes de perguntar

1. Se MCP disponível: `get_release_planning_context` / feature + RFs existentes (não inventar)
2. Se **401 / 403** → `setup`, depois volte
3. Se não houver item no Track ainda: esclareça no chat; **não** invente `featureId`/`req_*`
4. **Não pergunte o que o Track/contexto já responde** (nome da feature, RFs existentes, release) — use isso e só pergunte gaps reais

### 1b. Scope check (antes das perguntas)

Se o pedido cobrir **vários subsistemas independentes** (ex.: CRM + portal + billing numa tacada):

1. Diga que precisa decompor
2. Proponha fatias ordenadas (cada uma planejável sozinha)
3. Esclareça **só a primeira fatia** neste skill — não feche um “desenho monstro”

### 2. Perguntas-chave (uma por mensagem)

Foque só no que desbloqueia o plano. Preferir múltipla escolha. **Uma pergunta por vez.**

Perguntas típicas (escolha as necessárias — não roteiro fixo de 10):

1. **Quem** sofre / usa? (persona)
2. **Problema** que some se der certo? (dor / outcome)
3. **Pronto** = o quê? (1–3 critérios de aceite observáveis)
4. **Fora de escopo** nesta fatia? (o que explicitamente não entra) — **YAGNI**
5. **Trade-off** crítico? (ex.: só squad vs portfólio; blocking vs soft signal)

Pare quando der para escrever um desenho curto sem chute.

### 3. Abordagens (só se houver decisão real)

Se houver 2+ caminhos com trade-off material: apresente **2–3 opções**, recomende uma, peça escolha.  
Se for óbvio, pule — não encene brainstorming.

### 4. Desenho curto (no chat)

Em seções compactas (escala ao tamanho do problema). **YAGNI:** corte o que não é necessário para o outcome desta fatia.

- Objetivo / persona
- Escopo in / out
- Critérios de aceite (bullet observáveis)
- Superfícies tocadas (home, API, Inbox… — alto nível)
- Riscos ou dependências (se houver)

Se o desenho for longo: valide **por seção** (“essa parte ok?”) antes de pedir aprovação global.

### 4b. Self-review do desenho (antes de pedir aprovação)

Checklist rápido — corrija inline se achar problema:

1. **Placeholder:** “TBD”, “etc.”, “melhorar UX”, aceite não observável?
2. **Consistência:** persona/escopo/aceite se contradizem?
3. **Ambiguidade:** algum bullet dá para ler de 2 jeitos? Escolha um e deixe explícito
4. **Escopo:** ainda parece multi-subsistema? Volte ao 1b

Só então **peça aprovação explícita** (“pode seguir para planejar tasks?” / “aprova esse desenho?”).

Não grave `docs/superpowers/specs/…` por padrão. Só escreva doc se o humano pedir.

### 5. Handoff

Com desenho aprovado:

1. Se a feature/RFs no Track **ainda não refletem** o desenho → diga o que precisa atualizar (humano/MCP) antes ou junto do planejamento; não invente sync silenciosa
2. Invoque **`planejar-no-track`** para a tabela de tasks + confirmação + `create_feature_tasks`

## Não faça

- Virar implementação (“já deixo o endpoint pronto”)
- Criar tasks “provisórias” para destravar
- Copiar o ritual completo do Superpowers (`writing-plans`, spec file, visual companion obrigatório)
- Fazer 8 perguntas quando 2 bastam
- Assumir acceptance a partir do título da feature
- Perguntar o que o MCP/Track já mostrou
- Empacotar 3 produtos num único desenho “aprovado”

## Sinais vermelhos

| Pensamento | Realidade |
|------------|-----------|
| "Já entendi, vou montar as tasks" | Self-review + desenho aprovado primeiro |
| "Pergunto tudo de uma vez" | Uma pergunta por mensagem |
| "RF genérico serve" | Gate do `planejar-no-track` vai te devolver aqui |
| "Design doc formal é obrigatório" | Só se o humano pedir |
| "Superpowers brainstorming é a mesma skill" | Não — este é leve e Track-first |
| "Pergunto a persona mesmo com RF claro no Track" | Contexto primeiro; só gaps |
| "Cabe tudo nesta release" | YAGNI + fora de escopo explícito |
