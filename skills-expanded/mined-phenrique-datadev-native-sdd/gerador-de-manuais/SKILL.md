---
name: gerador-de-manuais
description: 'Gera tutorial, manual de marca (voz e tom) ou guia de convenções/contribuição a partir de template testado por projetos reais — referência do agente `documenter`. Cada tipo blinda uma falha específica: tutorial que não reproduz (curse of knowledge), voz que vira "4 empresas" ao traduzir, convenção que ninguém segue sem enforcement. Use quando pedirem para escrever/criar um tutorial, um manual de marca, um guia de tom de voz, um style guide de conteúdo, um guia de convenções de código ou um CONTRIBUTING.md.'
---

# gerador-de-manuais

Gera três artefatos de referência a partir de **template pronto** (não da memória): **tutorial**,
**manual de marca** (voz e tom) e **guia de convenções/contribuição**. Complementa o `documenter`
(que decide Diátaxis/ADR/changelog para `docs/`) — esta skill entra quando o pedido é por um desses
três artefatos **específicos**, geralmente como documento autônomo (não necessariamente em `docs/`).
Cada template existe porque um desses três **falha de um jeito conhecido** — a skill entrega a
estrutura que blinda essa falha, não um formato inventado.

## Quando usar
Gatilhos: "escreve um tutorial de X", "cria o manual de marca", "guia de tom de voz", "style guide de
conteúdo", "guia de convenções [de código/commit/contribuição]", "CONTRIBUTING.md". Se o pedido for
"documenta como X funciona" ou ADR/changelog/runbook, isso é `documenter` puro — não esta skill.

| Pedido | Template | Baseado em | Falha que blinda |
|--------|----------|-----------|------------------|
| Tutorial (aprender fazendo) | `assets/tutorial.md` | The Good Docs Project — Overview→Background→Before you begin→Steps→Summary→Next steps | passo que não reproduz; abandono no meio |
| Manual de marca / voz e tom | `assets/manual-de-marca.md` | Mailchimp Content Style Guide — voz constante × tom situacional | voz genérica; "4 empresas" ao traduzir; IA fora da voz |
| Guia de convenções / contribuição | `assets/guia-de-convencoes.md` | CONTRIBUTING best practices + The Good Docs Project | regra sem enforcement que ninguém segue |

## Passos
1. **Classifique o pedido** pela tabela. Ambíguo entre tutorial e how-to → pergunte (how-to é tarefa
   pontual pra quem já sabe; tutorial é aprendizado guiado do zero — mesmo critério Diátaxis do `documenter`).
2. **Copie o template** de `assets/` inteiro — não recrie a estrutura de cabeça; ele já encoda a ordem certa.
3. **Preencha com o real** (código/repo/decisões existentes: nome, convenções em uso, commits/PRs reais).
   Nunca invente traço de marca ou convenção que o projeto não tem — sem base, **pergunte** antes de inventar.
4. **Rode o checklist de Gotchas** abaixo e **proponha o plano** (o que cria, onde) antes de escrever — mesma
   disciplina do `documenter`.

## Casos reais (onde cada tipo quebra na prática)
- **Tutorial — curse of knowledge:** o autor é expert, então **omite os passos intermediários que são
  invisíveis pra ele** mas essenciais pro iniciante → confusão e abandono. O leitor abandona **no primeiro
  momento inesperado** (passo que não roda como descrito). Antídotos no template: testar cada passo num
  **ambiente limpo** (container/máquina nova, não a sua já-configurada), **fixar versões**, declarar o
  **resultado esperado por passo**, definir jargão no 1º uso, e reler com olho frio (ou testar com um
  iniciante real). Passo sem "resultado esperado" é onde o copy-paste vira cargo-cult e a pessoa trava.
- **Manual de marca — i18n e IA:** traduzir preserva o **significado**, não a **voz** — sem cuidado, a marca
  "vira 4 empresas" em 4 idiomas. O tom quebra na **microcopy**: um "Got it!" leve vira um "Confirmado" seco.
  O template pede **exemplos de calibração por idioma** e a **intenção emocional** de cada mensagem
  (tranquilizar/avisar/celebrar), não só a tradução literal. Para **conteúdo gerado por IA**: dê contexto
  (público/intenção/tom) + glossário + frases aprovadas, e meça a aderência — "não se mantém o que não se mede".
