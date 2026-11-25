---
name: tdd-workflow
description: Princípios do fluxo de Test-Driven Development. Ciclo RED-GREEN-REFACTOR.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Fluxo TDD

> Escreva testes primeiro, código depois.

---

## 1. O Ciclo TDD

```
🔴 RED → Escrever teste que falha
    ↓
🟢 GREEN → Escrever código mínimo para passar
    ↓
🔵 REFACTOR → Melhorar qualidade do código
    ↓
   Repetir...
```

---

## 2. As Três Leis do TDD

1. Escreva código de produção apenas para fazer um teste que falha passar
2. Escreva apenas o suficiente de teste para demonstrar falha
3. Escreva apenas o suficiente de código para fazer o teste passar

---

## 3. Princípios da Fase RED

### O que Escrever

| Foco | Exemplo |
|------|---------|
| Comportamento | "deve somar dois números" |
| Casos extremos | "deve lidar com entrada vazia" |
| Estados de erro | "deve lançar exceção para dados inválidos" |

### Regras da Fase RED

- Teste deve falhar primeiro
- Nome do teste descreve comportamento esperado
- Uma assertion por teste (idealmente)

---

## 4. Princípios da Fase GREEN

### Código Mínimo

| Princípio | Significado |
|-----------|-------------|
| **YAGNI** | You Aren't Gonna Need It |
| **Coisa mais simples** | Escreva o mínimo para passar |
| **Sem otimização** | Apenas faça funcionar |

### Regras da Fase GREEN

- Não escreva código desnecessário
- Não otimize ainda
- Passe no teste, nada mais

---

## 5. Princípios da Fase REFACTOR

### O que Melhorar

| Área | Ação |
|------|------|
| Duplicação | Extraia código comum |
| Nomeação | Deixe a intenção clara |
| Estrutura | Melhore a organização |
| Complexidade | Simplifique a lógica |

### Regras do REFACTOR

- Todos os testes devem ficar verdes
- Mudanças incrementais pequenas
- Commit após cada refatoração

---

## 6. Padrão AAA

Todo teste segue:

| Etapa | Propósito |
|-------|-----------|
| **Arrange** | Configurar dados do teste |
| **Act** | Executar código sob teste |
| **Assert** | Verificar resultado esperado |

---

## 7. Quando Usar TDD

| Cenário | Valor TDD |
|---------|-----------|
| Nova feature | Alto |
| Correção de bug | Alto (escreva teste primeiro) |
| Lógica complexa | Alto |
| Exploratório | Baixo (spike, depois TDD) |
| Layout de UI | Baixo |

---

## 8. Priorização de Testes

| Prioridade | Tipo de Teste |
|------------|---------------|
| 1 | Caminho feliz |
| 2 | Casos de erro |
| 3 | Casos extremos |
| 4 | Performance |

---

## 9. Anti-Padrões

| ❌ Não Faça | ✅ Faça |
|-------------|---------|
| Pule a fase RED | Veja o teste falhar primeiro |
| Escreva testes depois | Escreva testes antes |
| Sobre-engenharia inicial | Mantenha simples |
| Múltiplas assertions | Um comportamento por teste |
| Teste implementação | Teste comportamento |

---

## 10. TDD Aumentado com IA

### Padrão Multi-Agent

| Agent | Papel |
|-------|-------|
| Agent A | Escrever testes que falham (RED) |
| Agent B | Implementar para passar (GREEN) |
| Agent C | Otimizar (REFACTOR) |

---

> **Lembre-se:** O teste é a especificação. Se você não consegue escrever um teste, você não entende o requisito.