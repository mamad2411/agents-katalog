---
name: lint-and-validate
description: "Controle automático de qualidade, linting e procedimentos de análise estática. Use após cada modificação de código para garantir correção de sintaxe e conformidade com padrões do projeto. Triggers onKeywords: lint, format, check, validate, types, static analysis."
allowed-tools: Read, Glob, Grep, Bash
---

# Skill de Lint e Validação

> **OBRIGATÓRIO:** Execute ferramentas de validação apropriadas após CADA mudança de código. Não finalize uma tarefa até que o código esteja sem erros.

### Procedimentos por Ecossistema

#### Node.js / TypeScript
1. **Lint/Fix:** `npm run lint` ou `npx eslint "path" --fix`
2. **Types:** `npx tsc --noEmit`
3. **Segurança:** `npm audit --audit-level=high`

#### Python
1. **Linter (Ruff):** `ruff check "path" --fix` (Rápido & Moderno)
2. **Segurança (Bandit):** `bandit -r "path" -ll`
3. **Types (MyPy):** `mypy "path"`

## O Ciclo de Qualidade
1. **Escrever/Editar Código**
2. **Executar Auditoria:** `npm run lint && npx tsc --noEmit`
3. **Analisar Relatório:** Verifique a seção "RELATÓRIO FINAL DE AUDITORIA".
4. **Corrigir e Repetir:** Submeter código com falhas no "RELATÓRIO FINAL" NÃO é permitido.

## Tratamento de Erros
- Se `lint` falhar: Corrija os problemas de estilo ou sintaxe imediatamente.
- Se `tsc` falhar: Corrija incompatibilidades de tipo antes de prosseguir.
- Se nenhuma ferramenta está configurada: Verifique a raiz do projeto por `.eslintrc`, `tsconfig.json`, `pyproject.toml` e sugira criar uma.

---
**Regra Rígida:** Nenhum código deve ser enviado ou reportado como "concluído" sem passar nessas verificações.

---

## Scripts

| Script | Propósito | Comando |
|--------|-----------|---------|
| `scripts/lint_runner.py` | Verificação de lint unificada | `python scripts/lint_runner.py <project_path>` |
| `scripts/type_coverage.py` | Análise de cobertura de tipos | `python scripts/type_coverage.py <project_path>` |