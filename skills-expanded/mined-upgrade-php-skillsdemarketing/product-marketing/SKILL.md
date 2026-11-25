---
name: product-marketing
description: Quando o usuário quiser criar ou atualizar seu documento de contexto de product marketing. Use também quando o usuário mencionar "contexto de produto," "contexto de marketing," "configurar contexto," "posicionamento," "quem é meu público-alvo," "descrever meu produto," "ICP," "perfil de cliente ideal," ou quiser evitar repetir informação fundamental em várias tarefas de marketing. Use isso no início de qualquer projeto novo antes de usar as outras skills de marketing — cria o `.agents/product-marketing.md` que todas as outras skills consultam para contexto de produto, audiência, e posicionamento.
metadata:
  version: 2.1.0
---

# Contexto de Product Marketing

Você ajuda os usuários a criar e manter um documento de contexto de product marketing. Ele captura informação fundamental de posicionamento e mensagem que outras skills de marketing consultam, para que os usuários não precisem se repetir.

O documento fica salvo em `.agents/product-marketing.md`.

## Fluxo de trabalho

### Passo 1: Verificar Contexto Existente

Primeiro, verifique se `.agents/product-marketing.md` já existe. Verifique também `.claude/product-marketing.md` e o nome de arquivo legado `product-marketing-context.md` (em `.agents/` ou `.claude/`) para setups mais antigos — se encontrado em qualquer lugar diferente do local canônico `.agents/product-marketing.md`, ofereça-se para movê-lo para lá.

**Se existir:**

- Leia e resuma o que está capturado — anote a **Versão do documento** atual e as últimas entradas do **Changelog** para que o usuário veja onde o documento está e o que mudou recentemente
- Pergunte quais seções ele quer atualizar
- Colete informação só para essas seções
- Em qualquer salvamento substantivo, avance a versão e adicione uma entrada no changelog (veja Passo 4). Esse documento é o contexto compartilhado que toda outra skill de marketing lê, então manter um rastro datado de *o que mudou e por quê* vale a pena.

**Se não existir, ofereça duas opções:**

1. **Rascunho automático a partir do código** (recomendado): Você vai estudar o repositório — README, landing pages, copy de marketing, package.json, etc. — e rascunhar uma V1 do documento de contexto. O usuário então revisa, corrige, e preenche as lacunas. Isso é mais rápido do que começar do zero.

2. **Começar do zero**: Percorra cada seção conversacionalmente, coletando informação uma seção por vez.

A maioria dos usuários prefere a opção 1. Depois de apresentar o rascunho, pergunte: "O que precisa ser corrigido? O que está faltando?"

### Passo 2: Coletar Informação

**Se rascunhando automaticamente:**

1. Leia o código: README, landing pages, copy de marketing, páginas sobre, meta descriptions, package.json, qualquer documentação existente
2. Rascunhe todas as seções com base no que encontrar
3. Apresente o rascunho e pergunte o que precisa ser corrigido ou está faltando
4. Itere até o usuário ficar satisfeito

**Se começando do zero:**
Percorra cada seção abaixo conversacionalmente, uma de cada vez. Não jogue todas as perguntas de uma vez.

Para cada seção:

1. Explique brevemente o que você está capturando
2. Faça as perguntas relevantes
3. Confirme a precisão
4. Passe para a próxima

Busque a linguagem verbatim do cliente — frases exatas valem mais que descrições polidas porque refletem como os clientes de fato pensam e falam, o que torna a copy mais ressonante.

---

## Seções a Capturar

### 1. Visão Geral do Produto

- Descrição de uma linha
- O que ele faz (2-3 frases)
- Categoria de produto (em que "prateleira" você está — como os clientes te buscam)
- Tipo de produto (SaaS, marketplace, e-commerce, serviço, etc.)
- Modelo de negócio e preço

### 2. Público-Alvo

- Tipo de empresa-alvo (indústria, tamanho, estágio)
- Tomadores de decisão-alvo (cargos, departamentos)
- Caso de uso primário (o principal problema que você resolve)
- Jobs to be done (2-3 coisas que os clientes "contratam" você para fazer)
- Casos de uso ou cenários específicos

### 3. Personas (apenas B2B)

Se múltiplos stakeholders estão envolvidos na compra, capture para cada um:

- Usuário, Campeão, Tomador de Decisão, Comprador Financeiro, Influenciador Técnico
- O que cada um se importa, o desafio dele, e o valor que você promete a ele

### 4. Problemas e Pontos de Dor

- Desafio central que os clientes enfrentam antes de te encontrar
- Por que as soluções atuais são insuficientes
- O que isso custa a eles (tempo, dinheiro, oportunidades)
- Tensão emocional (estresse, medo, dúvida)

### 5. Panorama Competitivo

- **Concorrentes diretos**: Mesma solução, mesmo problema (ex.: Calendly vs. SavvyCal)
- **Concorrentes secundários**: Solução diferente, mesmo problema (ex.: Calendly vs. agendamento do Superhuman)
- **Concorrentes indiretos**: Abordagem conflitante (ex.: Calendly vs. assistente pessoal)
- Como cada um é insuficiente para os clientes

### 6. Diferenciação

- Principais diferenciais (capacidades que as alternativas não têm)
- Como você resolve isso de forma diferente
- Por que isso é melhor (benefícios)
- Por que os clientes te escolhem em vez das alternativas

### 7. Objeções e Anti-Personas

- Top 3 objeções ouvidas em vendas e como respondê-las
- Quem NÃO é um bom encaixe (anti-persona)

### 8. Dinâmica de Troca

As Quatro Forças do JTBD:

