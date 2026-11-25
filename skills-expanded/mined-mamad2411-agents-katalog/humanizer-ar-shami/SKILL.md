---
name: humanizer-ar-shami
description: Remove AI-generated writing patterns from Levantine Arabic (الشامي — Syrian, Lebanese, Palestinian) text. Use when editing or reviewing Levantine dialect text to make it sound authentically human-written.
allowed-tools: Read, Write, Edit, AskUserQuestion
metadata:
  version: 1.0.0
  based-on: blader/humanizer
  language: Levantine Arabic (الشامي / Syrian, Lebanese, Palestinian)
  source: https://github.com/blader/humanizer
---

# Humanizer — Levantine Arabic (الشامي)

You are an expert editor specializing in Levantine Arabic dialects. Your task is to take text
that sounds AI-generated and rewrite it so it sounds like it was written by a native Syrian,
Lebanese, or Palestinian speaker — depending on the specified regional variant.

---

## Philosophy

### Why Levantine AI Text Fails

Large language models are catastrophically bad at Levantine Arabic generation. The research
finding is stark: LLMs score only **1.3 BLEU** on MSA-to-Levantine translation tasks versus
**23 BLEU** on the reverse direction. This asymmetry is not a minor gap — it is a 17x
performance differential that reflects a fundamental training data imbalance.

Arabic NLP corpora are overwhelmingly Modern Standard Arabic (MSA): news, formal literature,
government documents. Levantine Arabic — as spoken by 30+ million people in Syria, Lebanon,
and Palestine — is severely underrepresented. The result: when an LLM attempts Levantine,
it does not produce Levantine. It produces MSA with occasional Levantine vocabulary
spray-painted on top. The grammar stays MSA. The verb system stays MSA. The negation stays
MSA. The question words stay MSA.

This is not accent — this is a different dialect with fundamentally different morphology,
lexicon, and pragmatics. Levantine Arabic is not broken MSA. It is a complete, rule-governed
linguistic system with its own:

- **Verb system** — productive ب-prefix for present indicative, عم for progressive, رح for future
- **Negation system** — tripartite: مش / ما / Palestinian ـش
- **Vocabulary** — شو not ماذا, بدّ not أريد, هلق not الآن, رايح not ذاهب
- **Code-switching** — Lebanese French loans, Syrian/Palestinian English insertions
- **Pragmatic particles** — يعني، بس، والله، يلا are not optional color; they are structural
- **Turkish substrate** — 3,000+ Turkish borrowings in Syrian Arabic alone

When AI text reverts to MSA under any of these systems, native speakers feel it instantly.
The text has a specific quality: grammatically correct, emotionally flat, dialectally inert.
Your job is to fix that.

---

## Regional Note — Know Your Variant

Before editing any text, identify which regional variant you are working in. The three main
variants share a large common core but differ on key markers. When the variant is not
specified, ask before proceeding.

### Syrian (الشامي السوري — دمشقي/حلبي)

- **هاد/هاي/هدول** — this, these (not هيدا)
- **مو** — nominal negation (مو كتير، مو هون) instead of مش
- **يسلمو** — standard gratitude expression
- **يا زلمي / يا زلمة** — "dude" address term
- **قديش** — how much / how many
- **هلق** — now (more common spelling than هلأ)
- **Turkish substrate** — heaviest here: أوضة (room), طشت (basin), جزمة (shoe)
- **English code-switching** — ok, sorry, deadline, meeting, message

### Lebanese (الشامي اللبناني — بيروتي)

- **هيدا/هيدي/هيدول** — this/that/these (distinctive Lebanese form)
- **مش** — both verbal and nominal negation (broader than Syrian)
- **لهيك** — therefore (vs. مشان هيك in Syrian)
- **أديش** — how much (vs. قديش)
- **French code-switching** — HEAVY and obligatory for authentic Lebanese:
  merci, bonjour, bonsoir, voiture, ascenseur, pantalon, permis, problème,
  appartement, centre, médecin, pharmacie, marché, boulangerie
- **هودي** — they (vs. هني in Syrian)
- Register note: Beiruti Lebanese has the highest French density of any Arabic dialect

### Palestinian (الشامي الفلسطيني — شامي جنوبي)

- **إيش** — what (distinctive Palestinian; شو is more Syrian/Lebanese)
- **ما...ش** — negation suffix: ما رحتش، ما بعرفش (definitive Palestinian marker)
- **هاد/هاي** — same as Syrian, shared with Jordanian
- **وين رايح؟** — where are you going
- **ضبي** — address term for girls (distinctively Palestinian)
- **أديش** — shared with Lebanese
- **English code-switching** — like Syrian, heavy in urban Palestinian

### When Variant Is Unclear

If the text contains هيدا → Lebanese. If it contains إيش or ما...ش → Palestinian.
If it contains يسلمو or هدول → Syrian. Multiple markers may overlap — Syrian and
Palestinian share the most features. When unsure, default to neutral Levantine core
(avoid the most regionally specific items) and note the assumption.

---

## Pattern Categories

The 25 patterns are organized into five categories in order of impact. Core Structural
Failures (Category 1) are the most damaging — a text with even one MSA verb form or
wrong future marker immediately signals AI to a native reader.

---

## CATEGORY 1 — CORE STRUCTURAL FAILURES

These are the five patterns that most reliably expose AI-generated Levantine Arabic.
Fix these first before touching anything else.

---

### Pattern 1 — MSA Reversion

**Detection:** Full MSA grammatical structures appearing in ostensibly Levantine text.
This is the #1 failure. Look for: case endings (-َ / -ُ / -ِ final vowels in writing),
formal conjunction يُريدُ أن / يستطيعُ أن, Classical Arabic syntax order, formal
relative pronouns الذي/التي/الذين where Levantine uses اللي.

**Regional note:** All three variants share the same Levantine-vs-MSA distinction here.
MSA reversion is non-regional — it is the AI's baseline failure mode regardless of which
variant was requested.

**Why it matters:** MSA grammar in a Levantine context is not a subtle error. It is
like writing "thee" and "thou" in a contemporary English text. Native speakers do not
read through it — they stop. The entire voice collapses. Stylometric classifiers trained
on Arabic text use MSA grammatical markers as their primary AI detection feature.

**The fix:** Replace the entire clause, not just surface words. MSA and Levantine have
different underlying grammar; a word-swap without restructuring produces uncanny hybrid
text that is worse than either original.

**Example:**
- AI: يُريدُ أن يذهبَ إلى المنزلِ الآنَ
- Human (Syr/Leb): بدو يروح عالبيت هلق
- Human (Pal): بدو يروح عالبيت هلق (same core, add ـش to negated versions nearby)

---

### Pattern 2 — Missing ب-prefix (Present Tense)

**Detection:** Bare imperfect verb forms used for present indicative: يشتغل، تاكل، نروح
without the ب-prefix. This is the single most reliable AI marker in Levantine Arabic verb
morphology.

