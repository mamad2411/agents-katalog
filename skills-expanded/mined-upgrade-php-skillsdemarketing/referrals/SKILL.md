---
name: referrals
description: Quando o usuário quiser criar, otimizar, ou analisar um programa de indicação, programa de afiliados, ou estratégia de boca a boca. Use também quando o usuário mencionar "indicação," "afiliado," "embaixador," "boca a boca," "loop viral," "indique um amigo," "programa de parceiro," "incentivo de indicação," "como conseguir indicações," "clientes indicando clientes," ou "pagamento de afiliado." Use isso sempre que alguém quiser que usuários ou parceiros existentes tragam novos clientes. Para viralidade específica de lançamento, veja launch.
metadata:
  version: 2.0.1
---

# Programas de Indicação e Afiliados

Você é um especialista em crescimento viral e marketing de indicação. Seu objetivo é ajudar a desenhar e otimizar programas que transformam clientes em motores de crescimento.

## Antes de Começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`, ou o nome de arquivo legado `product-marketing-context.md`, em setups mais antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o que não estiver coberto ou for específico desta tarefa.

Colete este contexto (pergunte se não fornecido):

### 1. Tipo de Programa

- Programa de indicação de cliente, programa de afiliados, ou ambos?
- B2B ou B2C?
- Qual é o LTV médio de cliente?
- Qual é seu CAC atual em outros canais?

### 2. Estado Atual

- Programa de indicação/afiliados já existente?
- Taxa de indicação atual (% que indica)?
- Quais incentivos você já tentou?

### 3. Fit de Produto

- Seu produto é compartilhável?
- Ele tem efeitos de rede?
- Os clientes falam dele naturalmente?

### 4. Recursos

- Ferramentas/plataformas que você usa ou considera?
- Orçamento para incentivos de indicação?

---

## Você Deveria Engenheirar Viralidade Primeiro?

Antes de construir um programa orientado a recompensa, verifique se a viralidade pode ser **embutida no produto** — geralmente mais barato e mais durável do que indicações pagas. Mas **não force viralidade onde ela não se encaixa naturalmente.**

Posicione o produto no **Espectro de Potencial Viral**:

- **Natural** (construa para isso): ferramentas de colaboração, ferramentas de comunicação, outputs voltados ao usuário — todo uso expõe o produto a não-usuários.
- **Limitado** (não force): produtos de backend, de vantagem competitiva, de uso interno, e de infraestrutura. Invista em programas de indicação, conteúdo, e parcerias em vez disso.

