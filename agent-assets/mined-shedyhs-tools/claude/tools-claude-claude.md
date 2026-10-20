# Ambiente: sandbox `config-ecc`

Você está num Docker Sandbox descartável, com permissões liberadas
(`bypassPermissions`). O workspace é um **bind mount read-write do host** — o que
você escreve lá persiste na máquina real. O resto do container é efêmero.

## ECC instalado de forma seletiva

Skills, agentes e comandos do ECC estão em `~/.claude/`. A lista curada de skills
vem de `~/.ecc-skills`; o clone do ECC fica em `~/.ecc/ECC` (tag e commit em
`~/.ecc/installed-ref`).

**Os agentes NÃO usam o prefixo `ecc:`** — aqui são agentes de usuário. Use
`planner`, `code-reviewer`, `tdd-guide`, `architect`, `build-error-resolver`,
`database-reviewer`, `doc-updater`, `e2e-runner`, `harness-optimizer`,
`loop-operator`, `python-reviewer`, `refactor-cleaner`.

Os hooks do ECC estão ativos (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`,
`SessionStart`, `SessionEnd`, `Stop`, `PreCompact`), carregados pela camada
`--settings` em `~/.config/claude/ecc.json`. O GateGuard pode exigir fatos antes
de comandos sensíveis — isso é esperado, não é bug. Para desligar, recrie o
sandbox com `--kit-arg gateguard=off` ou `--kit-arg disabled_hooks=<ids>`.

## Git e GitLab

`git` já tem identidade configurada — pode commitar direto.

`glab` está instalado e apontado para o GitLab de trabalho. A variável
`GITLAB_TOKEN` contém um **placeholder**, não o token real: o proxy do sandbox
substitui pelo valor verdadeiro nas requisições. Não tente ler, logar ou copiar
esse valor — ele não serve para nada fora daqui. Operações de git por HTTPS
autenticam pelo credential helper do glab.

## Rede

A saída é restrita a poucos domínios (GitHub, gitlab.com, o GitLab de trabalho,
TypeSafe e PyPI).
Se um download falhar por rede, é política do sandbox, não falta de conectividade
— relate em vez de procurar contorno.

## Roteador de modelos

Se o sandbox subiu com `model_router=on` e há chave da TypeSafe, as requisições
do Claude passam por um roteador local (`127.0.0.1:8788`). A cada mensagem sua,
o Jev (TypeSafe) escolhe o modelo (Haiku, Sonnet ou Opus) e o esforço (`low` a
`max`). O Jev também vê o fim da conversa anterior. Com dúvida, o roteador usa o
menor modelo que soma 80% da probabilidade. Com falha da TypeSafe, ele usa Opus e
`high`.

- O comando `/router` abre um painel com os turnos por modelo, o esforço e os
  fallbacks.
- `claude-model-router --stats` resume o dia. O log fica em
  `~/.local/state/claude-model-router/router.log`.
- Se o roteador não subiu, o Claude roda direto, sem ele. O motivo fica em
  `~/.local/state/claude-model-router/router.err`.
- `TYPESAFE_API_KEY` vale um **placeholder**, como `GITLAB_TOKEN`. Não leia nem
  copie esse valor.

## Technical Writing: ASD-STE100 (Simplified Technical English)

Write all English technical text in ASD-STE100. Pick the mode from the text
type:

- **Strict** — error messages, tool descriptions, prompts, inter-agent
  instructions, procedures, safety text. Apply every rule below.
- **STE-flavored** — READMEs, docs, PR descriptions, changelogs, commit
  messages, code comments. Apply the structural rules. Treat word choice as
  advice, so the prose keeps its range.

Structural rules:

- **Length:** procedural sentences ≤ 20 words. Descriptive sentences ≤ 25
  words. Paragraphs ≤ 6 sentences, one topic each.
- **Instructions:** imperative form, one instruction per sentence. Write the
  condition first: "If X, do Y." Use a numbered list for 3 or more steps.
- **Voice and tense:** active voice. Simple tenses. No present perfect,
  except when "has completed" carries current state that "completed" loses.
- **Punctuation:** no semicolons (Rule 8.1). Write separate sentences.
- **Verbs:** no phrasal verbs ("start", not "spin up", and "remove", not
  "take off"). Use the verb, not a noun form ("analyze", not "perform an analysis").
- **Grammar:** do not remove articles or verbs to make text shorter. Noun
  clusters ≤ 3 words.
- **Warnings:** start with a clear command, then give the risk.

Word choice: one word = one meaning. Use the same term for the same thing in
the whole document. Prefer simple, common words. No marketing adjectives
("seamless", "robust", "powerful").

Never change the meaning to obey a rule. Keep every hedge ("may", "could")
because a hedge is a statement of confidence. Never add facts. Do not change
code identifiers, quoted text, CLI output, or legal text.

For a full rewrite or review, use the `asd-ste100` skill. To check a file,
run `python3 ~/.claude/skills/asd-ste100/scripts/ste-lint.py <file>`.

### pt-BR: Português Técnico Simplificado

STE is English-only. For pt-BR text (chat replies, docs, comments, commit
messages), apply the pt-BR adaptation with the same two modes:

- Sentences ≤ 22 words (instructions) or ≤ 27 words (descriptions).
- Name who acts. No synthetic passive ("deve-se", "recomenda-se").
- Use the full verb, not a support verb ("analise", not "realize a análise").
- No gerundismo ("enviaremos", not "vamos estar enviando").
- No semicolons. Condition before the instruction. Direct word order.
- ≤ 2 chained "de" in a noun phrase.
- Use "você" and the imperative in the whole document.
- Avoid false cognates ("eventualmente", "endereçar", "suportar JSON").

For a full rewrite or review, use the `portugues-tecnico-simplificado` skill.
To check a file, run
`python3 ~/.claude/skills/portugues-tecnico-simplificado/scripts/pts-lint.py <file>`.
