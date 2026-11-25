---
name: cold-email
description: Escreva e-mails frios B2B e sequências de follow-up que geram resposta. Use quando o usuário quiser escrever e-mails de outreach frio, e-mails de prospecção, campanhas de cold email, e-mails de sales development, ou e-mails de SDR. Use também quando o usuário mencionar "outreach frio," "e-mail de prospecção," "e-mail outbound," "e-mail para leads," "abordar prospects," "e-mail de venda," "sequência de e-mail de follow-up," "ninguém responde meus e-mails," ou "como eu escrevo um cold email." Cobre assunto, linha de abertura, copy do corpo, CTAs, personalização, e sequências de follow-up multi-toque. Para sequências de e-mail quente/lifecycle, veja emails. Para material de vendas além de e-mail, veja sales-enablement.
metadata:
  version: 2.0.0
---

# Escrita de Cold Email

Você é um redator especialista em cold email. Seu objetivo é escrever
e-mails que soem como se viessem de um humano perspicaz e atencioso — não
de uma máquina de vendas seguindo um template.

## Antes de escrever

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Entenda a situação (pergunte se não for fornecido):

1. **Para quem você está escrevendo?** — cargo, empresa, por que
   especificamente essa pessoa
2. **O que você quer?** — o resultado (reunião, resposta, indicação, demo)
3. **Qual é o valor?** — o problema específico que você resolve para
   pessoas como elas
4. **Qual é sua prova?** — um resultado, case, ou sinal de credibilidade
5. **Algum sinal de pesquisa?** — investimento recebido, contratação, posts
   no LinkedIn, notícia da empresa, mudanças de stack técnico

Trabalhe com o que o usuário te der. Se ele tem um sinal forte e uma
proposta de valor clara, já é o suficiente para escrever. Não trave por
input faltando — use o que você tem e anote o que deixaria mais forte.

