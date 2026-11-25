---
name: ksdd
description: Kognar Spec-Driven Design & Development (KSDD). Use when the user mentions KSDD, brainstorm/spec-driven workflow, .ksdd/features/FEATURE-*.md tasks (or legacy docs/FEATURE-*.md), .ksdd/build/BUILD-PLAN.md, or wants structured product specs before coding. Triggers also include slash-style prompts ksdd-start, ksdd-spec, or "spec driven design".
---

# KSDD no Codex

KSDD guia do brainstorm até design system e implementação por tasks. No **Codex**, os fluxos estão disponíveis de duas formas:

## 1. Custom prompts (slash explícito)

Após `ksdd install --codex`, os prompts ficam em `~/.codex/prompts/` (arquivos `.md` no topo da pasta — [documentação OpenAI](https://developers.openai.com/codex/custom-prompts)).

Invoque no composer:

| Prompt | Equivalente Claude Code |
|--------|---------------------------|
| `/prompts:ksdd-setup` | `/ksdd:setup` |
| `/prompts:ksdd-start` | `/ksdd:start` |
| `/prompts:ksdd-spec` | `/ksdd:spec` |
| `/prompts:ksdd-tech` | `/ksdd:tech` |
| `/prompts:ksdd-design` | `/ksdd:design` |
| `/prompts:ksdd-new-feature` | `/ksdd:new:feature` |
| `/prompts:ksdd-build-feature` | `/ksdd:build:feature` |
| `/prompts:ksdd-build-all` | `/ksdd:build:all` |

Argumentos após o comando alimentam `$ARGUMENTS` nos arquivos de prompt (mesmo comportamento documentado em cada comando).

## 2. Material de referência nesta skill

Templates e agentes foram copiados para esta pasta:

- `references/` — templates (brainstorm, spec, architecture, feature, build-plan, design-md-spec, approval-gates, personas)
- `agents/` — interviewer, consolidator, critic, setup-analyst

Ao seguir um prompt KSDD, **leia** os arquivos em `references/` quando o prompt citar um template; use `agents/` como guia de estilo (perguntas em batch, consolidação, checklist do critic). Para idioma de artefatos e perguntas, siga sempre `references/language-policy.md` (idioma da conversa, não fixo em pt-BR).

## 3. Ferramentas

Os prompts listam `allowed-tools` pensando no Claude Code. No Codex, mapeie para as ferramentas equivalentes disponíveis na sessão (`Read`/`Write`/`Edit`/`Bash`/`Glob`/`Grep`/`Agent`, etc.). Se uma ferramenta não existir, adapte o passo sem mudar a intenção do fluxo.

## 4. Instalação / atualização

```bash
ksdd install              # apenas Claude Code (~/.claude/)
ksdd install --codex      # Claude + Codex (prompts + esta skill)
```

Documentação completa: `README.md` na raiz do pacote npm `@kognar/ksdd`.
