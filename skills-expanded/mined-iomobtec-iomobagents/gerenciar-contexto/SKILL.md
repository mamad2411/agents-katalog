---
name: gerenciar-contexto
description: "Estrutura e cura o contexto entregue aos agentes — hierarquia de 5 níveis, limite de 2.000 linhas e anti-padrões de context starvation e context flooding. Use quando o orquestrador ou o arquiteto monta o contexto de uma sessão."
author: "Pedro Andriow (https://github.com/Andriow)"
---

# Skill: gerenciar-contexto

Define como estruturar e manter o contexto relevante para agentes de IA, equilibrando profundidade de informação com foco no escopo da tarefa atual.

**Agente:** `orquestrador`, `arquiteto`  

---

## Quando usar

- Antes de iniciar uma sessão de desenvolvimento complexa
- Quando o agente começa a dar respostas inconsistentes ou alucinadas
- Ao coordenar múltiplos agentes numa mesma tarefa

---

## Processo

### Passo 1 — Delimitar o escopo antes de qualquer ação
Antes de carregar qualquer arquivo ou iniciar qualquer tarefa, defina explicitamente: quais arquivos e componentes são relevantes para ESTA tarefa? O escopo deve ser o menor conjunto de contexto que permite a tarefa ser executada corretamente. Escreva a lista de arquivos relevantes antes de abri-los.

### Passo 2 — Carregar contexto respeitando a hierarquia de autoridade
Carregue o contexto na ordem de autoridade abaixo. Contexto de nível superior sempre tem precedência sobre contexto de nível inferior em caso de conflito:

**Nível 1 — Rules Files** (maior autoridade): CLAUDE.md, guardrails, políticas de segurança. Sempre carregados, nunca ignorados.

**Nível 2 — Specs e Arquitetura**: planos em `plans/`, contratos de API, ADRs (Architecture Decision Records). Carregar para a tarefa em andamento.

**Nível 3 — Arquivos-Fonte**: código relevante ao escopo atual. Carregar seletivamente — apenas o que o Passo 1 identificou como relevante.

**Nível 4 — Saída de Erros**: output de testes, compilador, linter. Carregar apenas quando em modo de debugging.

**Nível 5 — Histórico de Conversa** (menor autoridade): pode conter premissas erradas ou informações desatualizadas. Tratar com ceticismo.

### Passo 3 — Manter menos de 2.000 linhas de contexto focado por tarefa
Contexto excessivo dilui o sinal. Se o contexto acumulado ultrapassar 2.000 linhas, revisar e remover o que não é diretamente necessário para a tarefa atual. Priorizar: contratos e interfaces > implementações > exemplos > comentários.

### Passo 4 — Identificar e remover referências obsoletas
Antes de usar qualquer parte do contexto, verificar se ela ainda reflete o estado atual do sistema. Sinais de referência obsoleta: código comentado que descreve comportamento diferente do código ativo, specs que contradizem a implementação atual, TODOs sem data ou dono que descrevem funcionalidades já implementadas. Remover ou sinalizar referências obsoletas antes de prosseguir.

### Passo 5 — Resetar o escopo ao mudar de tarefa
Ao iniciar uma nova tarefa, não acumule contexto da tarefa anterior. Contexto de tarefa anterior pode contaminar o raciocínio sobre a nova tarefa. Faça um reset explícito: liste o novo escopo a partir do zero, seguindo o Passo 1 novamente.

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Mais contexto é sempre melhor" | Contexto irrelevante tem custo — dilui o sinal e aumenta a probabilidade de o agente focar na coisa errada. Qualidade de contexto supera quantidade. |
| "O agente vai saber o que é relevante" | Agentes não filtram ativamente — processam tudo que está no contexto. Curadoria é responsabilidade de quem monta o contexto, não do agente. |
| "Não tenho tempo de delimitar escopo" | Delimitar escopo leva 2 minutos. Debugar output de agente desorientado por contexto ruim leva horas. |
| "O histórico de conversa captura tudo que é necessário" | Histórico de conversa tem a menor autoridade na hierarquia. Premissas incorretas discutidas no início da sessão se propagam como fatos. |
| "Vou carregar o repositório inteiro para não perder nada" | Context flooding é tão danoso quanto context starvation. Um agente com contexto excessivo tem desempenho pior do que um com contexto cirúrgico. |

---

## Anti-padrões bloqueados

- **Context starvation:** agente tentando inferir o que poderia simplesmente ler — sinal de que o contexto necessário não foi carregado
- **Context flooding:** carregar o repositório inteiro para uma mudança de 3 linhas
- **Referências obsoletas:** usar specs ou comentários que contradizem o código atual como fonte de verdade
- **Exemplos ausentes:** descrever um padrão sem mostrar um exemplo concreto do codebase — descrições abstratas geram implementações incorretas
- **Hierarquia invertida:** tratar o histórico de conversa como mais autoritativo do que Rules Files ou specs formais
- **Acumulação cross-task:** carregar na nova tarefa o contexto da tarefa anterior sem resetar o escopo

---

## Checklist de conclusão

- [ ] Escopo delimitado explicitamente antes de carregar qualquer arquivo
- [ ] Contexto carregado na ordem da hierarquia de autoridade (Rules Files → Specs → Código → Erros → Histórico)
- [ ] Contexto total abaixo de 2.000 linhas para a tarefa atual
- [ ] Referências obsoletas identificadas e removidas ou sinalizadas
- [ ] Exemplos concretos do codebase incluídos para cada padrão descrito
- [ ] Ao trocar de tarefa, escopo foi resetado explicitamente a partir do zero
- [ ] Conflitos entre níveis da hierarquia resolvidos em favor do nível de maior autoridade
