---
name: refinar-historia
description: "Refina histórias de usuário até o Definition of Ready, com critérios de aceite claros. Use quando o tech-lead vai preparar uma história para o desenvolvimento."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: refinar-historia

Refina uma **história de usuário** até que satisfaça o Definition of Ready: critérios de aceite não ambíguos, escopo delimitado, dependências identificadas e estimativa viável. Produz a história pronta para entrar no sprint.

**Agente:** tech-lead  
**Guardrails aplicáveis:** `00-core.md`, `processo.md`

---

## Quando usar

- Durante cerimônia de refinamento ou antes do planejamento do sprint
- Quando uma história chega ao backlog sem critérios de aceite claros
- Quando o escopo de uma história é ambíguo ou excessivamente grande
- Antes de acionar qualquer agente de desenvolvimento (DoR é pré-requisito)

---

## Conceitos fundamentais

**História de usuário:** descrição de uma necessidade do ponto de vista de quem usa o sistema.
Formato: `Como <papel>, quero <ação>, para <benefício>.`

**Critério de aceite:** condição verificável que, quando satisfeita, confirma que a história foi entregue corretamente. Deve ser testável — se não puder ser testado, não é critério.

**Definition of Ready (DoR):** conjunto de critérios que uma história precisa satisfazer antes de ser assumida por um desenvolvedor. Ver `processo.md §5`.

---

## Processo de execução

### Passo 1 — Avaliar o título e o "Como / Quero / Para"

O título deve descrever o valor entregue ao usuário, não a implementação técnica:

```
# ⛔ orientado à implementação
Criar endpoint POST /orders e tabela no banco

# ✅ orientado ao valor
Usuário consegue fazer um pedido de produto
```

Verificar se o "Para" declara o benefício de negócio. Se estiver ausente ou vago, preencher com o product owner antes de continuar.

### Passo 2 — Verificar e escrever critérios de aceite

Cada critério deve seguir o padrão: `Dado <contexto> / Quando <ação> / Então <resultado observável>` — ou uma afirmação direta verificável.

```markdown
## Critérios de aceite — Usuário consegue fazer um pedido

**CA-01:** Dado que o usuário está autenticado e tem itens no carrinho,
quando confirma o pedido com cartão válido,
então o pedido é criado com status "Confirmado" e o usuário recebe confirmação por e-mail.

**CA-02:** Quando o cartão é recusado,
então o pedido não é criado e o sistema exibe "Pagamento recusado. Verifique os dados do cartão."

**CA-03:** Quando o estoque do item é insuficiente para a quantidade solicitada,
então o sistema exibe a quantidade máxima disponível e impede a confirmação.

**CA-04:** O carrinho é esvaziado somente após o pedido ser confirmado com sucesso.
```

Sinais de critério mal escrito:
- "O sistema deve funcionar corretamente" → sem critério mensurável
- "Conforme o design" → design não é critério de aceite, é artefato separado
- "Rápido" / "performático" → sem métrica definida (SLA em ms é critério; "rápido" não é)

### Passo 3 — Delimitar o escopo ("o que NÃO está incluído")

Escrever explicitamente o que está fora do escopo desta história. Previne escopo crescente (scope creep) durante o desenvolvimento:

```markdown
## Fora do escopo desta história
- Pagamento via PIX (próxima história)
- Notificação por SMS (será avaliada separadamente)
- Histórico de pedidos (já existe em outra história)
- Relatório de vendas para o administrador
```

### Passo 4 — Identificar dependências

```markdown
## Dependências
- **Contrato de API:** endpoint `POST /orders` do BFF a ser definido pelo arquiteto antes do início
- **Serviço externo:** gateway de pagamento — contrato de sandbox disponível?
- **Design:** telas de checkout e confirmação aprovadas pelo produto?
- **Dado:** qual o comportamento quando o usuário não tem endereço cadastrado?
```

Se uma dependência está bloqueada, a história não está pronta (DoR não satisfeito).

### Passo 5 — Verificar se a história é divisível

Uma história é grande demais se:
- Tem mais de 5-6 critérios de aceite independentes entre si
- Envolve mais de 2-3 serviços com implementação nova
- A estimativa ultrapassa a capacidade de um desenvolvedor em um sprint

Como dividir:
```
# Antes (grande demais):
"Usuário gerencia seu perfil" — inclui edição de dados, troca de senha, upload de foto, exclusão de conta

# Depois (histórias menores e independentes):
1. Usuário edita nome e e-mail do perfil
2. Usuário altera sua senha
3. Usuário faz upload de foto de perfil
4. Usuário solicita exclusão de conta
```

### Passo 6 — Verificar DoR completo

```markdown
## Checklist DoR — <título da história>

- [ ] Título orientado ao valor do usuário
- [ ] "Como / Quero / Para" preenchido e compreensível
- [ ] Critérios de aceite escritos, verificáveis e não ambíguos
- [ ] Escopo delimitado — o que não está incluído está declarado
- [ ] Dependências identificadas (contratos, serviços, designs)
- [ ] História divisível avaliada — se grande demais, dividida
- [ ] Estimativa viável para um sprint
```

---

## Saída produzida

```markdown
# História: <título orientado ao valor>

**Como** <papel>  
**Quero** <ação>  
**Para** <benefício>

---

## Critérios de aceite

**CA-01:** <critério verificável>  
**CA-02:** <critério verificável>  
...

## Fora do escopo
- <item excluído 1>
- <item excluído 2>

## Dependências
- <dependência 1 — status: resolvida / bloqueada>
- <dependência 2 — status: resolvida / bloqueada>

## DoR
- [x] Critérios de aceite definidos e verificáveis
- [x] Escopo delimitado
- [ ] Contrato de API do BFF — pendente com arquiteto  ← bloqueador
```

---

## Checklist de conclusão

- [ ] Título orientado ao valor, não à implementação
- [ ] Todos os critérios de aceite verificáveis por teste
- [ ] Escopo delimitado com "fora do escopo" explícito
- [ ] Dependências identificadas e status declarado
- [ ] DoR completo — se bloqueada, dependência nomeada
