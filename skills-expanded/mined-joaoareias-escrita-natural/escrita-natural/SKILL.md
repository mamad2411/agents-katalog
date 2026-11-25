---
name: escrita-natural
description: >-
  Apply whenever you write or edit Portuguese prose — articles, blog/social content, emails, chat messages, reports, academic writing, marketing copy, narratives — or adapt/translate English into Portuguese. It fixes two things that make Portuguese feel artificial. First, "translationese": the English-shaped accent from mapping word-by-word instead of rewriting from meaning — false cognates, calqued connectors, passive and pronoun overuse, flat vocabulary. Second, "AI speech": the chatbot register — significance inflation, gerund-tail padding, AI vocabulary, rule of three, sycophancy, signposting, upbeat closers. Use it even when the user never says "translationese" or "make it natural"; if the deliverable is Portuguese meant to sound human, this applies (including asks like "tá com cara de IA" or "deixa mais natural"). Skip only for code or purely technical text where literal fidelity beats fluency. Default to Brazilian Portuguese unless told otherwise.
---

# Escrita natural em português

Two things make Portuguese writing feel artificial, and they stack:

- **Translationese** — the text reads as *translated*. An English (or other) sentence was formed first and rendered into Portuguese token by token, so the source language's skeleton shows through. Rarely ungrammatical — just lifeless and faintly foreign.
- **AI speech** — the text reads as *written by a chatbot*. Inflated significance, fake depth, hedging, sycophancy, upbeat filler. It can be perfect native Portuguese and still announce that no human wrote it.

For an LLM, both are the default pull. The model reasons in an English-dominant space (→ translationese) and was tuned to sound like a helpful assistant (→ AI speech). This skill interrupts both. The method below kills translationese at the source; the audit at the end catches what's left of either.

## The core move: deverbalize, then reformulate

The single most important idea here, from the Interpretive Theory of Translation (ESIT). When you write Portuguese, do **not** translate a sentence you've already formed in English. Instead:

1. **Deverbalize.** Hold only the *meaning, intent, and the effect you want on the reader* — stripped of any specific words. Let the source wording fall away completely.
2. **Reformulate from zero.** Ask: *how would a Brazilian, writing this from scratch for this audience, actually say it?* Write that. Aim for **equivalence of effect**, not equivalence of words.

Two fast tests for any sentence you doubt:
- **Read it aloud.** If it sounds like film dubbing, rewrite it.
- **"Would a native write this unprompted?"** Not "is it grammatical?" but "would a real Brazilian, with no English in front of them, have produced this?" If no, it's translationese.

The point is never to drift from the meaning — it's to carry the meaning across *without* dragging the source language's bones along.

## Match the register — and keep a pulse

Translationese and AI speech both pull toward stiff, over-correct, statistically-average prose. Resist in two directions at once: write in the register the context actually calls for, **and** don't sand the writing down to something voiceless.

| Context | Register |
| :-- | :-- |
| Blog / content / tech writing | Polished but energetic, the register of mainstream Brazilian tech journalism (think TecMundo/Voxel). Clean, medium-length sentences with real flair in word choice (*começa quente*, *uma enxurrada de novidades*), light reader address and the occasional rhetorical aside (*Quem diria, não?*), English tech/game terms kept as-is. Have a point of view, but write it as engaging journalism, not as loose spoken text (avoid *tava, te salva, modinha* and other text-message syntax). |
| Slack / WhatsApp / chat | Casual, direct, lean. Drop ceremony. Imperatives are fine. |
| Email / professional | Cordial but human. Polite ≠ stiff; an internal email rarely needs "Prezado(a) Senhor(a)." |
| Academic / master's | Precise and formal — but still native. Formality is rigor and clarity, not archaic constructions or passive-voice fog. |

