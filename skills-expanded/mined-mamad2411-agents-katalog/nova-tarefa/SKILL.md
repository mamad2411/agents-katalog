---
name: nova-tarefa
description: Guia criação completa de nova tarefa no sistema via perguntas sequenciais. Ativar quando Luiz disser "nova tarefa", "criar tarefa", "/nova-tarefa" ou pedir para adicionar algo ao kanban.
---

# Skill: nova-tarefa

Coleta informações via perguntas sequenciais e cria tarefa completa no sistema (arquivo de equipe + KANBAN + TAREFAS + Paperclip).

## Perguntas (verificar antes de agir)

Se o usuário não especificou equipe ou tarefa já foi mencionada antes, verificar:

1. **Relação com task existente** — se o tema soa familiar, ler o arquivo de equipe relevante e perguntar: "Esta tarefa está relacionada a [T-XXX-NNN · Título existente]? (s/n)"
2. **Domínio/equipe** — se não informado na mensagem, perguntar antes da Fase 1: "Qual equipe? juridica / comercial / dev / pesquisa / pessoal"

Se já informado na mensagem, pular as perguntas acima e ir direto à Fase 1.

## Passos

### Fase 1 — Coleta (uma pergunta por vez)

Fazer as perguntas em ordem, aguardar resposta de cada uma antes de prosseguir:

1. "Qual o título da tarefa?"
2. "Qual a descrição? (o que precisa ser feito)"
3. "Qual a equipe? juridica / comercial / dev / pesquisa / pessoal"
4. "Qual a prioridade? alta / media / baixa"
5. "Tem prazo? Se sim, qual data?"
6. "Tem algum bloqueio já conhecido?"

### Fase 2 — Geração automática

Com as respostas, executar tudo de uma vez:

**Determinar ID da tarefa:**
- Ler o arquivo da equipe para descobrir o maior número existente
- Incrementar: T-JUR-001, T-COM-002, T-DEV-005, etc.

**Criar bloco no arquivo da equipe** (`99_System/equipes/XXX-tarefas.md`):

```markdown
### ID · Título
- **Status:** 🔵 Ativa
- **Prioridade:** alta/media/baixa
- **Prazo:** YYYY-MM-DD (ou —)
- **Bloqueio:** descrição (ou —)
- **Descrição:** texto
- **Paperclip:** MEN-XX (preenchido após criação)

**Próximos passos:**
- [ ] ...
```

**Criar card no KANBAN.md** na coluna `🔵 Ativa`:

```markdown
- [ ] [[equipes/XXX-tarefas#ID|ID · Título curto]] #equipe #prioridade
```

**Atualizar TAREFAS.md** — adicionar entrada na seção da equipe com ID, título e status.

**Criar issue no Paperclip** via API REST:

```
POST http://127.0.0.1:3100/api/companies/6e2fe3bc-5f44-4070-af8c-98330bd47a39/issues
Authorization: Bearer $env:PAPERCLIP_API_KEY
Content-Type: application/json

{
  "title": "ID · Título",
  "description": "Descrição da tarefa.\n\n**Vault:** 99_System/equipes/XXX-tarefas.md#ID\n**Equipe:** nome\n**Prazo:** YYYY-MM-DD ou —",
  "status": "todo",
  "priority": "high|medium|low",
  "projectId": "a3df0837-7017-424d-80c9-4924b0b458ab"
}
```

Mapeamento de prioridade: alta → `high`, media → `medium`, baixa → `low`

Após criar, salvar o identifier retornado (ex: `MEN-25`) e atualizar o campo `**Paperclip:**` no bloco da equipe.

### Fase 3 — Confirmação

Exibir resumo do que foi criado:
- ID vault gerado (ex: T-DEV-003)
- Identifier Paperclip (ex: MEN-25) com link `http://127.0.0.1:3100`
- Arquivo de equipe atualizado
- Card adicionado no KANBAN na coluna correta
- Entrada adicionada no TAREFAS.md

## Referências Vault (sugerir ao completar)

Ao criar a tarefa, sugerir notas relacionadas:
- Se equipe = dev → verificar `14_Indexes/IDX-dev.md` para contexto de projetos relacionados
- Se equipe = juridica → verificar `14_Indexes/IDX-direito.md`
- Se equipe = comercial → verificar `14_Indexes/IDX-comercial.md`
- Sugerir 1-2 notas que possam ajudar na execução da tarefa recém-criada

## Restrições

- NUNCA criar tarefa sem card no KANBAN.md
- NUNCA criar tarefa no vault sem criar issue correspondente no Paperclip
- Se Paperclip estiver offline (conexão recusada), criar no vault e avisar que Paperclip estava offline
- NUNCA pular a fase de coleta — todas as 6 perguntas são obrigatórias
- Se Luiz já informou dados na mensagem inicial, não repetir as perguntas já respondidas
