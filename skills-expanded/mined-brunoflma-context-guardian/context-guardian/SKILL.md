---
name: context-guardian
description: |
  Protege contexto com 3 modos: Sentinela, Silencioso e Evacuação.

  SENTINELA — ativar com: "ativar context guardian", "cg on", "/cg",
  "ativar sentinela", "iniciar monitoramento", "proteção de contexto"
  Perguntar intervalo na ativação. Emitir lembrete a cada N turnos.

  SILENCIOSO — ativar com: "modo silencioso", "cg silent"

  EVACUAÇÃO — ativar IMEDIATAMENTE quando:
  - Claude incerto sobre algo estabelecido nesta conversa
  - Claude repetiu pergunta ou conteúdo fornecido
  - Claude contradiz decisão anterior
  - Usuário diz: "você esqueceu", "compile tudo", "nova conversa",
    "/evacuar", "resuma tudo", "checkpoint"
  - 50 turnos sem checkpoint confirmado

  Gerar .md + Prompts de Retomada via create_file + present_files.
  NUNCA só no chat.

  INTEGRAÇÃO COM SKILL context-status — quando as duas estão ativas:
  - Card do context-status substitui o lembrete do Sentinela no mesmo turno.
  - "Transferência Imediata" aciona Evacuação automaticamente.
  - Técnico e Conteúdo alimentam fatos-âncora do checkpoint.
---

# Context Guardian v1.4.1 — Guia Completo

---

## Limitações Honestas (ler antes de tudo)

Esta seção existe para que o usuário saiba exatamente o que a skill consegue
e o que não consegue.

### O que NÃO é possível no Claude.ai

**Monitoramento contínuo em background:** Claude não executa processos paralelos.
Ele processa uma mensagem e responde. Não há "loop" rodando entre as respostas.
A skill é lida na ativação — não é re-executada automaticamente a cada turno.

**Detecção de viradas de fase:** depende de Claude reconhecer ativamente o evento
enquanto está respondendo. Em conversas densas e técnicas, isso falha com frequência
porque o foco cognitivo está na tarefa, não no monitoramento.

**Evacuação pré-compactação:** Claude não tem acesso ao contador de tokens no Claude.ai.
Não é possível saber proativamente que a compactação está se aproximando.

### O que É garantido

**Evacuação por gatilho textual:** quando o usuário escreve um dos comandos de
evacuação, ou quando Claude percebe claramente que repetiu ou contradiz algo, a evacuação
acontece de forma confiável — esses são gatilhos binários e simples.

**Checkpoint por lembrete:** Claude emite lembretes de checkpoint em intervalos
definidos na ativação. Isso funciona porque não requer detecção — é uma contagem
explícita de turnos respondidos.

**Relatório completo na evacuação:** uma vez disparada, a evacuação gera o arquivo
.md e os Prompts de Retomada de forma confiável.

### Consequência para o design

**Checkpoints manuais periódicos são a camada primária de proteção.**
A detecção automática de fase é secundária e não deve ser confiada isoladamente.

---

## MODO SENTINELA

### Ativação

Frases aceitas:
`ativar context guardian` · `context guardian on` · `/cg` · `cg on`
`ativar sentinela` · `iniciar monitoramento` · `monitorar contexto` · `proteção de contexto`

### Pergunta obrigatória na ativação

Ao ativar, Claude deve SEMPRE perguntar antes de confirmar:

```
🛡️ Context Guardian — Ativando Sentinela

A cada quantos turnos você quer receber o lembrete de checkpoint?
Recomendado: 10 turnos para conversas técnicas densas, 15 para conversas mais leves.
(Responda com um número, ex: <kbd>"10"</kbd>)
```

### Resposta de confirmação — card visual (após o usuário definir o intervalo)

Emitir como **card HTML via ferramenta de visualização**, no mesmo estilo da skill context-status.
**Regras de Segurança e Acessibilidade:**

- 🛡️ **Segurança (Prevenção de XSS):** Antes de renderizar qualquer texto do usuário no HTML (como o "Objetivo" ou "Decisões"), você deve **escapar caracteres HTML** (substituir `<`, `>`, `&`, `"`, `'` por suas respectivas entidades HTML).
- ♿ **Acessibilidade:** Você deve incluir atributos ARIA (ex: `role="region"`, `aria-label="Context Guardian"`, `aria-hidden="true"` nos ícones SVG) em todos os componentes visuais.

O card tem quatro zonas (lembre-se de aplicar as regras acima):

