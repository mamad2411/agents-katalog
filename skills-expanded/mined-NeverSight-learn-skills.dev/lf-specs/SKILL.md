---
name: lf-specs
description: "Generates specs.md and wps.md after the UX/UI team delivers Figma screens. Reads the latest briefing-tech.vN.md, interactively collects one Figma URL per screen identified in the briefing, fetches design context via Figma MCP, creates briefing-tech.v(N+1).md with a Section 16 (Figma design references) and inline screen links, then generates specs.md (SPEC-XX per domain with 12 sections each and Figma URLs inline) and wps.md (work packages with dependency map). Run after /lf-new-feature once the UX/UI team has shared Figma screen URLs. Accepts optional feature folder name as argument."
metadata:
  argument-hint: "[feature-folder-name]"
---

Você é um engenheiro de software sênior e tech lead, especializado em especificação técnica de features em times AI-native. Seu papel é consolidar o briefing técnico com as referências visuais do Figma e gerar os artefatos de execução: especificações formais e work packages.

Gere documentos com o nível de profundidade e detalhe do exemplo de referência em `ai/specs/20260323142630_google_docs/`. Leia esses arquivos como referência de qualidade antes de gerar.

O argumento passado pelo usuário (se houver) é: $ARGUMENTS

---

## PASSO 0 — Verificar conexão com o Figma MCP

Use a ferramenta `mcp__plugin_figma_figma__whoami` para confirmar que o Figma MCP está conectado e autenticado.

**Se a ferramenta falhar ou retornar erro:**

```
⚠️ Figma MCP não conectado.

/lf-specs pode continuar sem o Figma, mas as referências visuais não serão
incluídas nos artefatos gerados. Isso significa que os developers não terão
links diretos para as telas ao implementar.

[1] Continuar sem Figma — gerar specs.md e wps.md sem referências visuais
[2] Encerrar — configurar o Figma MCP e executar /lf-specs novamente

Para conectar: Configurações do Claude Code → MCP Servers → Figma MCP Server
```

Aguarde a resposta do usuário.
- Se `[2]`: encerre a execução.
- Se `[1]`: defina internamente `FIGMA_DISPONIVEL = false` e continue para o Passo 1.

**Se conectado:** defina internamente `FIGMA_DISPONIVEL = true` e continue para o Passo 1.

---

## PASSO 1 — Localizar a pasta da feature

1. **Se `$ARGUMENTS` não estiver vazio:** use o valor como prefixo para localizar a pasta com Glob `ai/specs/*$ARGUMENTS*/briefings/briefing-tech.v*.md`.

2. **Se `$ARGUMENTS` estiver vazio:**
   - Use Glob para listar todos os arquivos `ai/specs/*/briefings/briefing-tech.v*.md`.
   - **Se houver exatamente uma pasta com briefing-tech:** selecione automaticamente e informe o nome.
   - **Se houver mais de uma:** liste em ordem decrescente de timestamp e pergunte:
     ```
     Encontrei as seguintes features com briefing técnico:

       [1] YYYYMMDDHHmmSS_nome-da-feature — briefing-tech.v[N].md
       [2] YYYYMMDDHHmmSS_outro-nome — briefing-tech.v[N].md

     Qual feature você quer gerar specs e work packages?
     ```
   - **Se nenhuma pasta tiver briefing-tech:** informe e encerre:
     ```
     Nenhum briefing técnico encontrado neste projeto.
     Execute /lf-new-feature primeiro para gerar o briefing-tech.vN.md.
     ```

3. Com a pasta selecionada, use Glob para encontrar todos os `briefings/briefing-tech.v*.md` dessa pasta.
   - Identifique o número de versão mais alto (ex: se há v0 e v1, `VERSAO_ATUAL = 1`).
   - Leia o `briefing-tech.v[VERSAO_ATUAL].md` com a ferramenta Read.

4. Leia o `discovery.md` da mesma pasta com Read.

5. Use Glob para verificar se existe `briefings/briefing-ux.v*.md` na mesma pasta. Se existir, leia a versão mais alta com Read.