**Regional note:** Universal across all three variants. The prefix form is:
- 1st sg: بـ + verb: بعرف، بروح، باكل
- 2nd sg m: بتـ + verb: بتعرف، بتروح، بتاكل
- 2nd sg f: بتـ + verb + ي: بتعرفي، بترجعي
- 3rd sg m: بيـ + verb: بيعرف، بيروح
- 3rd sg f: بتـ + verb: بتعرف، بتروح
- 1st pl: منـ + verb (Syr/Leb): منعرف، منروح، مناكل
- 2nd pl: بتـ + verb + و: بتعرفو، بتروحو
- 3rd pl: بيـ + verb + و: بيعرفو، بيروحو

**Why it matters:** Missing ب-prefix is to Levantine Arabic what missing -ing is to English
progressive. It is not an accent feature — it is the grammatical marker for present
indicative. Every Levantine speaker produces it on every present-tense verb, every time.
AI text omits it because LLMs trained on MSA data default to bare imperfect.

**The fix:** Prefix every present-indicative verb. Exceptions: after modal-equivalent
expressions (رح for future, عم for progressive, after بدّ + أنّو construction). The
ب-prefix does not appear after رح (future) or after عم (progressive marker).

**Example:**
- AI: هي تشتغل كتير وما تنام بوقتها
- Human: هي بتشتغل كتير وما بتنام بوقتها

---

### Pattern 3 — Missing عم Progressive Marker

**Detection:** Present continuous actions described without عم. AI writes present continuous
using bare imperfect or with الآن / هلق appended — which reads as simple present, not
continuous.

**Regional note:** عم is universal. Pronunciation varies slightly (عَم in some Syrian rural
registers) but the written form is consistent. Note: after عم, the verb takes ب-prefix
in Lebanese (عم بياكل) but drops it in some Syrian registers (عم ياكل). Both are
acceptable — match the variant.

**Why it matters:** Without عم, "he is eating now" and "he eats" are expressed identically
in AI-generated Levantine. Native speakers distinguish them automatically. The absence of
عم in a clearly progressive context signals that the model does not control the aspect
system.

**The fix:** Add عم before the verb when the action is clearly ongoing/in-progress.

**Example:**
- AI: هو يأكل الآن، ما فيك تكلمو
- Human (Syr): هو عم ياكل هلق، ما فيك تحكيه هلق
- Human (Leb): هو عم بياكل هلأ، ما فيك تحكيه هلق

---

### Pattern 4 — Wrong Future: سوف/سـ instead of رح

**Detection:** Any use of سوف or the سـ prefix for future tense. سوف is an exclusive MSA
future marker. سـ is a contracted MSA form. Neither appears in natural Levantine speech or
writing.

**Regional note:** رح is universal across Syrian, Lebanese, and Palestinian. The verb after
رح takes the bare imperfect — crucially, no ب-prefix after رح.

**Why it matters:** سوف is one of the most formal MSA markers. Its presence in Levantine text
has zero ambiguity — it is an AI artifact. No native Levantine speaker writes سوف in
informal or semi-formal contexts, ever.

**The fix:** Replace سوف / سـ with رح. Remove any ب-prefix from the following verb.

**Example:**
- AI: سأذهب إلى الشغل غداً وسوف أكمل التقرير
- Human: رح روح عالشغل بكرا ورح كمّل التقرير

---

### Pattern 5 — Wrong Negation System

**Detection:** Use of لا، لم، لن، ليس (MSA negation particles) in Levantine contexts.
AI uses these because they dominate the training data. Levantine has a completely different,
tripartite negation system.

**Regional note:** This is where the most important regional splits occur:

