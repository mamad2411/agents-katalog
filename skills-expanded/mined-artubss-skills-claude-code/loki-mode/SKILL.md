---
name: loki-mode
description: Sistema autônomo multi-agente para startups em Claude Code. Ativado com "Loki Mode". Orquestra 100+ agentes especializados em engenharia, QA, DevOps, segurança, dados/ML, operações comerciais, marketing, RH e sucesso do cliente. Vai de PRD para produto totalmente implantado e gerando receita com zero intervenção humana. Inclui ferramenta Task para despacho de subagentes, revisão de código paralela com 3 revisores especializados, triagem de problemas baseada em severidade, fila de tarefas distribuída com tratamento de dead letter, implantação automática em provedores de nuvem, testes A/B, loops de feedback de clientes, resposta a incidentes, circuit breakers e auto-recuperação. Gerencia limites de taxa via checkpoints de estado distribuído e retomada automática com backoff exponencial. Requer flag --dangerously-skip-permissions.
---

# Loki Mode - Sistema Autônomo Multi-Agente para Startups

> **Versão 2.35.0** | PRD para Produção | Zero Intervenção Humana
> Aprimorado com pesquisa: OpenAI SDK, DeepMind, Anthropic, AWS Bedrock, Agent SDK, HN Production (2025)

---

## Referência Rápida

### Primeiros Passos Críticos (A Cada Iteração)
1. **LEIA** `.loki/CONTINUITY.md` - Sua memória de trabalho + "Erros & Aprendizados"
2. **RECUPERE** Memórias relevantes de `.loki/memory/` (padrões episódicos, anti-padrões)
3. **VERIFIQUE** `.loki/state/orchestrator.json` - Fase atual/métricas
4. **ANALISE** `.loki/queue/pending.json` - Próximas tarefas
5. **SIGA** Ciclo RARV: RAZÃO, AÇÃO, REFLEXÃO, **VERIFICAÇÃO** (teste seu trabalho!)
6. **OTIMIZE** Opus=planejamento, Sonnet=desenvolvimento, Haiku=testes unitários/monitoramento - 10+ agentes Haiku em paralelo
7. **RASTREIE** Métricas de eficiência: tokens, tempo, contagem de agentes por tarefa
8. **CONSOLIDE** Após tarefa: Atualize memória episódica, extraia padrões para memória semântica

### Arquivos-Chave (Ordem de Prioridade)
| Arquivo | Propósito | Atualizar Quando |
|---------|-----------|-----------------|
| `.loki/CONTINUITY.md` | Memória de trabalho - o que estou fazendo AGORA? | A cada iteração |
| `.loki/memory/semantic/` | Padrões generalizados & anti-padrões | Após conclusão de tarefa |
| `.loki/memory/episodic/` | Traços de interação específicos | Após cada ação |
| `.loki/metrics/efficiency/` | Pontuações de eficiência de tarefas & recompensas | Após cada tarefa |
| `.loki/specs/openapi.yaml` | Spec de API - fonte de verdade | Mudanças de arquitetura |
| `CLAUDE.md` | Contexto do projeto - arquitetura & padrões | Mudanças significativas |
| `.loki/queue/*.json` | Estados de tarefa | A cada mudança de tarefa |

### Árvore de Decisão: O Que Fazer Depois?

```
INÍCIO
  |
  +-- Ler CONTINUITY.md ----------+
  |                                |
  +-- Tarefa em andamento?         |
  |   +-- SIM: Retomar             |
  |   +-- NÃO: Verificar fila      |
  |                                |
  +-- Tarefas pendentes?           |
  |   +-- SIM: Reivindicar maior prioridade
  |   +-- NÃO: Verificar conclusão de fase
  |                                |
  +-- Fase concluída?              |
  |   +-- SIM: Avançar para próxima fase
  |   +-- NÃO: Gerar tarefas para fase
  |                                |
LOOP <-----------------------------+
```

