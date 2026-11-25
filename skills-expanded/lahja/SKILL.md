---
name: lahja
description: Arabic dialects (لهجة) writing skill - write or rewrite Arabic in a specific spoken dialect with correct dialect GRAMMAR, not just sample words. Covers negation, future and aspect markers, demonstratives, question words, spelling habits, MSA leaks to remove, and how English tech terms sit inside dialect text. Covers Levantine (Palestinian-anchored), Egyptian, Gulf, Iraqi, Maghrebi (Moroccan, Algerian, Tunisian), Libyan, Sudanese, and Yemeni. Use when the user asks to write "بالعامية", "باللهجة الفلسطينية/الشامية/المصرية/الخليجية/العراقية/المغربية/الليبية/السودانية/اليمنية", "in Levantine/Palestinian/Egyptian/Gulf/Khaleeji/Iraqi/Moroccan/Libyan/Sudanese/Yemeni Arabic or Darija", "make this sound less formal/less translated", "convert فصحى to عامية", or writes to you in a dialect and wants dialect output (social posts, chat/WhatsApp copy, casual product copy, scripts). Built on the fasih method by Maher El Gamil. Works standalone; if the separate fasih skill is also available, invoke it for editorial quality while lahja owns the dialect forms. Do NOT use for formal MSA writing, legal/government/medical text, literal translation, or when no dialect is wanted.
---

# lahja - write Arabic in a real dialect

