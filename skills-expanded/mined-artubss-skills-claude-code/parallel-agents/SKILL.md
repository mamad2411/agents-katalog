---
name: parallel-agents
description: Padrões de orquestração multi-agente. Use quando múltiplas tarefas independentes podem rodar com diferentes especialidades de domínio ou quando uma análise abrangente requer múltiplas perspectivas.
allowed-tools: Read, Glob, Grep
---

# Agentes Paralelos Nativos

> Orquestração através do Agent Tool nativo do Claude Code

## Visão Geral

Esta habilidade permite coordenar múltiplos agentes especializados através do sistema de agentes nativo do Claude Code. Diferentemente de scripts externos, essa abordagem mantém toda a orquestração sob controle do Claude.

## Quando Usar Orquestração

✅ **Bom para:**
- Tarefas complexas que requerem múltiplos domínios de expertise
- Análise de código sob perspectivas de segurança, performance e qualidade
- Reviews abrangentes (arquitetura + segurança + testes)
- Implementação de features que precisam de trabalho backend + frontend + banco de dados

❌ **Não é para:**
- Tarefas simples de um único domínio
- Correções rápidas ou pequenas mudanças
- Tarefas onde um agente é suficiente

---

## Invocação de Agentes Nativos

### Agente Único
```
Use o agente security-auditor para revisar autenticação
```

### Cadeia Sequencial
```
Primeiro, use o explorer-agent para descobrir a estrutura do projeto.
Depois, use o backend-specialist para revisar endpoints da API.
Por fim, use o test-engineer para identificar gaps em testes.
```

### Com Passagem de Contexto
```
Use o frontend-specialist para analisar componentes React.
Com base nesses achados, peça ao test-engineer para gerar testes de componentes.
```

### Retomar Trabalho Anterior
```
Retome o agente [agentId] e continue com requisitos adicionais.
```

---

## Padrões de Orquestração

### Padrão 1: Análise Abrangente
```
Agentes: explorer-agent → [domain-agents] → synthesis

1. explorer-agent: Mapear estrutura da codebase
2. security-auditor: Postura de segurança
3. backend-specialist: Qualidade da API
4. frontend-specialist: Padrões de UI/UX
5. test-engineer: Cobertura de testes
6. Sintetizar todos os achados
```

### Padrão 2: Review de Feature
```
Agentes: affected-domain-agents → test-engineer

1. Identificar domínios afetados (backend? frontend? ambos?)
2. Invocar agentes de domínio relevantes
3. test-engineer verifica mudanças
4. Sintetizar recomendações
```

### Padrão 3: Auditoria de Segurança
```
Agentes: security-auditor → penetration-tester → synthesis

1. security-auditor: Review de configuração e código
2. penetration-tester: Testes de vulnerabilidades ativas
3. Sintetizar com remediação priorizada
```

---

## Agentes Disponíveis

| Agente | Expertise | Frases de Gatilho |
|--------|-----------|-------------------|
| `orchestrator` | Coordenação | "abrangente", "múltiplas perspectivas" |
| `security-auditor` | Segurança | "segurança", "autenticação", "vulnerabilidades" |
| `penetration-tester` | Teste de Segurança | "pentest", "red team", "exploit" |
| `backend-specialist` | Backend | "API", "servidor", "Node.js", "Express" |
| `frontend-specialist` | Frontend | "React", "UI", "componentes", "Next.js" |
| `test-engineer` | Testes | "testes", "cobertura", "TDD" |
| `devops-engineer` | DevOps | "deploy", "CI/CD", "infraestrutura" |
| `database-architect` | Banco de Dados | "schema", "Prisma", "migrations" |
| `mobile-developer` | Mobile | "React Native", "Flutter", "mobile" |
| `api-designer` | Design de API | "REST", "GraphQL", "OpenAPI" |
| `debugger` | Debugging | "bug", "erro", "não funciona" |
| `explorer-agent` | Discovery | "explorar", "mapear", "estrutura" |
| `documentation-writer` | Documentação | "escrever docs", "criar README", "gerar API docs" |
| `performance-optimizer` | Performance | "lento", "otimizar", "profiling" |
| `project-planner` | Planejamento | "planejar", "roadmap", "milestones" |
| `seo-specialist` | SEO | "SEO", "meta tags", "ranking de busca" |
| `game-developer` | Game Development | "game", "Unity", "Godot", "Phaser" |

---

## Agentes Nativos do Claude Code

Estes funcionam lado a lado com agentes customizados:

| Agente | Modelo | Propósito |
|--------|--------|----------|
| **Explore** | Haiku | Busca rápida e somente leitura na codebase |
| **Plan** | Sonnet | Pesquisa durante o modo plan |
| **General-purpose** | Sonnet | Modificações complexas em múltiplas etapas |

Use **Explore** para buscas rápidas, **agentes customizados** para expertise de domínio.

---

## Protocolo de Síntese

Após todos os agentes completarem, sintetize:

```markdown
## Síntese de Orquestração

### Resumo da Tarefa
[O que foi realizado]

### Contribuições dos Agentes
| Agente | Achado |
|--------|--------|
| security-auditor | Encontrou X |
| backend-specialist | Identificou Y |

### Recomendações Consolidadas
1. **Crítico**: [Problema do Agente A]
2. **Importante**: [Problema do Agente B]
3. **Nice-to-have**: [Melhoria do Agente C]

### Itens de Ação
- [ ] Corrigir problema crítico de segurança
- [ ] Refatorar endpoint da API
- [ ] Adicionar testes faltantes
```

---

## Melhores Práticas

1. **Agentes disponíveis** - 17 agentes especializados podem ser orquestrados
2. **Ordem lógica** - Discovery → Analysis → Implementation → Testing
3. **Compartilhar contexto** - Passar achados relevantes para agentes subsequentes
4. **Síntese única** - Um relatório unificado, não outputs separados
5. **Verificar mudanças** - Sempre incluir test-engineer para modificações de código

---

## Principais Benefícios

- ✅ **Sessão única** - Todos os agentes compartilham contexto
- ✅ **Controlado por IA** - Claude orquestra autonomamente
- ✅ **Integração nativa** - Funciona com agentes Explore e Plan nativos
- ✅ **Suporte a retomada** - Pode continuar trabalho anterior de agentes
- ✅ **Passagem de contexto** - Achados fluem entre agentes