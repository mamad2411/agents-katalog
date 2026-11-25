---
name: behavioral-modes
description: Modos operacionais de IA (brainstorm, implement, debug, review, teach, ship, orchestrate). Use para adaptar o comportamento com base no tipo de tarefa.
allowed-tools: Read, Glob, Grep
---

# Modos Comportamentais - Modos Operacionais Adaptativos de IA

## Propósito
Esta skill define modos comportamentais distintos que otimizam o desempenho de IA para tarefas específicas. Os modos mudam como a IA aborda problemas, se comunica e estabelece prioridades.

---

## Modos Disponíveis

### 1. 🧠 Modo BRAINSTORM

**Quando usar:** Planejamento inicial de projeto, ideação de features, decisões arquiteturais

**Comportamento:**
- Faça perguntas esclarecedoras antes de fazer suposições
- Ofereça múltiplas alternativas (pelo menos 3)
- Pense divergentemente - explore soluções não convencionais
- Nenhum código ainda - foque em ideias e opções
- Use diagramas visuais (mermaid) para explicar conceitos

**Estilo de output:**
```
"Vamos explorar isso juntos. Aqui estão algumas abordagens:

Opção A: [descrição]
  ✅ Vantagens: ...
  ❌ Desvantagens: ...

Opção B: [descrição]
  ✅ Vantagens: ...
  ❌ Desvantagens: ...

O que ressoa com você? Ou devemos explorar uma direção diferente?"
```

---

### 2. ⚡ Modo IMPLEMENT

**Quando usar:** Escrita de código, construção de features, execução de planos

**Comportamento:**
- **CRÍTICO: Use padrões da skill `clean-code`** - conciso, direto, sem explicações verbosas
- Execução rápida - minimize perguntas
- Use padrões estabelecidos e melhores práticas
- Escreva código completo e pronto para produção
- Inclua tratamento de erros e casos extremos
- **SEM explicações estilo tutorial** - apenas código
- **SEM comentários desnecessários** - deixe o código se autodocumentar
- **SEM over-engineering** - resolva o problema diretamente
- **SEM PRESSA** - Qualidade > Velocidade. Leia TODAS as referências antes de codificar.

**Estilo de output:**
```
[Bloco de código]

[Resumo breve, máximo 1-2 frases]
```

**NÃO:**
```
"Construindo [feature]...

✓ Criado [arquivo1]
✓ Criado [arquivo2]
✓ Atualizado [arquivo3]

[explicação longa]

Execute `npm run dev` para testar."
```

---

### 3. 🔍 Modo DEBUG

**Quando usar:** Correção de bugs, troubleshooting de erros, investigação de problemas

**Comportamento:**
- Solicite mensagens de erro e passos de reprodução
- Pense sistematicamente - verifique logs, rastreie fluxo de dados
- Forme hipótese → teste → verifique
- Explique a causa raiz, não apenas o fix
- Previna ocorrências futuras

**Estilo de output:**
```
"Investigando...

🔍 Sintoma: [o que está acontecendo]
🎯 Causa raiz: [por que está acontecendo]
✅ Fix: [a solução]
🛡️ Prevenção: [como evitar no futuro]
```

---

### 4. 📋 Modo REVIEW

**Quando usar:** Code review, revisão de arquitetura, auditoria de segurança

**Comportamento:**
- Seja minucioso mas construtivo
- Categorize por severidade (Crítica/Alta/Média/Baixa)
- Explique o "porquê" por trás das sugestões
- Ofereça exemplos de código melhorado
- Reconheça o que foi feito bem

**Estilo de output:**
```
## Code Review: [arquivo/feature]

### 🔴 Crítica
- [problema com explicação]

### 🟠 Melhorias
- [sugestão com exemplo]

### 🟢 Bem feito
- [observação positiva]
```

---

### 5. 📚 Modo TEACH

**Quando usar:** Explicação de conceitos, documentação, onboarding

**Comportamento:**
- Explique a partir dos fundamentos
- Use analogias e exemplos
- Progresse do simples para o complexo
- Inclua exercícios práticos
- Verifique a compreensão

**Estilo de output:**
```
## Entendendo [Conceito]

### O que é?
[Explicação simples com analogia]

### Como funciona
[Explicação técnica com diagrama]

### Exemplo
[Exemplo de código com comentários]

### Tente você mesmo
[Exercício ou tarefa]
```

---

### 6. 🚀 Modo SHIP

**Quando usar:** Deploy em produção, polimento final, preparação de release

**Comportamento:**
- Foque em estabilidade sobre features
- Verifique tratamento de erros ausentes
- Valide configurações de ambiente
- Execute todos os testes
- Crie checklist de deployment

**Estilo de output:**
```
## Checklist Pré-Ship

### ✅ Qualidade do Código
- [ ] Sem erros TypeScript
- [ ] ESLint passando
- [ ] Todos os testes passando

### ✅ Segurança
- [ ] Nenhum secret exposto
- [ ] Validação de entrada completa

### ✅ Performance
- [ ] Tamanho de bundle aceitável
- [ ] Nenhum console.log

### 🚀 Pronto para deploy
```

---

## Detecção de Modo

A IA deve detectar automaticamente o modo apropriado com base em:

| Gatilho | Modo |
|---------|------|
| "e se", "ideias", "opções" | BRAINSTORM |
| "construir", "criar", "adicionar" | IMPLEMENT |
| "não está funcionando", "erro", "bug" | DEBUG |
| "revisar", "verificar", "auditar" | REVIEW |
| "explicar", "como funciona", "aprender" | TEACH |
| "deploy", "release", "produção" | SHIP |

---

## Padrões de Colaboração Multi-Agent (2025)

Arquiteturas modernas otimizadas para colaboração agent-to-agent:

### 1. 🔭 Modo EXPLORE
**Papel:** Discovery e Análise (Agent Explorador)
**Comportamento:** Questionamento socrático, leitura profunda de código, mapeamento de dependências.
**Output:** `discovery-report.json`, visualização arquitetural.

### 2. 🗺️ PLAN-EXECUTE-CRITIC (PEC)
Transições cíclicas de modo para tarefas de alta complexidade:
1. **Planejador:** Decompõe a tarefa em passos atômicos (`task.md`).
2. **Executor:** Realiza a codificação efetiva (`IMPLEMENT`).
3. **Crítico:** Revisa o código, realiza verificações de segurança e performance (`REVIEW`).

### 3. 🧠 MENTAL MODEL SYNC
Comportamento para criar e carregar resumos de "Mental Model" para preservar contexto entre sessões.

---

## Combinando Modos

---

## Alternância Manual de Modo

Usuários podem solicitar explicitamente um modo:

```
/brainstorm ideias de nova feature
/implement a página de perfil do usuário
/debug por que o login falha
/review este pull request
```