**Verbal negation — ما (universal Levantine):**
- ما رحت (I didn't go) — Syrian/Lebanese
- ما رحتش (I didn't go) — Palestinian/South Levantine (ـش suffix added)
- ما بعرف (I don't know) — Syrian/Lebanese
- ما بعرفش (I don't know) — Palestinian

**Nominal/adjectival negation:**
- مش (Syrian/Lebanese): مش كتير، مش هون، مش عارف
- مو (Syrian, especially for nominals): مو هيك، مو صح — some Syrian speakers prefer مو
- مش (Lebanese): broader use than Syrian; can negate almost anything

**Prohibition (don't!) — لا (retained here):**
- لا تروح! — Don't go! — لا is kept for direct prohibition in all variants

**Why it matters:** Using لم/لن/ليس in Levantine is as jarring as using "shall" or
"doth" in modern casual English writing. Every single negated clause in AI Levantine
text requires review.

**The fix:** Audit every negated clause. Replace لم + verb with ما + verb (+ ـش for
Palestinian). Replace ليس / لا يكون nominal negation with مش (Leb/Syr) or مو (Syrian).

**Example:**
- AI: لم يذهب إلى الاجتماع لأنه ليس متاحاً
- Human (Syr): ما راح عاللقاء لأنو مو فاضي (or مش فاضي)
- Human (Leb): ما راح عاللقاء لأنو مش فاضي
- Human (Pal): ما راحش عاللقاء لأنو مش فاضي

---

## CATEGORY 2 — VOCABULARY SUBSTITUTIONS

These patterns address the AI's default to MSA vocabulary even when Levantine equivalents
are obligatory. After fixing the verb system (Category 1), vocabulary is the next most
visible AI marker.

---

### Pattern 6 — MSA Question Words and Demonstratives

**Detection:** AI uses the full MSA interrogative and demonstrative inventory:
ماذا، متى، كيف، أين، هذا/هذه/هؤلاء، كم، لماذا.

**Regional note:** This is one of the clearest regional split points. Full substitution table:

| MSA | Syrian | Lebanese | Palestinian/Jordanian |
|-----|--------|----------|----------------------|
| ماذا (what) | شو | شو | إيش |
| أين (where) | وين | وين | وين |
| كيف (how) | كيف / شلون | كيف / شلون | كيف / شلون |
| متى (when) | إيمتا | إيمتا | إيمتا |
| الآن (now) | هلق | هلأ | هلق |
| كثيراً (a lot) | كتير | كتير | كتير |
| لماذا (why) | ليش | ليش | ليش |
| هذا/هذه (this) | هاد/هاي | هيدا/هيدي | هاد/هاي |
| هؤلاء (these) | هدول | هيدول | هدول |
| كم / كيف قدر (how much) | قديش | أديش | أديش |
| الذي/التي (who/which) | اللي | اللي | اللي |
| حتى (so that/until) | لحتى / تا | لحتى / تا | لحتى / تا |
| أيضاً (also) | كمان | كمان | كمان |
| فقط (only) | بس | بس | بس |
| إذا (if) | إذا / لو | إذا / لو | إذا / لو |

**Why it matters:** Using ماذا in a Levantine text is like using "whom" in a casual text
message. It signals a register mismatch that native speakers find either robotic or
condescending. AI consistently uses MSA interrogatives because they dominate written
Arabic training data.

**The fix:** Replace every MSA question word and demonstrative. This is mechanical
substitution — do it systematically, then check that the grammar around each substitution
still coheres.

**Example:**
- AI: ماذا تريد أن تفعل الآن؟ هذا الأمر يحتاج إلى كثير من الوقت
- Human (Syr): شو بدك تعمل هلق؟ هاد الشي بدو كتير وقت
- Human (Leb): شو بدك تعمل هلأ؟ هيدا الشي بدو كتير وقت
- Human (Pal): إيش بدك تعمل هلق؟ هاد الشي بدو كتير وقت

---

### Pattern 7 — أريد instead of بدّ

**Detection:** Any use of أريد، أودّ، أتمنى، أرغب for "I want" in informal contexts.
The بدّ system is one of the most distinctive features of Levantine verb morphology and
AI almost never produces it spontaneously — defaulting instead to أريد even when the
surrounding text is otherwise Levantine.

**Regional note:** بدّ + possessive suffix is universal across all three variants.
Full conjugation (بدّ = want/will):

| Person | Form | Example |
|--------|------|---------|
| I want | بدّي | بدّي نام |
| You want (m) | بدّك | بدّك تيجي؟ |
| You want (f) | بدّك | بدّك تيجي؟ |
| He wants | بدّو | بدّو يروح |
| She wants | بدّها | بدّها تشتري |
| We want | بدّنا | بدّنا نفهم |
| You (pl) want | بدّكن / بدّكم | بدّكن تجو؟ |
| They want | بدّهن / بدّهم | بدّهن يعرفو |

Note: بدّ + subjunctive verb — the verb after بدّ takes bare imperfect (no ب-prefix):
بدّي نام (not بدّي بنام), بدّو يروح (not بدّو بيروح).

**Why it matters:** The بدّ system is a Levantine-specific modal that has no exact MSA
parallel. Producing أريد when بدّي is needed is like a French learner using "je veux"
where a native would say "j'ai envie" — technically comprehensible but immediately
exposing as non-native.

**The fix:** Replace أريد→بدّي, يريد→بدّو, تريد (f)→بدّها, نريد→بدّنا. Check that
the following verb is bare imperfect (no ب-prefix).

**Example:**
- AI: أريد أن أنام مبكراً الليلة، وهو يريد أن يذهب إلى السينما
- Human: بدّي نام بكير الليلة، وهو بدّو يروح عالسينما

---

### Pattern 8 — MSA Pronouns and Verb Agreement

**Detection:** AI uses MSA 2nd and 3rd person plural pronouns أنتم، هم، هن and
maintains dual forms هما, أنتما. Also: 2nd plural verb agreement without -و suffix.

**Regional note:** Pronoun inventory in Levantine:

| MSA | Syrian | Lebanese | Palestinian |
|-----|--------|----------|-------------|
| أنتم (you pl) | انتو | انتو | انتو |
| هم / هن (they) | هني / هنّ | هودي | هني |
| هما (dual) | هني (same as pl) | هودي (same as pl) | هني |
| نحن (we) | نحنا / إحنا | نحنا | إحنا |
| أنا (I) | أنا / انا | أنا / انا | أنا / انا |

Verb 2nd/3rd plural agreement: add -و:
بتشتغلو، بيروحو، بتاكلو، بتعملو (2nd pl and 3rd pl)

**Why it matters:** Using أنتم instantly reads as MSA. Levantine انتو is so obligatory
that its absence — in any register short of formal speech — marks the text as foreign
or AI-generated.

**The fix:** Replace أنتم→انتو, هم/هن→هني (Syr/Pal) or هودي (Leb). Remove all dual forms.
Add -و to plural verb forms.

**Example:**
- AI: هل أنتم موافقون؟ هم لم يفهموا ما قلته
- Human (Syr): انتو موافقين؟ هني ما فهمو شو قلت
- Human (Leb): انتو موافقين؟ هودي ما فهمو شو قلت

---

### Pattern 9 — MSA Prepositions (إلى/من instead of عـ)

**Detection:** AI uses إلى for motion-to: ذهب إلى البيت, and sometimes من for source.
Levantine contracts إلى + definite article into عـ in all motion and location contexts.

**Regional note:** The عـ contraction is universal Levantine. Forms:
- عالبيت (إلى البيت / في البيت)
- عالشغل (إلى الشغل / في الشغل)
- عالمدرسة، عالسوق، عالمستشفى
- With indefinite: عبيت (in a house), عشغل (at work — less common, usually definite)
- Note: رح عالبيت (I'm going home) vs. في البيت (literary, acceptable in some formal
  Levantine writing but not in casual text)

**Why it matters:** إلى البيت in casual Levantine text reads like "I am going to mine
domicile" in English — technically correct but register-wrong. The contracted عـ is
obligatory in any text that is not deliberately formal.

**The fix:** Wherever AI writes إلى + definite noun, contract to عـ + noun. Check
all location/destination phrases.

**Example:**
- AI: ذهب إلى البيت وأكل، ثم عاد إلى المدرسة
- Human: راح عالبيت واكل، وبعدين رجع عالمدرسة

---

### Pattern 10 — Active Participle as Present State

**Detection:** AI uses conjugated verb forms for states that Levantine expresses with
active participles: أنا أعرف، أنا أذهب، أنا أفهم — instead of the participial forms
that Levantine uses for stative predicates.

**Regional note:** Universal Levantine. Core participial predicates:

| Verb | Participle | Meaning |
|------|------------|---------|
| يعرف | عارف/عارفة | knows |
| يذهب | رايح/رايحة | going / about to go |
| يجي | جاي/جاية | coming |
| يمشي | ماشي/ماشية | walking / going / ok |
| يشوف | شايف/شايفة | seeing / understanding |
| يسمع | سامع/سامعة | hearing |
| يفهم | فاهم/فاهمة | understanding |
| يحب | حابب/حاببة | liking / loving |
| يخاف | خايف/خايفة | scared |
| يرفع | رافع/رافعة | holding up |

Usage: إنت فاهم شو قصدي؟ / هي رايحة عالشغل / أنا عارف هيك

**Why it matters:** The participle-as-present-state is a fundamental Levantine structural
feature. AI almost never produces it because MSA does not use participles this way.
Replacing conjugated verb forms with participles adds a layer of naturalness that is
impossible to achieve through vocabulary substitution alone.

**The fix:** Identify stative predicate contexts (knowing, being-somewhere, being-in-motion,
perceiving) and replace conjugated verbs with active participles. Agree the participle
for gender.

**Example:**
- AI: أنا أعرف هذا الموضوع جيداً وأنا ذاهب إلى هناك الآن
- Human: أنا عارف هاد الموضوع منيح وأنا رايح لهونيك هلق

---

## CATEGORY 3 — DISCOURSE AND REGISTER

These patterns address the texture and flow of the text — the markers that make writing
feel spoken, human, and emotionally present.

---

### Pattern 11 — Missing Discourse Fillers

**Detection:** Clean, particle-free sentences where every clause moves directly to the
next. AI writes: "هذا الأمر صعب وأحتاج وقتاً للتفكير فيه." Native Levantine speakers
load their text with particles that carry pragmatic, relational, and hesitation functions.

**Regional note:** Core inventory (universal unless noted):

| Particle | Function | Regional note |
|----------|----------|---------------|
| يعني | "I mean" / hedging / elaborating | Universal |
| بس | "but" / "just" / "only" / softener | Universal |
| هيك | "like this" / "so" / "right?" | Syr/Pal (هكّ in some registers) |
| طبعاً | "of course" | Universal |
| والله | "honestly" / "I swear" / "wow" | Universal |
| يلا | "come on" / "let's go" / "ok then" | Universal |
| لا2 | "no but actually" (discourse reversal) | Universal written form |
| آخ | frustration / longing / sympathy | Universal |
| بالكيف | "the right way / properly" | Syrian |
| عنجد | "seriously" / "really" | Lebanese heavy |
| وبعدين | "and then" / "and so" | Universal |
| ما أدري | "I don't know" (softer than ما بعرف) | Universal |

**Why it matters:** Stylometric research on Arabic text shows that discourse particle
frequency and distribution is one of the strongest human/AI discriminators. AI Arabic
has particle desert — long clause chains with zero particles. Humans sprinkle particles
every 2-3 clauses minimum in informal registers.

**The fix:** Do not mechanically insert particles — read the pragmatic need. Add يعني
when hedging or elaborating, بس when there is contrast or a softening moment, والله
when making a sincere statement, يلا at transitions. Each particle should feel earned.

**Example:**
- AI: هذا الأمر صعب وأحتاج وقتاً للتفكير فيه. لا أعرف ما يجب فعله
- Human: يعني هاد الشي صعب، بدّي وقت أفكر فيه بس، والله ما عارف شو لازم أعمل

---

### Pattern 12 — Formal Transition Phrases

**Detection:** AI uses written-Arabic transitions: من المهم أن نلاحظ، تجدر الإشارة إلى،
في هذا السياق، وفي ختام القول، علاوة على ذلك، من ناحية أخرى.

**Regional note:** Levantine spoken equivalents:

| Formal MSA | Syrian | Lebanese | Palestinian |
|-----------|--------|----------|-------------|
| من ناحية أخرى | بس من ناحية تانية | بس من ناحية تانية | بس من ناحية تانية |
| علاوة على ذلك | وكمان / وبعدين | وكمان / وبعدين | وكمان / وبعدين |
| في هذا السياق | يعني بهاد الموضوع | يعني بهيدا الموضوع | يعني بهاد الموضوع |
| من المهم أن | المهم / بدّنا | المهم / بدّنا | المهم / بدّنا |
| لذلك / لهذا | مشان هيك | لهيك | مشان هيك |
| بالإضافة إلى ذلك | وزيادة عليه / وكمان | وزيادة عليه / وكمان | وزيادة عليه |
| خلاصة القول | يعني بالآخر | يعني بالآخر | يعني بالآخر |

**Why it matters:** Formal transitions are the verbal equivalent of a suit and tie in
a text message. They signal that the author is performing writing rather than
communicating. In Levantine text this feels especially alien because the dialect has
a strong oral tradition — its natural connective tissue is paratactic (بس، وبعدين، يعني).

**The fix:** Replace every formal transition with its Levantine paratactic equivalent.
If the text has more than two formal transitions per 100 words, it needs structural
re-thinking, not just surface substitution.

**Example:**
- AI: من المهم أن نلاحظ أن هذا الوضع يحتاج إلى معالجة دقيقة. علاوة على ذلك، يجب أن نأخذ في الاعتبار
- Human: المهم هاد الوضع بدو معالجة منيحة. وكمان لازم ناخد بعين الاعتبار

---

### Pattern 13 — Uniform Register

**Detection:** The text maintains a flat, consistent formal-casual register throughout.
No emotional peaks, no sudden informality, no register drops. Every sentence sounds like
it was written at the same pitch by the same machine state.

**Regional note:** This is a universal human/AI discriminator, not specific to any
Levantine variant. However, Lebanese text tends to show the most dramatic register
swings (formal-then-suddenly-affectionate); Syrian tends to show warm-then-dry-then-funny.

**Why it matters:** Stylometric research on human Arabic text confirms that "formal tone
consistency" — uniform register across a text — is a primary AI authorship marker.
Humans shift register constantly: they start casual, get emotional, drop a joke, get
serious, then drop to a soft almost-whisper register for sensitive moments. AI writes
in a flat horizontal line.

**The fix:** Introduce deliberate register variation. Lower the register suddenly at
an emotional point. Add a brief joke or self-deprecating aside. Use intimate address
(حبيبي، والله) after a formal passage. The pattern: formal → sudden warmth → pull back
→ dry observation.

**Example:**
- AI (flat): هذا الموضوع يحتاج إلى اهتمام. يجب أن نتعامل معه بجدية. النتائج ستكون مهمة.
- Human (varied): هاد الموضوع بدو اهتمام، بس — والله يا حبيبي — لو تعرف قديش صار يعني. بدّنا نعمل شي. آخ.

---

### Pattern 14 — Heavy Passive Voice

**Detection:** Arabic passive forms: يُعتبَر، يُستخدَم، يُلاحَظ، يُقال، يُفترَض.
These passive forms are abundant in AI-generated MSA text and carry over into AI
Levantine generation. Levantine Arabic rarely uses the passive morphologically.

**Regional note:** All three Levantine variants avoid passive voice in the same way —
they prefer an active construction with dropped or backgrounded subject, or they use
صار (become/happen) as a passive equivalent: صار كلام = there was talk about it.

Levantine passive avoidance strategies:
- Drop subject: قالوا إنو... (they said that... = it is said that...)
- صار + noun: صار وضع غريب (a strange situation arose)
- مفعول participle in stative sense: الباب مقفول (the door is closed, not "was closed")
- Active with general subject: كل واحد بيستخدم... (everyone uses...)

**Why it matters:** Passive voice in Arabic is a written-register feature. In Levantine
informal text, even one passive verb stands out. Two or more and the text reads as
a news bulletin.

**The fix:** Convert every morphological passive to active with dropped subject (قالوا),
صار construction, or active participle stative.

**Example:**
- AI: يُعتبَر هذا الأمر مهماً ويُستخدَم كثيراً في هذا المجال
- Human: هاد الشي مهم وكل واحد بيستخدمو بهاد المجال

---

### Pattern 15 — No Reader-Directed Questions

**Detection:** The text monologues. It makes statements, explanations, arguments —
but never turns to address the reader directly with a question or confirmation check.

**Regional note:** Levantine confirmation-seeking questions (طلب تأكيد):

| Syrian | Lebanese | Palestinian |
|--------|----------|-------------|
| مش هيك؟ | مش هيك؟ | مش هيك؟ |
| بتفهم؟ | بتفهم؟ | بتفهم؟ |
| يعني؟ | يعني؟ | يعني؟ |
| شايف شو قصدي؟ | شايف شو قصدي؟ | شايف إيش قصدي؟ |
| مشان هيك؟ | لهيك؟ | مشان هيك؟ |
| آه؟ | آه؟ | آه؟ |
| صح؟ | صح؟ | صح؟ |

**Why it matters:** Levantine Arabic has a strong oral/dialogic tradition. Even in
written form, native speakers reach out and pull the reader into the conversation
at key points. AI writes soliloquy. Humans write dialogue even when alone.

**The fix:** Add 2-3 reader-directed confirmation questions at natural pause points —
after making a key argument, after a surprising statement, at the end of an explanation.
Not every sentence needs one; 2-3 per 200 words is natural.

**Example:**
- AI: هذا النهج أفضل لأنه يوفر الوقت والجهد. النتائج ستكون ممتازة.
- Human: هاد الأسلوب أحسن لأنو بيوفر وقت وجهد، بتفهم؟ يعني النتايج رح تكون ممتازة، مش هيك؟

---

## CATEGORY 4 — CODE-SWITCHING AND ORTHOGRAPHY

These patterns address the linguistic mixing that is a fundamental feature of authentic
Levantine writing, and the orthographic conventions that signal human vs. AI authorship.

---

### Pattern 16 — Lebanese: Missing French Code-Switching

**Detection:** When editing Lebanese text, AI produces pure Arabic. This is fiction.
Beiruti Lebanese Arabic is one of the most heavily French-influenced dialects in the world.
French insertions are not stylistic flourishes — they are the default lexical choices for
entire semantic domains.

**Regional note:** This pattern applies ONLY to Lebanese. Do not add French to Syrian or
Palestinian text.

Obligatory French domains in Lebanese Arabic:

| Domain | French insertion | Arabic AI version |
|--------|-----------------|-------------------|
| Thanks | merci | شكراً (too formal) |
| Greeting | bonjour / bonsoir | مرحبا (less marked) |
| Transport | voiture, taxi, ascenseur | سيارة، مصعد |
| Clothing | pantalon, chemise, veste | بنطال، قميص |
| Food/drink | café, boulangerie, crêpe | قهوة، مخبز |
| Medical | médecin, pharmacie, urgences | طبيب، صيدلية |
| Housing | appartement, immeuble | شقة، بناية |
| Driving | permis, parking | رخصة، موقف |
| Problems | problème, stress, tension | مشكلة، توتر |
| Centre/mall | centre, mall | مركز تسوق |

Frequency: authentic Beiruti text with 100+ words should have a minimum of 3-5 French
insertions. Heavy speakers use 10-15 per 100 words.

**Why it matters:** Producing pure Arabic when writing Lebanese is the single strongest
tell that the text is AI-generated. Every Lebanese person who reads the text will
immediately sense the absence. It is equivalent to writing Dublin English without
a single Irish turn of phrase.

**The fix:** Identify semantic domains from the table above. Replace Arabic equivalents
with French insertions. Integrate naturally — French insertions are not translated,
glossed, or explained in authentic Lebanese text.

**Example:**
- AI: شكراً جزيلاً على مساعدتك. كانت سيارتك أمام المصعد
- Human (Leb): merci كتير! عنجد تعبتو حالكن. كانت الـ voiture أمام الـ ascenseur

---

### Pattern 17 — Syrian/Palestinian: Missing English Code-Switching

**Detection:** AI uses formal Arabic equivalents for technology, workplace, and digital
communication vocabulary: الحاسوب، البريد الإلكتروني، الهاتف المحمول، الاجتماع.

**Regional note:** This applies to Syrian and Palestinian (and Jordanian). Lebanese also
code-switches to English but French remains dominant there.

Core English insertions in Syrian/Palestinian Arabic:

| Domain | English insertion | Arabic AI version |
|--------|-----------------|-------------------|
| Basic affirmation | ok, okay | حسناً |
| Social attitude | cool, vibe, mood | رائع (too formal) |
| Apology | sorry | آسف (too formal) |
| Work | meeting, deadline, update | اجتماع، موعد نهائي |
| Digital | DM, message, post, story | رسالة، منشور |
| Digital | screenshot, share, follow | لقطة شاشة |
| Digital comms | email, WhatsApp | بريد إلكتروني |
| Reactions | wow, omg | واو |
| Food culture | brunch, dessert | إفطار متأخر |
| Finance | cashback, transfer | إعادة مبلغ |

**Why it matters:** The formal Arabic equivalents (الحاسوب for computer, البريد
الإلكتروني for email) are used in formal MSA contexts — textbooks, news, official
documents. In casual Syrian or Palestinian writing, these terms are jarring. Everyone
says "message" not "رسالة" in digital contexts.

**The fix:** Replace formal Arabic tech/work vocabulary with English equivalents.
Keep Arabic for non-specialized domains. The code-switching should feel natural —
English for tech/work/digital, Arabic for emotion/family/social.

**Example:**
- AI: أرسل لي رسالة إلكترونية عندما تنتهي من الاجتماع
- Human (Syr): بعتلي message أو DM لمّا تخلص من الـ meeting

---

### Pattern 18 — Diacritics Present (Tashkeel)

**Detection:** Presence of full or partial tashkeel (حركات): fatha, kasra, damma,
sukun, tanwin in non-Quranic, non-pedagogical text. AI models sometimes add diacritics
because MSA training text often includes them for disambiguation.

**Regional note:** Universal — no Levantine variant uses tashkeel in casual text.
The single exception: shadda (ّ) is retained, particularly on doubled consonants
that carry meaning (بدّي, هلّق, etc.).

**Why it matters:** The research finding here is stark. Studies on Arabic authorship
attribution show that the presence of tashkeel in non-religious text is one of the
strongest single-feature predictors of AI authorship. Humans never write tashkeel
in casual Arabic. AI adds it because it was trained on tashkeel-bearing formal corpora.

**The fix:** Strip ALL diacritics except shadda. This is a mechanical operation —
find all fatha (َ), kasra (ِ), damma (ُ), sukun (ْ), tanwin forms (ً ٍ ٌ) and delete.
Retain shadda (ّ).

**Example:**
- AI: يُريدُ أنْ يَذهبَ إلى البَيتِ الآنَ
- Human: بدو يروح عالبيت هلق

---

### Pattern 19 — Formal Hamza Writing

**Detection:** AI writes initial hamza with full orthographic precision: أنا، إلى،
أكل، إنّ، أيضاً. Levantine informal writing consistently drops or simplifies initial
hamza.

**Regional note:** Universal Levantine informal orthography. Common hamza simplifications:

| Formal | Informal Levantine |
|--------|--------------------|
| أنا | انا |
| أكل / يأكل | اكل / ياكل |
| إلى | ل / عـ (usually contracted anyway) |
| أيضاً | كمان (replaced by different word) |
| أيمتى | ايمتا |
| إيش | ايش (Palestinian) |
| إنّ / إنّو | إنو / انو |

**Why it matters:** Formal hamza writing is an orthographic marker of formal register.
In handwritten and keyboard-typed Levantine Arabic, hamza simplification is the norm —
not laziness, but a stable sociolinguistic feature of informal Levantine orthography.
AI produces formal hamza because it was trained on edited/published text.

**The fix:** Apply hamza simplification selectively. Focus on أنا → انا (very common),
يأكل → ياكل (common), إنّو → انو (common). Do not over-apply — some words retain
hamza even in informal writing.

**Example:**
- AI: أنا أريد أن أكل شيئاً الآن
- Human: انا بدّي آكل شي هلق (or: انا بدي ياكل شي هلق in some orthographic registers)

---

### Pattern 20 — ث/ذ Not Phonologically Shifted

**Detection:** AI preserves MSA interdental letters ث (voiceless) and ذ (voiced)
in words where Levantine speech and informal writing often shifts these.

**Regional note:** This is one of the most dialect-specific orthographic features and
must be applied carefully and selectively. Over-application produces caricature.

Common shifts:
- هذا → هاد/هاداك (replacement, not just spelling — use هاد throughout)
- ثاني → تاني (ث→ت shift)
- كذب/كذبة → كدب/كدبة (ذ→د in Syrian)
- ذهب → راح (replacement verb, more natural)
- ثلاثة → تلاتة (ث→ت in counting, very common)
- ذوق → دوق (ذ→د)

**Why it matters:** The ث/ذ letters are preserved in MSA and in formal Arabic writing.
In casual Levantine, especially Syrian, these sounds are merged with ت/د respectively.
Reflecting this in informal writing adds authenticity. But: do not apply to words where
the Arabic letter is still the standard written form even in Levantine (some words retain
ذ/ث even when pronounced differently).

**The fix:** Apply selectively to the most common words (هذا, ثاني, كذب, تلاتة).
Do not mechanically shift every ث/ذ — consult the word-by-word usage pattern.

**Example:**
- AI: هذا الشخص كاذب، وهذا ثاني شخص يفعل هذا
- Human: هاد الشخص كدّاب، وهاد تاني شخص عم يعمل هيك

---

## CATEGORY 5 — CULTURAL AND PRAGMATIC

These patterns address the cultural and emotional texture that makes Levantine text
feel lived-in and specific to its community.

---

### Pattern 21 — Missing Interjections

**Detection:** Emotionally flat text. Descriptions of good food, surprising news, sad
events, or impressive feats that contain no interjective response. AI describes;
humans react.

**Regional note:** Full interjection inventory with regional notes:

| Interjection | Meaning/Function | Regional note |
|-------------|-----------------|---------------|
| والله / وبالله | "honestly" / "my God" / surprise | Universal; وبالله stronger |
| يخرب بيتك | affectionate curse (you rascal!) | Universal |
| يسلمو / يسلم إيدك | "bless you" / thanks | Syrian primary; يسلم إيدك for skill |
| يعطيك العافية | "may God give you strength" / thanks for work | Universal |
| يا سلام | "wow" / appreciative surprise | Universal |
| آخ / آخ يا... | frustration / longing | Universal; repeated for intensity |
| ضبي | address for girls (appreciative/familiar) | Palestinian/South Levantine |
| يا حيوان | affectionate insult (you animal!) | Syrian/Lebanese informal |
| شو هالشي! | "what a thing!" (surprise/admiration) | Syrian/Lebanese |
| ما شاء الله | admiration (MashaAllah) | Universal |
| يلعن دينو | strong frustration curse | Universal (moderate intensity) |
| حرام | "what a shame" / "poor thing" | Universal |
| الله يرحمو | "God rest his soul" | Universal (when mentioning deceased) |
| يا ويلي | "oh no!" / shock | Universal |

**Why it matters:** Levantine Arabic has one of the richest interjective systems in
Arabic. The emotional punctuation of a text through interjections is not optional color —
it is how native speakers signal their emotional presence in the text and their
relationship to the content. AI text without interjections reads as emotionally detached.

**The fix:** Read the emotional beats of the text. At each emotionally significant
moment (something impressive, something sad, something delicious, something surprising),
add the appropriate interjection. Interjections should precede, interrupt, or follow
the emotional content.

**Example:**
- AI: هذا الطعام لذيذ جداً، ويستحق المدح
- Human (Syr): والله يا حبيبي هاد الأكل يسلمو إيدو، آخ ما أحلاه، شو هالشي!

---

### Pattern 22 — Wrong Terms of Address

**Detection:** AI uses يا صديقي (formal), يا أخي (somewhat formal), يا سيدي
(very formal). These are MSA address conventions. Levantine address terms are
completely different.

**Regional note:** Full Levantine address term inventory:

| Relationship | Syrian | Lebanese | Palestinian |
|-------------|--------|----------|-------------|
| General affection (m/f) | حبيبي/حبيبتي | حبيبي/حبيبتي | حبيبي/حبيبتي |
| Older man (uncle register) | عمو | عمو | عمو |
| Older woman | عمتي | عمتي | عمتي |
| Male peer (informal) | يا زلمي / يا زلمة | يا زلمي | يا زلمي |
| Male peer (dude) | يا عمي | يا عمي | يا عمي |
| Group of guys | يا شباب | يا شباب | يا شباب |
| Girl/young woman | يا بنت | يا بنت | يا بنت / ضبي |
| Close friend (girl to girl) | يا روحي | يا روحي | يا روحي |
| Anyone (warm) | يا قلبي | يا قلبي | يا قلبي |
| Professional (neutral) | يا أستاذ | يا أستاذ | يا أستاذ |

Note: حبيبي is used for strangers in service contexts too (addressing a waiter,
a shopkeeper) — it does not imply romantic relationship.

**Why it matters:** يا صديقي in casual Levantine text reads as either deliberately
formal (a speech context) or AI-generated. No casual Levantine speaker addresses a
friend as يا صديقي.

**The fix:** Replace all يا صديقي / يا أخي / يا سيدي with the appropriate Levantine
address term for the context and relationship.

**Example:**
- AI: يا صديقي، أنت تعرف أن هذا صحيح
- Human: حبيبي، انت عارف إنو هاد صح، مش هيك؟

---

### Pattern 23 — Missing Turkish Loanwords (Syrian)

**Detection:** When editing Syrian Arabic specifically, AI uses Standard Arabic vocabulary
where Turkish loanwords are the natural Levantine choice. This applies primarily to
Syrian text — Turkish substrate is lighter in Lebanese and Palestinian.

**Regional note:** Syrian Arabic only. Do not introduce Turkish loans to Lebanese or
Palestinian text — they sound foreign there.

Core Turkish loan vocabulary in Syrian Arabic (selected):

| Turkish origin | Syrian Arabic | AI version (MSA/wrong) |
|---------------|--------------|----------------------|
| oda (room) | أوضة | غرفة |
| fincan (coffee cup) | فنجال | فنجان |
| çamaşır (laundry) | جمشير (archaic, less used now) | غسيل |
| tencere (pot) | طنجرة | وعاء / قدر |
| boya (paint/shoe polish) | بوية | صبغة |
| çizme (boot) | جزمة | حذاء |
| yufka (thin bread) | يفكة | خبز رقيق |
| bardak (glass) | بردقة (dialectal) | كأس |
| çanta (bag) | شنطة | حقيبة |
| kahve (coffee, specific type) | قهوة (shared root) | — |

**Why it matters:** Turkish loanwords in Syrian are not archaic or formal — they are
the default terms used in everyday speech. Using غرفة where أوضة is natural reads
as either educated-formal or non-Syrian. أوضة is what every Syrian says.

**The fix:** Apply selectively — only substitute where the Turkish loan is the clear
everyday default (أوضة for room, فنجال for coffee cup, طنجرة for pot, شنطة for bag).
Do not force Turkish loans into contexts where they do not fit naturally.

**Example:**
- AI: وضع حقيبته في الغرفة وانتظر
- Human (Syr): حط شنطتو بالأوضة وستنّا

---

### Pattern 24 — Uniform Sentence Length Distribution

**Detection:** AI Arabic shows statistically uniform sentence length distribution.
Sentences hover in a narrow band of 15-25 words each. There are no fragments. There
are no run-on paratactic chains that go for 60+ words connected by و/بس/وبعدين.

**Regional note:** Universal human characteristic, but Levantine human text is
particularly extreme in this variation because of its paratactic structure —
native speakers link clauses indefinitely with وبعدين / وبعدين / وبعدين without
feeling the need to end sentences.

Natural Levantine sentence length distribution should include:
- **Ultra-short utterances (1-4 words):** بدّك؟ ليش؟ مش هيك؟ والله؟ يعني...
- **Short sentences (5-10 words):** يا حبيبي هاد الشي مو صح
- **Medium sentences (11-20 words):** بدّي روح عالبيت بس ما بعرف إذا رح فرجع بكير
- **Long paratactic chains (30-60+ words):** وبعدين راح عندو وحكيتلو كل شي والله يا حبيبي
  هو انصدم بس بعدين فهم وقلّي هيك هيك وبعدين رحنا سوا وأكلنا...

**Why it matters:** Sentence length uniformity is one of the most robust machine-learning
features for AI text detection in Arabic. A text where every sentence is 18-22 words
is almost certainly AI-generated. A text that alternates between بدّك؟ and a 50-word
paratactic chain feels human.

**The fix:** Deliberately fragment some sentences into 1-4 word utterances. Deliberately
merge some short sentences into long paratactic chains using وبعدين, بس, ويلا. Aim
for a range of 3 to 50+ words across sentences.

**Example:**
- AI: ذهبت إلى السوق اليوم واشتريت بعض الأشياء. كان الطقس جميلاً وكنت سعيداً بتجربتي.
- Human: رحت عالسوق اليوم. والله. اشتريت أشياء وبعدين الجو كان منيح وكنت مبسوط وبعدين رجعت
  عالبيت وأكلت وناميت. بس هيك.

---

### Pattern 25 — Consistent Spelling of Variable Words

**Detection:** AI always spells variable words identically throughout a text.
هلق is always هلق. مش is always مش. هني is always هني. In AI text, each word has
exactly one spelling.

**Regional note:** Human writers naturally vary between accepted alternative spellings
of the same word within the same text. This is not inconsistency — it is the absence
of a prescriptive orthographic standard for dialect writing.

Key words with natural spelling variation:

| Word | Variant spellings | Note |
|------|-----------------|------|
| now | هلق / هلأ / هلأ | Both widely used |
| they (Syr) | هني / هنّي / هنّ | All Syrian |
| that/this (Syr) | هاد / هادا | Both natural |
| that/this (Leb) | هيدا / هيدا | Minor variation |
| not (verbs) | ما / ما (with spacing variations) | |
| want | بدّي / بدي | Shadda often dropped in fast typing |
| with me | معي / معي / مي | Regional + speed variation |
| how | كيف / كيف | |
| there | هونيك / هونيك / هون | Varying distance markers |
| so/but | بس / بس | Identical, but note spacing habits |

**Why it matters:** Perfect spelling consistency is an AI artifact. Human keyboard
writers in Arabic dialect have no spellchecker, no standard orthography, and type
fast. They naturally produce هلق in one sentence and هلأ two sentences later — not
because they are inconsistent, but because both forms are natural and neither is wrong.
AI picks one form and commits to it with machine consistency.

**The fix:** Introduce deliberate variation. If you wrote هلق three times, change
one instance to هلأ. If هني appears repeatedly in Syrian text, introduce one هنّ.
Do not overdo it — 1-2 variations per document is enough to break the AI pattern.

**Example:**
- AI: هو هني هلق. هني بيشتغلو هلق. ما بعرف وين هني.
- Human: هو هني هلق. هنّ عم يشتغلو هلأ. ما بعرف وينن.

---

## Processing Workflow

### Stage 1 — Regional Identification and Diagnosis

**Step 1: Identify the regional variant.**
- Scan for هيدا/هيدي/هيدول → Lebanese
- Scan for إيش → Palestinian
- Scan for ما...ش suffixes → Palestinian
- Scan for هاد/هدول/يسلمو → Syrian
- If unclear, ask: "Is this Syrian, Lebanese, or Palestinian text?"

**Step 2: Run the Category 1 diagnostic.**
Check each verb: Does it have ب-prefix? Is عم missing where needed? Is رح present or
did AI write سوف? Is negation using ما/مش or لم/ليس? Run MSA vocabulary scan: any
ماذا، أريد، أنتم, الآن, هذا?

Count the failures. If more than 5 Category 1 failures per 100 words → the text is
deeply MSA. Plan a full rewrite, not surface edits.

**Step 3: Check code-switching.**
Lebanese? Count French insertions. Zero French in 100+ word Lebanese text = AI artifact.
Syrian/Palestinian? Check for English tech/digital terms.

**Step 4: Check orthography.**
Any tashkeel? Remove. Heavy formal hamza? Simplify key words. ث/ذ preserved unnaturally?
Apply selective shifts.

---

### Stage 2 — Systematic Rewrite

Apply corrections in this order for maximum efficiency:

1. **Verb system first** (Category 1, Patterns 2-5): Add ب-prefix to all present indicative
   verbs. Add عم where progressive. Replace سوف/سـ with رح. Fix all negation particles.

2. **Vocabulary substitution** (Category 1, Pattern 1 + Category 2, Patterns 6-10):
   Replace MSA question words and demonstratives (full table). Replace أريد with بدّ
   conjugation. Replace pronouns. Contract إلى→عـ. Convert stative verbs to participles.

3. **Code-switching** (Category 4, Patterns 16-17): For Lebanese, inject French in
   relevant domains. For Syrian/Palestinian, inject English for tech/digital/work.

4. **Discourse particles** (Category 3, Patterns 11-15): Add يعني, بس, والله at
   natural pause points. Break uniform register. Convert passive to active. Add
   reader-directed questions.

5. **Cultural texture** (Category 5, Patterns 21-25): Add interjections at emotional
   beats. Fix address terms. For Syrian: check Turkish loans. Vary sentence length.
   Vary spelling of variable words.

6. **Orthographic cleanup** (Category 4, Patterns 18-20): Strip tashkeel (keep shadda).
   Simplify key hamzas. Apply selective ث/ذ shifts.

---

### Stage 3 — Audit and Polish

**The native speaker test:** Read the full text aloud in your head. At each sentence ask:
"Would a Syrian / Lebanese / Palestinian person read this sentence without pausing?"

If the answer is no, identify why and fix it. Common residual failures after Stage 2:

- **MSA vocabulary leaks:** A single ماذا or أريد that was missed
- **Flat emotional register:** Long passage with no interjection, no register shift
- **Missing code-switching:** Three paragraphs of Lebanese with no French
- **Orphaned formal transitions:** One من المهم أن that survived the pass
- **Pronoun mismatches:** هم survived somewhere instead of هني/هودي
- **Consistent spelling:** هلق appearing identically 5 times in a row

**Final check — the authenticity questions:**
1. Does this text have the regional vocabulary of its target variant throughout?
2. Is every present-indicative verb correctly ب-prefixed?
3. Is the negation system correct for the variant (ما + ـش for Palestinian)?
4. Does the text have the right code-switching language (French for Leb, English for Syr/Pal)?
5. Does the text have discourse particles at natural intervals?
6. Does the text have at least one emotional moment with an interjection?
7. Does the sentence length distribution vary from short fragments to long chains?
8. Are there no tashkeel marks (except shadda)?

If all 8 answers are yes: proceed to scoring.

---

## Voice Calibration

### Formal-Casual Continuum

Levantine Arabic exists on a spectrum from full dialect to something approaching formal
written Arabic. Your edit should match the register of the intended context:

**Ultra-casual (voice messages, WhatsApp):**
- Heavy particles (يعني كل تاني كلمة), heavy code-switching, spelling variation, fragments
- Example: يعني بدّي روح بس مو عارف، هيك، والله

**Casual written (social media, personal messages):**
- Standard Levantine dialect features, moderate particles, some code-switching
- Example: بدّي روح عالبيت هلق، مش عارف إذا رح ارجع بكير

**Semi-formal (blog, personal essay, newsletter):**
- Dialect features mostly preserved, fewer particles, minimal code-switching,
  occasional formal Arabic word acceptable if used deliberately
- Example: بدّي أحكي عن تجربتي لمّا رحت عالمستشفى

**Formal Levantine (speech, formal letter in dialect):**
- Levantine syntax and key vocabulary, but formal vocabulary acceptable,
  almost no code-switching, full sentence structures
- Example: بدّنا نتكلم عن هاد الموضوع بشكل جدي

When the register is not specified, ask or default to casual written register.

### Emotional Register Mapping

| Emotion | Levantine markers to introduce |
|---------|-------------------------------|
| Frustration | آخ، والله، ليش هيك، ما كان هيك لازم |
| Affection | حبيبي، يا روحي، والله عليك |
| Surprise | شو هالشي!، والله؟، لا2 جد؟ |
| Admiration | يا سلام، ما شاء الله، يسلمو إيدك |
| Sympathy | حرام عليك، آخ، الله يعينك |
| Enthusiasm | يلا!، ويلا شو منتظرين، يالله |
| Gratitude | يعطيك العافية، يسلمو، merci (Leb) |

---

## Quality Rubric — 50-Point Scale

Score the text after editing across five dimensions:

### Dimension 1 — Dialect Authenticity (1-10)

Score 9-10: Correct regional variant applied throughout. All demonstratives, question
words, and regional markers are consistently correct for the target variant (Syrian/
Lebanese/Palestinian). Code-switching is the right language for the variant.

Score 7-8: Mostly correct variant, minor lapses (one or two wrong demonstratives,
one or two missed regional markers).

Score 5-6: Inconsistent variant — some Lebanese features in Syrian text or vice versa.
Or: neutral Levantine core applied when a specific variant was requested.

Score 3-4: Variant mostly wrong. الشامي العام applied uniformly when a specific
variant was needed, or regional markers systematically from the wrong variant.

Score 1-2: MSA throughout. No regional variant applied at all.

---

### Dimension 2 — Verb System (1-10)

Score 9-10: All present-indicative verbs carry ب-prefix. عم appears correctly for
progressive. رح used for future (zero سوف/سـ). بدّ system used correctly for want
(zero أريد). Participial predicates used for stative contexts.

Score 7-8: One or two missed ب-prefixes. Or: one بدّ/أريد error. Generally correct.

Score 5-6: Multiple ب-prefix failures (more than 3 per 100 words). Or: رح/سوف
confusion surviving in multiple places.

Score 3-4: Systematic failures in verb system. ب-prefix absent on most verbs, or
سوف used throughout, or أريد never converted to بدّ.

Score 1-2: Full MSA verb system. No Levantine morphology applied.

---

### Dimension 3 — Code-Switching (1-10)

Score 9-10 (Lebanese): 3-8 French insertions per 100 words, naturally integrated
into correct semantic domains (transport, thanks, problems, medical).

Score 9-10 (Syrian/Palestinian): English tech/digital terms in all technology and
workplace contexts. Arabic retained for emotion, family, social.

Score 7-8: Code-switching present but sparse (1-2 insertions per 100 words Lebanese)
or limited to one domain.

Score 5-6: Code-switching present but mechanical — all instances in same domain,
or French in Palestinian text / English in Lebanese text.

Score 3-4: Minimal code-switching. One or two instances in a long text.

Score 1-2: Zero code-switching. Pure Arabic throughout (for a context where
code-switching is obligatory).

Note: If the text is very short (under 50 words), adjust this score to reflect
what is possible in that length.

---

### Dimension 4 — Discourse Flow (1-10)

Score 9-10: يعني، بس، والله, وبعدين, يلا appearing naturally at 2-4 instances per
100 words. Formal transitions (من المهم أن, علاوة على ذلك) completely absent.
Reader-directed questions present at natural pause points.

Score 7-8: Particles present but slightly sparse (1-2 per 100 words) or one
formal transition surviving.

Score 5-6: Particles present but feel forced or inserted at wrong pragmatic moments.
Or: formal transitions surviving in multiple places.

Score 3-4: Very sparse particles (1 per 200 words). Multiple formal transitions
surviving. No reader-directed questions.

Score 1-2: No discourse particles. Full formal transition vocabulary. Monologic
throughout.

---

### Dimension 5 — Emotional Texture (1-10)

Score 9-10: At least one interjection at an appropriate emotional moment. Address
terms correct for context (حبيبي for peers, عمو for older, يا شباب for groups).
Register variation — at least one moment where the register shifts noticeably.
Sentence length variation: fragments and long chains both present.
Spelling variation in variable words.

Score 7-8: Interjections present but only one or two in a long text. Or: register
flat but address terms correct.

Score 5-6: Address terms mostly correct. No interjections, or interjections at
wrong moments. Sentence length uniform.

Score 3-4: یا صديقي / يا أخي surviving (formal address). No interjections. Flat
register throughout. Uniform sentence length.

Score 1-2: Full formal address terms, no interjections, no emotional markers, uniform
sentences. Text is emotionally inert.

---

### Score Interpretation

| Total | Assessment |
|-------|------------|
| 45-50 | Passes native speaker test. Will not be flagged by a Syrian, Lebanese, or Palestinian reader as AI-generated. Ready to publish. |
| 40-44 | Near-native. Minor MSA leaks or thin code-switching. One more review pass recommended. |
| 35-39 | Good but noticeable. A careful native reader will spot 2-3 AI markers. Fix the lowest-scoring dimension before publishing. |
| 25-34 | Heavy MSA reversion on multiple dimensions. Return to Stage 2, focus on lowest scores. |
| Below 25 | Fundamental rewrite needed. Category 1 failures not resolved. Start from Stage 1 diagnostic. |

---

## Quick Reference Card

**When you receive text to humanize:**

1. Ask (if not specified): Syrian / Lebanese / Palestinian?
2. Ask (if not specified): Register level? (Ultra-casual / casual written / semi-formal)
3. Run Stage 1 diagnostic — count Category 1 failures
4. Apply Stage 2 rewrites in order: verbs → vocabulary → code-switching → discourse → culture → orthography
5. Run Stage 3 audit — 8 authenticity questions
6. Score across 5 dimensions
7. Report: original text, rewritten text, score breakdown, key changes made

**Non-negotiable fixes (must apply to every text):**
- ب-prefix on all present indicative verbs
- رح for future (never سوف/سـ)
- ما for verbal negation (never لم)
- مش/مو for nominal negation (never ليس)
- Remove all tashkeel except shadda
- Replace ماذا→شو/إيش, الآن→هلق/هلأ, كثيراً→كتير, هذا→هاد/هيدا, أريد→بدّي

**Regional non-negotiables:**
- Lebanese: At least 3 French insertions per 100 words
- Palestinian: ما...ش negation suffix on at least some negated verbs
- Syrian: هاد/هدول (not هيدا), يسلمو for thanks, Turkish loans for everyday objects
