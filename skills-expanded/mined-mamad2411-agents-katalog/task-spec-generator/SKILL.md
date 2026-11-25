---
name: task-spec-generator
description: >-
  Gera a especificação técnica de implementação (spec) e cria automaticamente a branch Git de uma task do projeto
  a partir do código identificador da task (ex: TK01.1, TK05.2) consultando o docs/PRD.md
  e o backlog. Estrutura a spec em specs/active/spec-<task-id>-<nome>.md.
---

# Gerador de Especificação Técnica de Tasks (Spec Generator)

Esta skill orienta assistentes e agentes de IA a criarem uma branch Git dedicada e gerarem especificações técnicas detalhadas antes de qualquer implementação de código, consultando os requisitos no `docs/PRD.md`.

## Fluxo de Execução

1. **Receber o Identificador da Task**:
   - O desenvolvedor informa o código da task (ex: `TK01.1`, `TK05.1`).
2. **Consultar a Fonte da Verdade (`docs/PRD.md`)**:
   - Localizar a task no `docs/PRD.md` ou no backlog do projeto.
   - Extrair a **História de Usuário (US)** associada, o **Épico/Feature**, os **Requisitos (RF/RNF)** e os **Critérios de Aceitação (CA)** em Gherkin.
3. **Criar a Branch Git da Task**:
   - Criar e alternar para a branch dedicada da task no padrão `feat/<task-id-kebab>-<nome-kebab>` (ou `fix/`, `test/`, etc., conforme o tipo da tarefa):
     ```bash
     git checkout -b feat/<task-id-kebab>-<nome-kebab>
     # Exemplo: git checkout -b feat/tk01-1-initial-structure
     ```
4. **Gerar a Especificação em `specs/active/`**:
   - Criar o arquivo `specs/active/spec-<task-id>-<nome-kebab-case>.md` seguindo a estrutura padrão abaixo, incluindo o nome da branch nos metadados.
5. **Ciclo de Vida da Spec e da Branch**:
   - Enquanto a tarefa estiver sendo planejada ou codificada, o trabalho é realizado na branch dedicada e a spec permanece em `specs/active/`.
   - Após a implementação, realização de commits atômicos com Conventional Commits e aprovação em todos os testes/critérios de validação:
     - Mover a spec concluída para `specs/archived/` (`git mv specs/active/... specs/archived/...`).
     - Realizar o merge ou abrir Pull Request da branch para a branch principal (`main`).

---

## Estrutura Padrão da Spec

```markdown
# Spec <task-id>: <Nome da Task>

- **Status**: Ativa
- **Data**: AAAA-MM-DD
- **Task**: <task-id>
- **Branch**: feat/<task-id-kebab>-<nome-kebab>
- **História de Usuário**: <USXX>
- **Requisitos Atendidos**: <RFXX / RNFXX>

## 1. Contexto e Objetivos

Explicação concisa do objetivo desta task, o problema que resolve e o impacto na aplicação.

## 2. Arquivos Afetados

Lista precisa dos arquivos que serão criados, modificados ou removidos:

| Arquivo | Ação | Responsabilidade |
| ------- | ---- | ---------------- |
| `src/...` | Criar / Modificar | Descrição do papel do arquivo |

## 3. Plano de Implementação por Fases

Detalhamento passo a passo em ordem lógica e incremental:

1. **Fase 1 · Preparação e Schemas**: criação de interfaces, tipos ou schemas.
2. **Fase 2 · Lógica e Camadas**: implementação em models, controllers ou serviços.
3. **Fase 3 · Integração e Rotas**: conexão aos middlewares e rotas da API/interface.

## 4. Critérios de Aceitação (Gherkin)

Cenários BDD extraídos do PRD correspondentes a esta task:

\`\`\`gherkin
Cenário: CAXX.Y - <Título do Cenário>
  Dado <condição inicial>
  Quando <ação executada>
  Então <resultado esperado>
\`\`\`

## 5. Plano de Verificação

Comandos e asserções que provam a conclusão com sucesso:

- `pnpm check` ou `biome check .`: conformidade estática e checagem de tipos.
- `pnpm build`: ausência total de erros de compilação e build.
- `pnpm test`: execução da suíte de testes automatizados.
- Verificação manual ou chamadas HTTP via `requests.http`.
```
## Kanban E GitHub Projects

Ao criar a spec e a branch, sugira sincronizar o Kanban com a skill `task-kanban-sync`:

- criar ou localizar o card/issue da task;
- colocar o item em `TODO` quando ainda nao houver responsavel executando;
- mover para `DOING` quando a task for atribuida a uma pessoa ou o usuario pedir inicio imediato;
- vincular o card a `docs/PRD.md`, a spec em `specs/active/` e a branch criada.

Criar ou mover card remoto exige autorizacao explicita ou pedido claro do usuario. Sem autorizacao, entregue a sugestao e os comandos/passos manuais.