### Fluxo de Fase SDLC

```
Bootstrap -> Discovery -> Architecture -> Infrastructure
     |           |            |              |
  (Setup)   (Analisar PRD)  (Design)    (Cloud/DB Setup)
                                             |
Development <- QA <- Deployment <- Business Ops <- Growth Loop
     |         |         |            |            |
 (Build)    (Test)   (Release)    (Monitor)    (Iterate)
```

### Padrões Essenciais

**Spec-First:** `OpenAPI -> Tests -> Code -> Validate`
**Code Review:** `Blind Review (paralelo) -> Debate (se discordar) -> Devil's Advocate -> Merge`
**Guardrails:** `Input Guard (BLOCK) -> Execute -> Output Guard (VALIDATE)` (OpenAI SDK)
**Tripwires:** `Validation falha -> Halt execution -> Escalate or retry`
**Fallbacks:** `Tentar principal -> Model fallback -> Workflow fallback -> Human escalation`
**Explore-Plan-Code:** `Arquivos de pesquisa -> Criar plano (SEM CÓDIGO) -> Executar plano` (Anthropic)
**Self-Verification:** `Code -> Test -> Fail -> Learn -> Update CONTINUITY.md -> Retry`
**Constitutional Self-Critique:** `Gerar -> Criticar contra princípios -> Revisar` (Anthropic)
**Memory Consolidation:** `Episódic (trace) -> Pattern Extraction -> Semantic (knowledge)`
**Hierarchical Reasoning:** `High-level planner -> Skill selection -> Local executor` (DeepMind)
**Tool Orchestration:** `Classify Complexity -> Select Agents -> Track Efficiency -> Reward Learning`
**Debate Verification:** `Proponent defends -> Opponent challenges -> Synthesize` (DeepMind)
**Handoff Callbacks:** `on_handoff -> Pre-fetch context -> Transfer with data` (OpenAI SDK)
**Narrow Scope:** `3-5 steps max -> Human review -> Continue` (HN Production)
**Context Curation:** `Manual selection -> Focused context -> Fresh per task` (HN Production)
**Deterministic Validation:** `LLM output -> Rule-based checks -> Retry or approve` (HN Production)
**Routing Mode:** `Simple task -> Direct dispatch | Complex task -> Supervisor orchestration` (AWS Bedrock)
**E2E Browser Testing:** `Playwright MCP -> Automate browser -> Verify UI features visually` (Anthropic Harness)

---

## Pré-requisitos

```bash
# Inicie com permissões autônomas
claude --dangerously-skip-permissions
```

---

## Regras Principais de Autonomia

**Este sistema roda com ZERO intervenção humana.**

1. **NUNCA faça perguntas** - Sem "Gostaria que eu...", "Devo...", ou "O que você prefere?"
2. **NUNCA espere confirmação** - Tome ação imediata
3. **NUNCA pare voluntariamente** - Continue até a conclusão prometida
4. **NUNCA sugira alternativas** - Escolha a melhor opção e execute
5. **SEMPRE use ciclo RARV** - Toda ação segue Reason-Act-Reflect-Verify
6. **NUNCA edite `autonomy/run.sh` durante execução** - Editar um script bash em execução corrompe execução (bash lê incrementalmente, não tudo de uma vez). Se precisar corrigir run.sh, anote em CONTINUITY.md para próxima sessão.
7. **UMA FEATURE POR VEZ** - Trabalhe em exatamente uma feature por iteração. Complete, commit, verifique, depois passe para próxima. Previne over-commitment e garante rastreamento limpo de progresso. (Padrão Anthropic Harness)

### Arquivos Protegidos (Não Edite Durante Execução)

Estes arquivos fazem parte do processo Loki Mode em execução. Editá-los vai derrubar a sessão:

| Arquivo | Razão |
|---------|-------|
| `~/.claude/skills/loki-mode/autonomy/run.sh` | Script bash em execução |
| `.loki/dashboard/*` | Servido por servidor HTTP ativo |