- **Empurrão (Push)**: Quais frustrações os afastam da solução atual
- **Atração (Pull)**: O que os atrai para você
- **Hábito**: O que os mantém presos à abordagem atual
- **Ansiedade**: O que os preocupa em relação à troca

### 9. Linguagem do Cliente

- Como os clientes descrevem o problema (verbatim)
- Como eles descrevem sua solução (verbatim)
- Palavras/frases a usar
- Palavras/frases a evitar
- Glossário de termos específicos do produto

### 10. Voz da Marca

- Tom (profissional, casual, brincalhão, etc.)
- Estilo de comunicação (direto, conversacional, técnico)
- Personalidade da marca (3-5 adjetivos)

### 11. Pontos de Prova

- Métricas ou resultados-chave a citar
- Clientes/logos notáveis
- Trechos de depoimento
- Principais temas de valor e evidências de suporte

### 12. Objetivos

- Objetivo principal de negócio
- Ação de conversão chave (o que você quer que as pessoas façam)
- Métricas atuais (se conhecidas)

---

## Passo 3: Criar o Documento

Depois de coletar a informação, crie `.agents/product-marketing.md` com esta estrutura:

```markdown
# Contexto de Product Marketing

**Versão do documento:** v1
**Última atualização:** [data]

## Visão Geral do Produto
**Uma linha:**
**O que faz:**
**Categoria de produto:**
**Tipo de produto:**
**Modelo de negócio:**

## Público-Alvo
**Empresas-alvo:**
**Tomadores de decisão:**
**Caso de uso primário:**
**Jobs to be done:**
-
**Casos de uso:**
-

## Personas
| Persona | Se importa com | Desafio | Valor que prometemos |
|---------|-----------------|---------|------------------------|
| | | | |

## Problemas e Pontos de Dor
**Problema central:**
**Por que as alternativas são insuficientes:**
-
**O que isso custa a eles:**
**Tensão emocional:**

## Panorama Competitivo
**Direto:** [Concorrente] — insuficiente porque...
**Secundário:** [Abordagem] — insuficiente porque...
**Indireto:** [Alternativa] — insuficiente porque...

## Diferenciação
**Principais diferenciais:**
-
**Como fazemos diferente:**
**Por que isso é melhor:**
**Por que os clientes nos escolhem:**

## Objeções
| Objeção | Resposta |
|---------|----------|
| | |

**Anti-persona:**

## Dinâmica de Troca
**Empurrão:**
**Atração:**
**Hábito:**
**Ansiedade:**

## Linguagem do Cliente
**Como eles descrevem o problema:**
- "[verbatim]"
**Como eles nos descrevem:**
- "[verbatim]"
**Palavras a usar:**
**Palavras a evitar:**
**Glossário:**
| Termo | Significado |
|-------|--------------|
| | |

## Voz da Marca
**Tom:**
**Estilo:**
**Personalidade:**

## Pontos de Prova
**Métricas:**
**Clientes:**
**Depoimentos:**
> "[citação]" — [quem]
**Temas de valor:**
| Tema | Prova |
|------|-------|
| | |

## Objetivos
**Objetivo de negócio:**
**Ação de conversão:**
**Métricas atuais:**

## Changelog
*Mais recente primeiro. Uma linha por revisão: o que mudou e por quê.*
- v1 ([data]) — Contexto inicial.
```

---

## Passo 4: Confirmar, Versionar, e Salvar

- Mostre o documento completo
- Pergunte se algo precisa de ajuste
- **Defina a versão e o changelog** — esse é o rastro de um documento que toda outra skill lê:
  - **Documento novo:** defina `Versão do documento: v1` e uma única entrada de Changelog — `- v1 ([hoje]) — Contexto inicial.`
  - **Atualizando um documento existente:** incremente a versão (v2 → v3 …), atualize `Última atualização` para hoje, e **adicione uma nova entrada de Changelog no topo** da lista (mais recente primeiro) resumindo *o que mudou e por quê* em uma linha. Nunca reescreva ou reordene entradas passadas.
  - Uma boa entrada nomeia as seções tocadas e o motivo, não "atualizou o documento". Exemplos:
    - `- v3 (2026-07-16) — Reposicionado de "ferramenta de e-mail" para "plataforma de entregabilidade"; adicionado RevOps ao ICP.`
    - `- v2 (2026-06-02) — Reescreveu proposta de valor e objeções após 5 entrevistas com clientes; adicionado concorrente Acme.`
  - Use a data de hoje em formato ISO (AAAA-MM-DD) para a entrada e para `Última atualização`.
  - **Correção só de erro de digitação:** não avance a versão nem adicione entrada no changelog — apenas salve a correção. Toda outra mudança avança a versão e ganha uma entrada. Quando a mudança é um reposicionamento de verdade, diga isso claramente — as skills downstream vão agora gerar em cima do novo contexto.
- Salve em `.agents/product-marketing.md`
- Diga ao usuário: "As outras skills de marketing agora vão usar esse contexto automaticamente. O Changelog no final rastreia cada revisão — confira para ver como seu posicionamento evoluiu. Rode `/product-marketing` a qualquer momento para atualizá-lo."

---

## Dicas

- **Seja específico**: Pergunte "Qual é a #1 frustração que os traz até você?" em vez de "Que problema eles resolvem?"
- **Capture as palavras exatas**: Linguagem do cliente vale mais que descrições polidas
- **Peça exemplos**: "Você pode me dar um exemplo?" desbloqueia respostas melhores
- **Valide enquanto avança**: Resuma cada seção e confirme antes de seguir
- **Pule o que não se aplica**: Nem todo produto precisa de todas as seções (ex.: Personas para B2C)
