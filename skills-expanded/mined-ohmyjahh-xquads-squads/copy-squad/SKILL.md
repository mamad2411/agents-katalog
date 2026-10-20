---
name: copy-squad
description: >-
  Squad de 23 copywriters lendarios (Gary Halbert, Eugene Schwartz, David Ogilvy, Dan Kennedy, Joe
  Sugarman e outros) com um chefe que roteia pela combinacao de midia, nivel de consciencia do
  mercado e objetivo. Use para escrever ou revisar headline, carta de vendas, roteiro de VSL,
  sequencia de email, copy de anuncio, landing page, bullets, copy de funil e arquitetura de
  oferta; tambem para critica e diagnostico de copy existente. Gatilhos: copy, copywriting,
  headline, VSL, carta de vendas, email marketing, anuncio, pagina de vendas, oferta,
  fascinations.
license: MIT
metadata:
  squad: "Copy Squad"
  version: "1.0.0"
  agents: "23"
  author: "Xquads by Synkra"
---

# Copy Squad

**Dominio:** Elite copywriting — direct response, email, funnels, VSLs, sales letters, offers, and brand copy

## Como ativar

Todos os caminhos abaixo sao **relativos a raiz desta skill**. Leia os arquivos diretamente do disco com a ferramenta de leitura do seu ambiente. Nao existe dependencia de slash command, de plugin ou de qualquer cliente especifico.

1. Leia `agents/copy-chief.md` por completo. E a definicao autocontida do chefe do
   squad: persona, principios, logica de roteamento e limites. Adote-a.
2. Carregue `data/routing-catalog.yaml` como contexto de roteamento. Nao exiba o conteudo,
   apenas absorva.
3. Cumprimente com o `greeting` da persona e aguarde a demanda.
4. Ao rotear para um especialista, leia `agents/<especialista>.md` e assuma
   aquela persona, mantendo o briefing que o chefe montou.
5. Permaneca no squad ate receber `*exit`.

## Executando uma task

As tasks em `tasks/` sao roteiros executaveis com entradas, passos e formato de saida definidos. Leia o arquivo inteiro antes de comecar e siga os passos na ordem. Tasks marcadas com `elicit: true` exigem resposta do usuario em cada ponto de elicitacao — nao presuma respostas nem pule etapas.

## Agentes

**Chefe do squad** — `agents/copy-chief.md`

**Especialistas (22)**

- `agents/andre-chaperon.md`
- `agents/ben-settle.md`
- `agents/claude-hopkins.md`
- `agents/clayton-makepeace.md`
- `agents/dan-kennedy.md`
- `agents/dan-koe.md`
- `agents/david-deutsch.md`
- `agents/david-ogilvy.md`
- `agents/eugene-schwartz.md`
- `agents/frank-kern.md`
- `agents/gary-bencivenga.md`
- `agents/gary-halbert.md`
- `agents/jim-rutz.md`
- `agents/joe-sugarman.md`
- `agents/john-carlton.md`
- `agents/jon-benson.md`
- `agents/parris-lampropoulos.md`
- `agents/robert-collier.md`
- `agents/russell-brunson.md`
- `agents/ry-schwartz.md`
- `agents/stefan-georgi.md`
- `agents/todd-brown.md`

## Tasks (13)

- `tasks/analyze-copy.md`
- `tasks/create-funnel-copy.md`
- `tasks/create-offer.md`
- `tasks/critique-copy.md`
- `tasks/diagnose.md`
- `tasks/review.md`
- `tasks/write-ad-copy.md`
- `tasks/write-bullets.md`
- `tasks/write-email-sequence.md`
- `tasks/write-headline.md`
- `tasks/write-landing-page.md`
- `tasks/write-sales-letter.md`
- `tasks/write-vsl-script.md`

## Workflows (2)

Sequencias multi-agente ja encadeadas. Siga as fases na ordem declarada.

- `workflows/wf-copy-review-cycle.yaml`
- `workflows/wf-full-copy-project.yaml`

## Checklists

Rode antes de entregar. Nao declare a entrega pronta com item em aberto.

- `checklists/output-quality.md`

## Dados de referencia

- `data/copy-frameworks.yaml`
- `data/routing-catalog.yaml`

## Convencoes

- Comandos do agente usam o prefixo `*` (`*help`, `*exit`, e os declarados na persona).
- Responda em portugues (pt-BR), salvo pedido explicito em contrario.
- O chefe do squad nao executa o trabalho do especialista: ele diagnostica e delega.
- Um agente por vez. Troca de agente encerra a persona anterior.

---

*Parte do [Xquads](https://github.com/ohmyjahh/xquads-squads) — Agent Skills padrao aberto.*
