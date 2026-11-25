# Skills Library

Esta pasta concentra as instruções reutilizáveis do `agents-mcp`.

## Camadas

- `shared/README.md`: mapa da camada compartilhada
- `shared/<categoria>/*.md`: skills operacionais por categoria
- `by-role/<agent>/README.md`: papel, limites, ownership e handoff
- `runners/README.md`: mapa dos workflows e entry points

## Categorias em shared/

| Categoria | Conteúdo |
|-----------|----------|
| `github/` | fluxo de branches, issues, workflow, publicação master |
| `documentation/` | governança de wiki técnica e tutorial |
| `security/` | guardrails de segurança editorial e operacional |
| `quality/` | qualidade de código e critérios de conclusão |
| `operations/` | baseline, handoff, wrapper, logs, source of truth |

## Regra de composição

1. identifique o tipo de decisão/execução
2. leia primeiro a área mais específica
3. se a regra servir para mais de um agent → `shared/`
4. mantenha `agents/roles/*/agent.md` enxuto
5. wrappers locais finos, sem biblioteca duplicada

Os materiais de execução continuam em `workers/automation/` e `workers/automate/`.