**Zona 1 — Header:** estruturar com `<header>` e usar `<h2>` para o título "Context Guardian" à esquerda + pills à direita (OBRIGATÓRIO usar semântica não-live com `aria-label` descritivo no contêiner da pill e `<span aria-hidden="true">` para o texto visual, ex: `<span aria-label="Turno atual: N"><span aria-hidden="true">Turno N</span></span>`):

- `Turno N` — pill neutra com borda (`aria-label="Turno N"`)
- badge de modo — verde (Sentinela) / cinza (Silencioso) (`aria-label="Modo: Sentinela"`)
- badge de perfil — neutro (Técnico / Estratégico / Criativo / Geral) (`aria-label="Perfil: Técnico"`)

**Zona 2 — Barra de checkpoint:** label "Checkpoint" + barra de progresso (height 6px,
border-radius 3px, cor `#639922`, role="progressbar", aria-valuenow="[turno atual]", aria-valuemin="0", aria-valuemax="[intervalo]", aria-valuetext="[texto do progresso]", aria-label="Progresso para o próximo checkpoint") mostrando progresso do turno atual até o próximo checkpoint.
Exemplo: turno 3, intervalo 10 → próximo em 13 → barra vazia no início, vai preenchendo
conforme os turnos avançam. Exibir texto `<span aria-hidden="true">Turno [atual] → [próximo]</span>` à direita.

**Zona 3 — Rows de dados** formatadas OBRIGATORIAMENTE como uma Definition List HTML (`<dl>`, `<dt>` para rótulo, `<dd>` para valor) para garantir acessibilidade semântica.
Incluir ícone SVG (16×16, stroke-only, `aria-hidden="true"`) + rótulo (cor terciária, min-width 72px) + valor (cor primária):

| Ícone SVG                                 | Rótulo (`<dt>`) | Conteúdo (`<dd>`)                                                                                                               |
| ----------------------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| relógio (`circle + polyline`)             | Intervalo       | `a cada N turnos · próximo checkpoint: Turno X`                                                                                 |
| usuário (`circle + path`)                 | Objetivo        | objetivo declarado na ativação                                                                                                  |
| lista/clipboard (`rect + lines`)          | Decisões        | decisões registradas, ou `nenhuma ainda`                                                                                        |
| escudo (`path`)                           | Protocolo       | tags inline: `garantido` (verde) para checkpoint e evacuação por gatilho · `melhor esforço` (âmbar) para fase e pré-compactação |
| triângulo alerta (`path + line + circle`) | Alertas         | degradação detectada, ou `—`                                                                                                    |

**Zona 4 — Barra de recomendação** (cor semântica, deve incluir `role="status" aria-live="polite"` para os estados Normal e Atenção, e `role="alert" aria-live="assertive"` para Crítico):

| Estado  | Cor                                    | Label               | Hint                                                            |
| ------- | -------------------------------------- | ------------------- | --------------------------------------------------------------- |
| Normal  | Verde (`--color-background-success`)   | Sentinela ativo     | `Digite <kbd>"checkpoint agora"</kbd> a qualquer momento`       |
| Atenção | Âmbar (`--color-background-warning`)   | Checkpoint pendente | `Digite <kbd>"ok"</kbd> para confirmar ou <kbd>"evacuar"</kbd>` |
| Crítico | Vermelho (`--color-background-danger`) | Evacuação imediata  | `Contexto comprometido`                                         |

### Lembrete de Checkpoint (emitir a cada N turnos respondidos)

Emitir o mesmo card HTML com a barra de checkpoint na zona 2 mostrando que o intervalo
foi atingido — barra completamente preenchida, recomendação no estado Atenção (âmbar):
label **Checkpoint pendente** · hint `Digite <kbd>"ok"</kbd> para confirmar ou <kbd>"evacuar"</kbd>`.

**Nota:** quando a skill context-status está ativa, o card do context-status no mesmo turno substitui
este lembrete — não emitir os dois.

Aguardar resposta do usuário:

- `"ok"` / `"tudo bem"` / qualquer confirmação → registrar checkpoint, reiniciar contagem
- `"evacuar"` / qualquer gatilho de evacuação → executar Modo Evacuação
- Usuário ignora e continua → registrar como não confirmado, emitir próximo lembrete normalmente

### Checkpoint Manual

`"fazer checkpoint"` · `"verificar contexto"` · `"checkpoint agora"`

```
🟢 **Checkpoint Context Guardian** (turno ~[N])

**Estado atual:**
- Objetivo: [confirmar se ainda é o mesmo]
- Fase: [em que fase estamos]
- Últimas decisões: [listar as 3 mais recentes]
- Pendências: [o que está em aberto]

Contexto íntegro? Se sim, diga <kbd>"ok"</kbd>. Se algo estiver errado, descreva.
```