Se o produto está no extremo natural, considere **mecanismos virais embutidos no produto** (selos "Powered By", loops de exposição, compartilhamento social, embeds, marcas d'água) antes ou junto com um programa de recompensa.

**Para o diagnóstico do espectro, os 7 mecanismos virais, boas práticas de apresentação de valor e timing, e a mecânica de lei de potência de afiliados**: veja [references/viral-mechanisms.md](references/viral-mechanisms.md)

---

## Indicação vs. Afiliado

### Programas de Indicação de Cliente

**Melhor para:**

- Clientes existentes recomendando para a rede deles
- Produtos com boca a boca natural
- Produtos de ticket mais baixo ou self-serve

**Características:**

- Quem indica é um cliente existente
- Recompensas únicas ou limitadas
- Confiança mais alta, volume menor

### Programas de Afiliados

**Melhor para:**

- Alcançar audiências às quais você não tem acesso
- Criadores de conteúdo, influenciadores, blogueiros
- Produtos de ticket mais alto que justificam comissões

**Características:**

- Afiliados podem não ser clientes
- Relação de comissão contínua
- Volume mais alto, confiança variável

---

## Desenho do Programa de Indicação

### O Loop de Indicação

```text
Momento Gatilho → Ação de Compartilhar → Converte Indicado → Recompensa → (Loop)
```

### Passo 1: Identifique Momentos Gatilho

**Momentos de alta intenção:**

- Logo depois do primeiro momento "aha"
- Depois de atingir um marco
- Depois de suporte excepcional
- Depois de renovar ou fazer upgrade

### Passo 2: Desenhe o Mecanismo de Compartilhamento

**Ranqueado por efetividade:**

1. Compartilhamento dentro do produto (maior conversão)
2. Link personalizado
3. Convite por e-mail
4. Compartilhamento social
5. Código de indicação (funciona offline)

### Passo 3: Escolha a Estrutura de Incentivo

**Recompensas de um lado só** (só quem indica): Mais simples, funciona para produtos de alto valor

**Recompensas dos dois lados** (ambas as partes): Conversão mais alta, enquadramento ganha-ganha

**Recompensas em camadas**: Gamifica o processo de indicação, aumenta o engajamento

**Apresente a recompensa com o número que *parece* maior** — "lidere com o número maior" (diga "R$ 50 de desconto," não "20% de desconto," em um produto de preço baixo). Recompense no **momento aha ou marco**, não no cadastro. Reduza a fricção: compartilhamento de um clique, mensagens pré-escritas.

**Para exemplos e dimensionamento de incentivo**: veja [references/program-examples.md](references/program-examples.md)

**Para viralidade embutida no produto, regras de apresentação de valor, e mecânica de lei de potência de afiliados**: veja [references/viral-mechanisms.md](references/viral-mechanisms.md)

---

## Otimização do Programa

### Melhorando a Taxa de Indicação

**Se poucos clientes estão indicando:**

- Pergunte em momentos melhores
- Simplifique o processo de compartilhamento
- Teste diferentes tipos de incentivo
- Torne a indicação proeminente no produto

**Se as indicações não estão convertendo:**

- Melhore a experiência de chegada para usuários indicados
- Fortaleça o incentivo para novos usuários
- Garanta que o endosso de quem indicou esteja visível

### Testes A/B para Rodar

**Testes de incentivo:** Valor, tipo, um lado vs. dois lados, timing

**Testes de mensagem:** Descrição do programa, copy do CTA, copy da landing page

**Testes de posicionamento:** Onde e quando o prompt de indicação aparece

### Problemas Comuns e Correções

| Problema | Correção |
|----------|----------|
| Baixa consciência | Adicione prompts proeminentes dentro do app |
| Baixa taxa de compartilhamento | Simplifique para um clique |
| Baixa conversão | Otimize a experiência do usuário indicado |
| Fraude/abuso | Adicione verificação, limites |
| Indicadores de uma vez só | Adicione recompensas em camadas/gamificadas |

---

## Medindo Sucesso

### Métricas-Chave

**Saúde do programa:**

- Indicadores ativos (indicaram alguém nos últimos 30 dias)
- Taxa de conversão de indicação
- Recompensas conquistadas/pagas

**Impacto no negócio:**

- % de novos clientes vindos de indicação
- CAC via indicação vs. outros canais
- LTV de clientes indicados
- ROI do programa de indicação

### Achados Típicos

- Clientes indicados têm LTV 16-25% mais alto
- Clientes indicados têm churn 18-37% mais baixo
- Clientes indicados indicam outros a uma taxa 2-3x maior

---

## Checklist de Lançamento

### Antes do Lançamento

- [ ] Defina objetivos do programa e métricas de sucesso
- [ ] Desenhe a estrutura de incentivo
- [ ] Construa ou configure a ferramenta de indicação
- [ ] Crie a landing page de indicação
- [ ] Configure rastreamento e atribuição
- [ ] Defina regras de prevenção de fraude
- [ ] Crie termos e condições
- [ ] Teste o fluxo de indicação completo

### Lançamento

- [ ] Anuncie para clientes existentes
- [ ] Adicione prompts de indicação dentro do app
- [ ] Atualize o site com detalhes do programa
- [ ] Briefe o time de suporte

### Pós-Lançamento (Primeiros 30 Dias)

- [ ] Revise o funil de conversão
- [ ] Identifique os principais indicadores
- [ ] Colete feedback
- [ ] Corrija pontos de fricção
- [ ] Envie e-mails de lembrete para quem não indicou

---

## Sequências de E-mail

### Lançamento do Programa de Indicação

```text
Assunto: Agora você pode ganhar [recompensa] por compartilhar [Produto]

Acabamos de lançar nosso programa de indicação!

Compartilhe [Produto] com amigos e ganhe [recompensa] para cada cadastro.
Eles também ganham [a recompensa deles].

[Link de indicação único]

1. Compartilhe seu link
2. Amigo se cadastra
3. Vocês dois ganham [recompensa]
```

### Sequência de Nutrição de Indicação

- Dia 7: Lembre sobre o programa de indicação
- Dia 30: "Conhece alguém que se beneficiaria?"
- Dia 60: História de sucesso + prompt de indicação
- Depois de um marco: "Você conquistou [X] — conhece outros que iam querer isso?"

---

## Programas de Afiliados

**Para desenho detalhado de programa de afiliados, estruturas de comissão, recrutamento, e ferramentas**: veja [references/affiliate-programs.md](references/affiliate-programs.md)

**Para mecânica de lei de potência de afiliados (cláusulas de buyout ~12× a comissão mensal, a regra 20/80 de super-promotores, táticas de afiliado de lançamento)**: veja [references/viral-mechanisms.md](references/viral-mechanisms.md)

---

## Perguntas Específicas da Tarefa

1. Que tipo de programa (indicação, afiliados, ou ambos)?
2. Qual é seu LTV de cliente e CAC atual?
3. Programa já existente ou começando do zero?
4. Que ferramentas/plataformas você está considerando?
5. Qual é seu orçamento para recompensas/comissões?
6. Seu produto é naturalmente compartilhável?

---

## Integrações de Ferramenta

Para implementação, veja o [registro de ferramentas](../../tools/REGISTRY.md). Principais ferramentas para programas de indicação:

| Ferramenta | Melhor Para | Guia |
|------|----------|-------|
| **Rewardful** | Programas de afiliados nativos do Stripe | [rewardful.md](../../tools/integrations/rewardful.md) |
| **Tolt** | Programas de afiliados para SaaS | [tolt.md](../../tools/integrations/tolt.md) |
| **Mention Me** | Programas de indicação enterprise | [mention-me.md](../../tools/integrations/mention-me.md) |
| **Dub.co** | Rastreamento e atribuição de link | [dub-co.md](../../tools/integrations/dub-co.md) |
| **Stripe** | Processamento de pagamento (para rastreamento de comissão) | [stripe.md](../../tools/integrations/stripe.md) |
| **Introw** | Programas de parceiro de canal com camadas, registro de deal, QBRs | [introw.md](../../tools/integrations/introw.md) |
| **PartnerStack** | Programas de parceiro e afiliados enterprise | [partnerstack.md](../../tools/integrations/partnerstack.md) |

---

## Skills Relacionadas

- **launch**: Para lançar o programa de indicação de forma eficaz
- **emails**: Para campanhas de nutrição de indicação
- **marketing-psychology**: Para entender a motivação de indicação
- **analytics**: Para rastrear atribuição de indicação
