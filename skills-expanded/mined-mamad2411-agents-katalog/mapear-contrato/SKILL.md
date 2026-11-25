---
name: mapear-contrato
description: "Formaliza contratos de comunicação entre serviços, definindo formatos de request e response. Use quando o arquiteto precisa documentar a integração entre dois serviços."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: mapear-contrato

Formaliza o **contrato de comunicação entre dois serviços**: define exatamente o que o produtor entrega e o que o consumidor espera, garantindo que ambos os lados possam evoluir independentemente sem quebrar a integração.

**Agente:** arquiteto  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `seguranca.md`

---

## Quando usar

- Ao definir nova integração entre System → Process, Process → BFF, ou serviço → parceiro externo
- Quando um contrato existente precisa evoluir (adicionar campo, mudar tipo, remover campo)
- Para documentar contratos implícitos que já existem mas nunca foram formalizados
- Antes de desenvolvimento paralelo (equipes diferentes implementando os dois lados)

---

## Conceitos

**Contrato:** acordo formal entre produtor (quem expõe) e consumidor (quem chama) sobre formato, tipos, campos obrigatórios, erros e garantias de compatibilidade.

**Breaking change:** mudança que faz o consumidor existente parar de funcionar sem alteração do seu lado.

| É breaking change | Não é breaking change |
|---|---|
| Remover campo obrigatório da response | Adicionar campo opcional à response |
| Mudar tipo de um campo (string → number) | Adicionar novo endpoint |
| Tornar campo opcional em obrigatório | Adicionar campo opcional ao request |
| Mudar semântica de código de status | Deprecar campo (ainda retornar, apenas marcar) |

---

## Entrada esperada

- Nome do produtor e do consumidor
- Operação a ser contratada (endpoint, evento, job)
- Entidades e campos envolvidos
- Versão atual do contrato (se evoluindo contrato existente)

---

## Processo de execução

### Passo 1 — Identificar as partes

```
Produtor: <serviço que expõe a operação>
Consumidor(es): <serviço(s) que chamam>
Operação: <POST /endpoint | GET /endpoint | tópico de evento>
```

### Passo 2 — Definir request (o que o consumidor envia)

Para cada campo:
- Nome em camelCase
- Tipo de dado
- Obrigatoriedade
- Restrições de validação
- Exemplo de valor válido

### Passo 3 — Definir response (o que o produtor retorna)

Para cada resposta possível:
- Código de status e condição
- Campos retornados
- Campos que NUNCA aparecem (dados sensíveis — ver `seguranca.md §1`)

### Passo 4 — Definir garantias do produtor

O produtor se compromete a:
- [ ] Nunca remover campo sem período de deprecação
- [ ] Nunca mudar tipo de campo sem versionamento
- [ ] Sempre retornar campos marcados como obrigatórios
- [ ] Manter idempotência quando declarada (ver `validar-idempotencia`)

### Passo 5 — Definir responsabilidades do consumidor

O consumidor se compromete a:
- [ ] Ignorar campos desconhecidos (tolerância a adições futuras)
- [ ] Não depender de campos marcados como `deprecated`
- [ ] Tratar todos os códigos de erro documentados

### Passo 6 — Registrar histórico de versão

Toda mudança de contrato tem entrada no histórico com: data, autor, tipo (breaking/non-breaking), motivo.

---

## Saída produzida

```markdown
## Contrato: <Produtor> → <Consumidor>

**Operação:** POST /api/v1/recursos  
**Versão:** 1.0  
**Data:** YYYY-MM-DD  
**Status:** Ativo | Deprecated (substituído por v2 em YYYY-MM-DD)

---

### Request

| Campo | Tipo | Obrigatório | Validação | Exemplo |
|---|---|---|---|---|
| nome | string | Sim | min:2, max:100 | "João Silva" |
| email | string (email) | Sim | formato válido | "joao@example.com" |
| roleId | uuid | Não | uuid v4 | "550e8400-..." |

### Response 201

| Campo | Tipo | Sempre presente | Observação |
|---|---|---|---|
| id | uuid | Sim | |
| nome | string | Sim | |
| createdAt | string (ISO 8601) | Sim | |

### Respostas de erro

| Código | Condição | Body |
|---|---|---|
| 400 | Campo inválido ou ausente | RFC 7807 com `detail` do campo |
| 409 | Email já cadastrado | RFC 7807 |
| 422 | Regra de negócio (descrição específica) | RFC 7807 |

---

### Garantias do produtor

- Campos da response 201 nunca serão removidos sem deprecação prévia de 30 dias
- Novos campos opcionais podem ser adicionados sem notificação
- Breaking changes requerem versionamento de API

### Responsabilidades do consumidor

- Ignorar campos desconhecidos na response
- Não assumir ordem dos campos no JSON
- Tratar 409 e 422 de forma diferente (409 = duplicidade, 422 = regra de negócio)

---

### Histórico

| Versão | Data | Tipo | Mudança |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | Inicial | Criação do contrato |
```
