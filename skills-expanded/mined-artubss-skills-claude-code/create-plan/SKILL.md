---
name: create-plan
description: Criar um plano conciso. Use quando um usuário solicitar explicitamente um plano relacionado a uma tarefa de codificação.
metadata:
  short-description: Criar um plano
---

# Criar Plano

## Objetivo

Transformar uma solicitação do usuário em **um único plano acionável** entregue na mensagem final do assistente.

## Fluxo mínimo

Durante todo o fluxo de trabalho, operem modo somente leitura. Não escreva nem atualize arquivos.

1. **Escaneie o contexto rapidamente**
   - Leia `README.md` e qualquer documentação óbvia (`docs/`, `CONTRIBUTING.md`, `ARCHITECTURE.md`).
   - Percorra rapidamente arquivos relevantes (aqueles mais prováveis de serem tocados).
   - Identifique restrições (linguagem, frameworks, comandos CI/teste, forma de deployment).

2. **Faça perguntas de acompanhamento apenas se forem bloqueantes**
   - Faça **no máximo 1–2 perguntas**.
   - Pergunte apenas se você não conseguir responsavelmente planejar sem a resposta; prefira múltipla escolha.
   - Se tiver dúvida mas não estiver bloqueado, faça uma suposição razoável e prossiga.

3. **Crie um plano usando o template abaixo**
   - Comece com **1 parágrafo curto** descrevendo a intenção e abordagem.
   - Deixe claro o que está **no escopo** e o que **não está no escopo** de forma breve.
   - Depois forneça uma **pequena checklist** de itens de ação (padrão 6–10 itens).
      - Cada item da checklist deve ser uma ação concreta e, quando útil, mencione arquivos/comandos.
      - **Torne os itens atômicos e ordenados**: descoberta → mudanças → testes → rollout.
      - **Comece com verbo**: "Adicionar…", "Refatorar…", "Verificar…", "Entregar…".
   - Inclua pelo menos um item para **testes/validação** e um para **casos extremos/risco** quando aplicável.
   - Se houver incógnitas, inclua uma seção **Perguntas em aberto** pequena (máx 3).

4. **Não preface o plano com explicações meta; exiba apenas o plano conforme o template**

## Template de plano (siga exatamente)

```markdown
# Plano

<1–3 frases: o que estamos fazendo, por quê, e a abordagem de alto nível.>

## Escopo
- Dentro:
- Fora:

## Itens de ação
[ ] <Etapa 1>
[ ] <Etapa 2>
[ ] <Etapa 3>
[ ] <Etapa 4>
[ ] <Etapa 5>
[ ] <Etapa 6>

## Perguntas em aberto
- <Pergunta 1>
- <Pergunta 2>
- <Pergunta 3>
```

## Guia para itens da checklist
Bons itens de checklist:
- Apontam para arquivos/módulos prováveis: src/..., app/..., services/...
- Nomeiam validação concreta: "Executar npm test", "Adicionar testes unitários para X"
- Incluem rollout seguro quando relevante: feature flag, plano de migração, nota de rollback

Evite:
- Etapas vagas ("lidar com backend", "fazer autenticação")
- Muitas micro-etapas
- Escrever snippets de código (mantenha o plano agnóstico em relação à implementação)