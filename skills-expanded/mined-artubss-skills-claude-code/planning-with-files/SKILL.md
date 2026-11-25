---
name: planning-with-files
description: Transforma o workflow para usar arquivos markdown persistentes ao estilo Manus para planejamento, rastreamento de progresso e armazenamento de conhecimento. Use ao iniciar tarefas complexas, projetos em múltiplas etapas, tarefas de pesquisa, ou quando o usuário menciona planejamento, organização de trabalho, rastreamento de progresso ou deseja saída estruturada.
---

# Planejamento com Arquivos

Trabalhe como Manus: Use arquivos markdown persistentes como sua "memória de trabalho no disco".

## Início Rápido

Antes de QUALQUER tarefa complexa:

1. **Crie `task_plan.md`** no diretório de trabalho
2. **Defina fases** com checkboxes
3. **Atualize após cada fase** - marque [x] e mude o status
4. **Leia antes de decidir** - refresque os objetivos na janela de atenção

## O Padrão de 3 Arquivos

Para toda tarefa não trivial, crie TRÊS arquivos:

| Arquivo | Propósito | Quando Atualizar |
|---------|-----------|------------------|
| `task_plan.md` | Rastrear fases e progresso | Após cada fase |
| `notes.md` | Armazenar descobertas e pesquisa | Durante pesquisa |
| `[deliverable].md` | Saída final | Na conclusão |

## Workflow Principal

```
Loop 1: Criar task_plan.md com objetivo e fases
Loop 2: Pesquisar → salvar em notes.md → atualizar task_plan.md
Loop 3: Ler notes.md → criar deliverable → atualizar task_plan.md
Loop 4: Entregar saída final
```

### O Loop em Detalhes

**Antes de cada ação principal:**
```bash
Read task_plan.md  # Refresque os objetivos na janela de atenção
```

**Após cada fase:**
```bash
Edit task_plan.md  # Marque [x], atualize o status
```

**Ao armazenar informações:**
```bash
Write notes.md     # Não abarrote contexto, armazene em arquivo
```

## Modelo task_plan.md

Crie este arquivo PRIMEIRO para qualquer tarefa complexa:

```markdown
# Plano de Tarefa: [Descrição Breve]

## Objetivo
[Uma frase descrevendo o estado final]

## Fases
- [ ] Fase 1: Planejamento e configuração
- [ ] Fase 2: Pesquisa/coleta de informações
- [ ] Fase 3: Execução/construção
- [ ] Fase 4: Revisão e entrega

## Perguntas-Chave
1. [Pergunta a responder]
2. [Pergunta a responder]

## Decisões Tomadas
- [Decisão]: [Fundamentação]

## Erros Encontrados
- [Erro]: [Resolução]

## Status
**Atualmente na Fase X** - [O que estou fazendo agora]
```

## Modelo notes.md

Para pesquisa e descobertas:

```markdown
# Notas: [Tópico]

## Fontes

### Fonte 1: [Nome]
- URL: [link]
- Pontos-chave:
  - [Descoberta]
  - [Descoberta]

## Descobertas Sintetizadas

### [Categoria]
- [Descoberta]
- [Descoberta]
```

## Regras Críticas

### 1. SEMPRE Crie o Plano Primeiro
Nunca inicie uma tarefa complexa sem `task_plan.md`. Isto é inegociável.

### 2. Leia Antes de Decidir
Antes de qualquer decisão importante, leia o arquivo de plano. Isto mantém os objetivos em sua janela de atenção.

### 3. Atualize Após Agir
Após completar qualquer fase, atualize imediatamente o arquivo de plano:
- Marque fases concluídas com [x]
- Atualize a seção Status
- Registre todos os erros encontrados

### 4. Armazene, Não Abarrote
Saídas grandes vão para arquivos, não contexto. Mantenha apenas paths na memória de trabalho.

### 5. Registre Todos os Erros
Todo erro vai na seção "Erros Encontrados". Isto constrói conhecimento para tarefas futuras.

## Quando Usar Este Padrão

**Use o padrão de 3 arquivos para:**
- Tarefas com múltiplas etapas (3+ etapas)
- Tarefas de pesquisa
- Construir/criar algo
- Tarefas que abrangem múltiplas chamadas de ferramenta
- Qualquer coisa que exija organização

**Pule para:**
- Perguntas simples
- Edições de arquivo único
- Buscas rápidas

## Anti-Padrões a Evitar

| Não Faça | Faça Ao Invés |
|----------|---------------|
| Use TodoWrite para persistência | Crie arquivo `task_plan.md` |
| Defina objetivos uma vez e esqueça | Releia o plano antes de cada decisão |
| Esconda erros e tente novamente | Registre erros no arquivo de plano |
| Abarrote tudo no contexto | Armazene conteúdo grande em arquivos |
| Comece executando imediatamente | Crie arquivo de plano PRIMEIRO |

## Padrões Avançados

Veja [reference.md](reference.md) para:
- Técnicas de manipulação de atenção
- Padrões de recuperação de erro
- Otimização de contexto do Manus

Veja [examples.md](examples.md) para:
- Exemplos de tarefas reais
- Padrões de workflow complexo