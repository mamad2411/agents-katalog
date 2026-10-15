---
name: planejar-no-track
description: Use when planning or breaking a Track feature/RFs into tasks, estimating EP, or the user asks to decompose work before implementation — requires MCP context and human confirmation before create_feature_tasks
---

# Planejar no Track

## Visão geral

Transformar feature/RFs do Track em tasks de dev com EP consistente — **proposta primeiro, gravação só após o humano confirmar**.

**Anuncie:** "Usando planejar-no-track para decompor o trabalho."

**Princípio:** sem confirmação humana, nenhuma `create_feature_tasks`.

## Lei de ferro

```
NÃO GRAVAR TASKS SEM CONFIRMAÇÃO EXPLÍCITA DO HUMANO
```

"Pode criar", "pode gravar", "confirma" = ok.  
Silêncio, "parece bom", ou seguir implementando ≠ confirmação de create.

## Processo

### 1. Contexto MCP (obrigatório)

Se `hous3_health` / tools de planejamento retornarem **401 / 403 / token expirado** → **PARE** e invoque `setup`. Só continue com MCP autenticado.

1. Identificar `projectId` + `releaseId` (ou `sourceRoadmapId` aceito por `get_release_planning_context`)
2. Chamar `get_release_planning_context` com `includeExistingTasks: true`
3. Se ambíguo: `search_projects` / perguntar — **não** chutar feature vizinha
4. Ler `scoringGuide` e, se preciso, recurso de rubrica EP do MCP

### 1b. Gate de clareza (obrigatório antes da tabela)

Antes de analisar código ou montar a tabela de tasks, avalie se o escopo está **planejável**.

Trate como **vago** (e **PARE** este skill) se qualquer um for verdade para a feature/RFs em foco:

- RF ou acceptance só repete o título / é genérico demais (“funcionar bem”, “melhorar UX”, “etc.”)
- Falta critério observável de pronto (não dá para saber o que testar)
- Persona / problema / fora-de-escopo contraditórios ou ausentes quando o pedido depende disso
- Humano ainda está explorando trade-offs de produto (não só decomposição técnica)
- Você precisaria **chutar** acceptance para escrever a task

Se vago:

1. Anuncie o gap em 1 frase
2. Invoque **`esclarecer-antes-de-planejar`**
3. **Não** mostre tabela de tasks e **não** chame `create_feature_tasks` até o desenho ser aprovado e você retomar este skill

Se estiver claro: siga para o passo 2.

Perguntas pontuais de decomposição técnica (1–3) *dentro* deste skill ainda são ok quando o produto já está fechado (ex.: “preferência de endpoint path?”). Isso **não** substitui `esclarecer-antes-de-planejar` quando o *quê* ainda é nebuloso.

### 2. Analisar localmente

- Mapear RFs → caminhos de código no repo (MCP não lê o git)
- Preferir **uma task por RF** (várias tasks por RF grande ok; nunca uma task cobrindo vários RFs)
- Separar camadas: backend / frontend / docs / automação quando fizer sentido
- EP só: **1, 2, 3, 5, 8** — preferir quebrar a EP 8
- Calibrar com `scoringGuide` e anchors da feature

### 3. Propor (tabela)

Mostre tabela antes de qualquer write:

| Título sugerido | RFs (`coveredRequirementIds`) | Tipo | EP | Justificativa curta |
|-----------------|-------------------------------|------|----|---------------------|

Padrão de título: `[Back] RF-00N — …` / `[Front] RF-00N — …` / `[Docs] RF-00N — …`

**Anti-placeholder na tabela:** proibido título/justificativa com “TBD”, “etc.”, “implementar feature”, “ajustar conforme necessário”. Cada linha precisa de RF(s) concretos e EP calibrado.

### 3b. Self-review da proposta (antes de pedir create)

1. **Cobertura:** cada RF **alta** (e ideally cada RF no escopo) aponta para ≥1 task? Liste gaps
2. **1 task ≠ N RFs:** nenhuma linha cobre vários RFs
3. **Placeholder scan:** busque vaguidão na tabela; corrija inline
4. **EP:** algum 8 que dá para partir? Prefira partir

Só então pergunte: **"Posso criar essas tasks no Track?"**

### 4. Gravar (só se sim)

- `create_feature_tasks` com `coveredRequirementIds` e `codeContext` conciso (sem secrets, sem dump)
- `list_squad_members` se for atribuir `responsibleId` / `reviewerId` por nome
- Releia contexto ou `list_my_tasks` para verificar

### 5. Se o humano disser não / ainda não

Pare. Ajuste a proposta. **Zero** calls de create.

## Não faça

- Setar `originalReleaseId` em tasks novas (só rollover)
- Criar design tasks quando `requiresDesign` é false
- Pular revisão humana
- Enviar credenciais / `.env` / arquivos inteiros no MCP
- Fuzzy-match de feature por nome parecido fora do escopo do projeto/release

## Sinais vermelhos

| Pensamento | Realidade |
|------------|-----------|
| "É óbvio, já crio" | Proposta → confirmação → create |
| "Ele disse 'bora' = pode criar" | Confirme o **plano de tasks**, não só a intenção de trabalhar |
| "EP 8 está fino" | Prefira split |
| "Uma task para três RFs é mais simples" | Proibido no método Track |
| "RF vago, mas eu invento acceptance na task" | Gate 1b → `esclarecer-antes-de-planejar` |
| "Faço as tasks e o PM ajusta depois" | Escopo fechado primeiro; tasks vêm depois |
| "RF alta ficou sem task, depois a gente vê" | Self-review 3b — cobertura antes do create |
| "Justificativa: implementar o RF" | Placeholder — diga o quê muda |