**Voiceless is its own tell.** Removing AI-isms is only half the job; flat, opinion-free, even-cadence prose reads as machine-made too. For content and opinion, let a real perspective and varied rhythm show. **But calibrate:** for academic, technical, legal, or reference text, neutral and plain *is* the correct human voice — don't inject fake opinions or first person into a thesis.

---

# Part 1 — Translationese: don't sound translated

The five recurring tells. Feel them, don't just match them — each has a *why*, and the why is what catches cases the examples don't cover. Full example tables and the complete false-cognate dictionary live in `references/translationese-pt.md`; read it when you want depth or the user asks for a thorough edit.

### 1. Explicitação — over-explaining
Spelling out what Portuguese leaves implicit: extra connectors, resolving ambiguity nobody needed resolved, naming cause where coordination would do. Result: padded, denser text. Native Portuguese trusts the reader.
- *Como consequência direta disso, as receitas caíram.* → *...e as receitas caíram.*
- *O cliente que nós visitamos ontem...* → *O cliente que visitamos ontem...*

### 2. Simplificação — flattened vocabulary
Reaching for the safe, generic, high-frequency word and pruning the specific one. The specific word carries image and energy; the generic one leaks both. (This is also where text starts to smell "AI-generated.")
- *Ele entrou e sentou no sofá.* → *Ele entrou arrastando os pés e se jogou no sofá.*
- *Cortar as plantas.* → *Podar os arbustos.*

### 3. Normalização — erased voice
Sanding off slang, neologisms, expressive punctuation, orality, regional flavor into a sterile, hyper-correct register nobody uses in that situation. How a bold brand ends up sounding like a government memo.
- *Conceda-me um instante.* → *Me dá um segundo.*

### 4. Interferência — the source language bleeding through
**The biggest one for an LLM.** Source morphology and syntax leak in: false cognates, calques, passive abuse, possessive and subject-pronoun overuse, English word order. This is the most *detectable* marker — it reads as foreign or as an outright error.
- *Eu finalmente realizei que estava errado.* → *Finalmente percebi que estava errado.*
- *Foi dito que as regras mudariam.* → *Disseram que as regras iam mudar.*
- *Ele levantou a sua mão.* → *Ele levantou a mão.*
- *Eu acho que eu vou sair.* → *Acho que vou sair.*

### 5. Nivelamento — everything in the same register
All voices collapsing to the statistical middle: in dialogue, a street kid and a judge speak identical neutral Portuguese; across a piece, every paragraph has the same flat texture. Give distinct speakers distinct registers; let intensity vary.

### Quick sweep: translationese fingerprints
- **False cognates** (trap → what you usually mean): *realizar* → **perceber/notar**; *eventualmente* → **no fim/acabar + gerúndio** (*eventualmente* = occasionally); *atualmente* is fine for "currently" but "actually" → **na verdade** (never *correntemente*); *ultimamente* = lately, "ultimately" → **no fim das contas**; *suportar* → for software **ser compatível com/ter suporte a**; *endereçar (um problema)* → **abordar/tratar de**; *aplicar (a uma vaga)* → **candidatar-se**; *pretender* = to intend, "pretend" → **fingir**. Full list in the reference.
- **Calqued connectors — a density problem, not banned words.** *Além disso, No entanto, Por outro lado, Em suma, Vale ressaltar que* are legitimate; the tell is opening paragraph after paragraph with them in a mechanical essay rhythm. Cut most, vary the rest, let coordination carry the logic. Watch literal idioms: *no final do dia* (at the end of the day), *em uma base diária* → **diariamente**.
- **Dropped subjects:** PT verbs carry the person. *eu/você/ele* repeated → drop unless needed for contrast.
- **Possessives** on body parts and obvious owners: *escove os seus dentes* → **escove os dentes**.
- **Passive** where active or *se* is natural: *o bug foi corrigido* → **corrigimos o bug** (keep passive only when the agent is genuinely unknown).
- **Gerundismo:** *vou estar verificando* → **vou verificar**.
- **English title-case** in headings → Portuguese sentence case.
- **Opener calques:** *Aqui está…, Vamos mergulhar…, Neste artigo vamos explorar…* — start where a Brazilian writer would start.