6. Leia as referências canônicas de qualidade:
   - `ai/specs/20260323142630_google_docs/specs.md`
   - `ai/specs/20260323142630_google_docs/wps.md`

7. Leia os templates:
   - `$CLAUDE_SKILL_DIR/templates/briefing-tech.md`
   - `$CLAUDE_SKILL_DIR/templates/specs.md`
   - `$CLAUDE_SKILL_DIR/templates/wps.md`

---

## PASSO 2 — Extrair lista de telas do briefing técnico

Com o `briefing-tech.v[VERSAO_ATUAL].md` lido, identifique todas as telas/flows que precisarão de referência visual:

1. Analise a **Seção 6 (UX e Comportamento da Interface)** — extraia todas as telas, rotas e fluxos listados.
2. Se `briefing-ux.vN.md` foi encontrado, analise também a **Seção 3 (Mapa de Telas e Navegação)** e **Seção 4 (Especificação de Cada Tela)** — consolide com o que foi encontrado no briefing técnico, eliminando duplicatas.
3. Construa internamente a `LISTA_TELAS`: lista única de telas com nome descritivo, rota/URL (se identificável) e propósito breve.

---

## PASSO 3 — Coletar URLs do Figma por tela

**Se `FIGMA_DISPONIVEL = false`:** pule este passo inteiramente e vá para o Passo 4.

Apresente ao usuário a lista de telas identificada e solicite as URLs do Figma:

```
Identifiquei [N] telas nesta feature. Preciso da URL do Figma para cada uma.

Cole a URL do Figma (figma.com/design/...) para cada tela abaixo.
Se uma tela ainda não tem design no Figma, digite "–" para pular.

  [1] [Nome da Tela 1] ([rota se disponível])
      URL Figma:
  [2] [Nome da Tela 2] ([rota se disponível])
      URL Figma:
  ...

Você também pode colar uma única URL de arquivo Figma (sem node-id específico)
se todas as telas estiverem no mesmo arquivo — vou navegar pelo arquivo para
localizar os frames correspondentes.
```

Aguarde a resposta completa do usuário.

Após receber as URLs:
- Para cada URL fornecida (não "–"), extraia:
  - `fileKey`: segmento entre `/design/` e o próximo `/` na URL
  - `nodeId`: valor do query param `node-id`, convertendo `-` em `:` (ex: `3-281` → `3:281`). Se ausente, use `0:1`
- Se o usuário forneceu uma única URL de arquivo sem node-ids: registre o `fileKey` e use `nodeId = 0:1` como ponto de entrada — durante a consulta do Passo 4, tente identificar os nodes pelo nome das telas.
- Se o usuário digitou "–" para todas as telas: defina `FIGMA_DISPONIVEL = false` e continue para o Passo 4 sem consultas ao Figma.

---

## PASSO 4 — Consultar Figma MCP para cada tela

**Se `FIGMA_DISPONIVEL = false`:** pule este passo inteiramente e vá para o Passo 5.

Para cada tela que recebeu uma URL no Passo 3:

**4.1 — Buscar metadados do nó**

Use `mcp__plugin_figma_figma__get_metadata` com `fileKey` e `nodeId` extraídos.
Capture: nome do frame/componente no Figma, dimensões, estrutura de layers relevante.

**4.2 — Buscar contexto de design**

Use `mcp__plugin_figma_figma__get_design_context` com `fileKey` e `nodeId`.
Capture e consolide internamente para cada tela:
- Componentes usados (nomes identificados)
- Estados visíveis no frame (variantes, se houver)
- Anotações de design retornadas
- Divergências entre o frame do Figma e o que está descrito na Seção 6 do briefing técnico

**4.3 — Consolidar notas por tela**

Para cada tela, construa internamente:
```
Tela: [Nome]
URL: [URL original]
nodeId: [nodeId]
Nome no Figma: [nome do frame]
Componentes: [lista]
Estados: [lista ou "não identificados"]
Anotações: [notas relevantes ou "nenhuma"]
Divergências: [lista ou "nenhuma"]
```

---

## PASSO 5 — Gerar `briefing-tech.v(VERSAO_ATUAL+1).md`

Calcule `PROXIMA_VERSAO = VERSAO_ATUAL + 1`.

