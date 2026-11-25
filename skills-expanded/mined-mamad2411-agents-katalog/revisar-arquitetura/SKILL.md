---
name: revisar-arquitetura
description: "Avalia soluções arquiteturais contra os princípios e guardrails do projeto, apontando riscos e alternativas. Use quando o arquiteto precisa validar ou comparar uma decisão de arquitetura antes de comprometê-la."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-arquitetura

Avalia se uma solução proposta ou existente respeita os **princípios arquiteturais do projeto**: separação de responsabilidades entre camadas, contratos bem definidos, ausência de acoplamento indevido, aderência aos guardrails e alinhamento com as decisões técnicas vigentes.

**Agente:** arquiteto  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `frontend.md`, `dados.md`, `seguranca.md`

---

## Quando usar

- Antes de aprovar um PR que introduz nova camada, novo padrão ou nova dependência
- Ao revisar design de feature antes do desenvolvimento começar
- Ao avaliar código já existente que será estendido ou refatorado
- Quando há dúvida sobre se uma solução viola um princípio arquitetural

---

## Entrada esperada

- Descrição da solução (texto, diagrama, código, PR link)
- Camada(s) envolvida(s): System, Process, BFF, Frontend
- Contexto de negócio: o que o usuário final precisa
- Restrições conhecidas: prazo, compatibilidade, consumidores existentes

---

## Processo de execução

### Passo 1 — Identificar o que está sendo avaliado

Classificar o artefato recebido:

| Tipo | Foco da revisão |
|---|---|
| Código novo | Responsabilidades, acoplamento, contrato de saída |
| Código existente sendo estendido | Coesão, impacto em consumidores |
| Diagrama / especificação | Clareza, completude, aderência às camadas |
| PR de arquitetura | Todos os pontos acima + guardrails |

### Passo 2 — Checar separação de responsabilidades

Verificar se cada camada faz apenas o que lhe compete:

| Camada | Responsabilidade esperada | Violação comum |
|---|---|---|
| System API | Persistência, regras de domínio, fonte da verdade | Lógica de orquestração; acesso direto ao banco por outra camada |
| Process API | Orquestração de fluxo, composição de Systems | Persistência própria; lógica de domínio |
| BFF | Adaptar para o frontend; agregar respostas | Lógica de negócio; chamadas diretas ao System |
| Frontend | Renderização; estado de UI | Chamadas diretas ao System ou Process bypassando BFF |

### Passo 3 — Checar contratos

- Endpoints retornam tipo e formato consistente?
- Erros seguem o padrão definido em `padronizar-erros`?
- Campos obrigatórios, opcionais e nulláveis estão declarados?
- Mudança introduz breaking change para consumidores existentes?

### Passo 4 — Checar acoplamento

- Um serviço importa diretamente o código de outro? (proibido)
- Há dependência de detalhe de implementação ao invés de contrato?
- Banco de dados é acessado por mais de um serviço? (cada serviço tem seu próprio store)

### Passo 5 — Checar guardrails

Percorrer os guardrails relevantes à camada e verificar:
- `backend.md §2` — floating promises
- `backend.md §3` — validação de entrada
- `dados.md §1` — queries parametrizadas
- `dados.md §2` — migrations aditivas
- `seguranca.md §1` e `§2` — dados pessoais e secrets

### Passo 6 — Emitir resultado

---

## Saída produzida

```markdown
## Revisão Arquitetural

**Artefato:** <nome / descrição>
**Camada:** <System / Process / BFF / Frontend>
**Veredicto:** ✅ Aprovado | ⚠️ Aprovado com ressalvas | ⛔ Reprovado

---

### Pontos aprovados
- <o que está correto e por quê>

### Ressalvas (não bloqueiam, mas devem ser tratadas)
- <ponto de atenção + recomendação>

### Bloqueios (impedem aprovação)
- <violação específica + guardrail citado + como corrigir>

### Próximos passos
1. <ação concreta para resolver cada bloqueio>
```

---

## Critérios de aprovação

| Critério | Obrigatório |
|---|---|
| Camadas com responsabilidades corretas | Sim |
| Contratos explícitos e completos | Sim |
| Sem acoplamento direto entre serviços | Sim |
| Guardrails de segurança respeitados | Sim |
| Sem breaking change não declarado | Sim |
| Sem `console.log` em código de produção | Sim |
| Nomes de função/módulo claros e consistentes | Não (ressalva) |
| Cobertura de teste adequada | Não (encaminhar para `dev-qa`) |