---

# Part 2 — AI speech: don't sound like a chatbot

These are language-agnostic chatbot habits, rendered for Portuguese. The fuller catalog (adapted from Wikipedia's "Signs of AI writing") is in `references/ai-speech-pt.md`. The seven clusters below cover most of it.

### A. Inflar importância (significance inflation, promo, aphorisms)
Puffing up arbitrary things with significance, legacy, and "broader trends," or dressing an ordinary claim as an aphorism.
**Watch:** *em um cenário em constante evolução, desempenha um papel crucial/fundamental, representa um marco, um divisor de águas, deixou uma marca indelével, X é a linguagem/moeda de Y; vibrante, rico em (figurative), de tirar o fôlego, imperdível, renomado, aninhado no coração de.*
- *Em um cenário tecnológico em constante evolução, os testes automatizados desempenham um papel crucial.* → *Teste automatizado avisa na hora quando algo quebra, em vez de três semanas depois em produção.*

### B. Profundidade falsa com gerúndio (the -ing tail)
Tacking gerund phrases onto a sentence to fake depth. In PT this is the *...garantindo... fomentando... refletindo... destacando...* tail.
- *A empresa adotou métodos ágeis, garantindo mais eficiência e refletindo seu compromisso com a inovação.* → *A empresa adotou métodos ágeis. As entregas ficaram mais frequentes.*

### C. Vocabulário de IA
Words that spike in post-2023 text and cluster together.
**Watch:** *crucial, fundamental, essencial, robusto, abrangente, aprimorar, ressaltar, destacar (verb), panorama, cenário, intrincado, mergulhar, desvendar, alavancar, fomentar, elevar (a um novo patamar), tapeçaria/mosaico (figurative).* Prefer the plain word.
- *Esta solução robusta e abrangente vai aprimorar seus processos e elevar a experiência a um novo patamar.* → *A ferramenta cobre o fluxo todo e deixa o app mais rápido.*

### D. Rodeios, regra de três, variação mecânica
- **Evitar "ser":** *serve como / configura-se como / representa / constitui* → often just **é**. (*O relatório serve como base.* → *O relatório é a base.*)
- **Regra de três:** forcing ideas into triplets to sound complete. *Oferece teoria, prática e networking.* → *Mistura teoria e prática, com tempo pra trocar ideia.*
- **Variação elegante:** PT does value not repeating a word — but robotic synonym-cycling (*o protagonista / o personagem / a figura central / o herói* across four sentences) is a tell. Repeat the plain noun or restructure.
- **Falsas escalas:** *de X a Y* where X and Y aren't on a scale.

### E. Frases de efeito fabricadas e paralelismos negativos
- **Paralelismo negativo:** *não é apenas X, é Y / não se trata só de X, mas de Y.* → state what it is. (*Não é só uma ferramenta, é uma filosofia.* → *É uma ferramenta.* — and if it's truly a philosophy, say which.)
- **Punchline fabricado / staccato:** a run of short fragments to manufacture drama. *Aí tudo mudou. Sem aviso. Sem volta. Nada como antes.* → *Aí tudo mudou, sem aviso e sem volta.* (One short sentence for emphasis is fine; a stack of them is engineered.)
- **Falsa autoridade:** *a verdadeira questão é, no fundo, na realidade, o que realmente importa, fundamentalmente, o cerne da questão* — usually ceremony before an ordinary point. Cut it.

### F. Resíduo de chatbot
The dead giveaway that assistant text got pasted as content.
**Watch:** *Ótima pergunta!, Claro!, Com certeza!, Você tem toda razão!, Espero que ajude!, Aqui está um resumo…, Quer que eu detalhe?, Posso continuar?; Até a minha última atualização…, com base nas informações disponíveis, mantém um perfil discreto; poderia possivelmente talvez; O futuro é promissor, tempos empolgantes estão por vir, um passo na direção certa.*
- Cut chatbot framing, cutoff disclaimers, sycophancy, and generic upbeat conclusions entirely. End on a concrete fact or just stop. *É possível que* beats *poderia possivelmente ser argumentado que talvez.*

### G. Formatação delatora
- **Title-case heading** → sentence case (*Como Aumentar Suas Vendas* → *Como aumentar suas vendas*).
- **Bold mecânico** scattered through prose → drop it; let the sentence carry emphasis.
- **Listas com cabeçalho em negrito + dois-pontos** (*- **Performance:** ...*) → fold into prose or use plain bullets.
- **Emojis** decorating headings/bullets → remove.
- **Travessão / em dash (—):** drop it. It's rare enough in everyday Portuguese that it reads as an AI tell, so replace each one with a comma, a period, a colon, or parentheses (in roughly that order of preference), or restructure the sentence. The only exception is dialogue in fiction, where the travessão is the correct convention (*— Vamos? — perguntou ela.*).

---

# Before you finalize: the audit

A quick draft → audit → fix loop, adapted from the humanizer:

1. Write the draft using the deverbalize → reformulate method.
2. Ask yourself two questions and answer honestly: **"Would a Brazilian write this unprompted?"** (translationese) and **"Does this sound like a person or like a chatbot?"** (AI speech). Name the specific tells you still see.
3. Fix those, then re-read aloud once more.

When rewriting existing text on request, deliver the rewrite and, if useful, a short note on what you changed — not a lecture.

# Guardrails — don't overcorrect

Naturalness is the target, not slang density, not hypercorrection, and not paranoia about every stylistic choice.

- **Keep consagrated loanwords in tech and professional contexts.** *deploy, commit, branch, merge, build, pipeline, design, feature, bug, review, deadline* are the natural words in dev/data work. *Implantação* for "deploy" or *ramo* for "branch" is itself unnatural. (Context matters: *push* stays *push* in Git, but a *push* on a door is **empurrar**.)
- **Don't manufacture regionalisms.** Don't stuff in *mano, tipo assim, sacou* to prove a point. A neutral-but-native sentence beats forced gíria.
- **Literal can be correct.** For technical specs, legal text, code, API docs, or anything where fidelity outranks fluency, a closer rendering is the right call.
- **Don't sacrifice meaning for flavor.** Equivalence of *effect* never means changing what's being said.
- **Isolated patterns aren't proof.** Polish ≠ AI: many people write clean, edited prose. One *No entanto*, one formal word, a salutation, or a single short emphatic sentence is not a tell. Mixed casual-and-formal register is often just a real person in a technical field, not a chatbot. Look for *clusters*, not isolated hits.
- **Preserve the human signals.** Specific, hard-to-fabricate detail; mixed feelings and unresolved tension; choices the writer could defend; varied sentence length; genuine asides. When you see these, lean toward leaving the prose alone — over-editing destroys exactly what makes it sound human.

# Worked example

A draft that's both translated *and* AI-slop, announcing a feature launch.

**Before:** *Nós estamos extremamente empolgados em anunciar que a nossa nova funcionalidade de colaboração está disponível. Projetada para revolucionar o trabalho em equipe, representa um marco em nossa jornada rumo à excelência.*

Tells (translationese): *Nós* + *a nossa* — pronoun and possessive overuse; *funcionalidade* stiff for *recurso*. Tells (AI speech): *extremamente empolgados, revolucionar, marco em nossa jornada rumo à excelência* — significance inflation.

**After:** *Chegou o novo recurso de colaboração. Agora dá pra trabalhar junto no mesmo lugar, sem trocar arquivo por email. Testa lá.*

Same message, no English skeleton, no inflation.