### Detecção Automática de Fase (melhor esforço)

| Evento                        | Como reconhecer                                       |
| ----------------------------- | ----------------------------------------------------- |
| Conclusão explícita de módulo | Usuário diz "perfeito", "feito", "próxima parte"      |
| Decisão arquitetural grande   | Escolha definitiva de tecnologia, padrão ou abordagem |
| Mudança clara de assunto      | Tópico muda sem relação com o anterior                |
| Acúmulo de 8+ decisões        | Contar decisões desde último checkpoint               |

### Checklist Interna (executar em todo checkpoint)

```
□ Sei o objetivo principal sem hesitar?
□ Consigo listar as 3 decisões mais recentes com suas justificativas?
□ Sei exatamente o que estava sendo feito antes deste turno?
□ Minhas respostas mantêm o nível de especificidade das anteriores?
□ Estou usando as convenções estabelecidas (nomes, estilo, padrões)?
□ Vou contradizer algo dito antes?
□ Vou perguntar algo que já foi respondido?
```

0 falhas → checkpoint verde, continuar.
1+ falha → evacuação imediata.

---

## MODO SILENCIOSO

`modo silencioso` · `cg silent` · `sentinela silencioso`

- Lembretes de checkpoint são **suprimidos**
- Claude só fala ao detectar degradação clara ou quando solicitado
- Desativar: `modo normal` · `cg verbose` · `desativar silencioso`

**Atenção ao usuário:** no modo silencioso, a responsabilidade de solicitar
checkpoints periódicos recai sobre você.

---

## MODO EVACUAÇÃO

### Gatilhos confiáveis

**Por sinal do usuário:**
`você esqueceu` · `já falei isso` · `compile tudo` · `gerar relatório`
`nova conversa` · `contexto perdido` · `transferir conversa` · `/evacuar`
`o que discutimos` · `resuma tudo` · `checkpoint agora`

**Por detecção interna:**

- Incerteza sobre fato já estabelecido nesta conversa
- Repetição de pergunta ou conteúdo já fornecido
- Contradição com decisão anterior documentada

**Por integração com a skill context-status:**

- Recomendação "Transferência Imediata" no card do context-status → acionar evacuação imediatamente

**Por contagem:**

- 50+ turnos sem checkpoint confirmado

### Passo 1 — Anúncio Imediato

```
⚠️ **Context Guardian — Modo Evacuação**
Motivo: [descrição precisa do gatilho]
Perfil: [Técnico / Estratégico / Criativo / Geral]

Gerando relatório .md + Prompts de Retomada.
Não farei mais nada até concluir.
```

### Passo 2 — Varredura Exaustiva (turno 1 → atual)

- **A — Identidade:** nome do projeto, objetivo exato, contexto do usuário, perfil
- **B — Fatos Técnicos** _(Técnico/Geral):_ linguagens+versões, frameworks, infra, configs
- **C — Decisões Cronológicas:** [turno aprox.] decisão — justificativa — alternativas rejeitadas
- **D — Código e Artefatos** _(Técnico):_ estrutura de pastas, snippets completos, código incompleto (NUNCA truncar)
- **E — Diretrizes Criativas** _(Criativo):_ tom, voz, restrições de estilo, estado da obra
- **F — Problemas e Tentativas:** problema → o que falhou e por quê → solução adotada
- **G — Requisitos e Restrições:** funcionais, técnicos, preferências do usuário, constraints
- **H — Estado Atual:** o que estava sendo feito, ponto exato de parada, próximos passos
- **I — Referências:** URLs, documentos, fontes citadas

### Passo 3 — Gerar Arquivo .md

**OBRIGATÓRIO:** `create_file` → `/mnt/user-data/outputs/context-guardian-[slug]-turno-[N].md`