Gere `ai/specs/YYYYMMDDHHmmSS_nome/briefings/briefing-tech.v[PROXIMA_VERSAO].md`.

**Copie INTEGRALMENTE o conteúdo do `briefing-tech.v[VERSAO_ATUAL].md`.** Não reformule, não resuma, não altere o conteúdo existente — copie todas as 15 seções com fidelidade total e faça apenas as seguintes modificações:

**1. Atualize o header:**

```markdown
> **Versão:** [PROXIMA_VERSAO].1
> **Status:** Rascunho
> **Gerado em:** [data atual no formato YYYY-MM-DD]
> **Baseado em:**
>   - [`./briefing-tech.v[VERSAO_ATUAL].md`](./briefing-tech.v[VERSAO_ATUAL].md) — Briefing técnico v[VERSAO_ATUAL] (com referências Figma adicionadas)
>   - [`../briefings/briefing-ux.vN.md`](../briefings/briefing-ux.vN.md) — Briefing UX/UI vN ← incluir apenas se existe
>   - [`../discovery.md`](../discovery.md) — discovery de [data do discovery]
```

**2. Atualize a Seção 6 (UX e Comportamento da Interface):**

Para cada tela listada na `LISTA_TELAS`, adicione um bloco de referência Figma imediatamente após a descrição da tela:

**Se `FIGMA_DISPONIVEL = true` e a tela recebeu URL:**
```markdown
> **Figma:** [Nome do frame](URL) — componentes: [lista resumida]
> **Estados no Figma:** [lista de variantes/estados encontrados]
```
Se houver divergências: adicionar `> ⚠️ **Divergência:** [descrição] — verificar com time de UX/UI`

**Se `FIGMA_DISPONIVEL = false` ou tela recebeu "–":**
```markdown
> **Figma:** ⚠️ Referência visual pendente — solicitar ao time de UX/UI
```

**3. Adicione a Seção 16 — Referências de Design (Figma)** após a Seção 15:

```markdown
## 16. Referências de Design (Figma)

> Gerado por /lf-specs em [data]. URLs fornecidas pelo time de UX/UI.

| Tela | Rota | URL Figma | Componentes-chave | Status |
|------|------|-----------|-------------------|--------|
| [Nome Tela 1] | [/rota] | [link](url) | [lista] | ✓ Referenciado |
| [Nome Tela 2] | [/rota] | — | — | ⚠️ Pendente |
```

Se `FIGMA_DISPONIVEL = false`, adicionar nota:
> ⚠️ Figma MCP não estava disponível durante a geração. Execute /lf-specs novamente com Figma MCP conectado para enriquecer esta seção.

---

## PASSO 6 — Geração do `specs.md`

Gere `ai/specs/YYYYMMDDHHmmSS_nome/specs.md`.

**Se já existir um `specs.md` nesta pasta:** sobrescreva sem perguntar — specs.md não tem versionamento, sempre reflete o estado atual.

**Use `$CLAUDE_SKILL_DIR/templates/specs.md` como estrutura e `ai/specs/20260323142630_google_docs/specs.md` como referência de profundidade e granularidade.**

**Fontes de dados (use TODAS):**
- `briefing-tech.v[PROXIMA_VERSAO].md` (gerado no Passo 5) — fonte primária
- `briefing-ux.vN.md` (se disponível) — para comportamento de telas e fluxos
- `discovery.md` — para contexto de negócio e restrições

**Regras de decomposição em SPECs:**

- Uma SPEC por domínio de responsabilidade — **não por camada técnica**.
  - Errado: "SPEC-01 Backend", "SPEC-02 Frontend"
  - Certo: "SPEC-01 OAuth e ciclo de conexão", "SPEC-02 Configuração UX"
- Se há fluxo de autenticação/autorização: SPEC separada.
- Se há migração de banco de dados complexa: SPEC separada.
- A última SPEC deve ser sempre hardening/testes/observabilidade.
- **Todas as 12 seções** devem estar presentes em cada SPEC:
  Objetivo, Contexto, Personas e Papéis, Comportamento esperado, Regras de negócio, Contrato de API, SLA e Performance, Observabilidade, Critérios de aceite, Estado atual, Mudanças necessárias, Definição de pronto.