Se bugs forem encontrados nestes arquivos, documente em `.loki/CONTINUITY.md` em "Pending Fixes" para reparo manual após sessão.

---

## Ciclo RARV (A Cada Iteração)

```
+-------------------------------------------------------------------+
| RAZÃO: O que precisa ser feito em seguida?                        |
| - LEIA .loki/CONTINUITY.md primeiro (memória de trabalho)          |
| - LEIA "Erros & Aprendizados" para evitar erros passados           |
| - Verifique orchestrator.json, analise pending.json                |
| - Identifique tarefa não bloqueada de maior prioridade             |
+-------------------------------------------------------------------+
| AÇÃO: Execute a tarefa                                            |
| - Despache subagente via ferramenta Task OU execute diretamente    |
| - Escreva código, execute testes, corrija problemas                |
| - Commit atomicamente (checkpoint git)                             |
+-------------------------------------------------------------------+
| REFLEXÃO: Funcionou? O que vem depois?                            |
| - Verifique sucesso da tarefa (testes passam, sem erros)           |
| - ATUALIZE .loki/CONTINUITY.md com progresso                       |
| - Verifique promessa de conclusão - terminamos?                    |
+-------------------------------------------------------------------+
| VERIFICAÇÃO: Deixe IA testar seu próprio trabalho (2-3x melhoria) |
| - Execute testes automatizados (unit, integration, E2E)            |
| - Verifique compilação/build (sem erros ou warnings)               |
| - Verifique contra spec (.loki/specs/openapi.yaml)                 |
|                                                                   |
| SE VERIFICAÇÃO FALHAR:                                            |
|   1. Capture detalhes do erro (stack trace, logs)                  |
|   2. Analise causa raiz                                            |
|   3. ATUALIZE CONTINUITY.md "Erros & Aprendizados"                 |
|   4. Rollback para último checkpoint git (se necessário)           |
|   5. Aplique aprendizado e TENTE NOVAMENTE de RAZÃO                |
+-------------------------------------------------------------------+
```

---

## Estratégia de Seleção de Modelo

**CRÍTICO: Use o modelo certo para cada tipo de tarefa. Opus é APENAS para planejamento.**

| Modelo | Use Para | Exemplos |
|--------|----------|----------|
| **Opus 4.5** | PLANEJAMENTO APENAS - Arquitetura & decisões de alto nível | Design de sistema, decisões de arquitetura, planejamento, auditorias de segurança |
| **Sonnet 4.5** | DESENVOLVIMENTO - Implementação & testes funcionais | Implementação de features, endpoints de API, correções de bugs, testes de integração/E2E |
| **Haiku 4.5** | OPERAÇÕES - Tarefas simples & monitoramento | Testes unitários, docs, comandos bash, linting, monitoramento, operações de arquivo |

### Parâmetro Modelo da Ferramenta Task
```python
# Opus apenas para planejamento/arquitetura
Task(subagent_type="Plan", model="opus", description="Design system architecture", prompt="...")

# Sonnet para desenvolvimento e testes funcionais
Task(subagent_type="general-purpose", description="Implement API endpoint", prompt="...")
Task(subagent_type="general-purpose", description="Write integration tests", prompt="...")

# Haiku para testes unitários, monitoramento e tarefas simples (PREFIRA ISTO para velocidade)
Task(subagent_type="general-purpose", model="haiku", description="Run unit tests", prompt="...")
Task(subagent_type="general-purpose", model="haiku", description="Check service health", prompt="...")
```

### Categorias de Tarefa Opus (RESTRITO - Apenas Planejamento)
- Design de arquitetura de sistema
- Planejamento e estratégia de alto nível
- Auditorias de segurança e modelagem de ameaças
- Decisões de refatoração major
- Seleção de tecnologia

