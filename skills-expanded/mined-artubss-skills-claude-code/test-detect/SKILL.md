---
name: test-detect
description: Detecta automaticamente o framework de testes e executa os testes relevantes. Identifica Jest, Vitest, Playwright, Cypress, pytest, Go test e outros. Pode executar todos os testes, testes de arquivo específico ou gerar testes básicos para código novo. Uso - /test-detect, /test-detect src/auth/login.ts, /test-detect generate src/utils.ts
---

# Test Detect

Detecta automaticamente o framework de testes no projeto atual e executa os testes corretos.

## Fluxo de trabalho

### Etapa 1: Detectar o framework de testes

Verifique estes arquivos em ordem (primeira correspondência vence):

| Verificação | Framework | Comando de Execução |
|-------|-----------|-------------|
| `vitest.config.*` existe OU `vitest` em devDeps | **Vitest** | `npx vitest run` |
| `jest.config.*` existe OU `jest` em devDeps | **Jest** | `npx jest` |
| `playwright.config.*` existe | **Playwright** | `npx playwright test` |
| `cypress.config.*` existe | **Cypress** | `npx cypress run` |
| `pytest.ini` ou `conftest.py` ou `pyproject.toml` com `[tool.pytest]` | **pytest** | `python -m pytest` |
| `go.mod` existe | **Go test** | `go test ./...` |
| `Cargo.toml` existe | **Rust/cargo** | `cargo test` |
| `mix.exs` existe | **ExUnit** | `mix test` |
| `Gemfile` com `rspec` | **RSpec** | `bundle exec rspec` |
| `package.json` tem `scripts.test` | **npm test** | `npm test` |

Reporte o framework detectado antes de prosseguir.

### Etapa 2: Analisar argumentos

Verifique `$ARGUMENTS` para o modo:

- **Sem argumentos** ou **"all"**: Executar o suite completo de testes (Etapa 3)
- **Caminho do arquivo** (ex: `src/auth/login.ts`): Executar testes para esse arquivo (Etapa 4)
- **"generate" + caminho do arquivo** (ex: `generate src/utils.ts`): Gerar testes (Etapa 5)

### Etapa 3: Executar o suite completo de testes

Execute o comando de testes detectado. Após a conclusão:

- Reporte total de testes, passados, falhados, pulados
- Se os testes falharem, mostre as primeiras 3 mensagens de falha com referências arquivo:linha
- Sugira: "Execute `/test-detect <failing-file>` para investigar uma falha específica"

### Etapa 4: Executar testes para um arquivo específico

Dado um caminho de arquivo de origem, encontre seu arquivo de testes:

**Estratégia de busca** (tente em ordem):
1. `__tests__/<filename>.test.<ext>` (convenção Jest)
2. `<filename>.test.<ext>` (co-localizado)
3. `<filename>.spec.<ext>` (convenção alternativa)
4. `test/<filename>_test.<ext>` (convenção Go/Python)
5. `tests/test_<filename>.<ext>` (convenção pytest)
6. `<filename>_test.go` (convenção Go)

Use Glob para encontrar correspondências. Se encontrado, execute apenas esse arquivo de testes:

| Framework | Comando |
|-----------|---------|
| Vitest | `npx vitest run <test-file>` |
| Jest | `npx jest <test-file>` |
| Playwright | `npx playwright test <test-file>` |
| Cypress | `npx cypress run <test-file>` |
| pytest | `python -m pytest <test-file>` |
| Go | `go test -run <TestName> ./<package>/` |
| Cargo | `cargo test <test_name>` |

Se nenhum arquivo de testes for encontrado, pergunte: "Nenhum teste encontrado para este arquivo. Quer que eu gere testes? Execute `/test-detect generate <file>`"

### Etapa 5: Gerar testes

Leia o arquivo de origem e analise:
1. Identifique todas as funções/classes/componentes exportados
2. Determine os padrões de testes apropriados para o framework
3. Gere um arquivo de testes com:
   - Instruções de importação
   - Bloco `describe` por função/classe
   - Blocos `it`/`test` cobrindo: caminho feliz, casos extremos, casos de erro
   - Assertions e mocking apropriados para o framework

**Salve no local convencional** para o framework detectado:
- Jest/Vitest: `__tests__/<filename>.test.<ext>` ou `<filename>.test.<ext>` (corresponder convenção existente)
- pytest: `tests/test_<filename>.py`
- Go: `<filename>_test.go` (mesmo diretório)
- RSpec: `spec/<filename>_spec.rb`

Mostre o caminho do arquivo gerado e pergunte se o usuário quer executar os novos testes.

## Dicas

- Se múltiplos frameworks forem detectados (ex: Vitest para testes unitários + Playwright para e2e), mencione ambos e padrão para o framework de testes unitários
- Para monorepos, detecte a partir do arquivo de configuração mais próximo ao diretório atual
- Se `package.json` tiver tanto `test` quanto scripts `test:unit`/`test:e2e`, prefira o específico quando o contexto for claro