🛡️ **Segurança (Path Traversal):** O `[slug]` deve ser rigorosamente sanitizado. Remova barras (`/`, `\`), pontos (`.`) e caracteres especiais. O caminho do arquivo deve ser SEMPRE exatamente dentro do diretório especificado, para evitar gravação fora da pasta.

Template por perfil em `references/transfer-report-template.md`.

Após criar: `present_files`.

### Passo 4 — Gerar Prompts de Retomada no Chat

**Prompt Completo:**

```
════════════════════════════════════════════════════════════════
PROMPT DE RETOMADA COMPLETO — CONTEXT GUARDIAN v1.4.1
════════════════════════════════════════════════════════════════
Você está assumindo uma conversa transferida. Leia tudo antes de responder.

## IDENTIDADE
Projeto: [nome] | Objetivo: [1 frase] | Perfil: [tipo]
Usuário: [papel/contexto]

## ESTADO NO MOMENTO DA SUSPENSÃO
Estávamos em: [atividade exata]
Ponto de parada: [última coisa dita/escrita — cirúrgico]
Status: [ex: código 60% escrito / decisão tomada sem implementação]

## DECISÕES TOMADAS — NÃO QUESTIONAR
1. [decisão] — [por quê]
2. [decisão] — [por quê]

## RESTRIÇÕES ABSOLUTAS
- ❌ [o que não usar/fazer] — [motivo]

## STACK E AMBIENTE
[linguagem+versão · framework · banco · infra]

## HISTÓRICO
[parágrafo denso: o que foi construído, problemas resolvidos, tentativas fracassadas]

## CÓDIGO RELEVANTE
[snippets críticos — especialmente código incompleto no momento da suspensão]

## PENDÊNCIAS
- ❓ [problema/questão em aberto]

## PRIMEIRA AÇÃO
[instrução imperativa sem ambiguidade — o que fazer agora]

## REFERÊNCIA COMPLETA
Arquivo: [nome-do-arquivo.md]
Faça upload junto com este prompt para contexto completo.
════════════════════════════════════════════════════════════════
```

**Prompt Compacto (~150 palavras):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RETOMADA RÁPIDA — [NOME DO PROJETO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Projeto: [nome] | Objetivo: [1 frase]
Stack: [lista compacta]
Fase: [onde estamos]

Decisões fixas:
1. [decisão] — [motivo]
2. [decisão] — [motivo]

Restrições: [lista compacta]

Parado em: [ponto exato — 1 frase]

Próxima ação: [instrução imperativa — 1 frase]

Ref: [nome-do-arquivo.md]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Passo 5 — Salvar Preferências na Memória

Via `memory_user_edits`: stack preferida, linguagem principal, estilo de código, idioma,
formato de resposta, contexto profissional. Nunca salvar dados de projeto específico ou sensíveis.

### Passo 6 — Instruções ao Usuário

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ EVACUAÇÃO CONCLUÍDA

  📄 Arquivo .md — relatório completo (baixe acima)
  📋 Prompt Completo — conversas técnicas e longas
  📋 Prompt Compacto — retomadas rápidas
  🧠 Preferências salvas na memória

COMO CONTINUAR:

Opção A — Upload + Prompt Completo:
  1. Baixe o .md
  2. Nova conversa no Claude
  3. Upload do .md + cole o Prompt Completo

Opção B — Retomada rápida:
  1. Nova conversa no Claude
  2. Cole o Prompt Compacto
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Perfis de Conversa

| Perfil          | Quando                       | Prioriza                          | Reduz             |
| --------------- | ---------------------------- | --------------------------------- | ----------------- |
| **Técnico**     | Linguagem, framework, código | Stack, artefatos, snippets        | —                 |
| **Estratégico** | Negócio, roadmap, OKRs       | Decisões, alternativas rejeitadas | Stack técnica     |
| **Criativo**    | Escrita, design, narrativa   | Tom, voz, restrições de estilo    | Stack, requisitos |
| **Geral**       | Fallback                     | Template completo                 | —                 |

Templates completos em `references/transfer-report-template.md`.

---

## Regras Absolutas

- ❌ NUNCA omitir informação por parecer pequena ou óbvia
- 🛡️ SEMPRE sanitizar entrada de usuário (escapar HTML) em cards visuais para prevenir XSS
- 🛡️ SEMPRE sanitizar nomes de arquivos para prevenir Path Traversal
- ❌ NUNCA truncar código parcial — incluir exatamente onde parou
- ❌ NUNCA gerar apenas no chat — sempre arquivo .md
- ❌ NUNCA prometer detecção automática de fase como garantia
- ✅ Completude > brevidade no relatório .md
- ✅ Marcar 🔴 itens críticos para o novo Claude
- ✅ Checkpoints manuais periódicos são a camada primária — comunicar isso ao usuário
- ✅ Salvar na memória apenas preferências recorrentes

---

## Automação Total — Ambientes Externos

| Ambiente            | Automação       | Nota                                                           |
| ------------------- | --------------- | -------------------------------------------------------------- |
| **Claude.ai**       | Semi-automático | Limitação de plataforma — sem acesso a tokens                  |
| **Claude Code**     | ✅ Total        | Subagentes nativos                                             |
| **API Python/Node** | ✅ Total        | Acesso a `usage.input_tokens` — evacuação real pré-compactação |
| **n8n**             | ✅ Total        | Fluxo visual sem código                                        |

Implementações em `references/automation-orchestrator.md`.
