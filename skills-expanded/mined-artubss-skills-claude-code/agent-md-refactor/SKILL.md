---
name: agent-md-refactor
description: Refatore arquivos de instruções de agentes AGENTS.md, CLAUDE.md ou similares para seguir princípios de divulgação progressiva. Divide arquivos monolíticos em documentação organizada e vinculada.
license: MIT
---

# Agent MD Refactor

Refatore arquivos de instruções de agentes bloated (AGENTS.md, CLAUDE.md, COPILOT.md, etc.) para seguir **princípios de divulgação progressiva** - mantendo essenciais na raiz e organizando o resto em arquivos categorizados e vinculados.

---

## Triggers

Use essa skill quando:
- "refatore meu AGENTS.md" / "refatore meu CLAUDE.md"
- "divida minhas instruções de agente"
- "organize meu arquivo CLAUDE.md"
- "meu AGENTS.md é muito longo"
- "divulgação progressiva para minhas instruções"
- "limpe minha configuração de agente"

---

## Referência Rápida

| Fase | Ação | Output |
|------|------|--------|
| 1. Analisar | Encontrar contradições | Lista de conflitos para resolver |
| 2. Extrair | Identificar essenciais | Instruções centrais para arquivo raiz |
| 3. Categorizar | Agrupar instruções restantes | Categorias lógicas |
| 4. Estruturar | Criar hierarquia de arquivos | Raiz + arquivos vinculados |
| 5. Podar | Sinalizar para exclusão | Instruções redundantes/vagas |

---

## Processo

### Fase 1: Encontrar Contradições

Identifique instruções que conflitem umas com as outras.

**Procure por:**
- Guias de estilo contraditórios (ex: "use ponto-e-vírgula" vs "sem ponto-e-vírgula")
- Instruções de workflow conflitantes
- Preferências de ferramentas incompatíveis
- Padrões mutuamente exclusivos

**Para cada contradição encontrada:**
```markdown
## Contradição Encontrada

**Instrução A:** [citação]
**Instrução B:** [citação]

**Pergunta:** Qual deve ter precedência, ou ambas devem ser condicionais?
```

Peça ao usuário para resolver antes de prosseguir.

---

### Fase 2: Identificar os Essenciais

Extraia APENAS o que pertence ao arquivo raiz do agente. A raiz deve ser mínima - informações que se aplicam a **todas as tarefas**.

**Conteúdo essencial (manter na raiz):**
| Categoria | Exemplo |
|-----------|---------|
| Descrição do projeto | Uma frase: "Um dashboard React para análise" |
| Gerenciador de pacotes | Apenas se não for npm (ex: "Usa pnpm") |
| Comandos não-padrão | Comandos customizados build/test/typecheck |
| Overrides críticos | Coisas que DEVEM sobrescrever padrões |
| Regras universais | Se aplica a 100% das tarefas |

**NÃO essencial (mover para arquivos vinculados):**
- Convenções específicas de linguagem
- Diretrizes de teste
- Detalhes de estilo de código
- Padrões de framework
- Padrões de documentação
- Detalhes de workflow Git

---

### Fase 3: Agrupar o Resto

Organize instruções restantes em categorias lógicas.

**Categorias comuns:**
| Categoria | Conteúdo |
|-----------|----------|
| `typescript.md` | Convenções TS, padrões de tipo, regras de modo strict |
| `testing.md` | Frameworks de teste, cobertura, padrões de mock |
| `code-style.md` | Formatação, naming, comentários, estrutura |
| `git-workflow.md` | Commits, branches, PRs, reviews |
| `architecture.md` | Padrões, estrutura de pastas, dependências |
| `api-design.md` | Convenções REST/GraphQL, tratamento de erros |
| `security.md` | Padrões de auth, validação de entrada, secrets |
| `performance.md` | Regras de otimização, caching, lazy loading |

**Regras de agrupamento:**
1. Cada arquivo deve ser auto-contido para seu tópico
2. Aim para 3-8 arquivos (nem muito granular, nem muito amplo)
3. Nomeie arquivos claramente: `{topico}.md`
4. Inclua apenas instruções acionáveis

---

### Fase 4: Criar a Estrutura de Arquivos

**Estrutura de output:**
```
project-root/
├── CLAUDE.md (ou AGENTS.md)      # Raiz mínima com links
└── .claude/                       # Ou docs/agent-instructions/
    ├── typescript.md
    ├── testing.md
    ├── code-style.md
    ├── git-workflow.md
    └── architecture.md
```

