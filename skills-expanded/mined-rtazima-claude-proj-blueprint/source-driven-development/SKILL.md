---
name: source-driven-development
description: "Source-driven development. Activated when the user mentions a framework, library, or SDK decision, or when implementing features with external dependencies. Keywords: \"official docs\", \"documentation\", \"how does X work\", \"what API\", \"which method\", \"framework\", \"library\", \"SDK\". Ensures every framework-specific decision is backed by official documentation, not training data."
allowed tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
---

# Source-Driven Development

Every framework-specific decision must be backed by **official documentation**, not training data.
LLMs hallucinate APIs, invent method signatures, and confuse library versions.
The antidote is to verify against the source of truth before writing code.

## Rules

1. **Detect the stack first** — read `CLAUDE.md`, `package.json`, `requirements.txt`, `go.mod`, or equivalent to know exact versions
2. **Fetch docs, don't guess** — use `WebFetch` to read official docs for the specific version in use
3. **Cite your source** — add a comment or docstring with the doc URL when using a non-obvious API
4. **Say UNVERIFIED** — if you cannot find official documentation for a claim, explicitly mark it as `// UNVERIFIED: could not find docs for this API`
5. **Never cite Stack Overflow, blog posts, or tutorials as primary source** — they may be outdated or wrong. Official docs and source code are the only primary sources
6. **Version matters** — docs for v3 don't apply to v2. Always check the version installed

## Workflow

### Phase 1: Detect stack and versions
```bash
# Node.js
cat package.json | grep -A1 '"dependencies"'

# Python
cat requirements.txt  # or pyproject.toml

# Go
cat go.mod
```

### Phase 2: Before implementing
For each framework-specific decision:
1. Identify the specific API/method/pattern you need
2. Fetch the official docs page for that API
3. Verify: does this method exist? What are the parameters? What version introduced it?
4. If docs are unavailable → mark as UNVERIFIED and note what you assumed

### Phase 3: Implement with citation
```typescript
// Ref: https://docs.example.com/api/v3/client#create
const client = new Client({ timeout: 5000 });
```

### Phase 4: Verify after implementing
1. Does the code compile/type-check? (catches hallucinated APIs)
2. Do tests pass? (catches wrong method signatures)
3. Are all UNVERIFIED markers resolved or documented?

## Source hierarchy

| Priority | Source | Use for |
|---|---|---|
| 1 | Official docs (versioned) | API signatures, configuration, behavior |
| 2 | Source code (GitHub) | When docs are incomplete or ambiguous |
| 3 | Official migration guides | Version upgrade patterns |
| 4 | Official examples/cookbooks | Integration patterns |
| 5 | UNVERIFIED (mark explicitly) | Last resort — document the assumption |

## Racionalizações comuns

| Racionalização | Realidade |
|---|---|
| "Eu sei como essa API funciona, não preciso checar docs" | Training data pode estar desatualizado. APIs mudam entre versões. Verifique. |
| "Buscar docs desperdiça tokens" | Alucinar uma API desperdiça mais — o debug custa 10x o fetch. |
| "Vi essa solução no Stack Overflow" | SO pode estar desatualizado ou errado. Valide contra docs oficiais. |
| "A assinatura do método é óbvia" | Parâmetros opcionais, overloads e breaking changes não são óbvios. Cheque. |

## Red Flags

- Usou API sem verificar se existe na versão instalada
- Nenhum `WebFetch` de documentação durante implementação com framework externo
- Comentário de referência aponta para URL genérica (ex: `// see docs`) em vez de URL específica
- Erro de compilação por método/propriedade inexistente (sinal de API alucinada)
- Markers UNVERIFIED que nunca foram resolvidos

## References
- Padrão inspirado em addyosmani/agent-skills `source-driven-development` skill
- `CLAUDE.md` — stack and versions
- `docs/specs/` — project-specific conventions
