---
name: auditar-cobertura
description: "Analisa relatórios de cobertura Jest e identifica lacunas na suíte de testes. Use quando um dev ou o tech-lead precisa avaliar a qualidade da cobertura antes do PR."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: auditar-cobertura

Analisa o **relatório de cobertura de testes** de um serviço Node.js, identifica gaps críticos e recomenda quais testes devem ser escritos para garantir qualidade mínima sem desperdício de esforço.

**Agente:** `dev-backend`, `dev-frontend`, `dev-mobile`, `tech-lead`  
**Guardrails aplicáveis:** `00-core.md`, `testes.md`

---

## Quando usar

- Antes de abrir PR para verificar se a cobertura está adequada
- Ao revisar serviço legado que precisa aumentar cobertura
- Após adicionar nova funcionalidade para garantir que foi coberta
- Para priorizar quais testes escrever quando o tempo é limitado

---

## Processo de execução

### Passo 1 — Gerar o relatório de cobertura

```bash
npm test -- --coverage --coverageReporters=text --coverageReporters=lcov
```

Ou, para um módulo específico:
```bash
npm test -- --coverage --testPathPattern="user" --coverageReporters=text
```

O relatório texto mostra:
```
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
user.service.ts     |   72.31 |    55.00 |   66.67 |   71.43 |
user.controller.ts  |   100   |   100    |   100   |   100   |
```

### Passo 2 — Identificar o que cada métrica significa

| Métrica | O que mede | Mais importante para |
|---|---|---|
| **Statements** | Linhas de código executadas | Cobertura geral |
| **Branches** | Caminhos de `if/else`, `switch`, `??` | Lógica condicional — o mais crítico |
| **Functions** | Funções/métodos chamados | Código morto |
| **Lines** | Linhas executadas (similar a Statements) | Referência geral |

**Branch coverage é o mais importante**: uma função com 100% de statement coverage pode ter 0% de branch coverage se nenhum `if` falso foi exercitado.

### Passo 3 — Classificar os gaps por criticidade

Não toda linha não coberta tem o mesmo risco:

| Tipo de código não coberto | Criticidade | Ação |
|---|---|---|
| Caminho de erro (catch, exceção lançada) | Alta | Escrever teste de erro |
| Condição de negócio (`if status !== 'active'`) | Alta | Escrever teste do caso negativo |
| Função nunca chamada | Média | Verificar se é código morto — remover ou testar |
| Linha de log ou telemetria | Baixa | Pode ignorar |
| Código de bootstrap/main | Baixa | Excluir da cobertura |
| Interfaces e tipos TypeScript | N/A | Não contam como código executável |

### Passo 4 — Definir limites mínimos

Limites recomendados por tipo de arquivo:

| Arquivo | Branches mínimo | Statements mínimo |
|---|---|---|
| `*.service.ts` (lógica de negócio) | 80% | 85% |
| `*.controller.ts` (rotas) | 70% | 80% |
| `*.guard.ts`, `*.filter.ts` | 70% | 80% |
| `*.dto.ts`, `*.entity.ts` | N/A — não são testados diretamente |
| `main.ts`, `*.module.ts` | Excluir da cobertura |

### Passo 5 — Priorizar o que testar

Ordenar por impacto de negócio × risco:

1. **Caminho de erro em operações críticas** — pagamento, criação de conta, autenticação
2. **Branches de regra de negócio** — condições que determinam comportamento importante
3. **Funções completamente não cobertas** — verificar se são dead code
4. **Caminho feliz de funcionalidades principais** — se ainda não coberto

### Passo 6 — Excluir da cobertura o que não deve ser medido

`package.json` (seção jest):
```json
"jest": {
  "coveragePathIgnorePatterns": [
    "/node_modules/",
    "/dist/",
    "main.ts",
    ".*\\.module\\.ts$",
    ".*\\.dto\\.ts$",
    ".*\\.entity\\.ts$"
  ]
}
```

---

## Saída produzida

```markdown
## Auditoria de Cobertura: <nome do serviço>

**Data:** YYYY-MM-DD  
**Cobertura atual:**

| Arquivo | Branches | Statements | Status |
|---|---|---|---|
| user.service.ts | 55% | 72% | ⛔ Abaixo do mínimo |
| user.controller.ts | 100% | 100% | ✅ OK |
| auth.guard.ts | 40% | 60% | ⛔ Abaixo do mínimo |

---

### Gaps críticos (escrever agora)

1. **user.service.ts — método `create` — branch: email já existente**  
   Linha 23: `if (existing)` — o caminho `true` nunca foi executado.  
   Risco: lógica de conflito não testada pode deixar duplicatas no banco.  
   Ação: adicionar `criar-teste-unitario` com caso `should throw ConflictException when email exists`.

2. **auth.guard.ts — branch: token expirado**  
   Linha 15: `if (!payload.sub)` — não coberto.  
   Risco: comportamento de autenticação com token inválido não validado.  
   Ação: adicionar teste do guard com token sem `sub`.

---

### Gaps de baixa prioridade (pode deixar para depois)

- `user.service.ts` linha 87: log de auditoria — não crítico.

---

### Recomendação

Escrever os 2 testes críticos antes de abrir PR. Cobertura esperada após: Branches 82%, Statements 89%.
```
