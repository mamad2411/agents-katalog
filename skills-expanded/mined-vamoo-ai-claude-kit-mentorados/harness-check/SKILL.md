---
name: harness-check
description: >-
  Mede para onde vão os seus tokens: o que a sessão carrega antes do 1º prompt
  (CLAUDE.md, skills, MCPs) e o gasto no uso, com rótulo MEDIDO vs ESTIMADO, e o
  que dá pra cortar sem perder nada. Use quando o limite ou a conta surpreender,
  a sessão nascer cara, houver dúvida se um MCP ou o CLAUDE.md pesa, "MCPs caros"
  ou "limpar ~/.claude". Só dispara quando você chama: /kit-vamoo:harness-check.
disable-model-invocation: true
allowed-tools:
  - 'Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/medir-sessao.py" *)'
  - 'Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/medir-sessao.py *)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/skills-projeto-scan.sh" *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/skills-projeto-scan.sh *)'
---

# Harness Check — para onde vai o seu token

Quem tenta economizar corta o que dá pra ver, o CLAUDE.md, e quase sempre ele é a menor
parte. Meça antes de cortar.

## Regra de ouro: rotule todo número

- **MEDIDO** — saiu de um comando ou de um relatório nesta sessão.
- **ESTIMADO** — `chars ÷ 4`, extrapolação, regra de bolso.
- **INDISPONÍVEL** — você não tem acesso. Diga isso; não chute para completar a tabela.

Número sem rótulo não entra no relatório. A maior fatia do preload são schemas de
ferramenta, que só o `/context` mede.

## Passo 1 — o que a sessão carrega antes do primeiro prompt

Peça ao usuário: **rode `/context` e cole o output**. Comando built-in do CLI não se
invoca por `Bash`: peça, não simule, não estime no lugar dele. Esse é o **preload**, relido
em toda request da sessão.

Leia o output com esta pergunta: **quanto do preload é arquivo meu?** Numa medição de
03/09/2026 (conta do autor do kit) o preload era **52,7K tokens** (MEDIDO) e só ~5K, 10%,
vinha de arquivo editável (ESTIMADO por `chars÷4`; CLAUDE.md 2,1K). O resto era system
prompt, schemas de ferramenta e MCP: enxugar o CLAUDE.md, o corte que todo mundo tenta
primeiro, economizaria ~2%.

O total do preload você mede sem pedir nada, direto do transcript:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/medir-sessao.py" --ultimas 3
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/medir-sessao.py" --comparar --cwd "$PWD"   # app × terminal
```

Por sessão: superfície, versão, `nascimento` = tokens do primeiro request (MEDIDO) e tools
MCP por servidor (MEDIDO quando o transcript registra; `?` quando não, e aí só o `/context`
responde). Em 23/09/2026 (conta do autor, mesmo diretório) o app nascia com ~74K tokens e
340 tools de 26 servidores, e o terminal com ~41K.

As skills em `.claude/skills` do repo aberto entram no mesmo catálogo, relido em toda
request, e só este comando as mede (skill com `name:` diferente da pasta paga a description
e nunca dispara):

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/skills-projeto-scan.sh" "$PWD"
```

Some esse número ao das suas skills globais antes de dizer quanto "os seus arquivos" pesam.
Passou do teto: a skill `skills-projeto` decide os cortes, não esta.

**Custo por skill e auditoria do prompt** não se reimplementam aqui: peça ao usuário rodar
e colar o `/skill-doctor` e o `/doctor prompt-audit`, built-in como o `/context`. CLI
que ainda não tem o comando: INDISPONÍVEL, não estimado.

## Passo 2 — o gasto durante o uso

```bash
npx -y ccusage@20.0.37 daily      # custo por dia e por modelo
npx -y ccusage@20.0.37 session    # custo por sessão — ache as caras
```

Olhe **cache read**: numa sessão longa costuma ser a maior linha da conta, porque cada
tool call relê tudo que veio antes. Se as sessões longas dominam a fatura (o normal), o
problema **não** é o seu CLAUDE.md: é o passo 4.

## Passo 3 — MCP que você não usa

Todo servidor MCP ligado injeta o schema de cada ferramenta no preload, usando ou não.

```bash
claude mcp list
claude mcp get <nome>   # escopo e comando de um servidor específico
```

Cruze com o `/context` (linha *MCP tools*) e pergunte, um por um: usei este mês? MCP que
aparece pouco pode estar configurado só num projeto e nem carregar aqui. **Conector do
claude.ai não sai por `claude mcp remove`**: no CLI, `"disableClaudeAiConnectors": true` no
`settings.json` desliga todos; no **app desktop** essa opção não vale, e se o `--comparar`
mostra o app muito acima do terminal, o corte é desconectar em Conectores, na conta do
claude.ai, ou trabalhar pelo terminal.

Para bloquear um servidor por vez, `deniedMcpServers` no `settings.json` é uma lista de
**objetos** (`{"serverName": "x"}`, `{"serverUrl": "https://*.exemplo.com/*"}`), não de
strings; a lista soma todas as fontes de configuração.

MCP ou ferramenta com muito erro: olhe **a data** dos erros antes de culpar o conector.
Erros concentrados num dia só são incidente passageiro (o serviço caiu), não defeito.

Skill que você só chama na mão sai da listagem com `"skillOverrides": {"minha-skill":
"user-invocable-only"}` no `settings.json`, e o `/minha-skill` continua funcionando.

## Passo 4 — os hábitos que realmente movem a conta

Em ordem de impacto medido:

1. **Sessão-maratona.** Sessão nova ao trocar de assunto (não `/clear`, que apaga o
   histórico) e `/compact` por volta de 150K: em janela de 1M o auto-compact só age perto
   do teto, e aí custa 100–200K tokens de uma vez.
2. **Modelo caro como padrão.** Modelo que você não escolheu no `ccusage daily` quase
   sempre vem de subagente ou da barra de status.
3. **Preload**, só depois dos dois acima e com o `/context` na mão.
4. **Esforço alto fixo** no `settings.json`: o mesmo nível pode pensar mais num modelo
   mais novo. Trocar `/effort` no meio da sessão faz a próxima mensagem reler tudo sem cache.

## Fechamento

Entregue uma tabela `PROBLEMA | SINAL | GANHO ESTIMADO POR SESSÃO | RISCO`, ordenada por
ganho, com o rótulo MEDIDO/ESTIMADO em cada número, e **não aplique nada sem o usuário
aprovar item a item**. Se o ganho total ficar abaixo de ~5% da fatura, diga isso: o dinheiro
está no passo 4.

- **Só entra o que muda a conta de forma perceptível**, pelo impacto medido; não há número
  fixo de linhas. **Passo medido e limpo não vira linha.**
- **Passo que você não conseguiu medir vira linha, com `INDISPONÍVEL`** (o caso comum é o
  `/context` que o usuário não colou): "não achei nada" e "não medi" são coisas diferentes.
- **A coluna SINAL diz de onde saiu a recomendação**: "`foo`: 38 tools no `medir-sessao.py`
  (MEDIDO), escopo user no `claude mcp get foo`, e você disse que não usou este mês". Só
  valem as fontes desta skill (`/context`, `/skill-doctor`, `/doctor prompt-audit`,
  `medir-sessao.py`, `skills-projeto-scan.sh`, `ccusage`, `claude mcp list/get` e o
  arquivo que você abriu); "você não usa" é o usuário quem responde.
- **Feche dizendo o que ficou de fora**, numa linha: *"deixei de fora N achados menores
  (MCP e skills) — peça se quiser a lista"*.
