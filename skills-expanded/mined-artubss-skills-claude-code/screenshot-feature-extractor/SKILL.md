---
name: screenshot-feature-extractor
description: "Analise capturas de tela de produtos para extrair listas de recursos e gerar checklists de tarefas de desenvolvimento. Use quando: (1) Analisando capturas de tela de produtos concorrentes para extração de recursos, (2) Gerando PRD/listas de tarefas a partir de designs de UI, (3) Analisando em lote várias telas de aplicativos, (4) Conduzindo análise competitiva a partir de referências visuais."
---

# Analisador de Capturas de Tela (Multi-Agent)

Extraia recursos de produtos de capturas de tela de UI usando um pipeline de análise coordenado com múltiplos agentes.

**Princípio central**: Descreva O QUE construir (recursos/interações), NÃO COMO (sem stack tecnológico).

## Arquitetura Multi-Agent

Esta skill orquestra 5 agentes especializados para análise abrangente:

```
                    ┌─────────────────┐
                    │   Coordenador   │
                    │   (esta skill)  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Analisador UI  │ │  Analisador de  │ │   Analisador    │
│  (paralelo)     │ │   Interação     │ │    de Negócios  │
│                 │ │  (paralelo)     │ │   (paralelo)    │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                    ┌─────────────────┐
                    │    Sintetizador │
                    │  (sequencial)   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Revisor       │
                    │  (sequencial)   │
                    └─────────────────┘
```

## Processo

### Fase 1: Coleta de Capturas de Tela

Reúna todas as capturas de tela para análise:
1. Leia o(s) arquivo(s) de captura de tela fornecido(s) pelo usuário
2. Para cada captura de tela, anote o caminho do arquivo e qualquer contexto fornecido
3. Se houver múltiplas capturas de tela, determine se elas são do mesmo produto

### Fase 2: Análise em Paralelo

Lance TRÊS agentes de Tarefa EM PARALELO para cada captura de tela:

**Agente 1: screenshot-ui-analyzer**
```
Analise esta captura de tela quanto a componentes de UI, estrutura de layout e padrões de design.
Captura de tela: [caminho do arquivo]
Retorne sua análise como JSON.
```

**Agente 2: screenshot-interaction-analyzer**
```
Analise esta captura de tela quanto a interações do usuário, fluxos de navegação e transições de estado.
Captura de tela: [caminho do arquivo]
Retorne sua análise como JSON.
```

**Agente 3: screenshot-business-analyzer**
```
Analise esta captura de tela quanto a funções de negócios, entidades de dados e lógica de domínio.
Captura de tela: [caminho do arquivo]
Retorne sua análise como JSON.
```

**IMPORTANTE**: Use a ferramenta Task com TRÊS chamadas em paralelo em uma única mensagem para maximizar a eficiência.

### Fase 3: Síntese

Após todas as análises em paralelo serem concluídas, lance o agente sintetizador:

**Agente 4: screenshot-synthesizer**
```
Sintetize estes resultados de análise em uma lista de tarefas de desenvolvimento unificada.

Análise de UI:
[cole o resultado do analisador de UI]

Análise de Interação:
[cole o resultado do analisador de interação]

Análise de Negócios:
[cole o resultado do analisador de negócios]

Nome do Produto: [nome do produto]
Arquivo de saída: docs/plans/YYYY-MM-DD-<produto>-features.md
```

### Fase 4: Revisão

Lance o agente revisor para validar a saída:

**Agente 5: screenshot-reviewer**
```
Revise esta lista de tarefas quanto a completude e qualidade.

Captura(s) de tela original(is): [caminhos de arquivo]
Lista de tarefas: [saída sintetizada]

Se problemas forem encontrados, forneça correções.
```

### Fase 5: Saída

1. Escreva a lista de tarefas final em `docs/plans/YYYY-MM-DD-<produto>-features.md`
2. Use o formato de [references/output-format.md](references/output-format.md)
3. Apresente um resumo ao usuário

## Diretrizes Principais

- Use formato de checkbox `- [ ]` para todas as tarefas
- Divida recursos em subtarefas pequenas e executáveis
- Foque em interações do usuário, não em detalhes de implementação
- Para múltiplas capturas de tela: deduplicar recursos em todas as telas
- Para análise competitiva: destacar recursos únicos e lacunas

## Benefícios da Abordagem Multi-Agent

1. **Abrangência** - Três perspectivas especializadas capturam mais detalhes
2. **Velocidade** - Análise em paralelo reduz o tempo total
3. **Qualidade** - Síntese + Revisão garante saída coerente e completa
4. **Especialização** - Cada agente foca em sua expertise de domínio