- **Guia de convenções — enforcement:** regra que depende de disciplina humana é **sistematicamente ignorada**
  ("human willpower is scarce; automation is reliable"). O que faz um guia ser seguido: **linter/formatter
  atrelado à regra** (roda no IDE **antes** do CI, menos disruptivo), **CODEOWNERS** distribuindo review,
  **template de PR** que torna a convenção visível no envio, e **motivo + link por regra** — sem isso, o dev
  contorna (`eslint-disable` espalhado) em vez de adotar. Regra que o linter não expressa fica pro review humano.

## Regras críticas (faça / não faça)
| Faça | Não faça |
|------|----------|
| **Tutorial:** testar cada passo num ambiente **limpo**, com versão fixada e resultado esperado | Escrever da máquina já-configurada, sem versão nem output — "funciona aqui" |
| **Tutorial:** ≤7 passos primários; definir jargão no 1º uso | Monólito de 15 passos "pra caber tudo"; assumir que o leitor já sabe |
| **Marca:** traço em par "X mas não Y" + 1 frase real; tom por contexto emocional | "Somos amigáveis" solto; um adjetivo como regra única |
| **Marca:** dar à tradução/IA a intenção emocional + glossário + exemplos de calibração por idioma | Traduzir literal e deixar a microcopy virar tom seco/genérico |
| **Convenções:** atrelar cada regra a um linter/formatter + motivo + link; usar CODEOWNERS/template de PR | Regra só em prosa, sem enforcement nem razão — vira letra morta |
| **Convenções:** cada convenção de código com snippet certo **e** errado lado a lado | Descrição em prosa sem exemplo; exemplo desatualizado que não compila |
| **Todos:** nomear um **dono** e a cadência de revisão do documento | Publicar e nunca mais tocar — o exemplo apodrece e mata a confiança |

## Gotchas
- **Voz é constante, tom é situacional** — o manual precisa de uma tabela "tom muda por contexto"
  (erro do usuário → empático; sucesso → celebrativo), não um adjetivo solto.
- **Do's/don'ts sem exemplo real não são seguidos** — cada regra do manual/guia precisa de ≥1 exemplo
  concreto (frase real, snippet real), não só a regra em prosa.
- **Exemplo desatualizado é pior que ausente** — snippet que não compila mais ou comando com flag inexistente
  corrói a confiança no guia inteiro (doc-rot); date/versione o volátil e nomeie quem mantém.
- **Enforcement mora fora do texto** — se o guia é sobre estilo de código, o valor real está no linter que o
  cobra automaticamente; o `.md` documenta o *porquê*, a máquina cobra o *o quê*.
- **Não confundir com `docs/` do `documenter`** — ADR/changelog/runbook em `docs/` são o `documenter` direto
  (Diátaxis/Nygard/Keep a Changelog); esta skill é para os três tipos da tabela, mesmo quando o destino é `docs/`.

## Se crescer
Surgindo um 4º tipo recorrente (ex.: guia de API pública, glossário), adicione um `assets/<tipo>.md` e uma
linha na tabela de Capacidade — mantenha este `SKILL.md` como **índice enxuto** (progressive disclosure: o
detalhe mora nos `assets/*.md`, não inline aqui).

## Referências
- The Good Docs Project — templates de tutorial/style guide/contributing guide: https://www.thegooddocsproject.dev/template
- Mailchimp Content Style Guide — voice and tone (voz constante × tom situacional): https://styleguide.mailchimp.com/voice-and-tone/
- Diátaxis — tutorial × how-to × reference × explanation (usado pelo `documenter`): https://diataxis.fr/
- Earthly — "The Curse of Knowledge in Technical Writing" (passo que não reproduz, jargão): https://earthly.dev/blog/curse-of-knowledge/
- "Predicting Abandonment in Online Coding Tutorials" (abandono no 1º passo que falha): https://arxiv.org/pdf/1707.04291
- Translated — "Consistent Brand Voice across 20 Languages" (voz × tradução, calibração por idioma): https://translated.com/resources/consistent-brand-voice-across-20-languages-framework
- Swarmia — "A complete guide to code reviews" (CODEOWNERS, CI, enforcement automatizado): https://www.swarmia.com/blog/a-complete-guide-to-code-reviews/
- Agoda Engineering — "How to Make Linting Rules Work: From Enforcement to Education" (regra precisa de motivo+link; dev contorna o punitivo): https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
