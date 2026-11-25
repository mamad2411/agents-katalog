---
name: documentation-publishing
description: Publicação de documentação técnica e manual do usuário no Flyee. Discovery de databases, upsert, mapeamento de fluxos para guias.
---

# Documentation Publishing

> **Publicação estruturada de documentação no Flyee (ou local) ao final de ciclos de projeto.**

---

## 🎯 PROPÓSITO

Garantir que ao concluir trabalho em um escopo/módulo:
1. **Handover** e **Test Guide** são criados
2. **Docs técnicos** são publicados para devs (Database "Documentação Técnica")
3. **Guias de usuário** são publicados para operadores (Database "Manual do Usuário")
4. **Modo Local** registra docs criados sem chamadas a APIs Flyee

---

## 🔴 REGRAS OBRIGATÓRIAS

> [!CAUTION]
> **REGRA BLOQUEANTE:** A publicação tem **DUAS partes obrigatórias:**
> 1. Criar HANDOVER + TEST-GUIDE para o escopo
> 2. Publicar TODOS os docs (flow docs, TDD, DS, handover, test-guide)
>
> Uma sem a outra = **fase INCOMPLETA**.

#### Historical Lesson — Publicação Incompleta

> 🔴 **FALHA (api/ e admin/):** Agente criou HANDOVER + TEST-GUIDE mas **PULOU a publicação
> dos flow docs/TDD/DS no Flyee** (Database "Documentação Técnica"). Devs ficaram sem acesso
> à documentação completa. **Causa raiz:** instrução dizia "Documentação Final" sem mencionar
> publicação Flyee — agente interpretou como "só criar handover".

---

### 1. Criação de Handover e Test Guide

#### HANDOVER-{escopo}.md

Caminho: `docs/handover/{escopo}/HANDOVER-{escopo}.md`

| Seção | Conteúdo |
|-------|----------|
| Visão Geral | Stack, arquitetura, dependências |
| Fluxos Críticos | Resumo dos flow docs |
| Integrações | APIs externas, gateways, services |
| Débitos Resolvidos | Lista de melhorias implementadas |
| Débitos Pendentes | Itens não implementados do TDD |
| Decisões Técnicas | Decisões tomadas durante o projeto |
| Como Rodar | Setup local, env vars, comandos |
| Referências | Links para docs detalhados |

#### TEST-GUIDE-{escopo}.md

Caminho: `docs/tests/{escopo}/TEST-GUIDE-{escopo}.md`

| Seção | Conteúdo |
|-------|----------|
| Stack de Testes | Ferramentas, versões, config |
| Estrutura | Diretórios e organização |
| Mapa de Testes | Tests por domínio (cobertura atual) |
| Como Executar | Comandos para rodar testes |
| Patterns Usados | MSW, mocks, factories, etc |
| Troubleshooting | Problemas comuns e soluções |
| Expansão | Próximos testes prioritários |

---

### 2. Publicação de Documentação Técnica (Flyee)

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Pular discovery e publicação Flyee.
> Registrar docs criados no arquivo de progresso com caminhos dos arquivos.

#### Passo 1: Discovery e Validação do Database

```json
// Buscar database "Documentação Técnica"
{
  "query": "Documentação Técnica",
  "filter": { "property": "object", "value": "data_source" }
}
```

> Se database ausente ou propriedades faltando → PARAR e notificar usuário.

#### Passo 2: Coletar Artefatos

| Fonte | Tipo | Publicar? |
|-------|------|-----------|
| Análise | Arquitetura (`CODEBASE-*.md`) | ✅ |
| Flow docs | Fluxos (`docs/flows/**/*.md`) | ✅ |
| TDD | Design (`docs/design/TDD-*.md`) | ✅ |
| Design System | DS (`design-system/MASTER.md`) | ✅ (se UI) |
| Testes | Cobertura (relatório) | ✅ |
| Handover | Handover (`docs/handover/**/*.md`) | ✅ |
| Test Guide | Testes (`docs/tests/**/*.md`) | ✅ |

#### Passo 3: Para Cada Artefato — Publicar

1. **Verificar upsert** — doc já existe no database? (query por Nome + Módulo)
2. **Ler conteúdo** do arquivo local
3. **Criar ou atualizar** página Flyee
4. **Propriedades:** Nome, Módulo, Tipo, Status, Última Atualização, Arquivo Local, Tasks Relacionadas
5. **Incluir histórico** referenciando tasks da database "Tarefas"

#### Passo 4: Gate de Saída

```
[ ] Database "Documentação Técnica" validado
[ ] Todos os artefatos publicados
[ ] Upsert verificado (sem duplicatas)
[ ] Histórico de atualizações em cada doc
[ ] Tasks relacionadas referenciadas
[ ] Arquivo de progresso atualizado
```

---

### 3. Publicação do Manual do Usuário (Flyee)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Para cada fluxo publicado, DEVE existir uma versão
> em linguagem acessível. Sem código, sem jargão técnico.

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Gerar guias como arquivos em
> `docs/user-guides/{escopo}/` e registrar no arquivo de progresso.

#### Passo 1: Discovery do Database

```json
{
  "query": "Manual do Usuário",
  "filter": { "property": "object", "value": "data_source" }
}
```

> Se database ausente → PARAR e notificar usuário.

#### Passo 2: Mapeamento Fluxo → Guia

Para cada fluxo técnico publicado, gerar versão em linguagem simples.

#### Passo 3: Para Cada Guia — Publicar

1. **Verificar upsert** — guia já existe? (query por Nome)
2. **Gerar conteúdo** em linguagem simples
3. **Criar ou atualizar** página com template de guia
4. **Propriedades:** Nome, Seção, Status, Público-alvo

#### Passo 4: Gate de Saída

```
[ ] Database "Manual do Usuário" validado
[ ] Todos os fluxos mapeados para guias
[ ] Upsert verificado (sem duplicatas)
[ ] Conteúdo sem jargão técnico
[ ] Arquivo de progresso atualizado
```

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Quando usar |
|----------|-------------|
| `/legacy-project` | Phases 8 + 8.5 (handover + publicação) |
| `/new-project` | Phase 7 (documentação final) |
| `/document` | Publicação standalone de docs |