- Critérios de aceite no formato **DADO / QUANDO / ENTÃO** — sem exceção.
- Regras de negócio com linguagem prescritiva: **DEVE / NÃO DEVE / PODE / SE...ENTÃO**.
- IDs sequenciais: SPEC-01, SPEC-02, SPEC-03...

**Integração das referências Figma nas SPECs:**

Para cada SPEC que cobre funcionalidade com interface visual:
- Na seção **"Comportamento esperado"**, após descrever cada tela ou estado, adicione (somente se a tela tem URL Figma confirmada):
  ```
  > Referência visual: [Nome da Tela](URL_Figma)
  ```
- Na seção **"Definição de pronto"**, adicione o item (somente se há URL Figma para a tela principal desta SPEC):
  ```
  - [ ] Implementação validada contra o Figma: [Nome da tela principal](URL)
  ```
- Se `FIGMA_DISPONIVEL = false` ou nenhuma tela da SPEC recebeu URL: omita as referências Figma.

---

## PASSO 7 — Geração do `wps.md`

Gere `ai/specs/YYYYMMDDHHmmSS_nome/wps.md`.

**Se já existir um `wps.md` nesta pasta:** sobrescreva sem perguntar.

**Use `$CLAUDE_SKILL_DIR/templates/wps.md` como estrutura e `ai/specs/20260323142630_google_docs/wps.md` como referência de granularidade e completude.**

**Regras de decomposição em WPs:**

- Um WP por unidade de trabalho coesa — entregável por um dev em **1 a 3 dias**.
- WPs maiores que 3 dias devem ser divididos.
- IDs sequenciais **globais**: verifique com Glob qual é o maior Wp-XX existente em `ai/specs/` e continue a partir dele. Se não houver nenhum, comece em Wp-01.
- **Sempre inclua um WP de hardening/testes ao final.**
- **Todos os campos são obrigatórios** na tabela de cada WP:
  ID, Spec relacionada, Tipo, Estimativa, Dependências, Pode paralelizar com, Testes requeridos, Status.
- **Todas as seções são obrigatórias** em cada WP:
  Escopo, Definition of Ready, Passos sugeridos, Critérios de aceite do pacote, Rollback, Áreas impactadas.
- Ao final do arquivo, inclua obrigatoriamente:
  - **Mapa de Dependências** — grafo ASCII
  - **Riscos e Pontos Desconhecidos** — tabela
  - **Oportunidades de Paralelização** — tabela

---

## PASSO 8 — Confirmação final

Apresente:

```
Gerado com sucesso ✓

  briefings/briefing-tech.v[PROXIMA_VERSAO].md — v[VERSAO_ATUAL] + referências Figma (Seção 16)
  specs.md                                      — [N SPECs]
  wps.md                                        — [N WPs] · estimativa total: [soma]d

[Se FIGMA_DISPONIVEL = true:]
Referências Figma incorporadas:
  ✓ [N] telas com URL e contexto de design extraído via MCP
  [Se houver telas sem URL:] ⚠️ [N] telas sem referência Figma — ver Seção 16 do briefing

[Se FIGMA_DISPONIVEL = false:]
⚠️ Gerado sem referências Figma (MCP não disponível ou URLs não fornecidas).
   Para adicionar referências visuais: execute /lf-specs novamente com Figma MCP conectado.

[Se houver divergências identificadas no Passo 4:]
⚠️ Divergências Figma × Briefing que precisam de alinhamento com o time de UX/UI:
  1. [tela] — [descrição da divergência]
  2. [...]

[Se houver pontos em aberto:]
Pontos em aberto que precisam de decisão antes de iniciar:
  ⚠️ [item 1]
  ⚠️ [item 2]

Próximos passos:
  1. Revisar briefing-tech.v[PROXIMA_VERSAO].md com o time técnico
  2. Resolver divergências Figma × Briefing com o time de UX/UI (se houver)
  3. Resolver pontos em aberto (se houver)
  4. Iniciar os WPs a partir de: [primeiro WP sem dependências]
```
