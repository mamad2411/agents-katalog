---
name: escrever-gherkin
description: "Escreve cenários BDD em sintaxe Gherkin para testes de aceitação. Use quando o dev-qa vai formalizar critérios de aceite executáveis."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: escrever-gherkin

Escreve **cenários de comportamento em Gherkin** (BDD): especificações legíveis por negócio e técnico que descrevem o que o sistema deve fazer, não como. Serve como contrato entre produto, QA e desenvolvimento antes da implementação.

**Agente:** dev-qa  
**Guardrails aplicáveis:** `00-core.md`, `processo.md`

---

## Quando usar

- Ao refinar uma história de usuário com critérios de aceite complexos ou ambíguos
- Para documentar fluxos de negócio críticos que precisam de rastreabilidade
- Quando produto, QA e dev precisam de linguagem comum sobre o comportamento esperado
- Como pré-requisito do DoR (`processo.md §5`) para histórias com múltiplos caminhos

---

## Conceitos fundamentais

**Gherkin** é a linguagem que descreve comportamentos em **Given / When / Then**:
- **Given** (Dado) — contexto de pré-condição, estado inicial do sistema
- **When** (Quando) — ação executada pelo usuário ou sistema
- **Then** (Então) — resultado observável esperado
- **And / But** — encadeamento de passos do mesmo tipo

**Feature** agrupa cenários relacionados a uma mesma funcionalidade.  
**Scenario** descreve um único comportamento sob uma condição específica.  
**Scenario Outline** parametriza o mesmo comportamento com múltiplos conjuntos de dados.

---

## Processo de execução

### Passo 1 — Identificar a Feature

- Uma Feature por funcionalidade de negócio — não por tela ou endpoint
- Título da Feature no nível do usuário: "Autenticação de usuário", "Checkout de pedido"

```gherkin
# language: pt

Funcionalidade: Autenticação de usuário
  Como um usuário registrado
  Quero fazer login no sistema
  Para acessar minhas informações e pedidos
```

### Passo 2 — Escrever o cenário do caminho feliz

```gherkin
Cenário: Login bem-sucedido com credenciais válidas
  Dado que o usuário "ana@example.com" está cadastrado com a senha "Senha@2024"
  Quando o usuário acessa a tela de login
  E informa o e-mail "ana@example.com" e a senha "Senha@2024"
  E clica no botão "Entrar"
  Então o usuário é redirecionado para a tela inicial
  E vê a mensagem de boas-vindas "Olá, Ana"
```

### Passo 3 — Escrever cenários de erro e caminhos alternativos

```gherkin
Cenário: Login com senha incorreta
  Dado que o usuário "ana@example.com" está cadastrado
  Quando o usuário tenta fazer login com a senha "SenhaErrada"
  Então o sistema exibe a mensagem "E-mail ou senha incorretos"
  E o usuário permanece na tela de login

Cenário: Login com conta bloqueada após 5 tentativas
  Dado que o usuário "ana@example.com" fez 5 tentativas de login com senha incorreta
  Quando o usuário tenta fazer login novamente
  Então o sistema exibe a mensagem "Conta temporariamente bloqueada. Tente novamente em 15 minutos"
  E o botão "Entrar" está desabilitado por 15 minutos

Cenário: Login com e-mail não cadastrado
  Quando o usuário tenta fazer login com o e-mail "naoexiste@example.com"
  Então o sistema exibe a mensagem "E-mail ou senha incorretos"
```

### Passo 4 — Usar Scenario Outline para múltiplos casos de dados

```gherkin
Esquema do Cenário: Validação de campos obrigatórios no login
  Quando o usuário acessa a tela de login
  E informa o e-mail "<email>" e a senha "<senha>"
  E clica no botão "Entrar"
  Então o sistema exibe a mensagem de validação "<mensagem>"

  Exemplos:
    | email                | senha      | mensagem                    |
    | (vazio)              | Senha@2024 | E-mail é obrigatório        |
    | emailinvalido        | Senha@2024 | Informe um e-mail válido    |
    | ana@example.com      | (vazio)    | Senha é obrigatória         |
```

### Passo 5 — Escrever Feature para fluxo de negócio completo

```gherkin
# language: pt

Funcionalidade: Checkout de pedido
  Como um usuário autenticado
  Quero finalizar a compra de itens no carrinho
  Para receber os produtos adquiridos

  Contexto:
    Dado que o usuário está autenticado
    E possui o produto "Produto A" no carrinho com quantidade 2

  Cenário: Finalizar compra com cartão aprovado
    Quando o usuário acessa o checkout
    E informa os dados do cartão de crédito válido
    E confirma o pedido
    Então o pedido é criado com status "Confirmado"
    E o usuário recebe a confirmação por e-mail
    E o carrinho é esvaziado

  Cenário: Checkout com cartão recusado
    Quando o usuário acessa o checkout
    E informa os dados de um cartão recusado
    E confirma o pedido
    Então o sistema exibe a mensagem "Pagamento recusado. Verifique os dados do cartão"
    E o pedido não é criado
    E o carrinho permanece com os itens

  Cenário: Checkout com estoque insuficiente
    Dado que o produto "Produto A" tem apenas 1 unidade em estoque
    Quando o usuário tenta confirmar o pedido com quantidade 2
    Então o sistema exibe a mensagem "Quantidade indisponível em estoque"
    E sugere a quantidade máxima disponível: 1
```

### Passo 6 — Regras de escrita

**Faça:**
- Usar linguagem de negócio — "pedido confirmado", não "INSERT no banco de dados"
- Escrever no presente do indicativo — "o sistema exibe", não "o sistema exibirá"
- Um comportamento por cenário — não agrupar múltiplas asserções não relacionadas
- `Contexto` (Background) para pré-condições comuns a todos os cenários da Feature

**Não faça:**
```gherkin
# ⛔ detalhes de implementação no Gherkin
Então o sistema insere um registro na tabela "orders" com status "CONFIRMED"
E o campo "payment_status" é atualizado para "APPROVED"

# ⛔ múltiplos comportamentos no mesmo cenário
Então o pedido é criado
E o e-mail é enviado
E o estoque é decrementado
E o carrinho é limpo
E o usuário é redirecionado
E a notificação push é enviada
# → dividir em cenários separados quando cada comportamento pode falhar independentemente

# ⛔ cenário sem contexto claro
Quando o usuário clica em confirmar
Então algo acontece
```

---

## Estrutura de arquivos

```
e2e/features/
├── autenticacao.feature
├── checkout.feature
├── perfil-usuario.feature
└── gestao-pedidos.feature
```

---

## Saída produzida

- Arquivo `.feature` com Feature completa: caminho feliz + caminhos de erro + validações
- Índice de cenários cobrindo os critérios de aceite da história
- Lacunas identificadas: comportamentos não especificados nos critérios de aceite que precisam de esclarecimento com produto

---

## Checklist de conclusão

- [ ] Feature tem título no nível do usuário — não técnico
- [ ] Caminho feliz coberto
- [ ] Ao menos um cenário de erro por ponto de falha relevante
- [ ] Scenario Outline para casos com múltiplos conjuntos de dados
- [ ] Linguagem de negócio — sem referência a banco, endpoints ou código
- [ ] Dados de teste sintéticos — sem CPF, cartão ou e-mail real (testes.md §7)
- [ ] Cenários mapeados para critérios de aceite da história