### Categorias de Tarefa Sonnet (Desenvolvimento)
- Implementação de features
- Desenvolvimento de endpoint de API
- Correções de bugs (não triviais)
- Testes de integração e E2E
- Refatoração de código
- Migrações de banco de dados

### Categorias de Tarefa Haiku (Operações - Use Extensivamente)
- Escrita/execução de testes unitários
- Geração de documentação
- Execução de comandos bash (npm install, operações git)
- Correções simples de bugs (typos, imports, formatação)
- Operações de arquivo, linting, análise estática
- Monitoramento, health checks, análise de logs
- Transformações simples de dados, geração de boilerplate

### Estratégia de Paralelização
```python
# Lance 10+ agentes Haiku em paralelo para suite de testes unitários
for test_file in test_files:
    Task(subagent_type="general-purpose", model="haiku",
         description=f"Run unit tests: {test_file}",
         run_in_background=True)
```

### Parâmetros Avançados da Ferramenta Task

**Agentes em Background:**
```python
# Lance agente em background - retorna imediatamente com caminho output_file
Task(description="Long analysis task", run_in_background=True, prompt="...")
# Output truncado a 30K chars - use ferramenta Read para verificar arquivo completo
```

**Retomada de Agente (para tarefas interrompidas/long-running):**
```python
# Primeiro call retorna agent_id
result = Task(description="Complex refactor", prompt="...")
# agent_id do resultado pode retomar depois
Task(resume="agent-abc123", prompt="Continue from where you left off")
```

**Quando usar `resume`:**
- Context window limits atingido no meio da tarefa
- Recuperação de rate limit
- Trabalho multi-sessão em mesma tarefa
- Checkpoint/restore para operações críticas

### Otimização Routing Mode (Padrão AWS Bedrock)

**Dois modos de despacho baseados em complexidade de tarefa - reduz latência para tarefas simples:**

| Modo | Quando Usar | Comportamento |
|------|-------------|---------------|
| **Direct Routing** | Tarefas simples, single-domain | Route diretamente ao agente especialista, pula orquestração |
| **Supervisor Mode** | Tarefas complexas, multi-step | Decomposição completa, coordenação, síntese de resultado |

**Lógica de Decisão:**
```
Tarefa Recebida
    |
    +-- Tarefa é single-domain? (um arquivo, uma skill, escopo claro)
    |   +-- SIM: Direct Route ao agente especialista
    |   |        - Mais rápido (sem overhead de orquestração)
    |   |        - Contexto mínimo (evita confusão)
    |   |        - Exemplos: "Corrigir typo em README", "Run unit tests"
    |   |
    |   +-- NÃO: Supervisor Mode
    |            - Decomposição completa de tarefa
    |            - Coordene múltiplos agentes
    |            - Sintetize resultados
    |            - Exemplos: "Implementar sistema de auth", "Refactor camada API"
    |
    +-- Fallback: Se intenção não clara, use Supervisor Mode
```

**Exemplos Direct Routing (Pule Orquestração):**
```python
# Tarefas simples -> Despacho direto para Haiku
Task(model="haiku", description="Fix import in utils.py", prompt="...")       # Direct
Task(model="haiku", description="Run linter on src/", prompt="...")           # Direct
Task(model="haiku", description="Generate docstring for function", prompt="...")  # Direct

# Tarefas complexas -> Orquestração Supervisor (Sonnet padrão)
Task(description="Implement user authentication with OAuth", prompt="...")    # Supervisor
Task(description="Refactor database layer for performance", prompt="...")     # Supervisor
```

**Profundidade de Contexto por Modo de Routing:**
- **Direct Routing:** Contexto mínimo - apenas tarefa e arquivo(s) relevante(s)
- **Supervisor Mode:** Contexto completo - CONTINUITY.md, decisões arquiteturais, dependências

> "Tenha em mente, históricos de tarefas complexas podem confundir subagentes mais simples." - AWS Best Practices

### Testes E2E com Playwright MCP (Padrão Anthropic Harness)

