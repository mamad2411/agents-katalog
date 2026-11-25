# Writing Plans

## Visão Geral

Escreva planos de implementação abrangentes assumindo que o engenheiro não tem contexto sobre nossa base de código e tem gosto questionável. Documente tudo o que ele precisa saber: quais arquivos tocar para cada tarefa, código, testes, docs que pode precisar consultar, como testar. Dê o plano todo em tarefas pequenas. DRY. YAGNI. TDD. Commits frequentes.

Assuma que ele é um desenvolvedor hábil, mas sabe quase nada sobre nossa ferramenta ou domínio do problema. Assuma que não conhece bem design de testes.

**Anuncie no início:** "Estou usando a skill writing-plans para criar o plano de implementação."

**Contexto:** Isso deve ser executado em uma worktree dedicada (criada pela skill de brainstorming).

**Salve planos em:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Granularidade de Tarefas Pequenas

**Cada passo é uma ação (2-5 minutos):**
- "Escrever o teste falhando" - passo
- "Executar para garantir que falha" - passo
- "Implementar o código mínimo para passar no teste" - passo
- "Executar os testes e garantir que passam" - passo
- "Fazer commit" - passo

## Cabeçalho do Documento do Plano

**Todo plano DEVE começar com este cabeçalho:**

```markdown
# [Nome da Feature] - Plano de Implementação

> **Para Claude:** SUB-SKILL OBRIGATÓRIA: Use superpowers:executing-plans para implementar este plano tarefa por tarefa.

**Objetivo:** [Uma frase descrevendo o que isso constrói]

**Arquitetura:** [2-3 frases sobre a abordagem]

**Tech Stack:** [Tecnologias/bibliotecas-chave]

---
```

## Estrutura de Tarefas

```markdown
### Tarefa N: [Nome do Componente]

**Arquivos:**
- Criar: `caminho/exato/para/arquivo.py`
- Modificar: `caminho/exato/para/existente.py:123-145`
- Teste: `tests/caminho/exato/para/teste.py`

**Passo 1: Escrever o teste falhando**

```python
def test_comportamento_especifico():
    resultado = funcao(entrada)
    assert resultado == esperado
```

**Passo 2: Executar teste para verificar que falha**

Execute: `pytest tests/caminho/teste.py::test_nome -v`
Esperado: FAIL com "function not defined"

**Passo 3: Escrever implementação mínima**

```python
def funcao(entrada):
    return esperado
```

**Passo 4: Executar teste para verificar que passa**

Execute: `pytest tests/caminho/teste.py::test_nome -v`
Esperado: PASS

**Passo 5: Fazer commit**

```bash
git add tests/caminho/teste.py src/caminho/arquivo.py
git commit -m "feat: add funcionalidade especifica"
```
```

## Lembre-se
- Caminhos de arquivo exatos sempre
- Código completo no plano (não "adicionar validação")
- Comandos exatos com output esperado
- Referencie skills relevantes com sintaxe @
- DRY, YAGNI, TDD, commits frequentes

## Handoff de Execução

Após salvar o plano, ofereça opção de execução:

**"Plano completo e salvo em `docs/plans/<filename>.md`. Duas opções de execução:**

**1. Dirigida por Subagent (esta sessão)** - Eu despacho subagent fresco por tarefa, reviso entre tarefas, iteração rápida

**2. Sessão Paralela (separada)** - Abra nova sessão com executing-plans, execução em lote com checkpoints

**Qual abordagem?"**

**Se Dirigida por Subagent escolhida:**
- **SUB-SKILL OBRIGATÓRIA:** Use superpowers:subagent-driven-development
- Permaneça nesta sessão
- Subagent fresco por tarefa + code review

**Se Sessão Paralela escolhida:**
- Guie-os a abrir nova sessão na worktree
- **SUB-SKILL OBRIGATÓRIA:** Nova sessão usa superpowers:executing-plans