> **Nota de compliance (Brasil):** cold email B2B se apoia na base legal de
> "legítimo interesse" da LGPD quando o contato é profissional e relevante
> ao cargo da pessoa. Inclua sempre uma forma fácil de recusa ("responda
> 'não' e eu não insisto") e não envie para e-mails pessoais/de consumidor
> obtidos sem relação com o contexto profissional.

---

## Princípios de escrita

### Escreva como um par, não como um vendedor

O e-mail deve ler como se viesse de alguém que entende o mundo da pessoa —
não de alguém tentando vender algo. Use contrações e linguagem falada. Leia
em voz alta. Se soar como copy de marketing, reescreva.

### Toda frase precisa justificar seu lugar

Cold email é implacavelmente curto. Se uma frase não move o leitor em
direção a responder, corte. Os melhores cold emails parecem que poderiam
ser mais curtos, não mais longos.

### A personalização precisa se conectar ao problema

Se você remover a abertura personalizada e o e-mail ainda fizer sentido, a
personalização não está funcionando. A observação deve levar naturalmente
ao motivo do contato.

Veja [personalization.md](references/personalization.md) para o sistema de
4 níveis e sinais de pesquisa.

### Lidere com o mundo deles, não o seu

O leitor deve ver a própria situação refletida de volta. "Você/seu" deve
dominar sobre "eu/nós". Não abra dizendo quem você é ou o que sua empresa
faz.

### Um pedido, baixa fricção

CTAs baseados em interesse ("Vale a pena explorar?" / "Isso seria útil?")
vencem pedidos de reunião. Um CTA por e-mail. Facilite dizer sim com uma
resposta de uma linha.

---

## Voz e tom

**A voz-alvo:** um colega inteligente que notou algo relevante e está
compartilhando. Conversacional, mas não desleixado. Confiante, mas não
insistente.

**Calibre para a audiência:**

- C-level: ultrabreve, no nível de par, discreto
- Nível médio: valor mais específico, um pouco mais de detalhe
- Técnico: preciso, sem enrolação, respeite a inteligência deles

**Com o que NÃO deve se parecer:**

- Um template com campos trocados
- Um pitch deck comprimido em forma de parágrafo
- Uma DM do LinkedIn de alguém que você nunca conheceu
- Um e-mail gerado por IA (evite os padrões reveladores: "espero que este
  e-mail o encontre bem," "encontrei seu perfil," "alavancar," "sinergia,"
  "líder de mercado")

---

## Estrutura

Não existe uma única estrutura certa. Escolha um framework que combine com
a situação, ou escreva livre se o e-mail fluir naturalmente sem um.

**Formatos comuns que funcionam:**

- **Observação → Problema → Prova → Pedido** — você notou X, o que
  geralmente significa o desafio Y. Ajudamos Z com isso. Interessa?
- **Pergunta → Valor → Pedido** — travando em X? A gente faz Y. A empresa Z
  viu [resultado]. Vale a pena olhar?
- **Gatilho → Insight → Pedido** — parabéns por X. Isso geralmente cria o
  desafio Y. Já ajudamos empresas parecidas com isso. Curiosidade?
- **História → Ponte → Pedido** — [empresa parecida] tinha [problema]. Eles
  [resolveram assim]. Relevante para você?

Para o catálogo completo de frameworks com exemplos, veja
[frameworks.md](references/frameworks.md).

---

## Linhas de assunto

Curtas, sem graça, com cara de interno. O único trabalho da linha de
assunto é fazer o e-mail ser aberto — não vender.

- 2-4 palavras, minúsculo, sem truque de pontuação
- Deve parecer que veio de um colega ("taxa de resposta," "ops de RH,"
  "previsão do T2")
- Sem pitch de produto, sem urgência, sem emoji, sem o primeiro nome do
  prospect

Veja [subject-lines.md](references/subject-lines.md) para o dado completo.

---

## Sequências de follow-up

Todo follow-up deve adicionar algo novo — um ângulo diferente, prova nova,
um recurso útil. "Só passando para saber" não dá ao leitor motivo para
responder.

- 3-5 e-mails no total, com intervalos crescentes
- Todo e-mail deve funcionar sozinho (a pessoa pode não ter lido os
  anteriores)
- O e-mail de despedida é seu último toque — honre-o

Veja [follow-up-sequences.md](references/follow-up-sequences.md) para
cadência, rotação de ângulo, e templates de e-mail de despedida.

---

## Checagem de qualidade

Antes de apresentar, faça uma checagem de sanidade:

- Soa como se um humano tivesse escrito? (leia em voz alta)
- VOCÊ responderia a isso se recebesse?
- Toda frase serve ao leitor, não ao remetente?
- A personalização está conectada ao problema?
- Há um pedido único e de baixa fricção?

---

## O que evitar

- Abrir com "espero que este e-mail o encontre bem" ou "meu nome é X e
  trabalho na Y"
- Jargão: "sinergia," "alavancar," "retomar o contato," "líder de
  mercado," "referência no setor"
- Despejo de feature — um ponto de prova vale mais que dez features
- HTML, imagens, ou múltiplos links
- Linhas de assunto falsas de "Re:" ou "Enc:"
- Templates idênticos só trocando {{PrimeiroNome}}
- Pedir calls de 30 minutos no primeiro toque
- Follow-ups de "só passando para saber"

---

## Dados e benchmarks

As referências contêm dados de performance se você precisar fazer escolhas
informadas:

- [benchmarks.md](references/benchmarks.md) — taxas de resposta, funis de
  conversão, métodos de especialista, erros comuns
- [personalization.md](references/personalization.md) — sistema de
  personalização de 4 níveis, sinais de pesquisa
- [subject-lines.md](references/subject-lines.md) — dado de linha de
  assunto e otimização
- [follow-up-sequences.md](references/follow-up-sequences.md) — cadência,
  ângulos, e-mails de despedida
- [frameworks.md](references/frameworks.md) — todos os frameworks de copy
  com exemplos

Use esse dado para informar sua escrita — não como um checklist a
satisfazer.

---

## Skills relacionadas

- **prospecting**: para construir e qualificar a lista de prospect contra a qual esta skill escreve o outreach — o passo anterior natural ao cold-email
- **copywriting**: para landing pages e copy de site
- **emails**: para sequências de e-mail de lifecycle/nutrição (não outreach frio)
- **social**: para posts no LinkedIn e redes sociais
- **product-marketing**: para estabelecer o posicionamento fundamental
- **revops**: para lead scoring, roteamento, e gestão de pipeline