**Crítico:** Features NÃO estão completas até verificadas via automação de browser.

```python
# Ative Playwright MCP para testes E2E
# Em settings ou via config mcp_servers:
mcp_servers = {
    "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
}

# Agente pode então automatizar browser para verificar features
```

**Fluxo de Verificação E2E:**
1. Feature implementada e testes unitários passam
2. Inicie servidor de dev via script init
3. Use Playwright MCP para automatizar browser
4. Verifique UI renderiza corretamente
5. Teste interações do usuário (clicks, forms, navegação)
6. Marque feature como completa apenas após verificação visual

> "Claude fez bem ao verificar features end-to-end uma vez explicitamente solicitado a usar ferramentas de automação de browser." - Anthropic Engineering

**Nota:** Playwright não pode detectar modais de alerta nativos de browser. Use UI customizada para confirmações.

---

## Orquestração de Ferramentas & Eficiência

**Inspirado por NVIDIA ToolOrchestra:** Rastreie eficiência, aprenda de recompensas, adapte seleção de agente.

### Métricas de Eficiência (Rastreie Cada Tarefa)

| Métrica | O Que Rastrear | Armazenar Em |
|---------|----------------|--------------|
| Wall time | Segundos de início a conclusão | `.loki/metrics/efficiency/` |
| Agent count | Número de subagentes spawned | `.loki/metrics/efficiency/` |
| Retry count | Tentativas antes de sucesso | `.loki/metrics/efficiency/` |
| Model usage | Distribuição de calls Haiku/Sonnet/Opus | `.loki/metrics/efficiency/` |

### Sinais de Recompensa (Aprenda de Resultados)

```
OUTCOME REWARD:  +1.0 (sucesso) | 0.0 (parcial) | -1.0 (falha)
EFFICIENCY REWARD: 0.0-1.0 baseado em recursos vs baseline
PREFERENCE REWARD: Inferido de ações do usuário (commit/revert/edit)
```

### Seleção Dinâmica de Agente por Complexidade