> **Built on the fasih method.** lahja follows the approach of [fasih](https://github.com/maherelgamil/fasih-skill) by Maher El Gamil: write Arabic that sounds native rather than translated, adapt instead of rendering word for word, never invent a fact or a form, and keep the register consistent. fasih covers Arabic levels and tone and deliberately keeps dialect short; lahja is the dialect-grammar layer under that same method.

AI dialect text fails on **grammar**, not vocabulary: it swaps أريد for بدي but keeps سوف, لقد, أن + verb, and MSA negation, so it still reads as translated فصحى. This skill fixes the grammar layer. **Pick one dialect, load its guide, write through it.**

## Step 1 - Detect the dialect FIRST (ask at most one question)

In order, stop at the first that answers:
1. **Named in the request:** a dialect, country, or city ("فلسطيني", "Egyptian", "for a Kuwaiti audience").
2. **The user's own Arabic** is clearly in one dialect -> match it. "Clearly" = **at least two markers from one row below and none from another row**. Forms shared across dialects don't count, however dialect-y they feel. The verified overlaps:
   | Form | Shared by |
   |---|---|
   | رح + verb | Levantine **and** Iraqi |
   | شلون | Gulf **and** Iraqi |
   | هاي | Levantine **and** Iraqi |
   | قاعد + verb | Gulf, Iraqi, rural Levantine, Egyptian, Tunisian |
   | شنو | Gulf, Iraqi, Moroccan, Tunisian |
   | أكو / ماكو | Iraqi **and** Kuwaiti |
   | فين | Egyptian, Moroccan, Tunisian |
   | وين | Levantine, Gulf, Iraqi, Algerian, Tunisian |
   | إيش / آش | Levantine, Hejazi, Moroccan, Tunisian |
   | كمان | Levantine **and** Egyptian |
   | شو | Levantine **and** Emirati |
   | ده / دي | Egyptian **and** Sudanese |
   | دا | Iraqi (progressive) **and** Sudanese (demonstrative) |
   | أبي / يبي | Gulf, Libyan, Yafi'i Yemeni |
   | ماش / ماشي | Yemeni (negator) **and** Maghrebi (negator or future) |
   | قداش | Maghrebi **and** Libyan |
   | غدوة | Yemeni **and** Libyan |
   | مش، بس، اللي، ما في، كتير، عشان، ليش، اكتبلي | most dialects |

   **One marker alone is never enough: ask.** Markers that do point to one dialect:

   | Dialect | Markers |
   |---|---|
   | Levantine | بدّي، هلأ / هلق، عم + verb، هيك، إشي، منيح |
   | Egyptian | إيه، عايز، دلوقتي، هـ future (هروح)، إزاي، بتاع، أوي، برضه |
   | Gulf | وش، الحين، أبغى، وايد، مب، ـج "you" suffix (شلونج) |
   | Iraqi | آني، هسّه / هسّة، شگد، شوكت، چان، گال، شكو، كلش، هواية، أكو |
   | Maghrebi | كنكتب، غادي، دابا / توّة، بزاف / برشا، ماكاينش / ماكاش / مافمّاش، كيفاش، ديال، نكتب meaning "I write" (only counts with clear 1sg context) |
   | Libyan | شن، توّا، هلبا، نتاع، باهي، هكي، احني، برّا |
   | Sudanese | ديل، ياتو، متين، هسع، داير، زول، كدي |
   | Yemeni | ذلحين، أشتي، مابش، للمه، محّد، قوّيت، ـش as "your" for a woman (حالش) |
3. **Audience or brand market** is stated (a Saudi app, a Cairo campaign).
4. Otherwise ask ONE question: "أي لهجة؟ شامية/فلسطينية، مصرية، خليجية، ولا غيرها؟" Do not guess, and do not default to a blend.

## Step 2 - Load the matching guide

| Dialect | Anchor | Reference |
|---|---|---|
| **Levantine** | urban Palestinian, with Jordanian, Syrian, Lebanese notes | `references/levantine.md` |
| **Egyptian** | Cairene | `references/egyptian.md` |
| **Gulf** | Kuwaiti, with Emirati, Najdi, Hejazi columns | `references/gulf.md` |
| **Iraqi** | Baghdadi gilit, with southern and Mosuli notes | `references/iraqi.md` |
| **Maghrebi** | Moroccan, with Algerian and Tunisian columns | `references/maghrebi.md` |
| **Libyan** | Tripoli / western, with Benghazi notes | `references/libyan.md` |
| **Sudanese** | Khartoum | `references/sudanese.md` |
| **Yemeni** | Sanaani, with Adeni, Hadhrami, Tihami notes | `references/yemeni.md` |

Every guide covers the same ground: negation, future, aspect, demonstratives and question words, pronouns, spelling habits, MSA leaks, English (or French) tech terms, worked rewrites, and sources. Each one also marks what it deliberately does **not** cover, either inline ("not sourced", "not verified") or in a closing section. Treat anything so marked as banned, not as a hint.

**Maghrebi, Iraqi, Gulf, Libyan, and Yemeni need a country or city too**, because the sub-dialects genuinely conflict:
- Maghrebi: Moroccan غادي = "will", Tunisian غادي = "there".
- Iraqi: Baghdadi uses ما, southern Iraqi uses ما...ش.
- Gulf: the negator splits inside a single country (Emirati مب in the north, مش in Abu Dhabi, ما on the East Coast), and Saudi splits into Najdi (Riyadh) and Hejazi (Jeddah), which are not interchangeable.
- Libyan: Tripoli and Benghazi differ on the ـش suffix and on everyday words (هلبا vs واجد).
- Yemeni: Sanaani, Ta'izzi-Adeni, Hadhrami, and Yafi'i differ on the future marker, on "want", and even on how the past tense is marked.

Use the country or city the user named. If they didn't name one and the text needs a form that splits, ask; otherwise use the guide's anchor and say which you used.

**A dialect with no guide here** (Omani, Chadian, Hassaniya, and the rest): say lahja has no guide for it, deliver your best attempt without asking again, and label it "unverified - no lahja guide for this dialect" outside the text. If the user only hinted at it, ask first.

## Rules that hold in every dialect

- **One dialect per text.** Never mix هلأ with دلوقتي or الحين in the same piece. Within Levantine, don't switch sub-dialect mid-text (عم vs قاعد, هلأ vs هلّق) unless the guide says the forms coexist.
- **Grammar before vocabulary.** Run the guide's MSA-leak list on every draft. One leftover سوف / لقد / ليس / لم / الذي undoes the whole text.
- **Kill translated-MSA patterns too:** a helper verb + verbal noun (قمنا بإطلاق، تم إطلاق) becomes the plain verb (أطلقنا), and descriptor nouns before a tech term go (بيئة الـ staging -> الـ staging). If fasih is loaded, its own `references/rewrite-patterns.md` goes deeper on this (that file is in the fasih skill, not in lahja).
- **Adapt, don't translate.** Rebuild the sentence the way a speaker would say it: shorter clauses, dialect word order, dialect connectors. Don't map MSA word by word.
- **Don't caricature.** Natural dialect is mostly neutral everyday words plus the right grammar. Stacking slang and idioms reads as a parody.
- **Informal spelling, applied consistently.** No tanween and no short-vowel marks (فتحة، ضمة، كسرة). Shadda is optional; use it where it helps reading (نبلّش، شغّال), and be consistent. Pick one spelling per word (هلأ or هلق) and keep it for the whole text.
- **Keep fixed items fixed:** names, numbers, links, code, product names, quoted text.
- **Tech terms follow the guide's English section.** Commands, product names, and code stay in Latin script. Don't invent Arabic coinages the audience doesn't use.
- **Register still matters inside dialect.** A support reply and a meme post are both dialect but not the same tone. Match the channel.

## With fasih (optional companion)

**lahja is standalone and complete without fasih**, even though it is built on fasih's method (see the note at the top). fasih itself is a separate skill, installed separately.

**How to invoke it:** if your available-skills list has an entry named `fasih` (or namespaced, `<plugin>:fasih`), invoke it with the Skill tool (`Skill(fasih)`) **before writing**, and write through both. If nothing matches, or two entries do, use lahja alone and don't mention fasih unless the user asks. Don't go hunting on disk to find out whether fasih exists, and don't install it. Once it **is** loaded, following its own pointers into its `references/*.md` is expected.

**When:** invoke it for copywriting, UX and product copy, microcopy, marketing text, and editing an existing text. Skip it for a one-line chat reply or a quick mechanical rewrite, where lahja alone is enough.

**Division of labour:** fasih owns meaning preservation, structure, filler removal, and not inventing facts. lahja owns every Arabic surface form: grammar, vocabulary, spelling, **and the register inside the dialect**.

- **fasih's own examples are MSA.** Its microcopy patterns (حاول مرة أخرى، تعذّر حفظ التغييرات، جارٍ) are structural templates, never strings to paste. Rewrite every surface word through the dialect guide.
- **fasih's tone table has no Levantine row** (فصحى رسمية، فصحى حديثة، عربية بيضاء، مصرية، خليجية أو محلية), so don't let Palestinian, Jordanian, Syrian, or Lebanese get filed under «خليجية أو محلية». The lahja guide governs the dialect.
- On any Arabic wording, lahja wins. On meaning, facts, and honesty, fasih wins.

## Before you deliver

Run the guide's leak list over your draft. If you can run shell commands and this skill is on disk, that check is scripted:

```bash
python3 scripts/check_output.py <dialect> draft.txt     # or: ... <dialect> -   to read stdin
```

It reads the guides live and flags three things: MSA leaks from that dialect's own table, forms that belong to a **different** dialect (the mixing that makes text read as no dialect at all), and tanween or short vowels. It flags candidates, you decide. If you can't run it, do the same pass by eye.

`scripts/check_skill.py` is a different tool: it checks the guide files themselves, for whoever edits this skill. It does not look at your output.

## Feedback and contributions

Arabic dialects vary by city, generation, and family, so a guide here can be thin or wrong for a given speaker. If the output was off, or a dialect you speak is missing or mishandled, tell Majd: **majd.ghithan20@gmail.com**, or open an issue or PR at **https://github.com/majdghithan/agent-skills**. Concrete corrections (the form, the region, and where it is used) are the most useful thing you can send.

## Output expectations

- Deliver the text in the requested format, with no change report unless asked.
- The one-question budget in Step 1 is for the **dialect only**. A missing topic, audience, or fact is a separate question, and asking it doesn't spend that budget.
- Name the dialect and sub-dialect you used in one short line, outside the deliverable (never inside copy the user might paste): "Palestinian (urban)", "Tunisian, not Moroccan".
- If the request needed a form the guide marks as not sourced, say which nuance you couldn't cover instead of inventing a form.
- If the source text is formal/legal/medical and the user still wants dialect, keep every fact and qualifier intact, and say what register you chose.
