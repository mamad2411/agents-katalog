---
name: plan-writing
description: Planejamento estruturado de tarefas com divisões claras, dependências e critérios de verificação. Use ao implementar recursos, refatorar ou realizar qualquer trabalho em múltiplas etapas.
allowed-tools: Read, Glob, Grep
---

# Escrita de Planos

> Fonte: obra/superpowers

## Visão Geral
Esta habilidade fornece um framework para dividir trabalho em tarefas claras e acionáveis com critérios de verificação.

## Princípios de Divisão de Tarefas

### 1. Tarefas Pequenas e Focadas
- Cada tarefa deve levar 2-5 minutos
- Um resultado claro por tarefa
- Independentemente verificável

### 2. Verificação Clara
- Como você sabe que está pronto?
- O que você pode verificar/testar?
- Qual é o resultado esperado?

### 3. Ordenação Lógica
- Dependências identificadas
- Trabalho paralelo quando possível
- Caminho crítico destacado
- **Fase X: Verificação é SEMPRE POR ÚLTIMO**

### 4. Nomenclatura Dinâmica na Raiz do Projeto
- Arquivos de plano são salvos como `{task-slug}.md` na RAIZ DO PROJETO
- Nome derivado da tarefa (ex: "add auth" → `auth-feature.md`)
- **NUNCA** dentro de `.claude/`, `docs/` ou pastas temporárias

## Princípios de Planejamento (NÃO Templates!)

> 🔴 **SEM templates fixos. Cada plano é ÚNICO para a tarefa.**

### Princípio 1: Mantenha CURTO

| ❌ Errado | ✅ Correto |
|----------|----------|
| 50 tarefas com sub-sub-tarefas | 5-10 tarefas claras no máximo |
| Cada micro-passo listado | Apenas itens acionáveis |
| Descrições verbosas | Uma linha por tarefa |

> **Regra:** Se o plano tem mais de 1 página, está muito longo. Simplifique.

---

### Princípio 2: Seja ESPECÍFICO, Não Genérico

| ❌ Errado | ✅ Correto |
|----------|----------|
| "Configurar projeto" | "Executar `npx create-next-app`" |
| "Adicionar autenticação" | "Instalar next-auth, criar `/api/auth/[...nextauth].ts`" |
| "Estilizar a UI" | "Adicionar classes Tailwind a `Header.tsx`" |

> **Regra:** Cada tarefa deve ter um resultado claro e verificável.

---

### Princípio 3: Conteúdo Dinâmico Baseado no Tipo de Projeto

**Para NOVO PROJETO:**
- Qual é o stack de tecnologia? (decide primeiro)
- Qual é o MVP? (recursos mínimos)
- Qual é a estrutura de arquivos?

**Para ADIÇÃO DE RECURSO:**
- Quais arquivos são afetados?
- Quais dependências são necessárias?
- Como verificar que funciona?

**Para CORREÇÃO DE BUG:**
- Qual é a causa raiz?
- Qual arquivo/linha mudar?
- Como testar a correção?

---

### Princípio 4: Scripts São Específicos do Projeto

> 🔴 **NÃO copie-cole comandos de script. Escolha baseado no tipo de projeto.**

| Tipo de Projeto | Scripts Relevantes |
|--------------|------------------|
| Frontend/React | `ux_audit.py`, `accessibility_checker.py` |
| Backend/API | `api_validator.py`, `security_scan.py` |
| Mobile | `mobile_audit.py` |
| Database | `schema_validator.py` |
| Full-stack | Mix dos acima baseado no que você tocou |

**Errado:** Adicionar todos os scripts a cada plano
**Correto:** Apenas scripts relevantes PARA ESTA tarefa

---

### Princípio 5: Verificação é Simples

| ❌ Errado | ✅ Correto |
|----------|----------|
| "Verificar que o componente funciona corretamente" | "Executar `npm run dev`, clicar no botão, ver toast" |
| "Testar a API" | "curl localhost:3000/api/users retorna 200" |
| "Verificar estilos" | "Abrir navegador, verificar que toggle de dark mode funciona" |

---

## Estrutura do Plano (Flexível, Não Fixa!)

```
# [Nome da Tarefa]

## Objetivo
Uma frase: O que estamos construindo/corrigindo?

## Tarefas
- [ ] Tarefa 1: [Ação específica] → Verificar: [Como verificar]
- [ ] Tarefa 2: [Ação específica] → Verificar: [Como verificar]
- [ ] Tarefa 3: [Ação específica] → Verificar: [Como verificar]

## Pronto Quando
- [ ] [Critério principal de sucesso]
```

> **É só isso.** Sem fases, sem sub-seções a menos que realmente necessário.
> Mantenha minimalista. Adicione complexidade apenas quando obrigatório.

## Notas
[Qualquer consideração importante]
```

---

## Melhores Práticas (Referência Rápida)

1. **Comece com o objetivo** - O que estamos construindo/corrigindo?
2. **Máximo 10 tarefas** - Se mais, divida em múltiplos planos
3. **Cada tarefa verificável** - Critérios claros de "pronto"
4. **Específico do projeto** - Sem templates copy-paste
5. **Atualize conforme avança** - Marque `[x]` quando completar

---

## Quando Usar

- Novo projeto do zero
- Adicionando um recurso
- Corrigindo um bug (se complexo)
- Refatorando múltiplos arquivos