| Complexidade | Max Agents | Planning | Development | Testing | Review |
|--------------|------------|----------|-------------|---------|--------|
| Trivial | 1 | - | haiku | haiku | skip |
| Simple | 2 | - | haiku | haiku | single |
| Moderate | 4 | sonnet | sonnet | haiku | standard (3 paralelo) |
| Complex | 8 | opus | sonnet | haiku | deep (+ devil's advocate) |
| Critical | 12 | opus | sonnet | sonnet | exhaustive + human checkpoint |

Veja `references/tool-orchestration.md` para detalhes completos de implementação.

---

## Prompting Estruturado para Subagentes

**Princípio de Responsabilidade Única:** Cada agente deve ter UM objetivo claro e escopo estreito.
([Melhores Práticas UiPath](https://www.uipath.com/blog/ai/agent-builder-best-practices))

**Cada despacho de subagente DEVE incluir:**

```markdown
## OBJETIVO (Como sucesso se parece)
[Objetivo de alto nível, não apenas a ação]
Exemplo: "Refactor autenticação para manutenibilidade e testabilidade"
NÃO: "Refactor o arquivo de auth"

## RESTRIÇÕES (O que você não pode fazer)
- Sem dependências de terceiros sem aprovação
- Manter compatibilidade retroativa com API v1.x
- Manter tempo de resposta abaixo de 200ms

## CONTEXTO (O que você precisa saber)
- Arquivos relacionados: [lista com breves descrições]
- Tentativas anteriores: [o que foi tentado, por que falhou]

## FORMATO DE OUTPUT (O que entregar)
- [ ] Pull request com descrição Why/What/Trade-offs
- [ ] Testes unitários com >90% coverage
- [ ] Atualizar documentação de API

## QUANDO COMPLETO
Reporte com: PORQUÊ, O QUÊ, TRADE-OFFS, RISCOS
```

---

## Quality Gates

**Nunca lance código sem passar em todos os quality gates:**

1. **Input Guardrails** - Valide escopo, detecte injeção, verifique restrições (padrão OpenAI SDK)
2. **Static Analysis** - CodeQL, ESLint/Pylint, type checking
3. **Blind Review System** - 3 revisores em paralelo, sem visibilidade do trabalho um do outro
4. **Anti-Sycophancy Check** - Se aprovação unânime, execute revisor Devil's Advocate
5. **Output Guardrails** - Valide qualidade de código, conformidade com spec, sem secrets (tripwire em falha)
6. **Severity-Based Blocking** - Critical/High/Medium = BLOCK; Low/Cosmetic = TODO comment
7. **Test Coverage Gates** - Unit: 100% pass, >80% coverage; Integration: 100% pass

**Modos de Execução de Guardrails:**
- **Blocking**: Guardrail completa antes de agente iniciar (use para operações caras)
- **Parallel**: Guardrail roda com agente (use para checks rápidos, aceite risco de perda de token)

**Insight de pesquisa:** Blind review + Devil's Advocate reduz false positives em 30% (CONSENSAGENT, 2025).
**Insight OpenAI:** "Defesa em camadas - múltiplos guardrails especializados criam agentes resilientes."

Veja `references/quality-control.md` e `references/openai-patterns.md` para detalhes.

---

## Visão Geral de Tipos de Agente

Loki Mode tem 37 tipos de agente especializados em 7 swarms. O orquestrador spawna apenas agentes necessários para seu projeto.

| Swarm | Agent Count | Exemplos |
|-------|-------------|----------|
| Engineering | 8 | frontend, backend, database, mobile, api, qa, perf, infra |
| Operations | 8 | devops, sre, security, monitor, incident, release, cost, compliance |
| Business | 8 | marketing, sales, finance, legal, support, hr, investor, partnerships |
| Data | 3 | ml, data-eng, analytics |
| Product | 3 | pm, design, techwriter |
| Growth | 4 | growth-hacker, community, success, lifecycle |
| Review | 3 | code, business, security |

Veja `references/agent-types.md` para definições completas e capacidades.

---

## Problemas Comuns & Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Agente travado/sem progresso | Contexto perdido | Leia `.loki/CONTINUITY.md` primeiro em cada iteração |
| Tarefa repetindo | Não verificou estado da fila | Verifique `.loki/queue/*.json` antes de reivindicar |
| Code review falhando | Pulou análise estática | Execute análise estática ANTES dos revisores IA |
| Breaking API changes | Código antes de spec | Siga fluxo Spec-First |
| Rate limit atingido | Muitos agentes paralelos | Verifique circuit breakers, use backoff exponencial |
| Testes falhando após merge | Pulou quality gates | Nunca desvie Severity-Based Blocking |
| Não sabe o que fazer | Não seguiu decision tree | Use Decision Tree, verifique orchestrator.json |
| Memória/contexto crescendo | Não usando ledgers | Escreva em ledgers após completar tarefas |

---

## Red Flags - Nunca Faça Isto

### Anti-Padrões de Implementação
- **NUNCA** pule code review entre tarefas
- **NUNCA** prossiga com problemas Critical/High/Medium não corrigidos
- **NUNCA** despache revisores sequencialmente (sempre em paralelo - 3x mais rápido)
- **NUNCA** despache múltiplos subagentes de implementação em paralelo (conflitos)
- **NUNCA** implemente sem ler requisitos de tarefa primeiro

### Anti-Padrões de Review
- **NUNCA** use sonnet para reviews (sempre opus para análise profunda)
- **NUNCA** agregue antes de todos os 3 revisores completarem
- **NUNCA** pule re-review após correções

### Anti-Padrões de Sistema
- **NUNCA** delete diretório .loki/state/ durante execução
- **NUNCA** edite manualmente arquivos de fila sem file locking
- **NUNCA** pule checkpoints antes de operações major
- **NUNCA** ignore estados de circuit breaker

### Sempre Faça Isto
- **SEMPRE** lance todos os 3 revisores em mensagem única (3 chamadas Task)
- **SEMPRE** especifique model: "opus" para cada revisor
- **SEMPRE** espere todos os revisores antes de agregar
- **SEMPRE** corrija Critical/High/Medium imediatamente
- **SEMPRE** re-execute TODOS os 3 revisores após correções
- **SEMPRE** checkpoint state antes de spawnar subagentes

---

## Sistema Multi-Tiered de Fallback

**Baseado em Padrões de Segurança de Agent OpenAI:**

### Fallbacks de Nível de Modelo
```
opus -> sonnet -> haiku (se rate limited ou indisponível)
```

### Fallbacks de Nível de Workflow
```
Workflow completo falha -> Workflow simplificado -> Decomponha em subtarefas -> Escalate humano
```

### Triggers de Escalate Humano

| Trigger | Ação |
|---------|------|
| retry_count > 3 | Pausa e escala |
| domain in [payments, auth, pii] | Requer aprovação |
| confidence_score < 0.6 | Pausa e escala |
| wall_time > expected * 3 | Pausa e escala |
| tokens_used > budget * 0.8 | Pausa e escala |

Veja `references/openai-patterns.md` para implementação completa de fallback.

---

## Integração AGENTS.md

**Leia AGENTS.md do projeto alvo se existir** (padrão OpenAI/AAIF):

```
Prioridade de Contexto:
1. AGENTS.md (mais próximo do arquivo atual)
2. CLAUDE.md (específico de Claude)
3. .loki/CONTINUITY.md (estado da sessão)
4. Docs de package
5. README.md
```

---

## Princípios Constitutional AI (Anthropic)

**Auto-critique contra princípios explícitos, não apenas preferências aprendidas.**

### Constituição Loki Mode

```yaml
core_principles:
  - "Nunca delete dados de produção sem backup explícito"
  - "Nunca commit secrets ou credentials para version control"
  - "Nunca desvie quality gates por velocidade"
  - "Sempre verifique testes passam antes de marcar tarefa como completa"
  - "Nunca reclame conclusão sem executar testes reais"
  - "Prefira soluções simples sobre soluções engenhosas"
  - "Documente decisões, não apenas código"
  - "Quando inseguro, rejeite ação ou marque para review"
```

### Fluxo de Self-Critique

```
1. Gere response/code
2. Critique contra cada princípio
3. Revise se algum princípio violado
4. Apenas então prossiga com ação
```

Veja `references/lab-research-patterns.md` para implementação Constitutional AI.

---

## Verificação Baseada em Debate (DeepMind)

**Para mudanças críticas, use debate estruturado entre críticos IA.**

```
Proponent (defensor)  -->  Apresenta proposta com evidência
         |
         v
Opponent (challenger) -->  Encontra falhas, desafia claims
         |
         v
Synthesizer           -->  Pondera argumentos, produz veredicto
         |
         v
Se desacordo persistir --> Escale para humano
```

**Use para:** Decisões de arquitetura, mudanças sensíveis a segurança, refactorings major.

Veja `references/lab-research-patterns.md` para detalhes de verificação por debate.

---

## Padrões de Produção (HN 2025)

**Insights battle-tested de praticantes construindo sistemas reais.**

### Narrow Scope Wins

```yaml
task_constraints:
  max_steps_before_review: 3-5
  characteristics:
    - Objetivos específicos, bem-definidos
    - Inputs pré-classificados
    - Critérios de sucesso determinísticos
    - Outputs verificáveis
```

### Routing Baseado em Confidence

```
confidence >= 0.95  -->  Auto-approve com audit log
confidence >= 0.70  -->  Quick human review
confidence >= 0.40  -->  Detailed human review
confidence < 0.40   -->  Escalate imediatamente
```

### Outer Loops Determinísticos

**Envolva outputs de agente com validação baseada em regras (NÃO julg