**Template do arquivo raiz:**
```markdown
# Nome do Projeto

Descrição de uma frase do projeto.

## Referência Rápida

- **Gerenciador de Pacotes:** pnpm
- **Build:** `pnpm build`
- **Teste:** `pnpm test`
- **Typecheck:** `pnpm typecheck`

## Instruções Detalhadas

Para diretrizes específicas, consulte:
- [Convenções TypeScript](.claude/typescript.md)
- [Diretrizes de Teste](.claude/testing.md)
- [Estilo de Código](.claude/code-style.md)
- [Workflow Git](.claude/git-workflow.md)
- [Padrões de Arquitetura](.claude/architecture.md)
```

**Template de cada arquivo vinculado:**
```markdown
# Diretrizes de {Tópico}

## Visão Geral
Contexto breve de quando estas diretrizes se aplicam.

## Regras

### Categoria de Regra 1
- Instrução específica e acionável
- Outra instrução específica

### Categoria de Regra 2
- Instrução específica e acionável

## Exemplos

### Bom
\`\`\`typescript
// Exemplo de padrão correto
\`\`\`

### Evitar
\`\`\`typescript
// Exemplo do que não fazer
\`\`\`
```

---

### Fase 5: Sinalizar para Exclusão

Identifique instruções que devem ser removidas completamente.

**Exclua se:**
| Critério | Exemplo | Por Quê Excluir |
|----------|---------|-----------------|
| Redundante | "Use TypeScript" (em projeto .ts) | Agent já sabe |
| Muito vago | "Escreva código limpo" | Não é acionável |
| Óbvio demais | "Não introduza bugs" | Desperdiça contexto |
| Comportamento padrão | "Use nomes descritivos de variáveis" | Prática padrão |
| Desatualizado | Referencia APIs obsoletas | Não se aplica mais |

**Formato de output:**
```markdown
## Sinalizado para Exclusão

| Instrução | Razão |
|-----------|-------|
| "Escreva código limpo e mantível" | Muito vago para ser acionável |
| "Use TypeScript" | Redundante - projeto já é TS |
| "Não cometa secrets" | Agent já sabe disso |
| "Siga best practices" | Sem sentido sem especificidades |
```

---

## Checklist de Execução

```
[ ] Fase 1: Todas as contradições identificadas e resolvidas
[ ] Fase 2: Arquivo raiz contém APENAS essenciais
[ ] Fase 3: Todas as instruções restantes categorizadas
[ ] Fase 4: Estrutura de arquivo criada com links apropriados
[ ] Fase 5: Instruções redundantes/vagas removidas
[ ] Verificar: Cada arquivo vinculado é auto-contido
[ ] Verificar: Arquivo raiz tem menos de 50 linhas
[ ] Verificar: Todos os links funcionam corretamente
```

---

## Anti-Padrões

| Evite | Por Quê | Ao Invés |
|-------|--------|---------|
| Manter tudo na raiz | Bloated, difícil de manter | Divida em arquivos vinculados |
| Muitas categorias | Fragmentação | Consolide tópicos relacionados |
| Instruções vagas | Desperdiça tokens, sem valor | Seja específico ou exclua |
| Duplicar padrões | Agent já sabe | Sobrescreva apenas quando necessário |
| Deep nesting | Difícil de navegar | Estrutura flat com links |

---

## Exemplos

### Antes (Raiz Bloated)
```markdown
# CLAUDE.md

Este é um projeto React.

## Code Style
- Use 2 espaços
- Use ponto-e-vírgula
- Prefira const sobre let
- Use arrow functions
... (200 linhas mais)

## Testing
- Use Jest
- Cobertura > 80%
... (100 linhas mais)

## TypeScript
- Habilite strict mode
... (150 linhas mais)
```

### Depois (Divulgação Progressiva)
```markdown
# CLAUDE.md

Dashboard React para visualização de análise em tempo real.

## Comandos
- `pnpm dev` - Inicie servidor de desenvolvimento
- `pnpm test` - Execute testes com cobertura
- `pnpm build` - Build de produção

## Diretrizes
- [Estilo de Código](.claude/code-style.md)
- [Teste](.claude/testing.md)
- [TypeScript](.claude/typescript.md)
```

---

## Verificação

Após refatorar, verifique:

1. **Arquivo raiz é mínimo** - Menos de 50 linhas, apenas info universal
2. **Links funcionam** - Todos os arquivos referenciados existem
3. **Sem contradições** - Instruções são consistentes
4. **Conteúdo acionável** - Cada instrução é específica
5. **Cobertura completa** - Nenhuma instrução foi perdida (a menos que sinalizada para exclusão)
6. **Arquivos auto-contidos** - Cada arquivo vinculado é independente

---